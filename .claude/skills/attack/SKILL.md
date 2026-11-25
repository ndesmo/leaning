---
name: attack
description: Derive a proof of a target statement, reducing it to cited theorems plus elementary steps that Lean can check, reusing existing lemmas, and auditing edge cases before write-up. When stuck, records the precise gap and falls back to an honest partial result. Use after /literature has fixed what can be cited.
---

# /attack: derive the proof

Follow the shared rules in `/prove`. Its `lessons.md` has the moves that worked before.

## Before starting

- **Read `LEDGER.md`.** If the target is a listed gap, read its section in the notes, where earlier
  sticking points are recorded. Skip any approach listed as failed unless you have a new ingredient,
  and name that ingredient.
- **Reuse lemmas.** Search the reusable-lemma table and grep `halfline_lt/` before proving a lemma.
  Import existing ones (`import HalflineLt.Spec`).

## Moves to consider

- Combine published inequalities.
- Restrict to a class where the problem gets easy, then make the class as large as possible.
- Use explicit solutions and symmetries: scaling, reflection.
- Use monotonicity and comparison: min–max, bracketing.
- Derive necessary conditions on a counterexample.
- Find the mechanism at the critical case.

These are prompts, not a checklist. A new problem may need something else.

## Write the proof as steps

- One claim per step, each with a label.
- Each elementary step becomes its own Lean theorem for `/lean-check`.
- Each cited step says which hypotheses of the cited theorem are met, and how.

## Audit before writing up

Check each of these explicitly:
- endpoints of every parameter range;
- degenerate inputs;
- infinite sums or spectra;
- both directions of any equality case;
- the sign of anything you divide by or multiply an inequality by;
- any uniformity a limit argument needs.

## When stuck

- **Write down the gap.** State it precisely in the notes, along with the step that would close it.
  Add it to `LEDGER.md`'s open gaps. Add dead approaches to "Approaches that failed", with the
  reason.
- **Look for a partial result.** Check whether what is proved forms one: if so, publish that.
  Otherwise go back to `/conjecture` for a weaker target.
