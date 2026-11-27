#!/usr/bin/env python3
"""Supervisor for the author, reviewer and explorer agents. Standard library only; Windows, macOS,
Linux. The explorer works moonshot issues in long passes on a stronger model.

Each pass is one fresh, non-interactive `claude -p "/<role>-loop ..."` run inside that role's
git worktree. The supervisor owns the schedule: it sleeps for the interval the pass asked for
(a final `NEXT: <minutes>` line), waits out usage limits, retries after crashes, and starts a
reviewer pass as soon as an author pass changes a pull request.

  python tools/agents.py run                 # run all roles until stopped (Ctrl+C)
  python tools/agents.py --roles author,reviewer run   # without the explorer
  python tools/agents.py once reviewer       # run a single pass, then exit
  python tools/agents.py once author --dry-run
  python tools/agents.py status              # last pass, next pass and open PRs
  python tools/agents.py setup               # create the worktrees and build Lean

Permissions: allow and deny rules are read from origin/main's .claude/settings.json (never from
a PR branch) and passed with --settings, with --permission-mode auto and --permission-prompts
none, so nothing ever waits on a prompt and the deny rules always apply.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import threading
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
LOGS = REPO / ".agent-logs"
ROLES = ("author", "reviewer", "explorer")
DEFAULT_WORKTREES = Path("C:/w") if os.name == "nt" else Path.home() / "proofs-worktrees"
DEFAULT_MODEL = "claude-opus-5-5"
# The explorer works moonshots in long passes on the strongest model (it uses the allowance faster).
ROLE_MODEL = {"explorer": "claude-fable-5-2"}
PASS_TIMEOUT = {"author": 2 * 3600, "reviewer": 2 * 3600, "explorer": 4 * 3600}  # seconds
DEFAULT_NEXT = {"author": 30, "reviewer": 20, "explorer": 30}   # minutes, if a pass doesn't say
CHANGES_PRS = ("author", "explorer")   # roles whose pull-request changes wake the reviewer
# Spending guards, in Claude Code's estimated USD. On a subscription these are not charges, but they
# track how much of the shared plan allowance a role uses. All roles share one account, so the caps
# keep the explorer from starving the author and reviewer. Override with --budgets.
PASS_BUDGET_USD = {"author": 6.0, "reviewer": 3.0, "explorer": 20.0}    # one pass is stopped here
DAILY_BUDGET_USD = {"author": 30.0, "reviewer": 12.0, "explorer": 40.0}  # role pauses until midnight
IDLE_NEXT = 60
RETRY_BACKOFF = [5, 15, 30, 60]     # minutes after consecutive failures
WAIT_STEP = 60                      # seconds; waits recheck the wall clock this often (see wait_until)
SUPERVISOR_NOTE = ("[supervisor] Started by tools/agents.py for a single iteration. Do not call "
                   "ScheduleWakeup and do not message other sessions; the supervisor schedules "
                   "and notifies. This run ends when your turn ends, and any subagent still "
                   "running is then killed and its work lost: run subagents in the foreground "
                   "(never in the background) and wait for every one of them before your final "
                   "message. Commit and push anything worth keeping before you finish. End your "
                   "final message with a line `NEXT: <minutes>`.")
# Markers a parent Claude Code session leaves in the environment; children must not inherit them.
STRIP_ENV = ("CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_MESSAGING_SOCKET",
             "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT",
             "CLAUDE_CODE_SSE_PORT")

_print_lock = threading.Lock()


def log(msg: str) -> None:
    """Print, and append to .agent-logs/supervisor.log (pythonw and Task Scheduler have no console)."""
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    with _print_lock:
        if sys.stdout:
            print(line, flush=True)
        try:
            LOGS.mkdir(exist_ok=True)
            with open(LOGS / "supervisor.log", "a", encoding="utf-8") as f:
                f.write(line + "\n")
        except OSError:
            pass


def run(cmd: list[str], cwd: Path | None = None, timeout: float | None = None,
        env: dict | None = None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                          errors="replace", timeout=timeout, env=env)


def git(wt: Path, *args: str) -> subprocess.CompletedProcess:
    return run(["git", "-C", str(wt), *args])


def find_claude() -> str:
    native = Path.home() / ".local" / "bin" / ("claude.exe" if os.name == "nt" else "claude")
    if native.exists():
        return str(native)
    found = shutil.which("claude")
    if not found:
        sys.exit("claude not found: install Claude Code first")
    return found


# ---------- pure helpers (tested in tools/test_agents.py) ----------

def parse_next(text: str) -> int | None:
    """Minutes from the last `NEXT: <n>` line of a pass's final message."""
    found = re.findall(r"NEXT:\s*(\d+)", text or "")
    return int(found[-1]) if found else None


