# Lessons from past proofs

Concrete episodes behind the rules in the skills. Read the section for the stage you are in. These
are examples, not a template: new problems may need different moves.

## Finding targets (/conjecture)

- **Paper remarks are targets.** Demirel-Frank's Remark (4) on star graphs asked whether
  L_{γ,1} ≤ 2L_γ could be improved. Answering it became Corollary 2.
- **Partial results are what got published.** The full conjecture (L^N_γ = 2L1 on (3/2, 5/2]) stayed
  open, but three weaker statements were provable:
  - an improved bound, by combining two published inequalities;
  - the conjecture on a natural subclass (potentials under a critical envelope);
  - necessary conditions on a counterexample.
- **Validate the solver on the failure side.** At γ = 3 the half-soliton is known to beat 2L1.
  Reproducing that, `R/(2L1) ≈ 1.000119`, showed the numerics could detect a counterexample.
- **Grid artifacts.** An early search "found" counterexamples that were discretization error.
  A two-grid Richardson objective with a penalty removed them.

## Literature (/literature)

- **Parity hypotheses matter.** Demirel-Frank's Prop. 4 needs N₀ < N *both odd*. The first draft
  of Corollary 2 relied on a paraphrase that dropped this.
- **Lifting arguments need their conditions checked.** ELU's Cor. 1.3 lifts γ = 3/2 to γ ≥ 3/2 by
  Aizenman–Lieb. That needs the left side to be monotone in each eigenvalue, with weights ≥ 0. Check
  this; don't assume it.
- **Papers state things loosely.** Demirel-Frank's eq. (5) says L_{γ,N} = L_γ "for all N" (quoted
  from Demirel–Harrell), but it cannot hold for N = 1. Note such slips; never build on them.
- **Preprints are labeled as preprints.** The Read–Schulz γ = 1 result is unrefereed and says it was
  developed with AI.

## Proving (/attack)

- **Combining two non-sharp inequalities can beat both.** ELU's (1.6) bounds ½|E₁|^γ + Σ_{j≥2}; the
  one-bound-state bound controls |E₁|^γ. Added, they give Lcl + L1 < 2Lcl.
- **Bound-state counting through explicit solutions.** A zero-energy solution with one zero means
  one bound state (Sturm oscillation). For 6 sech² that solution is 1 − 3 tanh², which Lean handles
  easily. Scaling and min–max then extend the count to a whole class.
- **The critical case explains sharpness.** The class stops at 6 sech² because the even sector has
  a zero-energy resonance there (ν = 2, γ = 5/2). Finding the mechanism made the theorem's boundary
  natural.
- **Edge cases the first write-up got wrong:**
  - "finitely many eigenvalues": the negative spectrum can be infinite;
  - the equality case at γ = 1/2, where the bound is strict;
  - V ≡ 0;
  - a hypothesis (∫(1 + x)V < ∞) imposed on all V when only the envelope needs it.

## Publishing (/review, /publish-proofs)

- **Uniformity claims.** "What remains open" first said Carlen–Frank–Lieb stability makes a
  counterexample close to a soliton. That needed the stability constant to be uniform in γ, which
  was never checked.
- **Antivirus slowdown.** Lean builds can take 10× longer while McAfee scans the Mathlib `.olean`
  files. Run long checks in the background and don't restart them.
