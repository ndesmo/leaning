# Results: the sharp Lieb–Thirring constant on the Neumann half-line

Status as of 2026-11-25. Each claim carries the labels of `prompt.txt`. Lean names refer to
`halfline_lt/HalflineLt/Spec.lean`; "standard" means a classical result cited, not re-proved.

## Setting

- Operator: H_V = −d²/dx² − V on L²(0, ∞), Neumann condition u'(0) = 0, defined by its quadratic
  form on H¹(0, ∞).
- Potentials: 0 ≤ V ∈ L^{γ+1/2}(0, ∞), γ ≥ 1/2.
- Spectrum: the negative spectrum of H_V consists of eigenvalues E₁ < E₂ < … < 0. Each is simple,
  and they can accumulate only at 0.
- Notation: S_γ(V) = Σ_j |E_j|^γ, M_γ(V) = ∫₀^∞ V^{γ+1/2}, and L^N_γ = sup_V S_γ(V)/M_γ(V).
- Constants:
  - L1(γ) = Γ(γ+1) / (√π Γ(γ+1/2)(γ+1/2)) · ((γ−1/2)/(γ+1/2))^{γ−1/2} (one bound state);
  - Lcl(γ) = Γ(γ+1) / (2√π Γ(γ+3/2)) (semiclassical);
  - r(γ) = L1(γ)/Lcl(γ). By [Lean] `r_strictAntiOn`, `r_lt_one`, `two_exp_neg_one_lt_r`:
    r decreases strictly on (1/2, ∞), r(3/2) = 1, and 2/e < r.

**Conjecture.** L^N_γ = 2·L1(γ) for 3/2 ≤ γ ≤ 5/2. [conjecture]

Known before this work, or elementary:
- (a) L^N_γ ≤ 2L_γ for γ ≥ 1/2, by even reflection [paper: Demirel-Frank, Lemma 3]. Since
  L_γ = Lcl(γ) for γ ≥ 3/2 (Lieb–Thirring, Aizenman–Lieb), L^N_γ ≤ 2Lcl(γ) there. ELU's own
  Thm 1.6 gives the same bound.
- (b) L^N_γ ≥ 2L1(γ) for γ > 1/2: the half-soliton (γ² − 1/4) sech² on (0, ∞) attains 2L1(γ)
  for γ ≤ 5/2. [Lean: `fact_b`; Pöschl–Teller inputs in `Spec.lean` §5]
- L^N_{1/2} = 1 [paper: Hundertmark–Lieb–Thomas 1998, introduction]; L^N_{3/2} = 3/8, from
  (a) and (b); L^N_1 = 2L1(1), from (a), (b) and L_1 = L1(1) [preprint: Read–Schulz].
- (d) L^N_γ > 2L1(γ) for γ > 5/2: the half-soliton then has a second Neumann state, from the
  even k = 2 Pöschl–Teller state. [Lean: `fact_d`, `pt_second_even_state`,
  `pt_second_even_state_sq_integrable`]

---

## Theorem 1 (improved upper bound)

For every γ ≥ 3/2,

  L^N_γ ≤ Lcl(γ) + L1(γ).

For γ > 3/2 this is strictly smaller than the previous bound 2·Lcl(γ). Relative to the conjectured
value it is (1 + 1/r(γ))/2: 1.0379 at γ = 2 and 1.0625 at γ = 5/2.

*Proof.* [paper: ELU Cor. 1.3 + Lieb–Thirring 1976], [Lean: `neumann_upper_ELU`, `r_lt_one`]
- Exner–Laptev–Usman (CMP 326 (2014), Cor. 1.3, eq. (1.6)), scalar Neumann case, γ ≥ 3/2:
  ½|E₁|^γ + Σ_{j≥2} |E_j|^γ ≤ Lcl(γ) M_γ(V).
- The even extension Ṽ(x) = V(|x|) has an even ground state, so the Neumann ground state is the
  ground state of −d² − Ṽ on ℝ.
- By the sharp one-bound-state bound in one dimension (Lieb–Thirring 1976), together with
  ∫_ℝ Ṽ^{γ+1/2} = 2M_γ(V) ([Lean] `even_extension_mass`):
  |E₁|^γ ≤ L1(γ) ∫_ℝ Ṽ^{γ+1/2} = 2 L1(γ) M_γ(V).
- Therefore S_γ(V) = (½|E₁|^γ + Σ_{j≥2} |E_j|^γ) + ½|E₁|^γ ≤ (Lcl(γ) + L1(γ)) M_γ(V). ∎

## Corollary 2 (star graphs)

Let Γ_N be the star graph with N half-line edges and Kirchhoff conditions at the vertex, and
L_{γ,N} its sharp Lieb–Thirring constant. For γ ≥ 3/2 and every odd N,

  L_{γ,N} ≤ Lcl(γ) + L1(γ)/N.