def parse_limit_reset(text: str, now: dt.datetime) -> dt.datetime | None:
    """Reset time from "You've hit your session limit · resets 3:45pm" (or "resets Mon 12:00am").

    Returns None if the text is not a usage-limit message."""
    # Any "You've hit your <session|weekly|5-hour|…> limit" wording, or a bare "usage limit".
    if not re.search(r"hit your [\w\s-]{0,30}?limit|usage limit", text or "", re.I):
        return None
    m = re.search(r"resets\s+(?:(mon|tue|wed|thu|fri|sat|sun)\w*\s+)?(\d{1,2})(?::(\d{2}))?\s*(am|pm)",
                  text, re.I)
    if not m:
        return now + dt.timedelta(minutes=30)
    day, hour, minute, ampm = m.group(1), int(m.group(2)), int(m.group(3) or 0), m.group(4).lower()
    hour = hour % 12 + (12 if ampm == "pm" else 0)
    reset = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if day:
        target = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"].index(day.lower()[:3])
        reset += dt.timedelta(days=(target - now.weekday()) % 7)
    if reset <= now:
        reset += dt.timedelta(days=7 if day else 1)
    return reset + dt.timedelta(minutes=2)


def parse_result(stdout: str) -> dict:
    """The final result object from `claude -p --output-format json` output.

    Accepts a single JSON object or a list of messages (takes the last one with type "result").
    Never raises; returns {} if nothing usable is found."""
    try:
        data = json.loads(stdout or "")
    except (json.JSONDecodeError, TypeError, ValueError):
        return {}
    if isinstance(data, dict):
        return data
    if isinstance(data, list):
        results = [m for m in data if isinstance(m, dict) and m.get("type") == "result"]
        return results[-1] if results else {}
    return {}


def agent_settings(main_settings_json: str) -> dict:
    """The --settings payload: main's allow and deny rules, never waiting on a prompt."""
    perms = json.loads(main_settings_json).get("permissions", {})
    return {"permissions": {"allow": perms.get("allow", []), "deny": perms.get("deny", []),
                            "denyInsteadOfPrompting": True}}


def load_records(logs: Path) -> list[dict]:
    records = []
    for f in sorted(logs.glob("*/*.json")):
        try:
            records.append(json.loads(f.read_text(encoding="utf-8")))
        except (json.JSONDecodeError, OSError):
            pass
    return records


def spent(records: list[dict], role: str, since: dt.datetime) -> float:
    """Estimated USD spent by a role on passes started at or after `since`."""
    return sum((r.get("cost_usd") or 0) for r in records
               if r.get("role") == role and dt.datetime.fromisoformat(r["started"]) >= since)


def summarize(records: list[dict], since: dt.datetime) -> dict:
    """Per role: passes, minutes, estimated USD, and tokens per model, since a time."""
    out: dict = {}
    for r in records:
        if dt.datetime.fromisoformat(r["started"]) < since:
            continue
        s = out.setdefault(r["role"], {"passes": 0, "minutes": 0.0, "usd": 0.0, "tokens": {}})
        s["passes"] += 1
        s["minutes"] += r.get("minutes") or 0
        s["usd"] += r.get("cost_usd") or 0
        for model, u in (r.get("model_usage") or {}).items():
            n = sum(v for k, v in (u or {}).items() if k.lower().endswith("tokens") and isinstance(v, (int, float)))
            s["tokens"][model] = s["tokens"].get(model, 0) + n
    return out


