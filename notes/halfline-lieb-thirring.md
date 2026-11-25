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
| L^N_γ ≤ Lcl + L1 for γ ≥ 3/2 | [Lean \| hyp: ELU (1.6), one-bound-state bound] | `Spec.lean` §3; `RESULTS.md` Thm 1 |
| A potential beating 2·L1 has e > 2 − 1/r(γ) (7/8 at γ = 5/2) | [Lean \| hyp: ELU (1.6)] | `Spec.lean` §3 |
| (a)–(d) in abstract form | [Lean \| hyp: spectral facts] | `Spec.lean` §4 |
| ∫_ℝ V(\|x\|)^p = 2 ∫_0^∞ V^p | [Lean] | `Spec.lean` §4 |
| Soliton bonus factors at γ = 3, 5 | [Lean] | `Spec.lean` §6 |
| L^N_{1/2} = 1 (sharp) | [paper: HLT 1998, intro] | Task 1 §1 |
| ½λ₁^γ + Σ_{n≥2} λ_n^γ ≤ Lcl ∫₀^∞ V^{γ+1/2}, scalar Neumann, γ ≥ 3/2 | [paper: ELU 2014, Cor. 1.3, (1.6)] | Task 1 §2 |
| L^N_γ ≤ 2L_γ, γ ≥ 1/2 | [paper: Demirel-Frank, Lemma 3] | Task 1 §4 |
| Schimmer Thm 1.1 at σ₀ = 0 (γ = 3/2), equality at the half-soliton | [paper: Schimmer, Thm 1.1] + hand check | Task 1 §3 |
| L_{1,1} = 4/(3√3π) | [preprint: Read–Schulz, Thm 1] | Task 1 §5 |
| L1(1) = 4/(3√3π), L1(2) = (16/(15π))(3/5)^{3/2} | [Lean] | `Spec.lean` §2 |
| 2·L1(1) ∈ (0.49006, 0.49008), 2·L1(2) ∈ (0.31559, 0.31561) | [Lean] | `Spec.lean` §2 |
| ψ₀ = sech^ν solves −ψ'' − ν(ν+1)sech²ψ = −ν²ψ | [Lean] | `Spec.lean` §5 |
| ψ₂ = sech^{ν−2}((2ν−1)tanh² − 1) solves it with −(ν−2)² | [Lean] | `Spec.lean` §5 |
| ψ₂ ∈ L²(0,∞) for ν > 2 | [Lean] | `Spec.lean` §5 |
| One-state sech² family is maximised at ν = γ − 1/2 | [Lean] | `Spec.lean` §5 |
| No tested potential beats 2·L1 for γ ∈ {1, 1.5, 1.75, 2, 2.25, 2.4, 2.5} (4 families + sech²) | [numerical ± 1e-10..3e-6] | Task 2, `results/` |
| γ = 3: R/(2L1) ≥ 1.000118753 for an explicit potential | [numerical ± 3.6e-8] | `results/checks.csv` |
| One Neumann bound state ⇒ R ≤ 2·L1; counterexamples need ≥ 2 states | [Lean \| hyp: one-bound-state bound] | `Spec.lean` §7 `single_state_ok` |
| At γ = 3/2, equality forces no odd states and no reflection | [Lean \| hyp: trace formula] | `Spec.lean` §7 `uniqueness_skeleton` |
| At γ = 3/2, equality holds only for the half-soliton 2κ² sech²(κx) | [paper: trace formula + reflectionless classification], sketch | Task 5 Step 1 |
| Counterexample threshold 2 − 1/r(γ) → 1 as γ ↓ 3/2 | [Lean] | `Spec.lean` §7 |
| Far mass is paid for at rate 2L1 − Lcl > 0 (bookkeeping) | [Lean] | `Spec.lean` §7 |
| Stability: e(V) near 1 forces V near a soliton (Task 5 Step 3) | [paper: Carlen–Frank–Lieb, GAFA 2014, Thm 2.2] (fixed γ; uniformity near 3/2 to check) | Task 5 round 2 |
| At ν = 2, ψ₂ = 3 tanh² − 1 is a bounded zero-energy solution (even resonance at γ = 5/2) | [Lean] | `Spec.lean` §7 `resonance_at_five_halves` |
| (a + b)^p ≥ a^p + p·a^{p−1}·b + b^p for p ≥ 2, a, b ≥ 0 | [Lean] | `Spec.lean` §7 `add_rpow_ge_tangent` |
| Star graphs: L_{γ,N} ≤ Lcl + L1/N for odd N, γ ≥ 3/2; strictly below Demirel-Frank's (1 + 1/N)Lcl for γ > 3/2 | [Lean \| hyp: Demirel-Frank Prop. 4 + Thm 1] | `Spec.lean` §8; `RESULTS.md` Cor. 2 |
| u = 1 − 3 tanh² (zero-energy Neumann solution for 6 sech²) has exactly one zero on (0, ∞), at arsinh √(1/2) | [Lean] | `Spec.lean` §8 `psi2_two_unique_zero` |
| V ≤ 6a⁻² sech²(x/a) ⇒ S_γ(V) ≤ 2L1(γ)M_γ(V) for all γ ≥ 1/2; for V ≢ 0, equality iff 1/2 < γ ≤ 5/2 and V = (γ² − 1/4)b⁻² sech²(x/b) for some b > 0 | Bound: [standard: PT33 (one state), Sim05 (Sturm cross-check), min–max] + [paper: DEL15 Lemma 1; Fra21 eq. (23) (one-bound-state bound)] + [Lean: §8 inputs]; "if": [standard: PT33 (single Neumann state)] + [paper: DEL15 Lemma 1 (attainment)] + [Lean: `half_soliton_fits_iff_gamma`]; "only if", γ > 1/2: [paper: CFL14 Thm 2.1 (uniqueness); DEL15 Lemma 1, Fra21 eq. (23) (sharp constant)] + [own argument, reviewed 2026-11-25: G9 steps 2–5] + [Lean: `half_soliton_fits_iff_gamma`]; γ = 1/2: [own argument, unreviewed: page Equality step]. The page still states the converse as conditional; page update pending | `RESULTS.md` Thm 3; G9 section |
| The half-soliton (γ² − 1/4) b⁻² sech²(x/b) fits under some 6a⁻² sech²(x/a) iff γ ≤ 5/2 | [Lean] | `Spec.lean` §8 `half_soliton_fits_iff_gamma` |
| A counterexample needs ≥ 2 Neumann states, must exceed every 6a⁻² sech²(x/a), and has e > 2 − 1/r(γ) | [Lean \| hyp: as above] | `RESULTS.md` Cor. 4 |
| L^N_γ = 2·L1(γ) on [3/2, 3/2 + ε) for some ε > 0 | [conjecture: conditional on Task 5 Step 5, plus γ-uniformity in Step 3] | Task 5 |
| Conjecture: L^N_γ = 2·L1(γ) on [3/2, 5/2] | [conjecture] | — |

## Open `sorry`s

None. Task 3 (2026-11-25) proved the 8 original targets.

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
   - **Verbatim quotations,** fetched 2026-11-25 from the ar5iv HTML of arXiv:1503.06915. The
     fetch tool gave displayed formulas in plain text, and they are transcribed that way here:
     - Prop. 4: "Let γ≥1/2. If N_0<N are both odd, then" L_{γ,N} ≤ ((N−N_0)/N)·L_γ +
       (N_0/N)·L_{γ,N_0}. "In particular, if L_{γ,N_0} = L_γ for some odd N_0∈ℕ, then
       L_{γ,N} = L_γ for all N ≥ N_0."
     - Thm 1: "Let γ≥1/2. If N is even, then L_{γ,N} = L_γ" "and, if N is odd, then"
       L_{γ,N} ≤ ((N+1)/N)·L_γ.
     - Remark (3): "For N=1, our bound states L_{γ,1}≤2L_γ." "The proof of Lemma 3 shows that this
       bound is optimal as long as the optimal potential for L_γ has a single bound state."
     - Remark (4): "For odd N≥3 our bound uses the bound L_{γ,1}≤2L_γ for N=1." "If the latter
       bound can be improved for some (large) γ, then also our bounds for arbitrary odd N≥3
       improve automatically."
     - Eq. (5): L_{γ,N} = L_γ for all γ≥2 and all N∈ℕ, introduced by "In [3] we have shown that"
       ([3] = Demirel–Harrell, Rev. Math. Phys. 2010).
     - L_{γ,N} is the sharp constant in Tr H_−^γ ≤ L_{γ,N} ∫_{Γ_N} V_−^{γ+1/2}, for the operator
       defined by its form on H¹(Γ_N), i.e. with Kirchhoff conditions at the vertex.
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

## Task 2: numerics in Lean (2026-11-24)

Everything in this section is [numerical]: `Float` computations, evidence and not proof.

**Code.**
- `halfline_lt/HalflineNum/` (core Lean only):
  - log-Gamma (Lanczos) and the constants L1, Lcl, r;
  - a SplitMix64 random generator;
  - the finite-difference solver: cell-centred grid, Neumann ghost point at 0, Dirichlet at
    L, negative eigenvalues by Sturm bisection;
  - Nelder–Mead.
- `halfline_lt/Search.lean`: subcommands `validate`, `sech2`, `run`, `check`, `bench`.
- Build with `lake build search`, run `halfline_lt\.lake\build\bin\search.exe <cmd>` from
  this folder; output goes to `results/`.
- Starts run in parallel via `Task.spawn` (22 cores).

**Validation** (`results/validation.csv`).
- Constants: correct to ≤ 2e-15.
- Pöschl–Teller Neumann levels for ν ∈ {0.75, 1.5, 2.5, 4.5}: within 6.6e-9 relative after
  Richardson (L = 40, h down to 0.0025). Observed order 2.000.