This improves Demirel-Frank's bound L_{γ,N} ≤ ((N+1)/N) L_γ for odd N (arXiv:1503.06915,
Thm 1) for every γ > 3/2. Her eq. (5) quotes L_{γ,N} = L_γ for γ ≥ 2 "and all N" from
Demirel–Harrell (Rev. Math. Phys. 2010). That cannot include N = 1, since L_{γ,1} ≥ 2L1(γ) > Lcl(γ)
(`two_exp_neg_one_lt_r`). So the new range is odd N ≥ 3 with 3/2 < γ < 2, plus N = 1 (which is
Theorem 1) for all γ > 3/2. Her Remark (4) says the odd-N bounds "improve automatically" if
L_{γ,1} ≤ 2L_γ can be improved; Theorem 1 is such an improvement.

*Proof.* [paper: Demirel-Frank, Prop. 4], [Lean: `star_graph_bound`, `star_graph_bound_strict`]
- Demirel-Frank, Prop. 4 ("Let γ ≥ 1/2. If N₀ < N are both odd, then …") with N₀ = 1:
  L_{γ,N} ≤ ((N−1)/N) L_γ + (1/N) L_{γ,1} for odd N ≥ 3.
- Γ₁ is the half-line with the Neumann condition, so L_{γ,1} = L^N_γ.
- L_γ = Lcl(γ) for γ ≥ 3/2.
- Insert Theorem 1. Strictness: L1 < Lcl for γ > 3/2. ∎

## Theorem 3 (the conjecture holds below the critical envelope)

Let γ ≥ 1/2. Suppose V ≥ 0 on (0, ∞) and, for some a > 0,

  V(x) ≤ 6 a⁻² sech²(x/a)  for all x > 0.

Then S_γ(V) ≤ 2 L1(γ) M_γ(V). If V ≢ 0, equality holds iff 1/2 < γ ≤ 5/2 and
V(x) = (γ² − 1/4) b⁻² sech²(x/b) for some b > 0.

*Proof.*
1. **U = 6 sech² has exactly one negative Neumann eigenvalue, −4.**
   - The solution of −u'' − U u = 0 with u(0) = 1, u'(0) = 0 is u = 1 − 3 tanh²x.
     [Lean: `resonance_at_five_halves`, `psi2_two_at_zero`, `psi2_two_formula`]
   - It has exactly one zero in (0, ∞), at x = arsinh √(1/2). [Lean: `psi2_two_unique_zero`]
   - For potentials with ∫₀^∞ (1 + x)|U| < ∞, the number of negative eigenvalues of the half-line
     operator with a given boundary condition equals the number of zeros in (0, ∞) of the
     zero-energy solution satisfying that condition. [standard: Sturm oscillation, e.g. B. Simon,
     "Sturm oscillation and comparison theorems" (2005)]
   - The eigenvalue is −4, with eigenfunction sech²x. [Lean: `pt_ground_state` at ν = 2]
   - Cross-check: the whole-line operator −d² − 6 sech² has exactly the eigenvalues −4 (even,
     sech²) and −1 (odd, sech·tanh), and the Neumann eigenvalues are the even ones.
     [standard: Pöschl–Teller]
2. **Scaling.** The dilation (D_a f)(x) = a^{−1/2} f(x/a) is unitary on L²(0, ∞) and preserves the
   Neumann condition. It conjugates H_U to a²·H_{U_a}, where U_a(x) = a⁻² U(x/a). So H_{U_a} also
   has exactly one negative eigenvalue.
3. **Monotonicity.** 0 ≤ V ≤ U_a implies H_V ≥ H_{U_a} as quadratic forms on H¹(0, ∞). By min–max,
   H_V has at most one negative eigenvalue.
4. **One state suffices.** With at most one Neumann eigenvalue, S_γ(V) ≤ |E₁|^γ ≤ 2L1(γ) M_γ(V) by
   the one-bound-state bound (as in Theorem 1). [Lean: `at_most_one_state_ok`]
5. **Equality case.** Let V ≢ 0.
   - Equality forces S_γ(V) = |E₁|^γ, i.e. exactly one eigenvalue.
   - It also forces equality in the one-bound-state bound for Ṽ.
   - For γ = 1/2 that bound, |E₁|^{1/2} ≤ ½∫Ṽ, is strict for every potential, because its
     extremal is a δ.
   - For γ > 1/2 its optimizers are exactly c² (γ² − 1/4) sech²(c(x − x₀)), c > 0 [standard:
     Lieb–Thirring 1976, by uniqueness of the Gagliardo–Nirenberg optimizer in one dimension].
     Evenness forces x₀ = 0.
   - Envelope test, writing b = 1/c: V = (γ² − 1/4) b⁻² sech²(x/b) lies under some envelope iff
     γ ≤ 5/2. [Lean: `half_soliton_fits_iff_gamma`, via `half_soliton_fits_iff` and
     `envelope_excludes_large`]
     - If γ² − 1/4 ≤ 6, take a = b.
     - If γ² − 1/4 > 6 and b ≤ a, the bound fails near x = 0.
     - If γ² − 1/4 > 6 and a < b, the envelope decays faster than V, so the bound fails for
       large x.
   - Conversely, for 1/2 < γ ≤ 5/2 this V has the single Neumann eigenvalue −(γ − 1/2)² b⁻². It
     attains the one-bound-state bound, so equality holds. ∎