def parse_budgets(spec: str, base: dict) -> dict:
    """'explorer=25,author=10' -> base with those roles overridden."""
    out = dict(base)
    for part in filter(None, (p.strip() for p in (spec or "").split(","))):
        role, _, value = part.partition("=")
        if role not in base or not value:
            raise ValueError(f"bad budget '{part}'; use role=dollars with role in {', '.join(base)}")
        out[role] = float(value)
    return out


def is_orphan_pass(command_line: str, role: str) -> bool:
    """True if a process command line is a supervisor-started pass of this role."""
    return f"/{role}-loop [supervisor]" in (command_line or "")


def child_env(base: dict) -> dict:
    env = {k: v for k, v in base.items() if k not in STRIP_ENV}
    env["CLAUDE_CODE_FORCE_SESSION_PERSISTENCE"] = "1"   # keep transcripts for status/auditing
    env["AGENT_SUPERVISOR"] = "1"
    return env


def process_command_lines() -> list[str]:
    """Command lines of running claude processes (best effort; empty list if unavailable)."""
    if os.name == "nt":
        r = run(["powershell.exe", "-NoProfile", "-Command",
                 "Get-CimInstance Win32_Process -Filter \"Name='claude.exe'\" | ForEach-Object CommandLine"])
    else:
        r = run(["ps", "-eo", "args"])
    return [line for line in (r.stdout or "").splitlines() if line.strip()]


# ---------- one pass ----------