- Soliton ratios: within 7e-9, including the predicted 1.000064 at γ = 3.

**Centred sech² family** (closed form, FD cross-check to 9 digits; `results/sech2_family.csv`).

| γ | best ν | R/(2L1) |
|---|---|---|
| ≤ 5/2 | γ − 1/2 (one state) | exactly 1 |
| 2.6 | 2.100043 (two states) | 1.000000133 |
| 3 | 2.505617 | 1.000065723 |

**Searches.** Nelder–Mead from 64 (bump, two-well) or 48 (expansion, dressed) random starts
per γ, with recorded seeds. The best start for each γ is refined by Richardson on two boxes
(L = 30, 45). Files: `results/search_*.csv`, `results/verified_*.csv`. Families:
- bump: e^a sech²(x − c);
- two-well: a well at the wall plus a second well;
- expansion: (Σ of 8 Gaussians)²;
- dressed: the half-soliton times exp(Σ of 8 Gaussians), so c = 0 is the soliton.

Best refined R/(2L1):

| γ | bump | two-well | expansion | dressed |
|---|---|---|---|---|
| 1.00 | 0.999999829 | 0.999999930 | 0.999850271 | 0.999991866 |
| 1.50 | 0.999999478 | 0.999997503 | 0.999819323 | 0.999991889 |
| 1.75 | 0.999999193 | 0.999997760 | 0.999856196 | 0.999980446 |
| 2.00 | 0.999998907 | 0.999998078 | 0.999857632 | 0.999973037 |
| 2.25 | 0.999998582 | 0.999991375 | 0.999849328 | 0.999989688 |
| 2.40 | 0.999998329 | 0.999999006 | 0.999842234 | 0.999987456 |
| 2.50 | 0.999998195 | 0.999999141 | 0.999837618 | 0.999987448 |
| 2.60 | 0.999998107 | 0.999999264 | 0.999832810 | 0.999988580 |
| 3.00 | 1.000064153 | 1.000064561 | 0.999891764 | 1.000065155 |

- Error estimates (Richardson plus box) are 1e-10 to 3e-6, and the observed order is 2.00
  throughout.
- Every known-bound check passes: R ≤ (Lcl + L1)/(2L1) for γ ≥ 3/2, and R ≤ 1 at γ = 1.

**Result.**
- No potential in any family beats 2·L1 for γ ≤ 5/2. Each family's best is (a scaled copy of)
  the half-soliton or lies below it. [numerical]
- Above 5/2 better shapes exist. At γ = 3 the best found is 1.000118753 ± 3.6e-8 (expansion
  family, 3 bound states, `results/checks.csv`), against 1.000064 for the soliton.

**Lessons.**
1. *Grid exploitation.* With one coarse grid inside the optimiser, the best values reached
   1.0028 for γ ≤ 5/2, from narrow under-resolved potentials, and all refined to below 1. The
   fix: maximise a two-grid Richardson value minus a penalty on the grid difference. The γ = 3
   maxima of the biased runs were re-verified from their parameters (`results/checks.csv`).
2. *Speed.* Lean rebuilds a float literal via `Float.ofScientific` at every use (about 3 µs for
   `1e-300`), which made the first solver 350× slower. Hot code now uses the top-level
   constants in `HalflineNum.Basic`.
3. Searches cannot prove the conjecture. Their value is calibration and the absence of
   counterexamples in the families tried.

**Derived along the way (not searched).**
- A potential with a single Neumann bound state satisfies R ≤ 2·L1: its sum is |E₁|^γ, which
  the one-bound-state bound for the even extension controls. So a counterexample needs at least
  two Neumann bound states, and e > 2 − 1/r(γ) by ELU. [paper: one-bound-state bound
  (Lieb–Thirring 1976) + ELU (1.6); the algebra is in Lean]
- For γ < 5/2 the half-soliton should be a local maximiser: nearby potentials keep a single
  even bound state, since the even-sector threshold resonance occurs only at ν = 2.
  [conjecture: argument sketch]
- The supremum of R over potentials with at least two Neumann states is 1: take a soliton plus a
  small distant bump. So there is no uniform "two-state gap", and ELU-type bounds alone cannot
  reach γ = 2. For example, sech² with ν just above 2 at γ = 2 has two Neumann states and
  e ≈ 0.976, above ELU's threshold 0.924, though its true ratio is only ≈ 0.976.
  [hand computation]
- The γ = 5/2 KdV trace formula gives a lower bound on the eigenvalue sum: by my expansion of
  the dispersion relation, its scattering term has the opposite sign to the one at γ = 3/2. It
  is no direct route to the endpoint. [hand derivation, unverified]

**Suggested next step: Task 5, starting at γ = 3/2.**
1. Uniqueness at 3/2: equality in the trace formula forces a reflectionless even extension with
   no odd states, i.e. the centred soliton.
2. Compactness just above 3/2: near-optimisers have e → 1, and splitting is excluded because
   far pieces have ratio ≤ Lcl < 2L1 ([Lean] r > 2/e).
3. Near the soliton there is only one Neumann state.

Expected outcome: L^N_γ = 2L1(γ) on [3/2, 3/2 + ε), with ε not explicit.

## Task 3: Lean spec (2026-11-25)

All 8 targets are proved in `halfline_lt/HalflineLt/Spec.lean`. The file builds with no `sorry`,
and `#print axioms` on each target shows only `propext`, `Classical.choice`, `Quot.sound`.
[Lean] The top-level `HalflineSpec.lean` is synced with it.

- `L1_one`, `L1_two`: closed forms, using Γ(s+1) = sΓ(s) and Γ(1/2) = √π.
- `two_L1_one_bounds`, `two_L1_two_bounds`: Mathlib's six-digit bounds on π, plus square-root
  bounds checked by squaring. This confirms the earlier numerics' 0.49007 and 0.31559.
- `pt_ground_state`: explicit first and second derivatives of `cosh^(-ν)` via
  `HasDerivAt.rpow_const`, then algebra with cosh² = sinh² + 1.
- `pt_second_even_state`: write ψ₂ = ψ₀ · (2(ν−1) sinh² − 1) (`psi2_eq`), differentiate twice,
  and express every term through B = cosh^(−ν−2). The identity is then a polynomial identity
  modulo cosh² = sinh² + 1, closed by `linear_combination`. This machine-checks the even k = 2
  eigenfunction I derived by hand.
- `pt_second_even_state_sq_integrable`: ψ₂² ≤ (2ν−1)²·4^ν·e^{−(2ν−4)x} on (0, ∞), using
  cosh x ≥ eˣ/2 and cosh x ≤ eˣ, then `exp_neg_integrableOn_Ioi`.
- `sech2_family_opt`: weighted AM–GM (`Real.geom_mean_le_arith_mean2_weighted`) raised to the
  power a + 1.

