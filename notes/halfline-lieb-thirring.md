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
| DF15 eq. (5) for star graphs with N ≥ 2 infinite edges, Kirchhoff centre: L_{γ,N} = L_γ = Lcl for γ ≥ 2. So Corollary 2 improves on known bounds exactly for odd N ≥ 3 and 3/2 < γ < 2. | [paper: Demirel–Harrell 2010, Thm 2.5 + Rem. 2.6, 2.10] | Literature item 4a |
| u = 1 − 3 tanh² (zero-energy Neumann solution for 6 sech²) has exactly one zero on (0, ∞), at arsinh √(1/2) | [Lean] | `Spec.lean` §8 `psi2_two_unique_zero` |
| V ≤ 6a⁻² sech²(x/a) ⇒ S_γ(V) ≤ 2L1(γ)M_γ(V) for all γ ≥ 1/2; for V ≢ 0, equality iff 1/2 < γ ≤ 5/2 and V is a half-soliton | [paper: Sturm oscillation, min–max, one-bound-state bound] + [Lean: §8 inputs] | `RESULTS.md` Thm 3 |
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
4a. **Demirel–Harrell [DH10]**, "On semiclassical and universal inequalities for eigenvalues of
   quantum graphs", arXiv:0911.1896 v1 (10 Nov 2009), Rev. Math. Phys. (2010),
   DOI 10.1142/S0129055X10003965. This closes ledger gap G10 (review M6). Read on 2026-11-25:
   pp. 1–12 of the arXiv PDF, through text extraction, with §§1–2.1 read directly. A fetch
   subagent read the ar5iv HTML as a cross-check. [paper]
   - **Setting (§1).** The operator comes from the form ∫|φ′|², "which leads to vanishing Dirichlet
     boundary conditions at the ends of exterior edges". At each vertex φ is continuous and
     Σ_j ∂φ/∂x_kj(0+) = 0 (eq. (1.2)). "In the literature these vertex conditions are usually
     known as Kirchhoff or Neumann conditions." H(α) = −α d²/dx² + V.
   - **Leaves (§2.1, p. 7).** "a leaf is joined to a vertex at only one of its endpoints, ie. there
     is a free end, at which we shall set Dirichlet boundary conditions."
   - **Theorem 2.5 (p. 8).** "For any tree graph with a finite number of vertices and edges, the
     mapping" α ↦ α^{1/2} Σ_{E_j(α)<0} (−E_j(α))² "is nonincreasing for all α > 0. Consequently"
     α^{1/2} Σ_{E_j(α)<0} (−E_j(α))² ≤ L^cl_{2,1} ∫_Γ (V_−(x))^{2+1/2} dx "for all α > 0."
     (Displayed formulas are transcribed from the PDF text.)
   - **Remark 2.6.** "By the monotonicity principle of Aizenman and Lieb (see [1]), Theorem 2.5 is
     also true with the sharp constant for higher moments of eigenvalues." It also says "Theorem 2.5
     can be extended by a density argument to potentials V ∈ L^{γ+1/2}(Γ)." The proof assumes
     V ∈ C₀^∞ (p. 5).
   - **Remark 2.10.** "The proof applies equally to metric trees with leaves of infinite lengths."
     The paper gives no separate proof of this.
   - **Sharpness.** The proof ends with Weyl's asymptotics,
     lim_{α→0+} α^{1/2} Σ (−E_j(α))² = L^cl_{2,1} ∫ V_−^{5/2}. That gives the lower bound
     L_{2,N} ≥ Lcl. For γ > 2 the same lower bound is the [standard] semiclassical limit.
   - **Why N = 1 is excluded (my check of the mechanism).** The proof averages Lemma 2.1 over
     piecewise-affine G with |G′| ∈ {0, 1} that satisfy (2.3), Σ_j ∂G/∂x_kj(0+) = 0, at every
     vertex. These G correspond to "admissible colorings": an even number of edges coloured 1 at each
     vertex (Def. 2.8). For a star with N leaves the admissible colourings are the even subsets of
     the leaves. Each leaf lies in the same number of them, 2^{N−2}, when N ≥ 2. For N = 1 the only
     admissible colouring is 0, so G is constant and (2.4) is vacuous. The paper states the same
     restriction for its circuit picture (p. 12): "there must be at least two leaves". The N = 1
     Neumann half-line is also not a tree in the paper's sense, because a degree-one free end gets
     Dirichlet there. **Verdict:** DF15 eq. (5) is correct for N ≥ 2. The "all N ∈ ℕ" in DF15 is
     a slip at N = 1 only.
   - **Hypothesis check for star graphs.** For N ≥ 2 infinite leaves, take G = x on leaf i, G = −x
     on leaf j and G = 0 elsewhere. This satisfies (2.3) at the centre, and summing over all pairs
     i < j gives every leaf weight N − 1, so (2.5) holds. Lemma 2.1 needs Gφ_j ∈ D(H). For
     V ∈ C₀^∞, negative-energy eigenfunctions decay exponentially on the infinite leaves, so an
     affine G is harmless. This is the content of Remark 2.10 for stars.
   - **Consequence for Corollary 2.** For odd N ≥ 3 and γ ≥ 2, L_{γ,N} = Lcl < Lcl + L1/N, so
     Corollary 2 is not an improvement there. Its improving range is exactly odd N ≥ 3 with
     3/2 < γ < 2, now unconditional. The page still says "if eq. (5) holds for N ≥ 3"; changing
     that is a page edit and needs `/review`.
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

## Log

- 2026-11-25 (author-loop): literature check of DH10 for ledger gap G10. DF15 eq. (5) holds for star graphs with N ≥ 2 infinite edges, so Corollary 2's improving range, odd N ≥ 3 with 3/2 < γ < 2, is unconditional. The page edit is pending. See Literature item 4a.
