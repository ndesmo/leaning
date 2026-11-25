---
name: scout
description: Search all of mathematics for open problems this harness can make real progress on, verify they are still open, score them for Lean fit and tractability, and write a ranked shortlist to PROBLEMS.md for the user to choose from. Never starts work on a candidate. Use when the user wants new problems, or occasionally (about weekly) to refresh the shortlist.
---

# /scout: find new problems worth working on

Follow the shared rules in `/prove`. The scout proposes; the user chooses. Each candidate gets a
GitHub issue labelled `problem`, and nothing is worked on until the owner adds the label
`approved` to it.

## 1. Gather candidates, any area, in parallel

Run one `general-purpose` subagent per source family, in one message. Each returns at most 8
candidates.

**Source families:**
- Curated open-problem lists with tracked status. Examples: Thomas Bloom's Erdős problems
  database, the Open Problem Garden, the Kourovka Notebook, field-specific problem lists.
- Open problems already stated in Lean, such as Google DeepMind's `formal-conjectures`
  repository.
- Recent papers (the last 2–3 years) that state explicit open questions: "we leave open",
  "it would be interesting", "Problem n", "Conjecture n".
- MathOverflow questions with no accepted answer and real expert interest, and OEIS conjectures.

**Each candidate must come back with:**
- the statement, verbatim, with its source link and date;
- the evidence that it is open: the most recent status the agent found, and where;
- the partial results known;
- one concrete first target: a small case, a weaker version, a computation, a counterexample
  search, or a missing citation.

**Respect each site's access rules.** If a site's `robots.txt` or terms exclude AI agents, don't
fetch it, and don't work around the block with another tool or user agent. Use another source
whose terms allow it, or ask the user to paste what they want considered.
- Known case: erdosproblems.com disallows Claude's agents (robots.txt, checked 2026-11-25). Don't
  fetch it.
- A mirror such as the `teorth/erdosproblems` GitHub repository may be used only if its own
  license or terms allow it. Check them first.
- An official API (for example the Stack Exchange API, for MathOverflow) is fine when its terms
  allow the use. A different user agent, or a plain `curl` against a page the site blocks, is not.
- Put this rule in every scout subagent's brief, so agents launched in parallel all follow it.

## 2. Screen every candidate

**Still open.** Search for a solution after the source's date: arXiv, Google Scholar, the list's
own status page.
- Record what was searched.
- Any credible sign it is solved means reject. Rejection is cheap; claiming a known result as new
  is not.
- AI-found "solutions" to listed problems have often turned out to be already in the literature,
  so this check is never skipped.

**Lean fit, 0–2:**
- 2: Mathlib can state it directly.
- 1: it needs modest new definitions.
- 0: it needs theory Mathlib lacks.

**Tractability, 0–2:**
- 2: a concrete first target that a few iterations could finish.
- 1: a plausible partial result.
- 0: only the full problem is meaningful.

**Value, 0–2:** who asked, how much the answer matters, and whether a partial result is
publishable.

**Reject:**
- famous hard problems with no concrete partial target, such as the Riemann hypothesis or
  twin primes;
- anything whose statement is ambiguous.

## 3. Write `PROBLEMS.md`

**Keep two parts:**
- A ranked table: id, short name, area, scores (open-evidence / Lean / tractability / value),
  status.
- One section per candidate: verbatim statement, source, open-status evidence with what was
  searched and the date, known partial results, first target, risks.

**Status** is one of:
- `candidate (#<issue>)`: an open issue labelled `problem` and a priority, never `approved`.
  Approval lives only on the issue, where the owner adds the label.
- `taken (#<issue>)`: it has a slug in `LEDGER.md`.
- `rejected: <reason>`: no issue, or the issue closed with the reason.

**Keep the record.** Rejected candidates stay listed, with their reason, so later scouts don't
redo them.

## Never

- Start work on a candidate the user has not approved.
- Call a problem open without dated evidence.
- Pad the list: three solid candidates beat twenty weak ones.