What remains a hypothesis in (b) and (d): that ψ₀, ψ₂ lie in the domain of the Neumann operator
(evenness gives ψ'(0) = 0; L² is proved), and that a sum over all eigenvalues dominates a sum over
some of them. Both are spectral-theory facts Mathlib does not have.

## Task 4: skipped

Task 2 found no counterexample, so there was nothing to certify.

## Task 5: proof attempt just above γ = 3/2 (2026-11-25)

**Target.** Some ε > 0 with L^N_γ = 2·L1(γ) for all γ ∈ [3/2, 3/2 + ε].

**Status: not proved.** Below is a five-step argument. Each step is marked [Lean],
[standard: references still to check], or **GAP**. The Lean pieces are in `Spec.lean` §7.

**Step 1: uniqueness at γ = 3/2.** Claim: for 0 ≤ V ∈ L¹ ∩ L²(0,∞),
S_{3/2}(V) ≤ (3/8)∫V², with equality iff V(x) = 2κ² sech²(κx) for some κ > 0.
- Trace formula for the even extension Ṽ (Buslaev–Faddeev, Zakharov–Faddeev; Schimmer eq. (1)):
  Σ_all |E_j|^{3/2} + T = (3/16)∫_ℝ Ṽ², with T = (3/π)∫₀^∞ k² log|a(k)| dk ≥ 0.
- Neumann states are the even states and Dirichlet states the odd ones, so
  S^N + S^D + T = (3/8) M.
- Equality forces S^D = 0 and T = 0. [Lean: `uniqueness_skeleton`]
- T = 0 means Ṽ is reflectionless, hence a finite soliton (Kay–Moses). For an even potential
  the bound states alternate in parity, so S^D = 0 leaves exactly one bound state, and an even
  1-soliton is centred.
- [standard: still to check the trace formula on L¹ ∩ L² (Deift–Killip-type results) and that
  the equality case passes to that class.]

**Step 2: a counterexample has a nearly optimal ground state.**
- Any V beating 2·L1 at γ has efficiency e > 2 − 1/r(γ) (ELU plus the one-bound-state bound),
  and that threshold tends to 1 as γ ↓ 3/2.
  [Lean: `beating_needs_big_ground_state`, `threshold_tendsto_one`, `threshold_eventually_gt`]
- It also needs at least two Neumann bound states. [Lean: `single_state_ok`]

**Step 3: stability. GAP.**
- Needed: if γ_k ↓ 3/2 and e_{γ_k}(V_k) → 1, then after scaling V_k converges to 2 sech² in
  L^{γ_k + 1/2}.
- Expected from concentration-compactness for the one-bound-state (Gagliardo–Nirenberg /
  Sz.-Nagy) problem: optimizers are unique up to symmetries, and even extensions exclude
  translations.
- Must be written out uniformly in γ.

**Step 4: local count near the soliton.** [standard: to cite]
- For ν ∈ (1, 2), the even sector of ν(ν+1) sech² has exactly one bound state and no zero-energy
  resonance.
- The first even resonance is at ν = 2 (γ = 5/2): there ψ₂ = 3 tanh² − 1 is a bounded
  zero-energy solution. [Lean: `pt_second_even_state` with ν = 2]
- So perturbations small in ∫(1 + x)|W| keep exactly one Neumann eigenvalue (continuity of the
  zero-energy solution plus Sturm oscillation). For such V the conjectured bound holds.
  [Lean: `single_state_ok` + the one-bound-state bound]

**Step 5: far mass. GAP, and the main obstacle.**
- Step 3 gives closeness in L^p, which does not control ∫(1 + x)|W|: a small, distant tail can
  bind a weak extra Neumann state.
- Plan: split V with an IMS partition of unity at scale R using logarithmic cutoffs, so the
  localization potential W_loc has ∫x W_loc → 0 and cannot bind by itself (Bargmann).
  - The near part is handled by Step 4.
  - The far part, with Dirichlet at its inner end, is bounded by whole-line LT with constant
    L_γ = Lcl < 2L1 ([Lean] `two_exp_neg_one_lt_r`).
- Bookkeeping gives S ≤ 2L1·M + 2L1·η − (2L1 − Lcl)·M_far. [Lean: `localization_bookkeeping`]
- Missing: show the localization errors are o(M_far) whenever far states exist.
- Alternative route:
  - Prove optimizers exist via the dual formulation, as in Frank–Gontier–Lewin. Strict binding
    holds, since L^N_γ ≥ 2L1 > Lcl = L_γ.
  - Then use the Euler–Lagrange relation V = c·(Σ_j |E_j|^{γ−1}|ψ_j|²)^{1/(γ−1/2)}, which forces
    exponential decay.
  - Even then, optimizers with a self-consistent near-threshold tail (∫x V_tail = O(1)) still
    have to be excluded.

**Conclusion.** Steps 1, 3, 4 and 5 together give L^N_γ = 2·L1(γ) on [3/2, 3/2 + ε), with ε
not explicit. [conjecture: conditional on Steps 3 and 5; Steps 1 and 4 need their citations
checked]

**Other routes considered.**
- *Aizenman–Lieb with the γ = 3/2 deficit.* S_γ ≤ 2Lcl·M − C_γ∫ D((V − t)₊) t^{γ−5/2} dt, where D
  is the Dirichlet sum plus the scattering term. The route needs the averaged deficit to be at
  least 2Lcl(1 − r(γ))M. As γ ↓ 3/2, C_γ ~ (γ − 3/2) and small t dominate, so the averaged deficit
  tends to D(V), which vanishes at the soliton. So this route cannot close near the optimizer
  without Step 4. [heuristic]
- *Cumulative mass* (Benguria–Loss / Read–Schulz) works at γ = 1 only.
  [Lean: `riccati_match_iff`, `mExp_new_range`]
- *γ = 5/2 trace formula:* the scattering term has the wrong sign for an upper bound (Task 2).

## Final report (2026-11-25)

**Proved in Lean** (no `sorry`, standard axioms only; `halfline_lt/HalflineLt/Spec.lean`):
- the constants L1, Lcl, r and their properties: r decreasing, r > 2/e, closed forms at γ = 1, 2;
- the bound L^N ≤ Lcl + L1 and the counterexample conditions, from ELU (1.6) and the
  one-bound-state bound taken as hypotheses;
- (a)–(d) in abstract form;
- the Pöschl–Teller eigenfunctions ψ₀, ψ₂ and ψ₂ ∈ L² (the analytic content of (b) and (d));
- optimality within the sech² family;
- the Task 5 skeleton lemmas.

**Literature.** Nothing settles L^N_γ on (3/2, 5/2]. The best published upper bound there is
2Lcl. Lcl + L1 follows by combining ELU (1.6) with the one-bound-state bound, which no paper I
read does.

**Numerics** (Lean `Float`, evidence only):
- no counterexample for γ ≤ 5/2 in four families plus the exact sech² family;
- at γ = 3 the best found is 1.000119 × 2L1, above the soliton's 1.000064.

**Open.** The conjecture itself. The near-3/2 theorem is conditional on Steps 3 (stability)
and 5 (far mass).

**What changed.**
1. The known upper bound improves from 2Lcl to Lcl + L1.
2. Counterexamples must have at least two Neumann states and ground-state efficiency above
   2 − 1/r(γ).
3. The numerical evidence is now robust to grid artefacts.
4. There is a concrete proof architecture near 3/2 with the gaps named precisely.

**Next steps.**
1. Write out Step 3 (stability of the one-bound-state inequality, uniformly in γ).
2. Attack Step 5: localization error control, or existence of optimizers plus Euler–Lagrange.
3. Check the citations behind Steps 1 and 4.
4. Optionally, test Step 5's key inequality numerically on distant-tail families.

## Task 5, round 2 (2026-11-25)

**Step 3 is a published theorem** at each fixed γ. Carlen–Frank–Lieb, "Stability estimates for the
lowest eigenvalue of a Schrödinger operator", GAFA 24 (2014) 63–84, arXiv:1301.5032, Thm 2.2:
- it covers d = 1 for every γ > 1/2;
- the eigenvalue deficit bounds the distance to the optimizers (translates and dilates of the
  soliton) in L^p, p = γ + 1/2, quadratically for p ≤ 2 and with power 2γ − 1 for p ≥ 2;
- the constants are not explicit.

For even extensions the nearest optimizer must be centred, since translates by ±x₀ are both
close. Still to check: that the constant stays bounded below as γ ↓ 3/2.
[paper: CFL Thm 2.2; read via the ar5iv HTML]

CFL's power does not close Step 5 by itself. For a distant tail of mass m, it only gives a
deficit of order m^{(2γ−1)/(γ+1/2)}, and that exponent is ≥ 1 for γ ≥ 3/2. So the deficit can be
smaller than the m-sized contribution of the tail's bound states.

**Step 4, made explicit.** At zero energy, t = tanh x turns the Pöschl–Teller equation into
Legendre's equation of degree ν.
- The Neumann solution is bounded exactly when P_ν'(0) = 0, i.e. ν ∈ {0, 2, 4, …}, by the
  closed form P_ν'(0) = −2√π / (Γ((ν+1)/2) Γ(−ν/2)) (DLMF 14.5.2 with μ = 0).
- So the even sector is non-resonant for ν ∈ (1, 2), and first resonant at ν = 2, i.e.
  γ = 5/2, where ψ₂ = 3 tanh² − 1. [Lean: `resonance_at_five_halves`]
- That bounded-perturbation statements hold at non-resonant thresholds is standard; references
  are still to check.

**Step 5: the missing mechanism.** Write V = V_sol + W, with V_sol the half-soliton, p = γ + 1/2
and ψ₁ the ground state (normalized on (0, ∞)). Then

  S(V) − 2L1·M(V) = [λ₁(V)^γ − 2L1·M(V)] + Σ_{n≥2} |E_n(V)|^γ.

- *First order cancels.* The soliton is a maximizer of the one-bound-state functional, so
  Euler–Lagrange holds: γ λ₁^{γ−1} ψ₁² = 2L1 · p · V_sol^{p−1}. The ground state's first-order gain
  ∫ W ψ₁² is therefore exactly matched by the first-order mass cost p ∫ V_sol^{p−1} W.
- *The self-mass is available.* For W ≥ 0 the tangent bound [Lean: `add_rpow_ge_tangent`] gives
  M(V_sol + W) ≥ M(V_sol) + p ∫ V_sol^{p−1} W + M(W). Hence
  λ₁(V)^γ − 2L1·M(V) ≤ R₂(W) − 2L1·M(W),
  where R₂(W) ≥ 0 is the second-order ground-state gain, quadratic in W and exponentially small
  when W is far away.
- *Excited states.* They come only from the tail. Step 4 excludes excited states near the
  soliton. The tail's states should be bounded by Lcl·M(W)·(1 + o(1)), via the commuted problem:
  the excited Neumann states of V are the Dirichlet states of V₁ = V + 2(log ψ₁)'', and
  V₁ ≈ PT(ν − 1) has no Dirichlet states and is non-resonant.
- *Net.* S − 2L1·M ≤ R₂ + R₂' − (2L1 − Lcl)·M(W), where R₂' collects the excited-state error
  terms. With 2L1 > Lcl ([Lean] `two_exp_neg_one_lt_r`), what remains is to show R₂ + R₂' = o(M(W)).

This explains the earlier worry (Task 2's derived notes). A distant tail's first-order effect on
the ground state is not a free gain; it is paid for at first order.

**The remaining gap, stated precisely.**
1. Control the second-order remainder R₂(W) and the excited-state error R₂'(W) by
   o(M(W)), uniformly over tails that create extra Neumann states. The likely-hard regime is long,
   weak tails near the binding threshold.
2. Handle W of both signs near the soliton (V < V_sol somewhere). That part is covered by the
   negative second variation (CFL) and has no excited states (Step 4).
3. Bound the L^p mass of (V₁)₊ on the tail by the tail's own mass times a factor below
   2L1/Lcl = 2r(γ). In the far linearized regime, V₁ ≈ −W + 4κ (K ∗ W) with
   K(s) = e^{−2κs} 1_{s>0}.
   - For slowly varying W, V₁ ≈ W, so the factor tends to 1.
   - For narrow W, V₁ is spread out and small.
   - Sharp edges contribute O(1/κ) corrections of either sign. By hand, for a box the net
     correction is negative at p = 2 but slightly positive at p = 3. [hand computation]
   - Young's inequality alone loses a factor up to 2^p, which is too much.

**Other references found.** Frank–Simon–Weidl, CMP 282 (2008), arXiv:0707.0998: comparison
theorems giving Lieb–Thirring bounds for perturbations of non-free operators with regular
ground states. A possible tool for R₂', but its constants are not sharp.

## Results write-up (2026-11-25)

`RESULTS.md` states and proves what this project has established:
- **Theorem 1.** L^N_γ ≤ Lcl + L1 for γ ≥ 3/2. This is new as far as the Task 1 search found.
- **Corollary 2.** For odd N, L_{γ,N} ≤ Lcl + L1/N on star graphs. This is new for odd N ≥ 3 with
  3/2 < γ < 2. It is the improvement asked for in Demirel-Frank's Remark (4), whose wording I
  re-checked against the paper (Prop. 4 needs N₀ < N, both odd).
- **Theorem 3.** The conjecture holds for every 0 ≤ V ≤ 6a⁻² sech²(x/a), for all γ ≥ 1/2. The
  envelope is critical, because of the even resonance at ν = 2.
- **Corollary 4.** What a counterexample must look like.

Lean, §8 of `Spec.lean`:
- the zero-energy solution and its unique zero;
- the star-graph algebra;
- the "only γ ≤ 5/2" step of Theorem 3's equality case, in `envelope_excludes_large`,
  `half_soliton_fits_iff` and `half_soliton_fits_iff_gamma`.

`lake build` passes, and all 64 theorems use only the standard axioms.

Corrections made while writing up:
- The negative spectrum need not be finite.
- The ∫(1 + x)V condition is needed only for U = 6 sech².
- The equality case needs V ≢ 0 and γ > 1/2.

**Machine note.** For part of 2026-11-25, `import Mathlib` took over 6 minutes instead of the
usual 35–45 s. During it, Lean made about 1,500 tiny reads per second, and McAfee's
`mc-pco-scanner` used about one full CPU core. A second import was just as slow, then the slowdown
cleared by itself. A file importing only `Mathlib.Data.Real.Basic` still took 11 s during the
slowdown, so the cost scales with the number of `.olean` files opened (8,747 for `Mathlib`). If it
returns, an antivirus exclusion for `halfline_lt\.lake` would likely avoid it. Antivirus settings
were not changed.

## G9: optimizer uniqueness citation (2026-11-25)

**Question** (review M3, C7). Theorem 3's converse needs: for γ > ½, if 0 ≤ Ṽ ∈ L^{γ+1/2}(ℝ)
gives equality |E₁(−d² − Ṽ)|^γ = L1(γ) ∫_ℝ Ṽ^{γ+1/2}, then Ṽ = c²(γ² − ¼) sech²(c(x − x₀)) for some
c > 0, x₀ ∈ ℝ. Our convention is H = −d² − V with V ≥ 0 a well. DEL15 uses the same convention.
CFL14 and Fra21 write −Δ + V and use V₋ = max{−V, 0}, so our Ṽ is their −Ṽ.

**Verdict.** Citation found. Each source supplies a different piece:
- **Uniqueness.** [CFL14, Thm 2.1] proves that for d = 1, γ > ½ the set of V ≢ 0 attaining the
  one-bound-state bound is {b²𝒱(b(· − a)) : b > 0, a ∈ ℝ} for one fixed 𝒱, so translations and
  dilations only, with no constant multiple. This is the load-bearing source.
- **Sharp constant.** [DEL15, Lemma 1] and [Fra21, eq. (23)] give its value, which equals our
  L1(γ) (checks below). Together with step 2 (U₀ attains L1), this puts −U₀ in CFL's set, so the
  set is {−c²U₀(c(· − x₀))}.
- **Corroboration.** [DEL15, Lemma 1] also states the equality case, in our sign convention, as
  q(q − 1) sech² s with q = γ + ½, so q(q − 1) = γ² − ¼. Its wording adds a spurious "multiplication
  by a positive constant": cV₁ with c ≠ 1 is not an optimizer, and DEL15's own proof gives only
  the two-parameter family. The lemma is headed "(See [11,12].)", and its "only if" is only
  sketched (Caveats below). So DEL15 is not used as the proof of uniqueness.
- [Fra21, §4.2] notes uniqueness "(up to symmetries)", inferred from Nagy [151] via duality.

Our own part: combining the citations (step 3); the Neumann ground energy equals the whole-line
ground energy of the even extension, and evenness forces x₀ = 0 (step 4); the γ > 5/2 exclusion
(step 5); the hand check in step 2; and the constant identities below.
Label for Theorem 3's "only if" (γ > ½): [paper: CFL14 Thm 2.1 (uniqueness); DEL15 Lemma 1, Fra21
eq. (23) (sharp constant)] + [own argument, reviewed 2026-11-25: steps 2–5 and the constant
identities below].

### Sources, verbatim

0. **[DEL15]** J. Dolbeault, M. J. Esteban, M. Loss, "Keller–Lieb–Thirring inequalities for
   Schrödinger operators on cylinders", C. R. Acad. Sci. Paris, Ser. I 353 (2015) 813–818,
   doi:10.1016/j.crma.2015.06.018. Open copy: https://numdam.org/item/10.1016/j.crma.2015.06.018.pdf.
   Read in full by a subagent; I re-checked the Lemma 1 statement and its proof myself in the
   extracted text. The extraction drops Greek letters, so symbols are restored from context and
   from the subagent's second extraction. [paper]
   - Setting (p. 814): Λ_R(μ) := sup{λ^R_1[V] : V ∈ L^q(R), ‖V‖_{L^q(R)} = μ}, "where … −λ^R_1[V]
     denote[s] the lowest eigenvalues of the Schrödinger operators … −∂²_s −V … on … R. … The
     expression of Λ_R(μ) was found by J.B. Keller in [11] and later rediscovered by E.H. Lieb and
     W. Thirring in [12]. We refer to this result as the Keller–Lieb–Thirring inequality".
   - Lemma 1 (p. 814): "Lemma 1. (See [11,12].) Assume that q ∈ (1, +∞). Then we have
     Λ_R(μ) = (q − 1)² (μ/μ_1)^β ∀μ > 0, with β = 2q/(2q−1). As a consequence, if V is a
     nonnegative real valued potential in L^q(R), then we have λ^R_1[V] ≤ Λ_R(‖V‖_{L^q(R)}) and
     equality holds if and only if, up to scalings, translations and multiplications by a positive
     constant, V(s) = q(q−1)/(cosh s)² =: V_1(s) ∀s ∈ R, where ‖V_1‖_{L^q(R)} = μ_1,
     λ^R_1[V_1] = (q−1)². Moreover, the function ϕ(s) = (cosh s)^{1−q} generates the corresponding
     eigenspace."
   - Proof (§2, pp. 815–816): Hölder, then "It is standard (see for instance [5]) that the function
     ϕ(s) = (cosh s)^{−2/(p−2)} is optimal for the inequality written with μ = μ_1", and
     V_1 = q(q−1)ϕ^{p−2} "corresponds to the equality case in Hölder's inequality. More details can
     be found in [2]." For general μ: "Optimality is therefore achieved for V_ν ∈ L^q(R) with
     ‖V_ν‖_{L^q(R)} = μ > 0 if and only if ν^{2−1/q} = μ/μ_1 and V(s) = V_1(s − s_0) for some
     s_0 ∈ R". Here q = p/(p − 2), [5] = Dolbeault–Esteban–Laptev–Loss, J. Lond. Math. Soc. 90
     (2014) 525–550, [2] = Dolbeault–Esteban, Nonlinearity 27 (2014) 435.
   - Caveats: the "only if" is a sketch resting on Hölder's equality case plus uniqueness of the GN
     optimizer, which [5] states (DELL14, after Thm 1.2, p. 3; quoted by a subagent as "up to
     translations, multiplication by a constant and scalings, the function v⋆ is the unique optimal
     function for (1.1)"; that quote was not re-checked). The written proof fixes the norm, so a
     free constant multiple does not actually occur: it gives V = V_{1,μ}(· − s₀) with
     V_{1,μ}(s) = ν²V₁(νs), ν = (μ/μ₁)^{q/(2q−1)}, so "scalings" is the dilation V ↦ ν²V(ν·).
     "V(s) = V_1(s − s_0)" should read V_{1,μ}; this is a typo in the paper.
   - Hypotheses checked: operator −∂² − V with V ≥ 0 ∈ L^q(ℝ), the same as ours for Ṽ. q = γ + ½,
     and q > 1 is γ > ½. No decay, continuity or existence of an eigenvalue is assumed.
   - Constant [own argument, reviewed 2026-11-25]: βγ = 2q(q − ½)/(2q − 1) = q, so
     Λ_R(‖V‖_q)^γ = (q−1)^{2γ} μ₁^{−q} ∫V^q, and μ₁^q = (q(q−1))^q √π Γ(q)/Γ(q+½) by the beta
     integral. Hence |E₁|^γ ≤ (q−1)^{2γ−q} q^{−q} Γ(q+½)/(√π Γ(q)) ∫V^q, and at q = γ + ½ this
     constant is (γ−½)^{γ−½}(γ+½)^{−γ−½} Γ(γ+1)/(√π Γ(γ+½)) = L1(γ).

1. **[CFL14]** E. A. Carlen, R. L. Frank, E. H. Lieb, "Stability estimates for the lowest
   eigenvalue of a Schrödinger operator", GAFA 24 (2014) 63–84, arXiv:1301.5032. Read via
   https://ar5iv.labs.arxiv.org/html/1301.5032 (the PDF did not decode, so no page numbers). The
   Theorem 2.1 passage was fetched twice, once by a subagent and once directly. [paper]
   - Operator: §2.1, "the smallest eigenvalue of the operator −Δ+V in L²(ℝ^d)", defined by
     eq. (2.1), λ(V) = inf{∫(|∇ψ|² + V|ψ|²) dx : ‖ψ‖₂ = 1} (the form infimum). §1 has "the lowest
     eigenvalue of the Schrödinger operator −Δ+V in L²(ℝ^d)".
   - Theorem 2.1 ("Existence and uniqueness of an optimal potential"): "Let γ>1/2 if d=1 and γ>0
     if d≥2 and define" 𝒞_{γ,d} := sup |λ(V)| / (∫V₋^{γ+d/2} dx)^{1/γ}. "Then there is a
     non-positive function 𝒱, which is unique up to translations and dilatons, such that" (2.2)
     M = {V ∈ L^{γ+d/2}(ℝ^d) : |λ(V)| = 𝒞_{γ,d}(∫V₋^{γ+d/2} dx)^{1/γ}} = {b²𝒱(b(· − a)) : b > 0,
     a ∈ ℝ^d}. (Formulas transcribed from the HTML as plain text.) Read literally, the first set
     in (2.2) also contains every V ≥ 0; we use (2.2) only when V₋ ≢ 0.
   - §1: "Keller solved the d=1 problem and computed 𝒞γ,1 by explicitly computing the optimal
     potential, which cannot be explicitly computed for d≥2."
   - §4.1: "In contrast, for d=1 the optimizers where explicitly found by Keller [19] by solving the
     corresponding Euler–Lagrange equation (although Keller did not prove the existence of a
     minimizer nor discuss the regularity needed for the solution of the Euler–Lagrange equation).
     The d=1 result is also implicitly contained in [26]." ([19] = Keller 1961, [26] = Sz.-Nagy
     1941, per a summary of the bibliography, not read verbatim.)
   - §2.2 (duality): eq. (2.11) "with equality if and only if U=(|ψ|/‖ψ‖_q)^{q−2}", and "the
     minimizer in (2.12) is unique up to translations and a sign"; eq. (2.14) M = {−b²|ψ(b·)|^{q−2}
     /‖ψ‖_q^{q−2} : ψ ∈ 𝒢, b > 0}, with 1/(γ + d/2) + 2/q = 1 (eq. (2.3)). So the paper itself does
     the duality and the transfer of the equality case.
   - No explicit formula for 𝒱 or 𝒞_{γ,1} in the text read.
