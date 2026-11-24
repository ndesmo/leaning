# NOTES: sharp Lieb–Thirring constant, Neumann half-line

Labels: [Lean], [Lean | hyp: …], [paper: ref, Thm], [preprint: ref, Thm],
[numerical ± err], [conjecture]. See `prompt.txt` for definitions.

## Task 0: setup (2026-11-24)

- Lean 4.37.0-rc1 (commit 0b77e129), Mathlib tag v4.37.0-rc1
  (commit 31ce06eaadf4a200c0e1407c5f10953cf606b8f8).
- Project `halfline_lt/`: library `HalflineLt` (`Basic`, `Spec`), executable `search`
  (core Lean only; placeholder `Search.lean`).
- `lake build` succeeds. The only warnings are 8 `sorry`s in `HalflineLt/Spec.lean` and one
  "consider adding `module`" hint per file importing Mathlib. Mathlib's style linters are off.
- `#print axioms` on the proved theorems of the spec shows only `propext`,
  `Classical.choice`, `Quot.sound`.
- Machine note: long paths are disabled. A project under a ~120-character path failed to
  unpack 25 Mathlib cache files; `subst` drives don't help because Lake resolves them.

## Claims ledger

| Claim | Label | Where |
|---|---|---|
| Completed square (Read–Schulz identity) and its real-exponent version | [Lean] | `Spec.lean` §1 |
| Riccati form only at m = 3; m(1) = 3; m ∈ [3/2, 2) on (3/2, 5/2] | [Lean] | `Spec.lean` §1 |
| L1 = r·Lcl; r(3/2) = 1; r(5/2) = 8/9 | [Lean] | `Spec.lean` §2 |
| r strictly decreasing on (1/2, ∞); r < 1 for γ > 3/2; r > 2/e > 1/2 | [Lean] | `Spec.lean` §2 |
| L^N_γ ≤ Lcl + L1 for γ ≥ 3/2 | [Lean \| hyp: ELU (1.6), one-bound-state bound] | `Spec.lean` §3 |
| A potential beating 2·L1 has e > 2 − 1/r(γ) (7/8 at γ = 5/2) | [Lean \| hyp: ELU (1.6)] | `Spec.lean` §3 |
| (a)–(d) in abstract form | [Lean \| hyp: spectral facts] | `Spec.lean` §4 |
| ∫_ℝ V(\|x\|)^p = 2 ∫_0^∞ V^p | [Lean] | `Spec.lean` §4 |
| Soliton bonus factors at γ = 3, 5 | [Lean] | `Spec.lean` §6 |
| L^N_{1/2} = 1 (sharp) | [paper: HLT 1998, intro] | Task 1 §1 |
| ½λ₁^γ + Σ_{n≥2} λ_n^γ ≤ Lcl ∫₀^∞ V^{γ+1/2}, scalar Neumann, γ ≥ 3/2 | [paper: ELU 2014, Cor. 1.3, (1.6)] | Task 1 §2 |
| L^N_γ ≤ 2L_γ, γ ≥ 1/2 | [paper: Demirel-Frank, Lemma 3] | Task 1 §4 |
| Schimmer Thm 1.1 at σ₀ = 0 (γ = 3/2), equality at the half-soliton | [paper: Schimmer, Thm 1.1] + hand check | Task 1 §3 |
| L_{1,1} = 4/(3√3π) | [preprint: Read–Schulz, Thm 1] | Task 1 §5 |
| Conjecture: L^N_γ = 2·L1(γ) on [3/2, 5/2] | [conjecture] | — |

## Open `sorry`s (8, all Task 3)

`L1_one`, `L1_two`, `two_L1_one_bounds`, `two_L1_two_bounds`, `pt_ground_state`,
`pt_second_even_state`, `pt_second_even_state_sq_integrable`, `sech2_family_opt`.

## Task 1: literature (2026-11-24)

