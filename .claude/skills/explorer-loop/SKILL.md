---
name: explorer-loop
description: One long unattended pass of the explorer agent on a moonshot problem (an approved issue labelled `moonshot`). Runs several attack strategies in parallel subagents, including computer search for checkable certificates, keeps a research journal on a long-lived branch, and opens a PR only for a verified finding or a clean negative result. Use only as the pass prompt of the explorer role in tools/agents.py.
---

# /explorer-loop: one explorer pass

Follow the shared rules in `/prove`. **Be bold in what you attempt and strict in what you
claim.** You work on hard problems over many passes. Most passes produce journal entries, not
PRs, and that is expected.

## 0. Preflight (stop the pass if any check fails)

- The repo root (`git rev-parse --show-toplevel`) is this role's worktree: its folder is named
  `explorer`, and `git rev-parse --git-dir` differs from `git rev-parse --git-common-dir` (a linked
  worktree, not the main checkout). By default it is `C:\w\explorer` on Windows and
  `~/proofs-worktrees/explorer` elsewhere. Otherwise say so and stop.
- `git status --porcelain` is empty, or you are on an `explore/*` branch with work from the last
  pass. In that case commit it to the journal first.
- `halfline_lt/.lake/packages/mathlib` exists. If not, say "run `python tools/agents.py setup`" and stop.

## 1. Pick the moonshot

- Run `gh issue list --state open --label approved --label moonshot --json number,title,labels`
  and take the highest priority, oldest first.
- **One explorer per moonshot.** If you already hold a claim on a moonshot, keep working it. Never
  take one claimed by someone else; stale claims and claiming are as "Claims" in `/prove` says,
  with the 7-day limit. Claim before the first pass on a problem, and re-read to confirm you won.
- Never add or remove `approved`, and never work on an unapproved issue.
- If there is no approved moonshot, end the pass with `NEXT: 240`.

## 2. Load the journal

- **Branch.** Work on the branch `explore/<slug>`. If it exists on origin, run
  `git checkout -B explore/<slug> origin/explore/<slug>`. Otherwise create it from `origin/main`.
- **Read first.** Read the notes' **Exploration journal** section and `search/<slug>/README.md`.
  - Don't repeat a recorded dead end unless you have a new ingredient, and name the ingredient.
- **First pass on a problem:**
  - re-check that the problem is still open (search for solutions after the scout's date);
  - create `notes/<slug>.md`, a `LEDGER.md` entry and `search/<slug>/`;
  - mark the problem `taken` in `PROBLEMS.md` (the claim itself is already on the issue).
  - If the problem has been solved, record it and open a PR that marks it rejected
    (`Closes #<n>`).

## 3. Attack, in parallel

Choose two to four **genuinely different** strategies. For example:
- a computer search for a construction or certificate;
- a structural or derivational argument;
- a reduction to a known theorem;
- a counterexample hunt;
- a weaker or special case that is a result in its own right.

Run each in its own `general-purpose` subagent, in one message.

**Brief each subagent with:**
- the problem;
- the relevant journal entries;
- its strategy and a time budget (at most about 90 minutes);
- what to return:
  - what it tried;
  - its results, with exact reproduction commands;
  - any certificate files;
  - an honest verdict.

**Tools.** Searches may use any tool available: Python, Lean, or a solver if one is installed.
Write search code under `search/<slug>/`. A search that runs longer than one pass must save
checkpoints there, so the next pass can resume. Keep files under 50 MB; record larger output in the
journal instead of committing it.

## 4. Verify before believing

- **Check every certificate twice.** A claimed construction or certificate gets a second,
  independent checker written straight from the definition, sharing no code with the search. It
  also gets a Lean check where feasible.
- **Label honestly.** Until Lean checks it, label it `[numerical: certificate checked by an
  independent script]`, never "proved".
- **Arguments need review.** A structural argument is `[own argument, unreviewed]` until it passes
  `/review`.

## 5. Record

- Add a dated journal entry to the notes:
  - the strategies tried and their results;
  - dead ends, with the reason each one died;
  - the next ideas, ranked.
- Commit, and push `explore/<slug>`. Do this every pass, even when nothing worked.

## 6. Open a PR only for a finding

Findings that qualify:
- a verified certificate or construction;
- a proved lemma or special case;
- a clean negative result, such as a precisely defined search space exhausted.

Then:
- **Run `/review` first.** The PR says `Part of #<n>` (or `Closes #<n>`) and lists the claim labels.
  If it changes `docs/`, say that merging publishes it.
- **Branch.** Open it from a branch cut from `explore/<slug>`, or from that branch itself.
- **Follow-ups.** File them as issues labelled `follow-up`, never `approved`.

## 7. End the pass

- If you changed anything on GitHub (an issue, label or PR), run `python tools/agents.py board-sync`.
- If everything is committed and pushed, finish on main: `git checkout --detach origin/main`.
- End with `NEXT: <minutes>`:
  - 30 if the attack is mid-way;
  - 120 if you are waiting on review;
  - 240 if you are blocked.

## Never

- Add or remove `approved`.
- Merge, push to `main`, or force-push.
- Call something proved without a Lean check or a passed `/review`.
- Delete another role's work, or work on issues that aren't labelled `moonshot`.