2. **[Fra21]** R. L. Frank, "The Lieb–Thirring inequalities: recent results and open problems",
   arXiv:2007.09326 (Proc. Symp. Pure Math. 104, AMS 2021). Read via the ar5iv HTML, §§1–4.4
   verbatim. [paper]
   - §4.2, eq. (20): "|E_1(−Δ+V)|^γ ≤ L^{(1)}_{γ,d} ∫ V(x)_−^{γ+d/2} dx", for γ, d as in Thm 10
     ("γ ≥ 1/2 if d = 1"), real V ∈ L^{γ+d/2}.
   - §4.2: "In dimensions d = 1, the value of the optimal constant K^{(1)}_{p,1} and the set of
     optimizers was determined by Nagy [151]. Via (22) this leads to the formula" (23)
     L^{(1)}_{γ,1} = π^{−1/2} Γ(γ+1)/Γ(γ+1/2) · (γ−1/2)^{γ−1/2}/(γ+1/2)^{γ+1/2}.
   - §4.2: "The duality used to derive (22) also shows that optimizers u of (21) are in one-to-one
     correspondence (modulo symmetries) with optimal potentials V in (20). In particular, we infer
     that there is a unique (up to symmetries) optimizing potential of (20)."
   - §1.2, d = 1 Sobolev case only: "equality in (2) is attained if and only if u coincides, up to
     translation, dilation and multiplication by a constant, with Q(x) = (cosh x)^{−1/2}."
   - No explicit sech² potential in the text read.

