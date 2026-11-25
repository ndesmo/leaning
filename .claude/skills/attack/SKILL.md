---
name: attack
description: Derive a proof of a target statement, reducing it to cited theorems plus elementary steps that Lean can check, and audit the edge cases before writing it up. Includes strategies that worked here and how to turn a stuck attempt into an honest partial result. Use after /literature has fixed what can be cited.
---

# /attack: derive the proof

Derive first. Search numerically only to test a step or find a counterexample.

## Before starting

- **Read `LEDGER.md`.**
  - If the target is a listed gap, read that gap's section in its notes file. Earlier attempts and
    their exact sticking points are recorded there.
  - Skip anything listed under "Approaches that failed" unless you have a new ingredient. Say what
    the ingredient is.
- **Reuse lemmas.** Before proving a lemma, check the ledger's reusable-lemma table and grep
  `halfline_lt/` for it. Import existing theorems (`import HalflineLt.Spec`) instead of re-proving
  them.

## Strategies that have worked

- **Combine published inequalities.** Two non-sharp bounds can combine into a better one. ELU (1.6)
  plus the one-bound-state bound gave Lcl + L1.
- **Restrict to where structure helps.**
  - Find a condition under which the sharp bound is easy. One bound state makes it the
    one-bound-state inequality.
  - Then find the largest natural class with that property.
  - Explicit solutions settle such classes: a zero-energy solution with one zero means one bound
    state, by Sturm oscillation.
- **Use symmetries.** Scaling, reflection and translation reduce a class to one representative,
  e.g. 6a⁻² sech²(x/a) → 6 sech² x.
- **Monotonicity and comparison.** Use min–max (V ≤ U ⇒ fewer bound states), and Dirichlet and
  Neumann bracketing.
- **Characterize counterexamples.** If the full claim resists, derive what a counterexample must
  satisfy. Each condition is a theorem, e.g. Corollary 4.
- **Find the critical case.** Where the claim stops holding, find the mechanism (a resonance, a new
  bound state). It explains the sharpness and often yields an explicit Lean-checkable function.

## Write the proof as steps

- Each step is one claim with one label: `[Lean]`, `[paper: …]` or `[standard: …]`.
- Every elementary step becomes a separate Lean theorem for `/lean-check`: algebra, an inequality,
  a derivative, a zero, a limit, an integrability bound.
- Cited steps state exactly which hypothesis of the cited theorem is being met, and how.

## Audit before writing up

Check each of these explicitly:
- endpoints of every parameter range (γ = 1/2, 3/2, the critical value);
- the zero and degenerate inputs (V ≡ 0);
- infinite sums or spectra;
- the equality case in both directions;
- the direction of every inequality, after any division by a quantity that could be negative or
  zero.

## When stuck

- State the gap precisely in the notes, along with the step that would close it.
- Add the gap to `LEDGER.md`'s open-gaps table. If an approach died, add it to "Approaches that
  failed" with the reason.
- Check whether what is already proved forms a coherent partial result: a subclass, a bound, or
  necessary conditions. If so, publish that, with the gap in "What remains open".
- Never present a step as proved because it seems plausible. Unchecked uniformity, constants or
  hypotheses go in the open-questions list.
