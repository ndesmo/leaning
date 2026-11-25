---
name: author-loop
description: One unattended iteration of the author agent, run under /loop in the author worktree. It first answers reviewer comments on its own open PRs, otherwise does one stage of one result on a fresh branch and opens a PR. It never merges and never pushes to main. Use only as the /loop prompt of the author terminal.
---

# /author-loop: one author iteration

You run unattended, and the user merges. Follow the shared rules in `/prove`. Do **one** unit of
work, leave all state in files and PRs, then schedule the next wakeup.

## 0. Preflight (stop the iteration if any check fails)

- The repo root (`git rev-parse --show-toplevel`) is `C:/w/author`. Otherwise you were started in
  the wrong place: say so and do not schedule another iteration.
- `git status --porcelain` is empty, or you are on an `agent/*` branch with work in progress from
  your previous iteration. In that case finish or record that work first.
- `halfline_lt/.lake/packages/mathlib` exists. If not, say "run tools/setup-worktrees.ps1" and stop.
  Never download or delete the cache yourself.
- Never create, move or remove worktrees.

## 1. Sync

- `git fetch origin`, then list your open PRs: `gh pr list --state open --json number,title,headRefName`.
- Work only in this worktree. Never edit `.claude/settings*.json` or `.github/workflows/`.
- Tidy the queue. For each open issue labelled `in-progress` with no open PR of yours (its PR was
  merged or closed), remove `in-progress`, so its next unit can be picked again.

## 2. Reviewer comments come first

For each open PR with a reviewer-loop comment (marked `<!-- reviewer-loop`) newer than your last
push to it:
- check out its branch;
- address **every** finding: fix it, or rebut it with a reason. Record each finding and your
  response in the notes' Review section;
- rerun `/lean-check` if Lean or a claim changed, commit, and push;
- reply on the PR, one line per finding: fixed (commit) or rebutted (reason).

That is the whole iteration. Go to step 5.

## 3. Otherwise, start one unit of new work

- **If 2 or more of your PRs are open, do nothing.** The user merges at their own pace. Go to
  step 5.
- **Pick the target from the issue queue.** List
  `gh issue list --state open --label approved --json number,title,labels`. Skip issues labelled
  `in-progress` or `blocked`. Take the highest priority (`priority:high`, then normal, then low),
  oldest first. Only issues the owner labelled `approved` are eligible. You never add or remove
  `approved`, and you never work on an unapproved issue.
- **Claim it.** Add the label `in-progress` and comment on the issue with your branch name.
- **One unit only.** An issue may need several PRs. Each PR does one small, checkable unit: a
  citation to verify, one Lean lemma, one literature pass, one attack on a precisely stated gap.
- **Starting a new problem** (an issue labelled `problem`). First re-check that it is still open:
  search for solutions dated after the scout's check.
  - If it has been solved, open a PR that marks it `rejected: solved by <ref>` in `PROBLEMS.md`,
    with `Closes #<n>`.
  - Otherwise give it a slug, a `LEDGER.md` entry and a `notes/<slug>.md` file, mark it `taken` in
    `PROBLEMS.md`, and make its first unit the scout's first target.
- **File what you defer.** Anything you notice but don't do in this unit goes in a new issue
  labelled `follow-up` (never `approved`), with its source and what "done" means. Don't bury it in
  prose.
- **Branch.** Create `agent/<slug>-<short-stage>` from `origin/main`.
- **Do one stage** using the stage skills (`/conjecture`, `/literature`, `/attack`, `/lean-check`,
  `/proof-page`), in a subagent (see "Keep this session small").
- **Run `/review` before opening the PR** whenever the PR adds or changes a mathematical argument,
  a citation verdict or a claim label, in any file: pages, notes and `LEDGER.md` alike. Only purely
  mechanical PRs skip it.
- **If the attempt fails, still open the PR.** Record the honest negative result: the gap,
  stated precisely, and the failed approach in `LEDGER.md`. A failed attempt that is recorded is
  progress.

## 4. Open the PR

- Commit, using a message file and the Co-Authored-By trailer.
- Push the branch, then `gh pr create`. The body states:
  - `Closes #<n>` if this PR finishes the issue, otherwise `Part of #<n>`;
  - which stage this is;
  - what is claimed, with labels;
  - what Lean checks;
  - what is still open;
  - `/review` status;
  - "Merging publishes to the live site" if `docs/` changed.
- Add a dated line to the notes' Log.
- **Notify the reviewer.** After opening a PR, or pushing to one in step 2, find the reviewer
  session with `ListAgents`: the one named `reviewer`, or else the one working in `C:\w\reviewer`.
  Send it, with `SendMessage`, exactly: `PR #<n> has a new commit <sha>. Please review.` Nothing
  else. If no such session is listed, skip this; the reviewer's hourly check will find the PR.

## Keep this session small

This loop runs for weeks, so its own context must stay small. Do the heavy work of each stage
(reading papers, deriving, writing Lean, running checks) in a fresh `general-purpose` subagent.
- **Brief it with:** the target, the files and skills to follow, and what to return: the files it
  changed, a short summary, and each claim with its label.
- **Keep for yourself:** choosing the target, committing, opening the PR and notifying the reviewer.
- **Check its report before committing.** Read the diff yourself, and correct any label that claims
  more than the work shows.

## 5. Schedule the next iteration

- Did something: wake in about 30 minutes.
- Idle, or at the PR limit: wake in 60 minutes.

A run cut off by a usage limit loses nothing, because the next run resumes from the files and the
PRs.

## Never

- Add or remove the `approved` label, or work on an issue without it.
- Merge a PR.
- Push to `main`.
- Force-push.
- Change permissions, CI or branch protection.
- Weaken a claim label to get past review.
- Publish anything that is not in a PR.
