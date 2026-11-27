# Proofs by Claude

Mathematical results found and proved by Claude, an AI model made by Anthropic. Steps that can be
checked by machine are verified in Lean 4 with Mathlib; steps that rest on published theorems cite
them. Nothing here has been peer reviewed.

**Site:** https://ndesmo.github.io/leaning/

## Proofs

| Date | Proof | Lean |
|---|---|---|
| 2026-11-25 | [Sharp Lieb–Thirring bounds on the Neumann half-line](https://ndesmo.github.io/leaning/halfline-lieb-thirring/) ([RESULTS.md](RESULTS.md)) | [`halfline_lt/HalflineLt/Spec.lean`](halfline_lt/HalflineLt/Spec.lean) |

## Layout

- [`LEDGER.md`](LEDGER.md) indexes every result, the reusable Lean lemmas, the open gaps and the
  approaches that failed.
- `docs/` is the GitHub Pages site. `docs/index.html` lists the proofs, and each proof has its own
  folder, `docs/<slug>/index.html`.
- `halfline_lt/` is the Lean project (Lean 4.37.0-rc1, Mathlib v4.37.0-rc1).
- `RESULTS.md` holds the half-line statements and proofs; `notes/<slug>.md` is each result's working log; `results/` holds
  numerics output.

## Checking the Lean

```
cd halfline_lt
lake exe cache get
lake build
```

The build should report no `sorry`. `#print axioms` on each theorem shows only `propext`,
`Classical.choice` and `Quot.sound`. Spectral theorems that Mathlib lacks enter the Lean statements
as explicit hypotheses; each proof page says which ones.

## Backlog

Work is tracked in [GitHub Issues](https://github.com/ndesmo/leaning/issues); knowledge is kept in
files.

| Label | Meaning |
|---|---|
| `approved` | The owner said yes. Only the owner adds it; agents work only on these. |
| `priority:high` / `normal` / `low` | The order in which approved work is taken. |
| `gap`, `problem`, `follow-up`, `tooling` | What kind of item it is. |
| `in-progress`, `blocked` | Its current state. |

- **Approving.** To approve something, add the `approved` label on GitHub; no pull request is
  needed.
- **Board.** The [project board](https://github.com/users/ndesmo/projects/1) shows the same
  items in Todo / In Progress / In Review / Done. `python tools/agents.py board-sync` keeps it in
  step, and the author runs it after each iteration.
- **Sub-issues.** Big items are split into sub-issues, one per pull request-sized unit. A sub-issue
  is approved while its parent is.
- **Finishing results.** When a result is proved, the author files sub-issues under the same
  parent to finish it: check citations, formalize it in Lean, write its page. Merging the page PR
  publishes it. New questions and extensions are filed as separate `follow-up` issues for the owner
  to approve.
- **Claims.** An agent claims an issue by assigning its GitHub login and adding `in-progress`,
  then backs off if someone else claimed it first. It never changes another login's claim. A claim
  with no activity for 48 hours (7 days for a moonshot) may be taken over. Rules: "Claims" in
  `.claude/skills/prove/SKILL.md`. Several contributors with write access can run agents at once on this basis;
  assigning needs write access, and there is no fork workflow yet for contributors without it.
- **Linking.** Pull requests say `Closes #n` or `Part of #n`.
- **Files.** `LEDGER.md` (results, gaps, failed approaches) and `PROBLEMS.md` (scouted candidates
  and their evidence) link each item to its issue.

## Running the agents

Three agents work in separate git worktrees, and only the owner merges. To run them yourself, see
[`CONTRIBUTING.md`](CONTRIBUTING.md).

### Roles

- **Author:** works approved issues in small, reviewed units, one pull request each.
- **Reviewer:** independently reviews every pull request.
- **Explorer:** works approved `moonshot` issues in long passes. It runs several strategies in
  parallel, including computer searches for certificates, keeps a research journal on a branch
  `explore/<slug>`, and opens a pull request only for a verified finding or a clean negative result.

Searches may use any tool. A claim needs an independently checked certificate, ideally checked
in Lean.

### Supervisor (Windows, macOS, Linux)

`tools/agents.py` (Python 3.9+, standard library only) runs each agent pass as a fresh,
non-interactive `claude -p` session. It schedules the next pass, waits out usage limits, retries
after failures, and starts a reviewer pass as soon as the author changes a pull request.

```
python tools/agents.py doctor          # check the prerequisites; changes nothing
python tools/agents.py setup           # create the worktrees and build Lean (once; safe to rerun)
python tools/agents.py run             # run the agents until stopped
python tools/agents.py status          # last pass, next pass, open pull requests
python tools/agents.py usage           # passes, tokens and estimated cost per role
python tools/agents.py once reviewer   # a single pass, for testing
python tools/agents.py board-sync      # bring the project board in step with GitHub
python tools/agents.py teardown        # remove the worktrees; refuses if work would be lost
```

- **Models.** The author and reviewer use `claude-opus-5-5`. The explorer defaults to
  `claude-fable-5-2`; `--explorer-model` changes it.
- **Budgets.** All agents share one plan allowance. Each pass is capped (`--pass-budgets`), and
  each role has a daily cap (`--daily-budgets`, for example `explorer=25`). A role that reaches its
  cap pauses until midnight. The amounts are Claude Code's estimated USD, which is only a proxy on a
  subscription; run `/usage` in an interactive session for the plan's real limits.
- **Worktrees:** `C:\w\` on Windows, `~/proofs-worktrees/` elsewhere. Change with `--worktrees`.
- **Logs:** every pass is logged in `.agent-logs/`, with a summary in `.agent-logs/supervisor.log`.
- **Permissions:** the agents' allow and deny rules always come from `main`'s
  `.claude/settings.json`, and anything unlisted is denied, never left waiting on a prompt. The
  agents cannot push to `main`, merge, approve issues, or change CI or permissions.
- **Sleep.** Nothing runs while the machine sleeps; passes that are due start within a minute of
  waking.

**Start it at login** (replace `<repo>` with the full path of your clone):
- **Windows** (PowerShell, once):
  `Register-ScheduledTask -TaskName "Proofs supervisor" -Trigger (New-ScheduledTaskTrigger -AtLogOn -User $env:USERNAME) -Action (New-ScheduledTaskAction -Execute pythonw.exe -Argument "<repo>\tools\agents.py run" -WorkingDirectory <repo>)`
- **macOS:** a LaunchAgent plist whose `ProgramArguments` is `python3 <repo>/tools/agents.py run`,
  with `RunAtLoad` and `KeepAlive` set.
- **Linux:** a systemd user unit with `ExecStart=python3 <repo>/tools/agents.py run` and
  `Restart=always`; enable it with `systemctl --user enable --now`.

After pulling changes to `tools/`, restart the supervisor so it runs the new code.

**Older Windows scripts.** `tools/*.ps1` (interactive `/loop` terminals, worktree setup and
teardown, status, board sync) still work on Windows but are superseded by the commands above.

## Adding a proof

Proofs reach the site through pull requests, like everything else:

1. Put the write-up in `docs/<slug>/index.html`, labelling each step as Lean, paper or standard.
2. Add an entry at the top of the list in `docs/index.html` and a row to the table above.
3. Open a pull request. When the owner merges it, the site updates within a few minutes.

## Licence

- **Code** (Lean, Python, PowerShell, agent instructions under `.claude/`, CI): Apache License 2.0,
  in [`LICENSE`](LICENSE). Mathlib uses the same licence.
- **Mathematics and prose** (`docs/`, `notes/`, `RESULTS.md`, `LEDGER.md`, `PROBLEMS.md` and other
  Markdown): Creative Commons Attribution 4.0 International, in
  [`LICENSE-CC-BY-4.0`](LICENSE-CC-BY-4.0).

Copyright the "Proofs by Claude" contributors. Contributions are accepted under the same terms.
