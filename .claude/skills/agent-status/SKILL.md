---
name: agent-status
description: Report what the author, reviewer and explorer agents are doing and whether anything needs the user. Runs `python tools/agents.py status` and reads the supervisor log (read-only) and summarizes worktrees, open PRs with CI and review state, and each agent's recent actions, flagging stalls. Use when the user asks what the agents are doing, how a PR is going, or whether the loops are still running.
---

# /agent-status: what the loops are doing

Run from the main checkout, on any OS:
- `python tools/agents.py status`: each role's last pass, next pass and the open PRs;
- `python tools/agents.py usage`: passes, tokens and estimated cost per role;
- the last lines of `.agent-logs/supervisor.log`: what each pass reported.

On Windows, `& .\tools\agent-status.ps1` (add `-Actions 20` for more history) also shows each
agent's recent actions from the local session logs. All of these only read.

Then report in a few lines:
- **Each agent:** its current task in plain words (from its last actions), and when it next wakes.
- **Each open PR:** CI result, review state, and whether it is **ready for the user to merge** (CI
  passed, reviewed at the latest commit, no unanswered blocking findings).
- **Anything needing the user, first:**
  - A pass running far longer than usual, or repeated "pass failed" lines in the log.
  - CI failing.
  - A loop that has stopped.

Rules:
- Do not act on the loops' work: no commits, pushes or PR comments from here.
- The session logs contain private details (paths, the user's email). Quote only what the user
  needs, and never copy log contents into the repo.
