# Contributing

"Proofs by Claude" is worked on by Claude Code agents. You contribute by running the agents on
your own machine, with your own Claude plan. They pick up approved work from the issue queue, open
pull requests, and review each other's pull requests. The owner approves work and merges.

This guide is for collaborators with **write access** to the repository. There is no fork workflow
yet, so ask the owner for access first.

## What you need

| Tool | Why | Get it |
|---|---|---|
| Python 3.9+ | runs the supervisor, `tools/agents.py` | python.org, or your package manager |
| Git | worktrees and branches | git-scm.com |
| GitHub CLI `gh`, signed in | issues, pull requests, the board | cli.github.com, then `gh auth login` |
| Claude Code | the agents themselves | claude.com/claude-code, then sign in |
| Lean's `elan` | builds and checks the Lean proofs | github.com/leanprover/elan |
| PowerShell 7 (`pwsh`) | the Lean audit scripts that CI also runs | aka.ms/powershell; built into Windows as `powershell`, but install 7 for parity |

Each agent worktree holds its own copy of the Mathlib build cache, about 7 GB, so allow roughly
30 GB of free disk space for all four.

## Get running

```
git clone https://github.com/ndesmo/leaning.git
cd leaning
python tools/agents.py doctor    # checks everything above; changes nothing
python tools/agents.py setup     # worktrees, Mathlib cache, Lean build, a self-test
python tools/agents.py run       # runs the agents until you stop it (Ctrl+C)
```

To keep the agents running across reboots, start the supervisor at login. The README, under
"Start it at login", has the command for Windows, macOS and Linux.

## Controlling cost

The agents run on your Claude plan, and the explorer is the most expensive.
- **Pick roles.** The roles are author, reviewer, explorer and formalizer. `--roles author,reviewer`
  runs only those two.
- **Cap spending.** `--daily-budgets explorer=15` and `--pass-budgets explorer=8` set daily and
  per-pass caps. A role that reaches its daily cap pauses until midnight.
- **Change the explorer's model.** `--explorer-model claude-opus-5-5` uses less allowance than the
  default.
- **Watch it.** `python tools/agents.py usage` reports passes, tokens and estimated cost per role.

The supervisor waits out usage limits on its own and resumes when they reset.

## Rules the agents follow

These are in the skills under `.claude/skills/`, and they apply to people too.

- **Only approved work.** Only the owner adds the `approved` label. Agents never add or remove it,
  and work only on approved issues or their sub-issues.
- **Claims.** Before working on an issue, an agent assigns itself and adds `in-progress`, then
  backs off if someone else claimed it first. A claim with no activity for 48 hours (7 days for a
  moonshot) may be taken over. Details: "Claims" in `.claude/skills/prove/SKILL.md`.
- **One unit per pull request.** Every PR is reviewed by the reviewer agent and passes CI. Only
  the owner merges.
- **Truth first.** Every claim carries a label saying what supports it: Lean, a cited paper, a
  numerical check, our own argument, and so on. Novelty is never claimed beyond "not found in the
  works searched". The rules are in `.claude/skills/prove/SKILL.md`.
- **Credit.** Results are credited to Claude, the AI model, not to whoever ran the agents.
- **Privacy.** Nothing committed may contain personal paths, names or email addresses.

## Changing the process

Skills, tools and CI change through pull requests like everything else. The reviewer flags any
change under `.claude/`, `tools/` or `.github/` for the owner's own review. Agents cannot change
`.claude/settings.json` or the CI workflow; only the owner can.

## Stopping and cleaning up

- **Stop:** Ctrl+C, or stop the login task.
- **Remove the worktrees:** `python tools/agents.py teardown`. It refuses if any work there is
  uncommitted or unpushed.

## Licence

Code is under Apache-2.0 (`LICENSE`); mathematics and prose are under CC BY 4.0
(`LICENSE-CC-BY-4.0`). By contributing, you agree that your contributions are licensed the same way.
See "Licence" in the README for which files are which.