**Hypotheses against our setting** [own argument, reviewed 2026-11-25].
- γ > ½ and d = 1: Theorem 3's converse is for γ > ½ (γ = ½ is a separate argument on the page).
  γ > ½ is exactly q > 1, DEL15's range.
- Ṽ ∈ L^{γ+1/2}(ℝ) because V ∈ L^{γ+1/2}(0, ∞). CFL's class is all real V ∈ L^{γ+1/2}, so 0 ≤ Ṽ
  is covered after the sign flip V ↦ −Ṽ.
- Constants. Our L1(γ) is exactly Fra21 (23): Γ(γ+1)/(√π Γ(γ+½)(γ+½)) · ((γ−½)/(γ+½))^{γ−½} =
  π^{−1/2} Γ(γ+1)/Γ(γ+½) · (γ−½)^{γ−½}/(γ+½)^{γ+½}. CFL's 𝒞_{γ,1}^γ = L^{(1)}_{γ,1}, since CFL raise
  the mass to the power 1/γ. Fra21 (23), stated for real V, is what fixes CFL's 𝒞. DEL15's
  constant is L1(γ) too (Constant bullet above), and its supremum over V ≥ 0 is the same as CFL's
  over real V, since λ(V) ≥ λ(−V₋) and ∫V₋^q is unchanged; so DEL15 is a cross-check.

### Applying it to Theorem 3

Let U₀ = (γ² − ¼) sech² x on ℝ and ν = γ − ½.
1. U₀ has ground state sech^ν x with eigenvalue −ν². [Lean: `pt_ground_state` (eigen-equation only)] + [paper: DEL15
   Lemma 1 (ground state, λ₁[V₁] = (q−1)²), "ϕ(s) = (cosh s)^{1−q} generates the corresponding
   eigenspace", q − 1 = ν]. `pt_ground_state` proves only the pointwise ODE
   −ψ″ − ν(ν+1) sech² ψ = −ν²ψ; that ψ ∈ H¹ and that −ν² is the form infimum come from DEL15.
   Note ν(ν+1) = γ² − ¼.
2. U₀ attains the sharp constant. [paper: DEL15 Lemma 1, λ^R_1[V_1] = (q−1)² with equality]
   Cross-check by hand, using ∫_ℝ sech^{2s} x dx = √π Γ(s)/Γ(s + ½) [standard: beta integral,
   B(s, ½)] at s = γ + ½, so ∫_ℝ U₀^{γ+1/2} = (γ²−¼)^{γ+½} √π Γ(γ+½)/Γ(γ+1). The Γ factors cancel
   against L1(γ):
   L1(γ) ∫U₀^{γ+1/2} = (γ−½)^{γ−½}(γ+½)^{−γ−½} · (γ−½)^{γ+½}(γ+½)^{γ+½} = (γ−½)^{2γ} = |E₁|^γ.
   The integral is over ℝ; on (0, ∞) it is half, matching 2L1 M_γ in Theorem 3.
   [own argument, reviewed 2026-11-25; not in Lean, see G6]
3. So for γ > ½ the equality cases of |E₁(−d² − W)|^γ ≤ L1(γ)∫W^{γ+1/2} with 0 ≤ W ∈ L^{γ+1/2}(ℝ),
   W ≢ 0, are exactly W = c²(γ² − ¼) sech²(c(x − x₀)) a.e., c > 0, x₀ ∈ ℝ. Here E₁ means the form
   infimum, as in CFL (2.1). Proof: L1(γ) is the sharp constant [paper: DEL15 Lemma 1; Fra21
   eq. (23)], so equality means −W lies in CFL's set M of (2.2), and (−W)₋ = W ≢ 0. By step 2, −U₀ ∈ M, so by
   [paper: CFL14 Thm 2.1] {V ∈ M : V₋ ≢ 0} = {−b²U₀(b(· − a)) : b > 0, a ∈ ℝ}, and b²U₀(bx) =
   b²(γ²−¼) sech²(bx). [own argument, reviewed 2026-11-25: combining the citations] DEL15 Lemma 1
   states the same family, up to its spurious constant multiple (see Verdict).
4. Reduction to the line. Let V satisfy Theorem 3's hypotheses with γ > ½, V ≢ 0 and
   S_γ(V) = 2L1 M_γ(V). The envelope gives at most one Neumann state, so S_γ(V) = |E₁^N(V)|^γ (and
   S_γ > 0 gives exactly one). So |E₁^N(V)|^γ = 2L1 M_γ(V) = L1∫_ℝ Ṽ^{γ+1/2}.
   Next, E₁^N(V) = E₁(Ṽ), both as form infima. (E₁^N ≥ E₁(Ṽ)) The even extension of any u ∈ H¹(0, ∞) is in
   H¹(ℝ) with twice the form value and twice the norm². (E₁^N ≤ E₁(Ṽ)) Split φ ∈ H¹(ℝ) as φ = φ_e + φ_o. Since
   Ṽ is even, the cross terms vanish in both the form and the norm. The even part restricts to
   H¹(0, ∞), giving a quotient ≥ E₁^N. The odd part restricts to H¹₀(0, ∞) ⊂ H¹(0, ∞), also ≥ E₁^N.
   So the form of φ is ≥ E₁^N‖φ‖². Hence Ṽ = c²(γ²−¼) sech²(c(x − x₀)) a.e. by step 3.
   Evenness: Ṽ(x) = Ṽ(−x) for all x, so the continuous right-hand side satisfies
   sech²(c(x − x₀)) = sech²(c(x + x₀)) a.e., hence for all x. At x = x₀ this is 1 = sech²(2cx₀), so
   x₀ = 0, and V = c²(γ²−¼) sech²(cx) for a.e. x > 0, which is the page's form with b = 1/c. (Both
   sides of the envelope inequality in step 5 are then continuous, so a.e. and pointwise agree.)
   [own argument, reviewed 2026-11-25]
5. Range of γ. The potential from step 4 lies under some envelope 6a⁻² sech²(x/a) if and only if
   γ ≤ 5/2. [Lean: `half_soliton_fits_iff_gamma`] So for γ > 5/2 no V ≢ 0 in Theorem 3's class
   attains equality. For ½ < γ ≤ 5/2 the equality cases with V ≢ 0 are exactly the half-solitons
   (γ² − ¼) b⁻² sech²(x/b), b > 0; the "if" half is the page's Equality step. γ = ½ is not covered
   here: both citations need γ > ½, and the page treats it by a separate argument.
   [own argument, reviewed 2026-11-25]

