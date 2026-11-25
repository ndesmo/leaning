# Ledger

The index of everything proved here, the reusable Lean lemmas, the open gaps and the approaches
that failed. `/prove`, `/conjecture` and `/attack` read this first. `/publish-proofs` updates it
whenever something ships. Details live in each result's notes file.

Status words:
- **published**: live on the site.
- **open**: stated precisely, not proved.
- **idea**: untested.

## Results

### halfline-lieb-thirring: published 2026-11-25

- Page: https://ndesmo.github.io/leaning/halfline-lieb-thirring/
- Notes: [notes/halfline-lieb-thirring.md](notes/halfline-lieb-thirring.md)
- Write-up: [RESULTS.md](RESULTS.md)
- Lean: [halfline_lt/HalflineLt/Spec.lean](halfline_lt/HalflineLt/Spec.lean), 70 theorems, all clean.
- Reviewed 2026-11-25 by two independent Claude subagents (`/review`). There were 26 findings and
  all were addressed; see the notes' Review section.

| Result | Statement | Lean |
|---|---|---|
| Theorem 1 | L^N_γ ≤ Lcl(γ) + L1(γ) for γ ≥ 3/2 | `neumann_upper_ELU`, `even_extension_mass`, `r_lt_one` |
| Corollary 2 | Star graphs, odd N, γ ≥ 3/2: L_{γ,N} ≤ Lcl + L1/N | `star_graph_bound`, `star_graph_bound_strict` |
| Theorem 3 | 0 ≤ V ≤ 6a⁻² sech²(x/a) a.e. ⇒ S_γ ≤ 2L1·M_γ, all γ ≥ 1/2. Equality for half-solitons when 1/2 < γ ≤ 5/2, and only for V = 0 at γ = 1/2. "Only half-solitons" is conditional on G9. | `psi2_two_unique_zero`, `at_most_one_state_ok`, `half_soliton_fits_iff_gamma` |
| Corollary 4 | A counterexample needs ≥ 2 Neumann states, must exceed every envelope, and has e > 2 − 1/r(γ) | `beating_needs_big_ground_state`, `threshold_tendsto_one` |

## Reusable Lean lemmas

All of these are in `HalflineLt/Spec.lean`, namespace `HalflineLt`. Reuse them with
`import HalflineLt.Spec`.

| Topic | Theorems |
|---|---|
| LT constants and their ratio | `L1`, `Lcl`, `r`, `L1_eq_r_mul_Lcl`, `Lcl_pos`, `L1_lt_Lcl`, `upper_bound_lt_two_Lcl`, `threshold_identity`, `r_eq_exp`, `r_strictAntiOn`, `r_lt_one`, `one_lt_r`, `two_exp_neg_one_lt_r`, `continuousOn_r`; closed forms `L1_one`, `L1_two`; numeric bounds `two_L1_one_bounds`, `two_L1_two_bounds` |
| Pöschl–Teller eigenfunctions | `psi0`, `psi2`, `pt_ground_state`, `psi0_neumann`, `psi2_neumann`, `pt_second_even_state`, `pt_second_even_state_sq_integrable`, `deriv_psi0`, `deriv_psi2`, `deriv2_psi2`, `psi2_two_formula`, `psi2_two_unique_zero`, `resonance_at_five_halves` |
| sech² envelopes | `envelope_excludes_large`, `half_soliton_fits_iff`, `half_soliton_fits_iff_gamma`, `sech2_family_opt` |
| Inequalities for t^p | `real_add_rpow_le` (superadditivity, p ≥ 1), `add_rpow_ge_tangent` (tangent bound, p ≥ 2) |
| Abstract spectral bookkeeping | `fact_a` … `fact_d`, `Admissible`, `single_state_ok`, `at_most_one_state_ok`, `localization_bookkeeping`, `uniqueness_skeleton` |
| Integrals | `even_extension_mass` (∫_ℝ V(\|x\|)^p = 2∫₀^∞ V^p) |
| Completed square (Read–Schulz) | `complete_square`, `complete_square_rpow`, `riccati_match_iff`, `mExp_new_range` |

## Open gaps

Each gap has a GitHub issue (number in brackets). Approval, priority and progress live on the issue.

| Id | Gap | Status | Where |
|---|---|---|---|
| G1 (#11) | **Main conjecture:** L^N_γ = 2L1(γ) on (3/2, 5/2] | open | notes, Task 5 |
| G2 (#12) | **Step 5, far mass:** the second-order remainder R₂ and the excited-state error R₂′ are o(M(W)), uniformly over tails that create extra Neumann states. This would give the conjecture on [3/2, 3/2 + ε). | open, main obstacle | notes, Task 5 round 2 |
| G3 (#13) | **Step 3 uniformity:** the Carlen–Frank–Lieb stability constant stays bounded below as γ ↓ 3/2 | open, unchecked | notes, Task 5 round 2 |
| G4 (#14) | **Step 1 citation:** the γ = 3/2 equality case (trace formula plus reflectionless classification) holds on L¹ ∩ L² | open, citation to check | notes, Task 5 |
| G5 (#15) | **Step 4 citation:** a perturbation small in ∫(1 + x)\|W\| keeps exactly one Neumann state for ν ∈ (1, 2) | open, citation to check | notes, Task 5 |
| G6 (#16) | **Fully formal (b):** formalize ∫₀^∞ cosh^{−s} = (√π/2) Γ(s/2)/Γ((s+1)/2), so the half-soliton value 2L1 is computed in Lean | idea | none |
| G7 (#17) | **Theorem 3, Bargmann and Hardy classes:** at most one Neumann state when ∫xV < 1 or V ≤ 1/(4x²). Stated as a remark, not proved in detail. | idea | RESULTS.md, Thm 3 remarks |
| G9 (#19) | **Optimizer uniqueness citation:** find a source stating that the one-bound-state optimizers in 1D are exactly c²(γ² − 1/4) sech²(c(x − x₀)) (Keller 1961? Sz.-Nagy?). This is needed for the "only if" half of Theorem 3's equality case. | open, citation to find | review M3 |
|
| G8 (#18) | **Other conditions:** Robin conditions u′(0) = σu(0), or star graphs with even N or N₀ > 1. Do Theorem 1 and Theorem 3 transfer? | idea | none |

## Approaches that failed

Don't repeat these without a new ingredient.

- **Aizenman–Lieb with the γ = 3/2 deficit.** The averaged deficit vanishes at the soliton as
  γ ↓ 3/2. (notes, Task 5)
- **Cumulative mass (Benguria–Loss, Read–Schulz).** It works only at γ = 1, since the Riccati form
  needs m = 3 (`riccati_match_iff`, `mExp_new_range`).
- **CFL stability alone for Step 5.** Its power 2γ − 1 gives a deficit of order
  m^{(2γ−1)/(γ+1/2)}, too small against an m-sized tail contribution.
- **Young's inequality for the commuted tail potential.** It loses a factor up to 2^p, too much
  against 2r(γ). (notes, Task 5 round 2)
- **ELU-type bounds alone up to γ = 2.** There is no uniform two-state gap: a soliton plus a small
  distant bump has ratio → 1.
- **The γ = 5/2 KdV trace formula.** Its scattering term has the wrong sign for an upper bound
  (hand derivation, unverified).
- **Brute-force numerics.** No counterexample for γ ≤ 5/2 in four families. Use numerics to test
  claims, not as a proof strategy.
