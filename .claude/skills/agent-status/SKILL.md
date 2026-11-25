---
name: agent-status
description: Report what the author and reviewer loops are doing and whether anything needs the user. Runs tools/agent-status.ps1 (read-only) and summarizes worktrees, open PRs with CI and review state, and each agent's recent actions, flagging stalls. Use when the user asks what the agents are doing, how a PR is going, or whether the loops are still running.
---

# /agent-status: what the loops are doing

Run from the main checkout: `& .\tools\agent-status.ps1` (add `-Actions 20` for more history). It
only reads: worktrees, `gh`, and the local session logs in `~/.claude/projects/`.

Then report in a few lines:
- **Each agent:** its current task in plain words (from its last actions), and when it next wakes.
- **Each open PR:** CI result, review state, and whether it is **ready for the user to merge** (CI
  passed, reviewed at the latest commit, no unanswered blocking findings).
- **Anything needing the user, first:**
  - "POSSIBLY STUCK": usually a permission prompt waiting in that terminal. Ask the user to look
    at it and to tell you the command, so it can be allowlisted through a PR.
  - CI failing.
  - A loop that has stopped.

Rules:
- Do not act on the loops' work: no commits, pushes or PR comments from here.
- The session logs contain private details (paths, the user's email). Quote only what the user
  needs, and never copy log contents into the repo.