### Search scope (G9)

- Read: DEL15 (full, PDF from numdam); CFL14 (ar5iv, about 80% verbatim, bibliography summarized
  only); Fra21 (ar5iv, §§1–4.4 verbatim, the rest summarized only).
- Also read, supporting the GN-duality route but not needed given DEL15 and CFL14:
  - Dolbeault–Esteban–Laptev–Loss, J. Lond. Math. Soc. 90 (2014), arXiv:1309.0987, after Thm 1.2
    (read by a subagent; not re-checked):
    GN optimizer v⋆ = (cosh x)^{−2/(p−2)} unique up to translation, constant multiple and scaling.
  - Frank–Gontier–Lewin, CMP 384 (2021), arXiv:2002.04964, §2: "the optimiser is unique up to
    translations, dilations and multiplication by a phase factor" in d = 1, citing [Nag41].
  - Dolbeault–Gontier–Pizzichillo–Van Den Bosch, Rev. Mat. Iberoam. 40 (2024), arXiv:2210.03091,
    p. 3: GN optimizers give optimal potentials (one direction only).
- Read, optimizer named without a uniqueness claim: Schimmer arXiv:2203.06051 §4.1 eq. (11)
  ("achieved for the Pöschl–Teller potential"); Benguria–Loss math-ph/0402048; Dolbeault–Esteban–
  Laptev arXiv:1301.1210 (points to LT76 p. 290 for the explicit 1D case); Frank–Gontier–Lewin
  arXiv:2010.02981 (γ = 3/2 only); Levitt arXiv:1206.1473 (numerical); Read–Schulz arXiv:2609.10478.
- Not accessed: Keller 1961 (J. Math. Phys. 2, 262–266; the publisher link returned a different
  article); Lieb–Thirring 1976 (no open copy); Frank–Laptev–Weidl Ch. 5 (chapter abstract only,
  "We discuss Keller's problem…"); Weinstein 1983 (empty PDF); Sz.-Nagy 1941 and Kwong 1989 (not
  attempted); Frank's BIRS 2013 slides (403); Veling, JIPAM 2002 (503).
- The PDFs of CFL14 and Fra21 did not decode in the fetch tool, so those quotes have no page
  numbers.

## Review

### 2026-11-25: first independent review (`/review`)

**Setup.** Two `general-purpose` Claude subagents ran in parallel. Neither saw the derivation, this
log, or any opinion on which parts were solid.
- **Inputs:** `docs/halfline-lieb-thirring/index.html`, the "Task 1: literature" section of these
  notes, and `halfline_lt/HalflineLt/Spec.lean`.
- **Mathematics reviewer:** asked to check every step, the cited hypotheses, edge cases, hidden
  uniformity, and gaps in "What remains open".
- **Claims reviewer:** asked to check every Lean name against its statement, the evidence labels,
  the novelty scope and the numbers.
- **Citation search:** a third agent searched the works citing [DF15], because the claims reviewer
  found that search missing.

**Findings and responses.** "Fixed" means the page was changed. The page is
`docs/halfline-lieb-thirring/index.html`; this list replaces its earlier copy in `RESULTS.md`.

Mathematics reviewer:

| # | Finding (abridged) | Severity | Response |
|---|---|---|---|
| M1 | "What remains open": the route does not prove the conjecture; Lᵖ-closeness does not keep V under an envelope | FIX | Fixed: rewritten as "one possible route" with each gap listed, including the missing bound on Σ_{j≥2}. Labeled Conjecture. |
| M2 | (b) and (d) labeled Lean, but `fact_b` and `fact_d` are abstract | FIX | Fixed: relabeled Standard [PT33, LT76], with Lean shown for the eigenfunction equations, the new `psi0_neumann`/`psi2_neumann`, and L². |
| M3 | Equality case needs uniqueness of one-bound-state optimizers; LT76 may not state it | FIX | Fixed: the converse is now conditional and marked "Unverified citation". The statement asserts only the "if" direction and the γ = ½ case. |
| M4 | γ = ½ strictness argued only heuristically | FIX | Fixed: the Green's-function argument is now written out on the page. |
| M5 | Novelty box omits Aljahili–Laptev and the FLW Comments gaps | FIX | Fixed: search scope and gaps now listed. |
| M6 | "New range" assumes DF15 eq. (5) holds for odd N ≥ 3 | FIX | Fixed: now conditional ("we have not checked it for odd N ≥ 3"). |
| M7 | Statement says every odd N; the proof needs N ≥ 3 | MINOR | Fixed: odd N ≥ 3, with N = 1 being Theorem 1. |
| M8 | Bargmann/Hardy remark needs the Setting's V ∈ L^{γ+1/2} | MINOR | Fixed: "Within the Setting", and the remark is marked as not proved in detail. |
| M9 | "Conjectured optimizer for every γ ≤ 5/2" fails at γ = ½ and outside the conjecture's range | MINOR | Fixed. |
| M10 | 0⁰ at γ = ½ | MINOR | Fixed: the convention is stated. |
| M11 | Pointwise conditions on an Lᵖ function | MINOR | Fixed: "almost every x" and "a set of positive measure". |
| M12 | Corollary 4 item 1 does not follow from Theorem 3 as stated | MINOR | Fixed: now cites step 4 and N_D ≥ N_N − 1. |
| M13 | Sturm count cited for Neumann without comment | MINOR | Fixed: [PT33] is now the primary argument; Sturm is a cross-check. |

Claims reviewer:

| # | Finding (abridged) | Severity | Response |
|---|---|---|---|
| C1 | (b) Lean chip on abstract `fact_b` | BLOCKER | Fixed, as for M2. |
| C2 | (d) Lean chip on abstract `fact_d`; the Neumann condition is checked only at ν = 2 | BLOCKER | Fixed: relabeled, and `psi2_neumann` added for all ν. H¹ membership and ground-state identity stay Standard. |
| C3 | How much the chips depend on hypotheses is disclosed only at the bottom | FIX | Fixed: new "Lean + cited" chip, a status-box sentence, and a paragraph in "What Lean checks". |
| C4 | "64 theorems" counts unrelated results | FIX | Fixed: "70 in the file; this page cites 30" (counted by script). |
| C5 | Strictness needs `L1_eq_r_mul_Lcl` and Lcl > 0, which was not in the file | FIX | Fixed: added `Lcl_pos`, `L1_lt_Lcl`, `upper_bound_lt_two_Lcl` and `threshold_identity`, all cited. |
| C6 | Steps without chips | FIX | Fixed: chips added to scaling, step 4, step 5, the endpoints, Corollary 4 and the Remarks. |
| C7 | LT76 uniqueness citation not in the literature record | FIX | Fixed, as for M3. |
| C8 | Novelty scope larger than the record | FIX | Fixed: scope stated exactly. Works citing DF15 were searched (below). |
| C9 | DF15 quotations not in the notes | FIX | Fixed: verbatim quotations added to the Task 1 section. They were fetched 2026-11-25. |
| C10 | Strictness claim for γ ≥ 2, where DF15 states a sharper value | FIX | Fixed: the page now says the improvement for odd N ≥ 3 matters only for 3/2 < γ < 2, if eq. (5) holds there. The comparison of the two bounds is still stated; it is true. |
| C11 | "Would prove" is an unproved roadmap | FIX | Fixed, as for M1. |
| C12 | `pt_ground_state` gives the ODE only; Lean states the results for −u | MINOR | Fixed: the page says so. |
| C13 | "Every γ ≤ 5/2" outside the conjecture's range | MINOR | Fixed, as for M9. |

**Citation search** (works citing arXiv:1503.06915):
- Semantic Scholar and OpenAlex each list one citing work: Band–Berkolaiko–Weyand,
  arXiv:1503.07245. It is about nodal counts and is unrelated.
- Web searches found no later improvement of L_{γ,1} ≤ 2L_γ for γ > 3/2, and no improvement of
  the odd-N bound for 3/2 < γ < 2.
- Not reachable: Google Scholar and the NASA ADS citation list.

**Lean.** `check.ps1`: CLEAN, 70 theorems, standard axioms only.

**Verbatim reports.** The full reports are kept below so the record can be checked. Their file
paths are omitted.

<details><summary>Mathematics reviewer</summary>

I checked the core logic and found no blocking error in it. That covers Theorem 1's steps 1–3, the Corollary 2 algebra, Theorem 3's steps 1–4 and its equality "iff", Corollary 4 items 1–3, both tables, r(γ), L1, Lcl, 3/8 and 1. I confirmed DF15 Thm 1 and Prop. 4 ("N₀ < N both odd", γ ≥ ½) from the arXiv PDF. The problems are below.

1. **Corollary 4 / "What remains open", last sentence.** Claim: "Excluding that would prove the conjecture on [3/2, 3/2+ε)." Being Lᵖ-close to a half-soliton says nothing about pointwise envelope bounds. A small spike or a far, thin tail stays Lᵖ-small but escapes every envelope, so "near-optimizer" plus "escapes every envelope" is not a contradiction. Nothing stated shows that near-optimizers have at most one Neumann state. The route as written does not give a proof. Also, CFL14 Thm 2.2 is a whole-line result; its γ-range and its use on the even extension Ṽ are not checked. **FIX.** Change to "one possible route", and name the missing step: a quantitative bound on Σ_{j≥2}|E_j|^γ for near-optimizers.