*Remarks.*
- The class is invariant under V ↦ λ²V(λ·), as is S_γ/M_γ. It contains every half-soliton
  ν(ν+1) sech² with ν ≤ 2, i.e. the conjectured optimizer for every γ ≤ 5/2.
- The envelope is critical. At 6 sech² the even sector has a zero-energy resonance: u = 1 − 3 tanh²
  is bounded and tends to −2. Every larger envelope μ(μ+1) sech² with μ > 2 has a second Neumann
  state, and for γ > 5/2 the half-soliton with ν = γ − 1/2 > 2 beats 2L1(γ) (fact (d)).
- For 1/2 ≤ γ < 3/2, L^N_γ = 2L1(γ) would follow from the whole-line Lieb–Thirring conjecture
  L_γ = L1(γ), by (a) and (b). Theorem 3 proves it unconditionally on the envelope class.
- Only "at most one Neumann state" is used. So the same bound holds whenever the Dirichlet
  operator on (0, ∞) has no negative eigenvalue, because the Dirichlet and Neumann counts
  satisfy N_D ≥ N_N − 1 (the Dirichlet form domain has codimension 1). Two standard
  sufficient conditions:
  - Bargmann: ∫₀^∞ x V(x) dx < 1.
  - Hardy: V(x) ≤ 1/(4x²).
  Both classes are scale-invariant, and both contain potentials under no sech² envelope.

## Corollary 4 (what a counterexample must look like)

Let γ ≥ 3/2 and suppose S_γ(V) > 2L1(γ) M_γ(V). Then:
1. H_V has at least two Neumann bound states, and its Dirichlet counterpart has at least one.
   [Theorem 3, step 4; `at_most_one_state_ok`]
2. For every a > 0 there is an x > 0 with V(x) > 6a⁻² sech²(x/a). [Theorem 3]
3. |E₁|^γ > (2 − 1/r(γ)) · 2L1(γ) M_γ(V). The factor 2 − 1/r(γ) equals 7/8 at γ = 5/2, is ≈ 0.924
   at γ = 2, and tends to 1 as γ ↓ 3/2. [Lean: `beating_needs_big_ground_state`,
   `threshold_tendsto_one`, `threshold_five_halves`]

Items 1 and 2 hold for every γ ≥ 1/2. Item 3 uses ELU (1.6), so it needs γ ≥ 3/2.

---

## What remains open

The conjecture itself.
- Corollary 4(3) forces the ground-state efficiency of a counterexample towards 1 as γ ↓ 3/2.
- By Carlen–Frank–Lieb stability (GAFA 2014, Thm 2.2), such a counterexample is then L^p-close to a
  half-soliton after rescaling. This step needs the stability constant to be uniform in γ, which
  I have not checked.
- By Corollary 4(2), it must still escape every envelope of Theorem 3, for instance through a
  spike or a slowly decaying tail.
- Excluding this (Task 5, Step 5 in `NOTES.md`) would prove the conjecture on [3/2, 3/2 + ε).

## Lean

Checked 2026-11-25:
- `lake build` succeeds.
- All 64 theorems in `Spec.lean` are proved with no `sorry`.
- `#print axioms` on each shows only `propext`, `Classical.choice`, `Quot.sound`.

The results above use these Lean statements:

| Result | Lean |
|---|---|
| Theorem 1 | `neumann_upper_ELU`, `even_extension_mass`, `r_lt_one` |
| Corollary 2 | `star_graph_bound`, `star_graph_bound_strict` |
| Theorem 3, steps 1 and 4 | `psi2_two_formula`, `psi2_two_at_zero`, `psi2_two_unique_zero`, `resonance_at_five_halves`, `pt_ground_state`, `at_most_one_state_ok` |
| Theorem 3, equality case | `half_soliton_fits_iff_gamma`, `half_soliton_fits_iff`, `envelope_excludes_large` |
| Corollary 4 | `beating_needs_big_ground_state`, `threshold_tendsto_one`, `threshold_five_halves` |

Not formalized: the cited spectral theorems. These are ELU (1.6), the one-bound-state bound and
its optimizers, Sturm oscillation, min–max, Demirel-Frank Prop. 4 and the Pöschl–Teller spectrum.
They enter the Lean statements as hypotheses. Mathlib has no theory of Schrödinger operators.