**Question.** Is L^N_γ known for any γ ∈ (3/2, 5/2], or is any upper bound better than
Lcl + L1 known?

**Answer.** Not in anything I could find. The sharp Neumann constant is known only at
γ = 1/2 (stated explicitly), at γ = 3/2 (immediate from (a) and (b)), and at γ = 1 (via (a),
(b) and the Read–Schulz preprint; not stated anywhere). Published upper bounds for γ > 3/2
are 2L_γ = 2Lcl. Lcl + L1 is our combination of ELU (1.6) with the one-bound-state bound; no
paper I read states it.

### Results, with exact statements

1. **Hundertmark–Lieb–Thomas**, Adv. Theor. Math. Phys. 2 (1998), arXiv:math-ph/9806012,
   introduction: "A corollary of our result is that for the half-line problem with Neumann
   boundary conditions considered by Weidl, the sharp constant is 1." So L^N_{1/2} = 1.
   [paper: HLT 1998, intro]
2. **Exner–Laptev–Usman**, Comm. Math. Phys. 326 (2014) 531–541, arXiv:1301.4986. Read in
   full. [paper: ELU]
   - Thm 1.1 (γ = 3/2, Hermitian N×N matrix V ≥ 0 with Tr V² ∈ L¹(ℝ₊), condition
     φ'(0) − 𝔖φ(0) = 0): (3/4)λ₁ Tr 𝔖 + ½(2ϰ₁ − N)λ₁^{3/2} + Σ_{n≥2} ϰ_n λ_n^{3/2}
     ≤ (3/16)∫₀^∞ Tr V² + ¼ Tr 𝔖³. The proof removes λ₁ by single commutation (§3), leaving a
     Dirichlet problem with potential V + 2F₁', then applies Laptev–Weidl on ℝ.
   - Cor. 1.2/1.3: for Tr 𝔖³ ≤ 0 and Tr V^{γ+1/2} ∈ L¹, γ ≥ 3/2, by Aizenman–Lieb (p. 10). I
     checked that the lifting is valid: the left side is monotone in each λ_n, and the weights
     are ≥ 0.
   - Scalar Neumann case, eq. (1.6): ½λ₁^γ + Σ_{n≥2} λ_n^γ ≤ Lcl(γ) ∫₀^∞ V^{γ+1/2}, γ ≥ 3/2.
   - Their own conclusion, Thm 1.6 / eq. (1.9) with d = 1, bounds ½λ₁^γ by (1.6) again and gets
     only Σλ_n^γ ≤ 2Lcl ∫ V^{γ+1/2}.
3. **Schimmer**, arXiv:1912.13264 (J. Spectral Theory). Read in full. [paper: Schimmer]
   - Thm 1.1 (γ = 3/2, V ∈ L¹∩L²(ℝ₊), Robin φ'(0) − σ₀φ(0) = 0, sign convention −d² + V):
     Σ|λ_j|^{3/2} + ¼Σ(σ_j³ − σ_{j−1}³) ≤ (3/16)∫₀^∞ V² + ¾Σ|λ_j|(σ_j − σ_{j−1}), where
     σ_j = σ_{j−1} + |φ_j(0)|²/‖φ_j‖². It comes from an exact identity (double commutation;
     §3.1) after dropping ∫V_N² ≥ 0.
   - At σ₀ = 0: Σ|λ_j|^{3/2} + ¼σ_N³ ≤ (3/16)∫V² + ¾Σ|λ_j|(σ_j − σ_{j−1}). Consistency check
     (by hand): the half-soliton at γ = 3/2 (λ₁ = −1, φ₁ = sech, σ₁ = 1, ∫₀^∞ 4 sech⁴ = 8/3)
     gives equality, 5/4 = 1/2 + 3/4.
   - §4.2: for σ₀ ≥ 0, the eigenfunction-free consequence is ½|λ₁|^{3/2} + Σ_{j≥2}|λ_j|^{3/2}
     ≤ (3/16)∫V², which is ELU (1.6) at γ = 3/2. Nothing better without eigenfunction data.
   - Nothing for γ > 3/2. The σ_j depend on eigenfunctions, so Aizenman–Lieb does not lift
     Thm 1.1; lifting the §4.2 form just reproduces ELU Cor. 1.3.
   - After his Thm 1.3: the single-commutation route cannot be sharp when V has more than
     one eigenvalue.
4. **Demirel-Frank**, "Sharp eigenvalue bounds on quantum star graphs", arXiv:1503.06915.
   Read pp. 1–4 and 8–10. [paper: Demirel-Frank]
   - Lemma 3: Neumann half-line, Tr(H^Neu)_−^γ ≤ 2L_γ ∫_{ℝ₊} V_−^{γ+1/2}, γ ≥ 1/2. This is (a).
   - Remark (3): optimal as long as the optimal potential for L_γ has a single bound state.
   - Remark (4): asks whether L_{γ,1} ≤ 2L_γ can be improved for large γ (which would improve
     her odd-N star-graph bounds). For γ > 3/2, Lcl + L1 < 2Lcl gives such an improvement.
   - Her eq. (5), "L_{γ,N} = L_γ for all γ ≥ 2 and all N", cites Demirel–Harrell (Rev. Math.
     Phys. 22 (2010), arXiv:0911.1896). It cannot include N = 1: there, L_{γ,1} = L^N_γ ≥ 2L1
     > Lcl = L_γ ([Lean] `two_exp_neg_one_lt_r` + (b)). Demirel–Harrell put Dirichlet
     conditions at free ends and never treat a Neumann degree-one vertex, so there is no real
     conflict, only a loose "all N".
5. **Read–Schulz**, arXiv:2609.10478 v2 (14 Sep 2026). Read in full. [preprint]
   - Whole line, γ = 1 only. Nothing on the half-line or other γ.
   - The method: Benguria–Loss cumulative mass, q = −α tan(α(s − 1/2)), the condition
     q(s)q(t) + (q(s) − q(t))/(s − t) ≤ −κ (Lemma 3), and a matrix cumulative mass for
     orthonormal families.
   - p. 16, "Use of AI": the authors say a first version of the main argument was developed
     with AI models, then restructured and verified by them. The paper is unrefereed.
6. **Schimmer**, "The state of the Lieb–Thirring conjecture", arXiv:2203.06051. Checked via
   the ar5iv HTML. It mentions ELU only in passing (§4.4, Robin half-axis via commutation)
   and has no half-line constants. [paper]
7. **Frank–Laptev–Weidl**, CUP 2022/23. Table of contents only; full text not accessed. No
   section title on the half-line, Neumann-Schrödinger or Robin LT inequalities. The
   "Comments" sections (5.6, 7.5, 8.5) were not checked.

### Search scope

- Works citing ELU (Semantic Scholar, 13 entries) and Schimmer (3 entries).
- Web searches for half-line / Neumann / Robin sharp LT constants (2014–2026).
- Not relevant on inspection: Read 2022 (arXiv:2205.06582, single-well comparison bounds),
  Laptev 2020 (Dirichlet + Hardy term, γ = 3/2), Ekholm–Frank (math/0611247, Dirichlet,
  critical exponent), Weder 2024 (arXiv:2405.00799, reverse LT for matrix operators),
  Zia–Usman 2019 (fourth order), Mickelin 2016 (magnetic), Granovskyi–Malamud 2019.
- Not accessed: Aljahili–Laptev, J. Math. Sci. (2023), DOI 10.1007/s10958-023-06386-1
  (paywalled, no abstract available).

### Implications for later tasks

- Bounds to use in Task 2's checks: 2L1 ≤ L^N ≤ Lcl + L1 on (3/2, 5/2].
- Schimmer's exact identity (before dropping ∫V_N²) is tight at the half-soliton at γ = 3/2.
  This suggests a perturbative route for Task 5 just above 3/2.
