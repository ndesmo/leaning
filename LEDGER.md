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
| G9 (#19) | **Optimizer uniqueness citation:** for γ > 1/2 and V ≢ 0, the one-bound-state optimizers in 1D are exactly c²(γ² − 1/4) sech²(c(x − x₀)). Needed for the "only if" half of Theorem 3's equality case. Found: Carlen–Frank–Lieb, GAFA 24 (2014), Thm 2.1 proves the optimal potential is unique up to translation and dilation for d = 1, γ > 1/2 (the load-bearing source). The sharp constant, equal to L1(γ), is from Dolbeault–Esteban–Loss, C. R. Math. 353 (2015) 813–818, Lemma 1, and Frank, arXiv:2007.09326, eq. (23). DEL15 Lemma 1 also states the equality case, as q(q−1) sech² (q = γ + 1/2) "up to scalings, translations and multiplications by a positive constant"; the constant multiple is spurious (its own proof and CFL14 exclude it), and its "only if" is only sketched. Our own argument, reviewed 2026-11-25 (notes, G9 review): G9 steps 2–5 (combining the citations, the even extension has the Neumann ground energy and evenness forces x₀ = 0, the γ > 5/2 exclusion) and the constant identities. Page and RESULTS.md not yet updated; the page should then also cite DEL15 or Frank eq. (23) for the sharp one-bound-state bound, now cited only to LT76 (not accessed), and label its γ = 1/2 argument. | citation found and reviewed; page update pending | review M3; notes, G9 section and G9 review |
| G10 (#20) | **DF15 eq. (5) for odd N ≥ 3:** check Demirel–Harrell's claim L_{γ,N} = L_γ (γ ≥ 2) for odd N ≥ 3 with Kirchhoff conditions. This decides where Corollary 2 is new. | **checked 2026-11-25:** eq. (5) holds for star graphs with N ≥ 2 infinite edges and a Kirchhoff centre, by [DH10, Thm 2.5 + Rem. 2.6] on finite stars with Dirichlet ends, plus [standard: Dirichlet truncation limit] as the leaves grow (Rem. 2.10 as corroboration; revised after the PR #6 review). The proof gives nothing at N = 1, which matches the N = 1 failure. Follow-up: drop the "if eq. (5) holds" condition on the page (#32, needs `/review`). | notes, Literature item 4a |
| G8 (#18) | **Other conditions:** Robin conditions u′(0) = σu(0), or star graphs with even N or N₀ > 1. Do Theorem 1 and Theorem 3 transfer? | idea | none |

## Problems in progress

### weakly-consecutive: open (P1, #21)

- Notes: [notes/weakly-consecutive.md](notes/weakly-consecutive.md)
- Target: Conjecture 5.2 of Garrison–Seiler–Knowles, arXiv:2401.09497: every weakly consecutive
  permutation σ of [k] has σ(1) = 1 or σ(k) = 1. [conjecture]
- Literature stage done 2026-11-25: no proof or counterexample found, and no citing work other than
  OEIS A395372, which lists counts only (scope in the notes). Exact enumeration finds no counterexample for k ≤ 23 (Python, not yet Lean); the
  authors report checking their stronger Conjecture 5.1 up to k = 500.
- Attack stage 2026-11-25 (#48): an argument for k a prime power (own argument, unreviewed; /review found no
  mathematical error; notes A6.3),
  via σ(1), σ(k) being coprime divisors of k. Gap: k with two or more distinct prime factors; class-size
  counting alone (A3's plan) cannot work: the size-only relaxation admits an interior 1 (Python search, notes A6.5).
- Lean 2026-11-25 (#47): Conjecture 5.2 for k ≤ 16 by `decide +kernel` (`conjecture_5_2_le_16`).
- Attack stage 2026-11-26 (#68): a slice lemma (the slice through position 1 starts with 1, so
  its last value divides its length) gives Conjecture 5.2 for k = r·s^b with r, s distinct
  primes and s ∤ r − 1, including every squarefree k = pq and every 2·s^b (own argument,
  unreviewed; `/review` found no mathematical error; notes A7). Gap: p^a q^b with a, b ≥ 2, or r·s^b with b ≥ 2
  and s ∣ r − 1 (e.g. 12, 20, 36, 63; notes A7.3).
- Attack stage 2026-11-27 (#68): Conjecture 5.2 for k = 4r, r ≥ 5 prime (own argument, unreviewed;
  notes A7.4: A7.1 forces σ(1) = 2, σ(k − 1) = 4 up to reversal, the slice of T_4 forces
  σ(3) = 4r, contradicting T_r = multiples of r); with k = 12 from Lean, every k = 4r is done.
  Failed: extending the chain to 2^b·r, b ≥ 3 (the second slice need not end in a multiple of r).
  Remaining gap: A7.3 (a) and (b) with k ≠ 4r (e.g. (a) 36, 72, 100; (b) 24, 40, 63).

| Id | Item | Status | Where |
|---|---|---|---|
| WC1 (#21) | **Conjecture 5.2** for all k | open | notes, Statement |
| WC1a (#68) | **Conjecture 5.2 for k with 2 distinct prime factors** (k = r·s^b with s ∤ r − 1, incl. all pq: A7.2; k = 4r: A7.4 + Lean k = 12; own argument, unreviewed; GSK24 citations re-proved, #80) | partial; open for a, b ≥ 2 or r·s^b with b ≥ 2, s ∣ r − 1, k ≠ 4r | notes, A7.3 |
| WC1c | Conjecture 5.2 for prime-power k | own argument, unreviewed (GSK24 citations re-proved, #80) | notes, A6.3 |
| WC1b | Conjecture 5.2 for k with ≥ 3 distinct prime factors | open | notes, A6.5 |
| WC2 | Lean check of 5.2 for small k by `decide`, plus Lemmas 2.2–2.4 of the paper | small-k part done (k ≤ 16, [Lean], `halfline_lt/Proofs/WeaklyConsecutive.lean`); Lemmas 2.2–2.4 not formalized | notes, A5, Log 2026-11-25 (Lean) |

### central-2adic: proved in Lean (P2, #22)

- Notes: [notes/central-2adic.md](notes/central-2adic.md)
- Target: OEIS A402341 conjecture: for even n, v₂(a(n)) = s₂(15n/2), where a(n) is the central
  coefficient of (1 + x + … + x¹⁵)ⁿ. [conjecture]
- Literature stage done 2026-11-26: no proof, disproof or discussion found; the entry is unchanged
  since 2026-11-17 (scope in the notes). Closest known results are for the infinite product
  ∏(1 − x^{2^j}) (Gawron–Miska–Ulas arXiv:1703.01955, Shen arXiv:2609.16966).
- Attack stage 2026-11-27 (#65): proof by termwise 2-adic dominance in the entry's u-formula
  (notes, Attack S0–S5), for every q = 2^r and every even n. [own argument, unreviewed; steps
  checked numerically; Lean check done (#66, see below); /review 2026-11-27 (two fresh reviewers): no
  mathematical error found, 12 wording findings, all fixed (notes, Review)]
- Citation stage 2026-11-27 (#77): both `[standard]` inputs checked against source text. Coefficient
  formula for 2T_{2^j}(u/2) in S1: [standard: DLMF 18.5.11_1, text checked 2026-11-27] (notes L7,
  with the specialisation to γ_{j,k}). Kummer v₂(C(2m, m)) = s₂(m) in S5: [standard: Mathlib
  `sub_one_mul_multiplicity_choose_eq_sub_sum_digits`, statement checked 2026-11-27] (notes L3).
  Before this the coefficient formula was labelled "no reference text checked". /review 2026-11-27
  (two fresh reviewers): no error, 4 wording findings, all fixed (notes, Review).
- Numerics (Python, not Lean): holds for even n ≤ 4000; the analogue for q = 2^r (q = 4, 8, 32,
  64) holds for even n ≤ 2000 and fails for q = 3, 6, 12. In the entry's u-formula the top term
  C(15n, 15n/2) strictly dominates every other term 2-adically for even n ≤ 120 (notes A1); termwise dominance
  for all even n is now part of the Attack proof (S4–S5).
- Lean stage 2026-11-27 (#66): the full Theorem (every q = 2^r, every even n) is proved in Lean,
  `Central2adic.central_2adic` and `Central2adic.a402341_conjecture`, standard axioms only.

| Id | Item | Status | Where |
|---|---|---|---|
| CA1 (#22) | **A402341 conjecture** for all even n | [Lean] `Central2adic.a402341_conjecture` (#66) | notes, Attack; `halfline_lt/Proofs/Central2adic.lean` |
| CA2 | q = 4 case (A005190): termwise carry inequality t + v₂(C(n,t)) + s₂(3n/2 − t) > s₂(3n/2) | proved (special case of CA3, derived in the Attack Audit) [own argument, unreviewed] | notes, Attack |
| CA3 | General q = 2^r analogue, even n | [Lean] `Central2adic.central_2adic` (#66) | notes, Attack; `halfline_lt/Proofs/Central2adic.lean` |
| CA4 | Odd n: any closed form for v₂(a(n)) (N3 shows v₂ − s₂(⌊15n/2⌋) ranges −11..10) | open, no conjecture | notes, N3 |

### min-modulus: open (P3, #23)

- Notes: [notes/min-modulus.md](notes/min-modulus.md)
- Target: Fonollosa's Conjecture 1 (arXiv:2607.08366 v2): for n ≥ 2 and N < 2^n − 2^⌊log₂ n⌋, no
  set of n residues mod N is valid. [conjecture] Statement in Lean:
  formal-conjectures `Arxiv/2607.08366/MinModulus.lean`, `min_modulus` (tagged open).
- Literature + setup 2026-11-27 (#86): not found resolved for n ≥ 8 in the works searched (notes, Search scope); the paper's
  CP-SAT certifies n ≤ 7.
  Known: the bound is attained by {2^k − 1} [preprint: Fon26, Thms A, B]; N ≥ 2^{n−1} (Inal, OSF
  preprint, not accessed; several Lean proofs); third-party Lean claims of n ≤ 6 and
  N ≥ 2^{n−1}(1 + 1/(72(n−1)√((n−1) ln n))) (Sun16z/min-modulus-gap, 2026-11-27). None re-checked here.
- Numerics (Python, not Lean): least valid modulus is 2, 6, 12, 28 for n = 2..5 (exhaustive).

| Id | Item | Status | Where |
|---|---|---|---|
| MM1 (#23) | **Conjecture 1** for all n | open | notes, Statement |
| MM2 (#87) | n = 8: no valid set for N < 248 (the scout wrote 252; the threshold is 248). Unconditional target 8 ≤ N < 248; N < 129 follows from Inal's/L3's claimed bound and equality case (not re-checked), leaving 129 ≤ N < 248 | open | notes, Attack ideas |
| MM3 (#88) | A general lower bound beating 2^{n−1}(1 + 1/(72(n−1)√((n−1) ln n))) | open, crowded | notes, L3–L4 |

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
- **WCS: slice lemma alone for k = p^a q^b (#68).** Its divisibility constraints are satisfiable
  in at least one uncovered case (k = 12, (σ(1), σ(12)) = (4, 3)). For k = 12, (2, 3) the hand
  check closes it using the singleton class of 7 ∈ (k/2, k]. (notes, A7.3)
- **Brute-force numerics.** No counterexample for γ ≤ 5/2 in four families. Use numerics to test
  claims, not as a proof strategy.