2. **Known facts (b), label.** (b) is labeled only "Lean fact_b". In Spec.lean, `fact_b` is the abstract statement "c·M(V₀) ≤ S(V₀) ⇒ c ≤ C". The real content is not in Lean: the half-soliton gives |E₁|^γ = 2L1·M, and it has no second Neumann state for γ ≤ 5/2 (from [PT33]/[LT76]). **FIX.** Add Standard/Paper labels citing PT33 and LT76. The same applies to (d): that −ν² is the ground state uses "a positive eigenfunction is the ground state", which is not in Lean (**MINOR**).

3. **Theorem 3, Equality step.** "For γ > ½ its optimizers are c²(γ²−¼)sech²(c(x−x₀)) [LT76]." The proof needs uniqueness of the optimizers up to translation and dilation, not just that they exist. Uniqueness comes from the Sz.-Nagy/Keller uniqueness for the 1D Gagliardo–Nirenberg problem; it is not clear LT76 states it. **FIX.** Cite a source that states uniqueness.

4. **Theorem 3, Equality, γ = ½.** "That bound is strict for every potential, because its extremal is a δ." This is a heuristic with no citation. The statement is true: equality would need ψ = ψ_max·e^{−κ|x−x₀|}, which forces V = 0 a.e. **FIX.** Give this two-line argument or a reference.

5. **Status box, "Novelty".** It says Theorem 1 and Corollary 2 "appear in no paper found". The literature notes record two gaps it does not mention: Aljahili–Laptev (J. Math. Sci. 2023) was not accessed, and the "Comments" sections of Frank–Laptev–Weidl were not checked. **FIX.** State these search gaps on the page.

6. **Corollary 2, "new range".** "The new range is therefore odd N ≥ 3 with 3/2 < γ < 2." This assumes DF15 eq. (5), L_{γ,N} = L_γ for γ ≥ 2, holds for odd N ≥ 3. The page itself shows eq. (5) is false at N = 1, and the source [DH10] (per the notes) treats different vertex conditions. Its validity for odd N ≥ 3 is therefore unverified. **FIX.** Say "if eq. (5) holds for N ≥ 3".

7. **Corollary 2, statement vs. proof.** The statement covers "every odd N", but Prop. 4 with N₀ = 1 needs N₀ < N, so the proof covers only N ≥ 3. **MINOR.** Say that N = 1 is Theorem 1.

8. **Remarks, item 4 (Bargmann/Hardy classes).** "V(x) ≤ 1/(4x²)" and "∫xV < 1" do not by themselves make the Neumann form defined on H¹. Example: V ~ x^{−3/2} near 0 has ∫xV < ∞, but ∫V|u|² = ∞ when u(0) ≠ 0. The claim holds only together with the Setting's V ∈ L^{γ+½}. **MINOR.** Write "within the Setting".

9. **Remarks, item 1.** "…the conjectured optimizer for every γ ≤ 5/2." This fails at γ = ½: there ν = 0 gives V ≡ 0, and the bound is never attained (the extremal is a δ). Also, the page's Conjecture covers only 3/2 ≤ γ ≤ 5/2. **MINOR.** Write "½ < γ ≤ 5/2", and for γ < 3/2 make it conditional on the whole-line conjecture.

10. **Setting / L1 formula at γ = ½.** ((γ−½)/(γ+½))^{γ−½} is 0⁰ at γ = ½, but the page uses L1(½) = ½ (endpoint L^N_{1/2} = 1, and Theorem 3 at γ = ½). **MINOR.** State the convention 0⁰ = 1 (the limit as γ ↓ ½).

11. **Theorem 3 hypothesis and Corollary 4(2).** "For all x > 0" and "there is an x > 0 with V(x) > …" are pointwise, but V ∈ Lᵖ is only defined almost everywhere. **MINOR.** Write "for a.e. x" in Theorem 3 and "on a set of positive measure" in Corollary 4(2).

12. **Corollary 4, "Items 1 and 2 follow from Theorem 3".** Item 1 does not follow from Theorem 3 as stated, which is about the envelope class. It follows from step 4 ("one state suffices") together with N_D ≥ N_N − 1 from the Remarks. **MINOR.** Cite those instead.

13. **Theorem 3, step 1 (Sturm).** [Sim05]'s zero-counting theorem is stated for the Dirichlet or whole-line problem, and the Neumann version is used without comment. The conclusion is already settled by the Pöschl–Teller cross-check [PT33], so nothing breaks. **MINOR.** Say it is the Neumann analogue, or rely on PT33 alone.

</details>

<details><summary>Claims reviewer</summary>

The page's numbers all check out, but it overstates what Lean verifies in several places, leaves several steps without an evidence chip, and its novelty claim goes beyond the recorded search. 13 findings, numbered by severity.

**Numbers I checked and found correct (check D):**
- Both tables at γ = 3/2, 7/4, 2, 9/4, 5/2 recompute exactly.
- x₀ = arsinh √(1/2) = 0.6585.
- L^N_{3/2} = 3/8.
- Spec.lean has exactly 64 `theorem` declarations.
- The Lean and Mathlib versions match `lean-toolchain` and `lake-manifest.json`.

**1. BLOCKER — Setting (b), Lean chip on `fact_b`.** The page claims "L^N_γ ≥ 2L₁(γ) … the half-soliton attains this for γ ≤ 5/2". In Lean, `fact_b` is an abstract three-line lemma: if some V₀ has c·M V₀ ≤ S V₀ and M V₀ > 0, then every admissible C is at least c. The actual content, that the half-soliton's S/M equals 2L₁, is the hypothesis `hV₀`. So is "attains for γ ≤ 5/2", which needs that state to be the only Neumann state. Fix: relabel as Standard/Paper (Pöschl–Teller plus a mass computation), with Lean covering only "test potential ⇒ lower bound".

**2. BLOCKER — Setting (d), Lean chip on `fact_d`.** `fact_d` is a `linarith` step whose hypothesis `S V₀ = 2l₁M V₀ + δ`, δ > 0, carries everything. `pt_second_even_state` and `..._sq_integrable` do check the ODE and L²(0,∞) for ν > 2. They do not check:
- the Neumann condition ψ₂′(0) = 0 for general ν (Lean proves it only at ν = 2, in `psi2_two_at_zero`);
- H¹ membership;
- that the ground-state term alone already gives 2L₁M.

Fix: say "Lean checks the eigenfunction equation and L² membership; the rest is Standard".

**3. FIX — How hypothesis-dependent the Lean chips are is only disclosed at the bottom.** `neumann_upper_ELU`, `beating_needs_big_ground_state`, `at_most_one_state_ok` and `star_graph_bound` are all `linarith` or Finset steps on real numbers. ELU (1.6), the one-bound-state bound and DF Prop. 4 enter as hypotheses. Lean has no operator, no supremum and no infinite eigenvalue sum. Yet the status box ("64 theorems … steps checked in Lean") and each chip read as if the results were verified. Fix: add "(modulo cited hypotheses)" to every such chip, and a status-box sentence saying the Lean files check only the arithmetic and calculus steps.

**4. FIX — Status box, "64 theorems".** Many of the 64 are unrelated to these results: `complete_square*`, `mExp*`, `L1_one`, `two_L1_*_bounds`, `uniqueness_skeleton`, `localization_bookkeeping`, `add_rpow_ge_tangent`, `soliton_bonus_*`, `sech2_family_opt`. Fix: give the number actually used by the page (about 25), or say "64 in the file, N used here".

**5. FIX — Theorem 1 statement and step 3, and Corollary 4(3).**
- Going from `r_lt_one` to "Lcl + L₁ < 2Lcl" needs `L1_eq_r_mul_Lcl` and Lcl > 0. Neither is cited, and Lcl > 0 is not in the file.
- The same applies to `star_graph_bound_strict`, whose hypothesis is l₁ < lcl.
- Corollary 4(3) is stated with 2 − 1/r, but Lean's conclusion is 2(2l₁ − lcl)M. Equating the two also needs `L1_eq_r_mul_Lcl`.
- Step 3 says "The bound is strict", which can be read as S < (Lcl + L₁)M.

Fix: cite `L1_eq_r_mul_Lcl` and reword step 3 to "strictly below 2Lcl".

**6. FIX — Missing or incomplete chips (check B).**
- Theorem 3, step 2 (scaling): no label.
- Step 4: Lean chip only, but it uses the one-bound-state bound, which is Standard.
- Step 5: the optimizer characterization [LT76], "strict at γ = ½ because its extremal is a δ", and the converse (single eigenvalue −(γ−½)²b⁻²) have no label and no citation.
- The Endpoints bullet, which depends on HLT98 and the RS26 preprint, has no label.
- Corollary 4 items 1–2 have no label; the Dirichlet part relies on N_D ≥ N_N − 1, which is uncited.
- The Remarks rely on Pöschl–Teller and Bar52 with no labels.

**7. FIX — Step 5 citation.** The page cites [LT76] for uniqueness of the one-bound-state optimizers. The Task 1 record contains no quoted statement for this. Fix: quote the exact source (Gagliardo–Nirenberg optimizer uniqueness) or mark it unverified.

**8. FIX — Novelty scope (check C).**
- The page says the search "covered [DF15]". The notes say only pp. 1–4 and 8–10 were read.
- Works citing DF15 were never searched, yet Corollary 2 is a star-graph result.
- Not disclosed: Frank–Laptev–Weidl was checked by table of contents only (its Comments sections were not checked), and Aljahili–Laptev 2023 was not accessed.

Fix: state the partial DF15 reading and these gaps, or search the works citing DF15 before claiming Corollary 2 is new.

**9. FIX — Quotations not in the literature record.**
- DF15 Thm 1's bound ((N+1)/N)Lcl and the statement of Prop. 4 are not quoted in the notes.
- The quoted phrase "improve automatically" does not appear in the notes. The notes only paraphrase Remark (4).

Fix: verify the text and quote it in the notes, or remove the quotation marks.

