---
name: formalizer-loop
description: One long unattended pass of the formalizer agent, which proves already-reviewed results in Lean. It takes only issues labelled `lean`, formalizes exactly the statement in the notes, keeps work in progress on its branch across passes, and opens small PRs of lemmas that build cleanly. It never merges and never pushes to main. Use only as the pass prompt of the formalizer role in tools/agents.py.
---

# /formalizer-loop: one formalizer pass

You turn proofs that already passed review into Lean. You run unattended, and the owner merges.
Follow the shared rules in `/prove`, including "Claims", and the Lean rules in `/lean-check`. Do
**one** Lean unit per pass, or one well-defined step of it.

## 0. Preflight (stop the pass if any check fails)

- The repo root (`git rev-parse --show-toplevel`) is this role's worktree: its folder is named
  `formalizer`, and `git rev-parse --git-dir` differs from `git rev-parse --git-common-dir`.
- `git status --porcelain` is empty, or you are on an `agent/*` branch with Lean work from the last
  pass. In that case continue it (step 2).
- `halfline_lt/.lake/packages/mathlib` exists. If not, say "run `python tools/agents.py setup`" and
  stop. Never download or delete the cache yourself.
- Never edit `.claude/settings*.json` or `.github/workflows/`.

## 1. Your open PRs first

List your PRs: `gh pr list --state open --author @me --json number,title,headRefName`, keeping
branches that start with `agent/<me>/lean-`. Handle them exactly as `/author-loop` step 2 says:
- conflicts with main;
- every reviewer-loop finding, fixed or rebutted.

If you did either, that is the pass. If 2 or more of your PRs are open, do nothing new.

## 2. Pick, or resume, one Lean unit

- **Resume** if you hold a claim on a `lean` issue: check out its branch from origin and continue
  from its progress note (below).
- **Otherwise pick:** issues labelled `lean` that are approved, or are sub-issues of an approved
  issue (check the parent, as in `/author-loop`), and are not claimed. Take the highest priority,
  then the oldest. Claim it as "Claims" in `/prove` says. Branch `agent/<me>/lean-<slug>` from
  `origin/main`.
- If there is none, end the pass with `NEXT: 120`.

## 3. Formalize

- **The statement comes from the notes.** Read the result's section in `notes/<slug>.md` and the
  `LEDGER.md` row. Formalize **exactly** that statement, with every hypothesis it states and no
  others.
- **Write the statement first.** Start with the Lean statement, with a docstring quoting the notes,
  as a `theorem ... := by sorry` skeleton, then fill in the proof. A `sorry` may live on your
  branch between passes, but never in a PR: before opening one, finish or remove every unfinished
  part, and keep its plan in the progress note.
- **If the statement is wrong or needs more,** for example an extra hypothesis, or a false case
  found while formalizing: stop. Do not prove a weaker statement in its place. Comment on the issue
  with the exact problem, file a `follow-up` issue for the author (never `approved`), keep your
  partial Lean on the branch, and release your claim.
- **Small units.** Split a long proof into lemmas. A PR may hold a few lemmas that build cleanly
  and pass the audit, even before the main theorem is done; it then says `Part of #<n>`.
- **Where files go:** `halfline_lt/Proofs/<Name>.lean`, imported from `halfline_lt/Proofs.lean`,
  as `/lean-check` says. Reuse existing lemmas; check `LEDGER.md` for them.
- **Check:** `lake build`, then the audit in `/lean-check` (no `sorry`, standard axioms only).
- **Search Mathlib** with grep over `.lake/packages/mathlib`, and with subagents for long searches.
  Do the heavy work in foreground subagents and keep your own context small.

## 4. Keep progress across passes

A proof often needs several passes. Before the pass ends:
- update a progress note at the top of the Lean file's module docstring: what is proved, what is
  left, and the next step;
- commit and push the branch, even if the proof is unfinished. Work that is not pushed is lost
  when the pass ends.

## 5. Open the PR

Open it when a unit builds and passes the audit. The PR body states:
- `Closes #<n>` if the issue's statement is now fully proved, otherwise `Part of #<n>`;
- each theorem's Lean name next to the statement in the notes, so the reviewer can compare them;
- the `#print axioms` result;
- what is left.

Then update the notes' claims ledger and `LEDGER.md` to label the proved parts `[Lean]`, and add a
dated line to the notes' Log. Run `python tools/agents.py board-sync` if you changed anything on
GitHub.

## 6. Finish

- If everything is pushed, end on main: `git checkout --detach origin/main`.
- **Started by the supervisor** (`[supervisor]` in the arguments): don't call `ScheduleWakeup`.
  End your final message with a line `NEXT: <minutes>`: 30 after progress, 120 when there was
  nothing to do.

## Never

- Add or remove the `approved` label, or work on an issue without approval.
- Change a statement to make it provable, or weaken it, without the steps in "If the statement is
  wrong".
- Use `sorry`, `admit`, `native_decide` or new axioms in a PR.
- Merge a PR, push to `main`, or force-push.
- Change permissions, CI or branch protection.