class Supervisor:
    def __init__(self, worktrees: Path, model: str, dry_run: bool = False,
                 roles: tuple = ROLES, explorer_model: str | None = None,
                 pass_budget: dict | None = None, daily_budget: dict | None = None):
        self.worktrees, self.model, self.dry_run, self.roles = worktrees, model, dry_run, roles
        self.models = {r: ROLE_MODEL.get(r, model) for r in ROLES}
        if explorer_model:
            self.models["explorer"] = explorer_model
        self.pass_budget = pass_budget or dict(PASS_BUDGET_USD)
        self.daily_budget = daily_budget or dict(DAILY_BUDGET_USD)
        self.claude = find_claude()
        self.wake = {r: threading.Event() for r in ROLES}
        self.stop = threading.Event()
        self.state_lock = threading.Lock()
        LOGS.mkdir(exist_ok=True)

    def wt(self, role: str) -> Path:
        return self.worktrees / role

    def open_pr_heads(self) -> dict:
        r = run(["gh", "pr", "list", "--state", "open", "--json", "number,headRefOid"], cwd=REPO)
        try:
            return {p["number"]: p["headRefOid"] for p in json.loads(r.stdout or "[]")}
        except json.JSONDecodeError:
            return {}

    def save_state(self, role: str, **fields) -> None:
        with self.state_lock:
            path = LOGS / "state.json"
            state = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
            state.setdefault(role, {}).update(fields)
            path.write_text(json.dumps(state, indent=2), encoding="utf-8")

    def run_pass(self, role: str) -> tuple[str, int]:
        """Run one pass. Returns (outcome, minutes until the next pass)."""
        wt = self.wt(role)
        if not (wt / ".git").exists():
            log(f"{role}: no worktree at {wt}; run `agents.py setup`")
            return "no-worktree", IDLE_NEXT
        if not self.dry_run and any(is_orphan_pass(c, role) for c in process_command_lines()):
            # A pass started by an earlier supervisor is still working in this worktree.
            log(f"{role}: an earlier {role} pass is still running; checking again in 5 min")
            return "busy", 5
        if not self.dry_run:
            git(wt, "fetch", "-q", "origin")
            if not git(wt, "status", "--porcelain").stdout.strip():
                git(wt, "checkout", "-q", "--detach", "origin/main")
        settings_json = git(wt, "show", "origin/main:.claude/settings.json").stdout
        settings_file = LOGS / f"settings-{role}.json"
        settings_file.write_text(json.dumps(agent_settings(settings_json), indent=2), encoding="utf-8")

        cmd = [self.claude, "-p", f"/{role}-loop {SUPERVISOR_NOTE}", "--model", self.models[role],
               "--output-format", "json", "--permission-mode", "auto",
               "--permission-prompts", "none", "--settings", str(settings_file),
               "--max-budget-usd", str(self.pass_budget[role])]
        if self.dry_run:
            log(f"{role}: would run in {wt}: {' '.join(cmd[:3])} ...")
            return "dry-run", 0

        started = dt.datetime.now()
        self.save_state(role, status="running", started=started.isoformat(timespec="seconds"))
        log(f"{role}: pass started")
        try:
            r = run(cmd, cwd=wt, timeout=PASS_TIMEOUT[role], env=child_env(dict(os.environ)))
            out, err, code = r.stdout, r.stderr, r.returncode
        except subprocess.TimeoutExpired as e:
            out, err, code = (e.stdout or ""), (e.stderr or ""), -1
            if isinstance(out, bytes):
                out = out.decode("utf-8", "replace")
            if isinstance(err, bytes):
                err = err.decode("utf-8", "replace")
            err += f"\n[supervisor] killed after {PASS_TIMEOUT[role] // 60} minutes"
        minutes = (dt.datetime.now() - started).total_seconds() / 60

        result = parse_result(out)
        text = result.get("result") or ""
        if not isinstance(text, str):
            text = json.dumps(text)
        record = {"role": role, "started": started.isoformat(timespec="seconds"),
                  "minutes": round(minutes, 1), "exit_code": code,
                  "subtype": result.get("subtype"), "session_id": result.get("session_id"),
                  "cost_usd": result.get("total_cost_usd"), "model_usage": result.get("modelUsage"),
                  "model": self.models[role], "result": text,
                  "stderr_tail": (err or "")[-2000:]}
        (LOGS / role).mkdir(exist_ok=True)
        (LOGS / role / f"{started:%Y%m%d-%H%M%S}.json").write_text(
            json.dumps(record, indent=2, ensure_ascii=False), encoding="utf-8")

        reset = parse_limit_reset(f"{text}\n{err}\n{out[-2000:]}", dt.datetime.now())
        if reset:
            wait = max(1, int((reset - dt.datetime.now()).total_seconds() // 60))
            self.save_state(role, status="usage-limit", resumes=reset.isoformat(timespec="minutes"))
            log(f"{role}: usage limit; resuming at {reset:%a %H:%M}")
            return "usage-limit", wait
        if result.get("subtype") == "error_max_budget_usd":
            # Hit the per-pass cap: not a crash. Work so far is committed per the skills' rules.
            self.save_state(role, status="pass-budget-hit", finished=dt.datetime.now().isoformat(timespec="seconds"))
            log(f"{role}: pass stopped at its ${self.pass_budget[role]:.0f} budget after {minutes:.0f} min")
            return "ok", DEFAULT_NEXT[role]
        if code != 0 or result.get("subtype") not in (None, "success"):
            self.save_state(role, status="failed", exit_code=code)
            log(f"{role}: pass failed (exit {code}, {result.get('subtype')}); see .agent-logs/{role}/")
            return "failed", 0
        nxt = parse_next(text) or DEFAULT_NEXT[role]
        summary = text.strip().splitlines()[0][:200] if text.strip() else ""
        self.save_state(role, status="ok", finished=dt.datetime.now().isoformat(timespec="seconds"),
                        summary=summary, cost_usd=result.get("total_cost_usd"))
        log(f"{role}: pass done in {minutes:.0f} min; next in {nxt} min. {summary}")
        return "ok", nxt

    def worker(self, role: str) -> None:
        failures = 0
        while not self.stop.is_set():
            midnight = dt.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            today = spent(load_records(LOGS), role, midnight)
            if today >= self.daily_budget[role]:
                resume = midnight + dt.timedelta(days=1, minutes=1)
                log(f"{role}: daily budget reached (${today:.2f} of ${self.daily_budget[role]:.0f}); "
                    f"paused until {resume:%a %H:%M}")
                self.save_state(role, status="budget-paused", resumes=resume.isoformat(timespec="minutes"))
                self.wait_until(role, resume)
                continue
            before = self.open_pr_heads() if role in CHANGES_PRS else None
            try:
                outcome, nxt = self.run_pass(role)
            except Exception as e:  # never let one pass kill the worker
                log(f"{role}: supervisor error: {e!r}")
                outcome, nxt = "failed", 0
            if outcome == "failed":
                nxt = RETRY_BACKOFF[min(failures, len(RETRY_BACKOFF) - 1)]
                failures += 1
            else:
                failures = 0
            if role in CHANGES_PRS and outcome == "ok" and self.open_pr_heads() != before:
                log(f"{role} changed a pull request; waking the reviewer")
                self.wake["reviewer"].set()
            nxt_at = dt.datetime.now() + dt.timedelta(minutes=nxt)
            self.save_state(role, next=nxt_at.isoformat(timespec="minutes"))
            self.wait_until(role, nxt_at)

    def wait_until(self, role: str, when: dt.datetime) -> None:
        """Wait until the wall-clock time `when`, or until woken.

        Waits in short steps and rereads the clock each time: on Windows a timed wait does not
        count time the machine spends asleep, so one long wait can run hours late after sleep.
        """
        while not self.stop.is_set():
            left = (when - dt.datetime.now()).total_seconds()
            if left <= 0 or self.wake[role].wait(timeout=min(left, WAIT_STEP)):
                break
        self.wake[role].clear()

    def run_forever(self) -> None:
        threads = [threading.Thread(target=self.worker, args=(r,), daemon=True) for r in self.roles]
        for t in threads:
            t.start()
            time.sleep(5)   # stagger the first passes
        try:
            while any(t.is_alive() for t in threads):
                time.sleep(1)
        except KeyboardInterrupt:
            log("stopping (Ctrl+C); passes in progress are abandoned")
            self.stop.set()


# ---------- single-instance lock ----------

def pid_alive(pid: int) -> bool:
    if os.name == "nt":   # os.kill(pid, 0) would send CTRL_C_EVENT on Windows
        r = run(["tasklist", "/FI", f"PID eq {pid}", "/NH"])
        return str(pid) in r.stdout
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def acquire_lock() -> Path:
    LOGS.mkdir(exist_ok=True)
    lock = LOGS / "supervisor.pid"
    if lock.exists():
        try:
            pid = int(lock.read_text().strip())
        except ValueError:
            pid = 0
        # On a restart the old supervisor may still be exiting; give it a minute.
        for _ in range(12):
            if not (pid and pid_alive(pid)):
                break
            time.sleep(5)
        else:
            sys.exit(f"supervisor already running (pid {pid})")
    lock.write_text(str(os.getpid()))
    return lock


# ---------- commands ----------

def cmd_status(_args) -> None:
    path = LOGS / "state.json"
    state = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    lock = LOGS / "supervisor.pid"
    pid = int(lock.read_text()) if lock.exists() and lock.read_text().strip().isdigit() else 0
    print(f"supervisor: {'running (pid %d)' % pid if pid and pid_alive(pid) else 'not running'}")
    for role in ROLES:
        s = state.get(role, {})
        print(f"{role}: {s.get('status', 'never run')}; last {s.get('finished') or s.get('started', '-')}; "
              f"next {s.get('resumes') or s.get('next', '-')}")
        if s.get("summary"):
            print(f"  {s['summary']}")
    r = run(["gh", "pr", "list", "--state", "open"], cwd=REPO)
    print("open pull requests:\n" + (r.stdout.strip() or "  none"))


def cmd_usage(args) -> None:
    records = load_records(LOGS)
    now = dt.datetime.now()
    midnight = now.replace(hour=0, minute=0, second=0, microsecond=0)
    print("Estimated cost is Claude Code's own estimate. On a subscription it is not billed, but it")
    print("tracks use of the shared plan allowance. For the plan's real limits, run /usage in an")
    print("interactive Claude Code session.\n")
    for label, since in (("today", midnight), ("last 7 days", now - dt.timedelta(days=7))):
        print(f"== {label}")
        summary = summarize(records, since)
        if not summary:
            print("  no passes")
        for role in ROLES:
            s = summary.get(role)
            if not s:
                continue
            cap = f" of ${args.daily[role]:.0f} daily cap" if label == "today" else ""
            print(f"  {role:9} {s['passes']:3} passes {s['minutes']:6.0f} min  ${s['usd']:7.2f}{cap}")
            for model, n in sorted(s["tokens"].items(), key=lambda kv: -kv[1]):
                print(f"            {model:24} {n:>12,} tokens")


def cmd_setup(args) -> None:
    run(["git", "-C", str(REPO), "fetch", "-q", "origin"])
    for role in ROLES:
        wt = args.worktrees / role
        if not (wt / ".git").exists():
            log(f"creating worktree {wt}")
            r = run(["git", "-C", str(REPO), "worktree", "add", "--detach", str(wt), "origin/main"])
            if r.returncode:
                sys.exit(r.stderr)
        log(f"{role}: fetching the Mathlib cache and building (first time: several minutes)")
        for step in (["lake", "exe", "cache", "get"], ["lake", "build"]):
            r = run(step, cwd=wt / "halfline_lt")
            if r.returncode:
                sys.exit(f"{' '.join(step)} failed in {wt}:\n{r.stdout[-2000:]}{r.stderr[-2000:]}")
    log("worktrees ready")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--worktrees", type=Path, default=DEFAULT_WORKTREES)
    ap.add_argument("--model", default=DEFAULT_MODEL, help="model for author and reviewer")
    ap.add_argument("--explorer-model", default=None,
                    help=f"model for the explorer (default {ROLE_MODEL['explorer']})")
    ap.add_argument("--roles", default=",".join(ROLES),
                    help="comma-separated roles to run (default: all)")
    ap.add_argument("--daily-budgets", default="",
                    help="daily estimated-USD caps, e.g. explorer=25,author=20 "
                         f"(default {DAILY_BUDGET_USD})")
    ap.add_argument("--pass-budgets", default="",
                    help=f"per-pass estimated-USD caps, e.g. explorer=15 (default {PASS_BUDGET_USD})")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run", help="run all roles until stopped")
    sub.add_parser("usage", help="passes, tokens and estimated cost per role, today and last 7 days")
    once = sub.add_parser("once", help="run a single pass of one role")
    once.add_argument("role", choices=ROLES)
    once.add_argument("--dry-run", action="store_true")
    sub.add_parser("status", help="show the last and next pass of each role")
    sub.add_parser("setup", help="create the worktrees and build Lean")
    args = ap.parse_args()
    roles = tuple(r for r in args.roles.split(",") if r)
    bad = [r for r in roles if r not in ROLES]
    if bad:
        sys.exit(f"unknown role(s): {', '.join(bad)}; choose from {', '.join(ROLES)}")
    try:
        args.daily = parse_budgets(args.daily_budgets, DAILY_BUDGET_USD)
        args.per_pass = parse_budgets(args.pass_budgets, PASS_BUDGET_USD)
    except ValueError as e:
        sys.exit(str(e))

    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "usage":
        return cmd_usage(args)
    if args.cmd == "setup":
        return cmd_setup(args)
    if args.cmd == "once":
        sup = Supervisor(args.worktrees, args.model, dry_run=args.dry_run,
                         explorer_model=args.explorer_model, pass_budget=args.per_pass)
        outcome, nxt = sup.run_pass(args.role)
        print(f"{args.role}: {outcome}; would run next in {nxt} min")
        return
    lock = acquire_lock()
    try:
        sup = Supervisor(args.worktrees, args.model, roles=roles, explorer_model=args.explorer_model,
                         pass_budget=args.per_pass, daily_budget=args.daily)
        log(f"supervisor started: roles {', '.join(roles)}; models {sup.models}; "
            f"daily caps {sup.daily_budget}; worktrees {args.worktrees}")
        sup.run_forever()
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