**10. FIX — Corollary 2's "new range".** The page relies on DF eq. (5) (L_{γ,N} = L_γ for γ ≥ 2) for N ≥ 3 while also calling that equation unreliable for N = 1. It also says, for every odd N and γ > 3/2, that the bound is "strictly below Demirel-Frank's bound", even though for γ ≥ 2 a sharper value is known. Fix: limit the strictness claim to 3/2 < γ < 2 for N ≥ 3.

**11. FIX — "What remains open".** "Excluding that would prove the conjecture on [3/2, 3/2+ε)" is an unproved roadmap stated as an implication. It also depends on an unchecked uniformity of the CFL14 stability constant. Fix: "might", plus a Conjecture chip.

**12. MINOR — Theorem 3 step 1, `pt_ground_state`.** It proves the ODE for general ν only. L² membership of sech² and the claim that −4 is the only eigenvalue are not Lean (they come from Sturm). The Lean results are also stated for ψ₂ = −u, not for u. Fix: add a note.

**13. MINOR — Remarks.** "Conjectured optimizer for every γ ≤ 5/2" should be "for 3/2 ≤ γ ≤ 5/2", since the conjecture covers only that range.

</details>

### 2026-11-25: G9 review (`/review`)

**Setup.** Two `general-purpose` Claude subagents ran in parallel. Neither saw the derivation
history or any opinion on which parts were solid.
- **Inputs:** the page's Setting, Theorem 1 and Theorem 3 (HTML stripped to text); the "G9:
  optimizer uniqueness citation" section of these notes; the Theorem 3 claims-ledger row and the
  LEDGER G9 row; the label rules. Both fetched DEL15 (numdam PDF), CFL14 and Fra21 (ar5iv)
  themselves.
- **Mathematics reviewer (G9-M):** quotes, hypotheses (sign convention, L^q class, γ range, the
  even-extension reduction, γ ≤ 5/2), step 2's computation, and whether DEL15 proves its "only if".
- **Claims reviewer (G9-C):** quotes, labels against the rules, row consistency, search scope.
- **Re-review (G9-R):** a third subagent, after the fixes, of the changed parts only (Verdict,
  DEL15 Constant bullet, Hypotheses list, steps 2–5). Then stopped, as the skill says.

**Findings and responses.** Every quote was found accurate by both reviewers, apart from G9-C1.
No mathematical error was found. The page and `RESULTS.md` were not changed (out of scope for
this pass); the items they need are listed in the LEDGER G9 row.

Mathematics reviewer:

| # | Finding (abridged) | Severity | Response |
|---|---|---|---|
| G9-M1 | LEDGER G9 row drops DEL15's "multiplications by a positive constant" from the quote | FIX | Fixed: quoted in full, with the note that the constant multiple is spurious. |
| G9-M2 | Verdict: "DEL15 states exactly what Theorem 3 needs" is overstated; read literally, Lemma 1 admits cV₁ | FIX | Fixed: Verdict rewritten; DEL15 is now corroboration, with the spurious clause stated. |
| G9-M3 | DEL15's "only if" is not load-bearing: CFL14 Thm 2.1 + sharp constant + step 2 suffice; Fra21 (23) missing from the ledger label | FIX | Fixed: step 3 now argues this way; labels name CFL14 for uniqueness and DEL15/Fra21 for the constant, in both places. |
| G9-M4 | CFL (2.2) read literally contains V = 0 | FIX | Fixed: noted under the CFL quote; step 3 uses M ∖ {0}. |
| G9-M5 | "Its proof is short" implies DEL15 proves the "only if"; it is only sketched | FIX | Fixed: Verdict says the "only if" is sketched and headed "(See [11,12].)". |
| G9-M6 | Quotes: no problems | none | No action. |
| G9-M7 | Hypotheses and constants: no problems | none | No action. |
| G9-M8 | Step 4 correct; conclusion should say "a.e."; "evenly extended eigenfunction" gives only one inequality by itself | FIX | Fixed: "a.e. x > 0"; step 4 now proves both inequalities by the even/odd splitting of the form. |
| G9-M9 | Step 2 correct; the middle expression hides the cancelled Γ factors | FIX | Fixed: ∫U₀^{γ+1/2} written out, and the ℝ vs (0, ∞) factor 2 stated. |

Claims reviewer:

| # | Finding (abridged) | Severity | Response |
|---|---|---|---|
| G9-C1 | CFL "the Schrödinger operator −Δ+V in L²(ℝ^d)" is from §1, not at eq. (2.1) | FIX | Fixed: §2.1 wording quoted at (2.1), the §1 phrase attributed to §1. |
| G9-C2 | Same as G9-M2 | FIX | Fixed, as for G9-M2. |
| G9-C3 | DEL15 as primary [paper] source for "only if" overstates it; CFL14 is the source that proves uniqueness | FIX | Fixed, as for G9-M3. |
| G9-C4 | Verdict label and ledger label disagree (Fra21); neither says what each source supplies | FIX | Fixed: one label, with roles, in the Verdict, the claims row and the LEDGER row. The side note (page cites the sharp bound only to LT76, not accessed) is recorded in the LEDGER row as a page item. |
| G9-C5 | Fra21 does not "state the same uniqueness"; it infers uniqueness "up to symmetries" | FIX | Fixed: reworded. |
| G9-C6 | "Hypotheses against our setting" unlabeled; "[derived: …]" is not an allowed label | FIX | Fixed: labeled [own argument, reviewed 2026-11-25], rewrite shown. |
| G9-C7 | DEL15 constant identity stated without computation or label | FIX | Fixed: new Constant bullet with the μ₁^q computation, labeled. |
| G9-C8 | "[hand computation; not in Lean]" is not an allowed label | FIX | Fixed: [own argument, reviewed 2026-11-25; not in Lean, see G6]. |
| G9-C9 | Step 4 "[standard]" with no reference | FIX | Fixed: replaced by a written-out variational proof (even/odd splitting), labeled own argument, so no textbook reference is needed. |
| G9-C10 | "Routine" beside an unreviewed own argument claims it settled | FIX | Fixed: "routine" removed everywhere. |
| G9-C11 | Same as G9-M1 | FIX | Fixed, as for G9-M1. |
| G9-C12 | Theorem 3 row label "[paper: Sturm oscillation, min–max, …]" names no paper | FIX | Fixed: [standard: PT33, Sim05, min–max] + [paper: DEL15 Lemma 1; Fra21 eq. (23)]. |
| G9-C13 | Theorem 3 row covers γ = ½ without a label for that argument | FIX | Fixed: [own argument, unreviewed: page Equality step] added. It stays unreviewed: this pass did not check it. |
| G9-C14 | "V is a half-soliton" is vague; full "iff" stated while the page is still conditional | FIX | Fixed: explicit formula; row says the page still states the converse as conditional. |
| G9-C15 | DELL14 quote came from a subagent only | FIX | Fixed: marked "not re-checked", in Caveats and Search scope. |

Re-review of the changed parts:

| # | Finding (abridged) | Severity | Response |
|---|---|---|---|
| G9-R1 | "γ ∈ (½, 1] is q ∈ (1, 3/2]" reads as partial coverage | FIX | Fixed: "γ > ½ is exactly q > 1". |
| G9-R2 | DEL15's supremum is over V ≥ 0, CFL's over real V; equality of the two needs a line | FIX | Fixed: Fra21 (23) named as what fixes CFL's 𝒞; the line λ(V) ≥ λ(−V₋) added; DEL15 a cross-check. |
| G9-R3 | Verdict's "our own part" lists less than the label (steps 2–5) | FIX | Fixed: list now matches the label. |
| G9-R4 | Minor: "a.e." conclusion vs the pointwise Lean envelope lemma | FIX | Fixed: one clause noting both sides are continuous. |

**Label changes.**
- G9 own steps (2–5, constant identities, hypotheses check): [own argument, unreviewed] →
  [own argument, reviewed 2026-11-25]. All three reviewers checked them and found no error; the
  only changes after the first pass were the step 3/4 rewrites, which G9-R checked.
- Theorem 3 "only if" (γ > ½): primary source changed from DEL15 Lemma 1 to CFL14 Thm 2.1, with
  DEL15 Lemma 1 and Fra21 (23) for the sharp constant.
- Theorem 3 row: the bound's label now names its sources; γ = ½ gets its own
  [own argument, unreviewed] label (new, not a downgrade: it was unlabeled).
- Step 4's ground-state identity: [standard] (no reference) → own argument, reviewed.

### 2026-11-25: PR #9 reviewer-loop comment (commit f62877c)

| # | Finding (abridged) | Severity | Response |
|---|---|---|---|
| PR9-1 | Read literally, CFL's M contains every V ≥ 0, so "M ∖ {0}" is not the soliton family | FIX | Fixed: step 3 uses {V ∈ M : V₋ ≢ 0} and notes (−W)₋ = W ≢ 0; the CFL bullet says "every V ≥ 0". Conclusion unchanged. |
| PR9-2 | Step 1's [Lean: `pt_ground_state`] covers only the eigen-equation, not H¹ membership or the form infimum | FIX | Fixed: label now "[Lean: `pt_ground_state` (eigen-equation only)] + [paper: DEL15 Lemma 1 (ground state, λ₁[V₁] = (q−1)²)]", with ν(ν+1) = γ² − ¼ noted. |
| PR9-3 | LEDGER G9 statement omits "γ > 1/2 and V ≢ 0" | MINOR | Fixed in LEDGER.md. |
| PR9-4 | LEDGER G9 row understates the own-argument part | MINOR | Fixed: "Our own argument, reviewed 2026-11-25: G9 steps 2–5 and the constant identities", matching the notes and the claims row. |

No label was strengthened; PR9-2 narrows a Lean label. No Lean changed.
