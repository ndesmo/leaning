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

- `git fetch origin`, then list your open PRs:
  `gh pr list --state open --author @me --json number,title,headRefName`, keeping those whose
  branch starts with `agent/`. Other people's PRs are not yours to fix. "Claims" in `/prove`
  defines `<me>`, claiming and releasing.
- Work only in this worktree. Never edit `.claude/settings*.json` or `.github/workflows/`.
- Tidy the queue. Release your own claims whose PR was merged or closed, as "Claims" says. Only
  claims whose claim comment names an `agent/` branch are the author's: the explorer and reviewer
  may share your login, so skip `moonshot` issues and any claim naming another branch prefix. Never
  touch an issue claimed by someone else.

## 2. Keep your open PRs healthy (this comes before new work)

**Always start from GitHub's copy of a PR branch.** Someone else may have pushed to it. Run
`git fetch origin`, then `git checkout -B <branch> origin/<branch>`. Never work from a stale local
copy.

**Conflicts with main.** For each of your open PRs, check `gh pr view <n> --json mergeable`. If it
is `CONFLICTING`, CI cannot run and the PR cannot merge:
- check out its branch from origin (above);
- `git merge origin/main`, then resolve each conflict by keeping both sides' intent (usually main's
  structure plus the PR's new content);
- check the result with `git diff origin/main`: only the PR's intended changes may differ;
- commit, push, and comment on the PR with what you resolved.

That is the whole iteration. Go to step 5.

**Reviewer comments.** For each open PR with a reviewer-loop comment (marked `<!-- reviewer-loop`)
newer than your last push to it:
- check out its branch from origin (above);
- address **every** finding: fix it, or rebut it with a reason. Record each finding and your
  response in the notes' Review section;
- rerun `/lean-check` if Lean or a claim changed, commit, and push;
- reply on the PR, one line per finding: fixed (commit) or rebutted (reason).

That is the whole iteration. Go to step 5.

## 3. Otherwise, start one unit of new work

- **If 2 or more of your PRs are open, do nothing.** The user merges at their own pace. Go to
  step 5.
- **Pick the target from the issue queue.** List
  `gh issue list --state open --label approved --json number,title,labels`. Add the open
  sub-issues of each listed issue (`gh api repos/ndesmo/leaning/issues/<n>/sub_issues`), which
  carry no `approved` label of their own, and prefer them to their parent. Skip issues that are
  claimed (see "Claims" in `/prove`) or labelled `blocked` or `moonshot`; the explorer works the
  moonshots. Take the highest priority (`priority:high`, then normal, then low). Within a
  priority, **finish before you start**, in this order:
  1. units that finish a proved result (citations, Lean, page; "Finishing a result" in `/prove`);
  2. other units of problems already under way;
  3. a new problem.

  Within each group, take the oldest first.
  Only issues the owner labelled `approved` are eligible. You never add or remove `approved`, and
  you never work on an unapproved issue.
- **Claim it** as "Claims" says, and re-read to make sure you won. If you lost, pick the next one.
- **One unit only.** An issue may need several PRs. Each PR does one small, checkable unit: a
  citation to verify, one Lean lemma, one literature pass, one attack on a precisely stated gap.
- **Split big issues into sub-issues.** When an approved issue needs more than one unit, create a
  sub-issue for each unit you identify:
  - create it with `gh issue create`, with the parent's kind and priority labels, and never
    `approved`;
  - link it with `gh api -X POST repos/ndesmo/leaning/issues/<parent>/sub_issues -F sub_issue_id=<id>`,
    where `<id>` comes from `gh api repos/ndesmo/leaning/issues/<n> --jq .id`.

  A sub-issue is eligible only while its parent carries `approved`. Check the parent
  (`gh api repos/ndesmo/leaning/issues/<n>/parent`) before working on it. Work the units one at a
  time; the parent closes when its last unit lands.
- **Finish what is proved.** `/prove` defines when a result is finished (reviewed, citations
  checked, Lean, page).
  - **New results.** When your PR proves a result, or part of one stated exactly, file a sub-issue
    under the same approved parent for each missing item, and list them in the PR body.
  - **Results already merged.** When picking a target, check `LEDGER.md` for proved results that
    lack these sub-issues, and file them.
  - **Superseded targets.** When a result supersedes an open sub-issue's target, for example one
    asking for a special case of what is now proved, retarget it with `gh issue edit` (title and
    body) and comment why.
- **Starting a new problem** (an issue labelled `problem`). First re-check that it is still open:
  search for solutions dated after the scout's check.
  - If it has been solved, open a PR that marks it `rejected: solved by <ref>` in `PROBLEMS.md`,
    with `Closes #<n>`.
  - Otherwise give it a slug, a `LEDGER.md` entry and a `notes/<slug>.md` file, mark it `taken` in
    `PROBLEMS.md`, and make its first unit the scout's first target.
- **File what you defer.** Work that finishes an approved result goes under its parent (above).
  Anything else you notice but don't do in this unit goes in a new standalone issue labelled
  `follow-up` (never `approved`), with its source and what "done" means, for the owner to approve:
  new questions, extensions, other cases, tooling. Don't bury it in prose.
- **Branch.** Create `agent/<me>/<slug>-<short-stage>` from `origin/main`, so two contributors'
  branches never share a name.
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
  - the sub-issues filed to finish the result, if it proves one;
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

- If you changed anything on GitHub this iteration (an issue, label or PR), run
  `& .\tools\board-sync.ps1` so the project board matches.
- If everything is committed and pushed, finish on main: `git checkout --detach origin/main`. The
  next iteration then loads current instructions, not a PR branch's older copy. If something is
  uncommitted, leave it; preflight picks it up next time.
- Did something: wake in about 30 minutes.
- Idle, or at the PR limit: wake in 60 minutes.
- **Under `/loop`:** schedule the wake with `ScheduleWakeup`.
- **Started by the supervisor** (`tools/agents.py`; the arguments say `[supervisor]`): don't call
  `ScheduleWakeup`, and skip "Notify the reviewer", since the supervisor wakes the reviewer itself.
  End your final message with a line `NEXT: <minutes>`.

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
