#!/usr/bin/env python3
"""Supervisor for the author and reviewer agents. Standard library only; Windows, macOS, Linux.

Each pass is one fresh, non-interactive `claude -p "/<role>-loop ..."` run inside that role's
git worktree. The supervisor owns the schedule: it sleeps for the interval the pass asked for
(a final `NEXT: <minutes>` line), waits out usage limits, retries after crashes, and starts a
reviewer pass as soon as an author pass changes a pull request.

  python tools/agents.py run                 # run both roles until stopped (Ctrl+C)
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
ROLES = ("author", "reviewer")
DEFAULT_WORKTREES = Path("C:/w") if os.name == "nt" else Path.home() / "proofs-worktrees"
DEFAULT_MODEL = "claude-opus-5-5"
PASS_TIMEOUT = 2 * 60 * 60          # a pass that runs longer than this is killed
DEFAULT_NEXT = {"author": 30, "reviewer": 20}   # minutes, if a pass doesn't say
IDLE_NEXT = 60
RETRY_BACKOFF = [5, 15, 30, 60]     # minutes after consecutive failures
SUPERVISOR_NOTE = ("[supervisor] Started by tools/agents.py for a single iteration. Do not call "
                   "ScheduleWakeup and do not message other sessions; the supervisor schedules "
                   "and notifies. End your final message with a line `NEXT: <minutes>`.")
# Markers a parent Claude Code session leaves in the environment; children must not inherit them.
STRIP_ENV = ("CLAUDE_CODE_CHILD_SESSION", "CLAUDE_CODE_MESSAGING_SOCKET",
             "CLAUDE_CODE_MESSAGING_TOKEN", "CLAUDECODE", "CLAUDE_CODE_ENTRYPOINT",
             "CLAUDE_CODE_SSE_PORT")

_print_lock = threading.Lock()


def log(msg: str) -> None:
    with _print_lock:
        print(f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}", flush=True)


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
    if not re.search(r"hit your (session|weekly|usage)? ?limit|usage limit", text or "", re.I):
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


def agent_settings(main_settings_json: str) -> dict:
    """The --settings payload: main's allow and deny rules, never waiting on a prompt."""
    perms = json.loads(main_settings_json).get("permissions", {})
    return {"permissions": {"allow": perms.get("allow", []), "deny": perms.get("deny", []),
                            "denyInsteadOfPrompting": True}}


def child_env(base: dict) -> dict:
    env = {k: v for k, v in base.items() if k not in STRIP_ENV}
    env["CLAUDE_CODE_FORCE_SESSION_PERSISTENCE"] = "1"   # keep transcripts for status/auditing
    env["AGENT_SUPERVISOR"] = "1"
    return env


# ---------- one pass ----------

class Supervisor:
    def __init__(self, worktrees: Path, model: str, dry_run: bool = False):
        self.worktrees, self.model, self.dry_run = worktrees, model, dry_run
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
        if not self.dry_run:
            git(wt, "fetch", "-q", "origin")
            if not git(wt, "status", "--porcelain").stdout.strip():
                git(wt, "checkout", "-q", "--detach", "origin/main")
        settings_json = git(wt, "show", "origin/main:.claude/settings.json").stdout
        settings_file = LOGS / f"settings-{role}.json"
        settings_file.write_text(json.dumps(agent_settings(settings_json), indent=2), encoding="utf-8")

        cmd = [self.claude, "-p", f"/{role}-loop {SUPERVISOR_NOTE}", "--model", self.model,
               "--output-format", "json", "--permission-mode", "auto",
               "--permission-prompts", "none", "--settings", str(settings_file)]
        if self.dry_run:
            log(f"{role}: would run in {wt}: {' '.join(cmd[:3])} ...")
            return "dry-run", 0

        started = dt.datetime.now()
        self.save_state(role, status="running", started=started.isoformat(timespec="seconds"))
        log(f"{role}: pass started")
        try:
            r = run(cmd, cwd=wt, timeout=PASS_TIMEOUT, env=child_env(dict(os.environ)))
            out, err, code = r.stdout, r.stderr, r.returncode
        except subprocess.TimeoutExpired as e:
            out, err, code = (e.stdout or ""), (e.stderr or ""), -1
            if isinstance(out, bytes):
                out = out.decode("utf-8", "replace")
            if isinstance(err, bytes):
                err = err.decode("utf-8", "replace")
            err += f"\n[supervisor] killed after {PASS_TIMEOUT // 60} minutes"
        minutes = (dt.datetime.now() - started).total_seconds() / 60

        try:
            result = json.loads(out)
        except (json.JSONDecodeError, TypeError):
            result = {}
        text = result.get("result") or ""
        record = {"role": role, "started": started.isoformat(timespec="seconds"),
                  "minutes": round(minutes, 1), "exit_code": code,
                  "subtype": result.get("subtype"), "session_id": result.get("session_id"),
                  "cost_usd": result.get("total_cost_usd"), "result": text,
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
            before = self.open_pr_heads() if role == "author" else None
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
            if role == "author" and outcome == "ok" and self.open_pr_heads() != before:
                log("author changed a pull request; waking the reviewer")
                self.wake["reviewer"].set()
            nxt_at = dt.datetime.now() + dt.timedelta(minutes=nxt)
            self.save_state(role, next=nxt_at.isoformat(timespec="minutes"))
            self.wake[role].wait(timeout=nxt * 60)
            self.wake[role].clear()

    def run_forever(self) -> None:
        threads = [threading.Thread(target=self.worker, args=(r,), daemon=True) for r in ROLES]
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
        if pid and pid_alive(pid):
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
    ap.add_argument("--model", default=DEFAULT_MODEL)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("run", help="run both roles until stopped")
    once = sub.add_parser("once", help="run a single pass of one role")
    once.add_argument("role", choices=ROLES)
    once.add_argument("--dry-run", action="store_true")
    sub.add_parser("status", help="show the last and next pass of each role")
    sub.add_parser("setup", help="create the worktrees and build Lean")
    args = ap.parse_args()

    if args.cmd == "status":
        return cmd_status(args)
    if args.cmd == "setup":
        return cmd_setup(args)
    if args.cmd == "once":
        sup = Supervisor(args.worktrees, args.model, dry_run=args.dry_run)
        outcome, nxt = sup.run_pass(args.role)
        print(f"{args.role}: {outcome}; would run next in {nxt} min")
        return
    lock = acquire_lock()
    try:
        log(f"supervisor started (model {args.model}, worktrees {args.worktrees})")
        Supervisor(args.worktrees, args.model).run_forever()
    finally:
        lock.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
