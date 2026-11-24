import Mathlib

/-!
# Specification: sharp Lieb–Thirring constant for the Neumann half-line

Definitions and theorem statements for `prompt.txt`. Proved items must stay proved; every
`sorry` is a task (Task 3). Spectral facts about Schrödinger operators are not in Mathlib and
enter only as named hypotheses.

Notation: `γ` eigenvalue exponent; `ν = γ - 1/2` Pöschl–Teller parameter; `L1` one-bound-state
constant; `Lcl` semiclassical constant; `r = L1 / Lcl`.
-/

open Real

namespace HalflineLt

/-! ## 1. The completed square

Pointwise identity from Read–Schulz, arXiv:2609.10478, p. 3: with cumulative mass
`a(x) = ∫_{-∞}^x u²` (so `a' = u²`), `v = u'`, `Q = q(a)`, `Qp = q'(a)`, the bracket
`u³vQ + ¼u⁶Qp` is the derivative of `¼u⁴q(a)`. -/

theorem complete_square (u v Q Qp : ℝ) :
    v^2 - (u^3*v*Q + (1/4)*u^6*Qp) = (v - (1/2)*u^3*Q)^2 - (1/4)*u^6*(Qp + Q^2) := by
  ring

/-- General real exponent (`u > 0`). The auxiliary term is `u^(m+1) q(a) / (m+1)`, whose
derivative is `u^m v Q + u^(m+3) Qp / (m+1)`. -/
theorem complete_square_rpow {u : ℝ} (hu : 0 < u) (m v Q Qp : ℝ) :
    v^2 - (u^m*v*Q + (1/(m+1))*u^(m+3)*Qp)
      = (v - (1/2)*u^m*Q)^2 - (1/4)*u^(2*m)*Q^2 - (1/(m+1))*u^(m+3)*Qp := by
  have h : u^(2*m) = (u^m)^2 := by
    rw [show (2:ℝ)*m = m*2 by ring, rpow_mul hu.le, rpow_two]
  rw [h]
  ring

/-- The leftover is a multiple of the Riccati combination `Qp + Q²` for all `u > 0`
only when `m = 3`. -/
theorem riccati_match_iff (m : ℝ) : (∀ u : ℝ, 0 < u → u^(2*m) = u^(m+3)) ↔ m = 3 := by
  constructor
  · intro h
    have h2 := congrArg log (h 2 two_pos)
    rw [log_rpow two_pos, log_rpow two_pos] at h2
    have := mul_right_cancel₀ (log_pos one_lt_two).ne' h2
    linarith
  · rintro rfl u _
    norm_num

/-- Hölder dual of `p = γ + 1/2`: the one-bound-state bound at exponent `γ` is dual to a
Gagliardo–Nirenberg inequality in `∫ u^(2m)`. `m = 3` is Sz.-Nagy's `u⁶`, i.e. `γ = 1`. -/
noncomputable def mExp (γ : ℝ) : ℝ := (γ + 1/2) / (γ - 1/2)

theorem mExp_one : mExp 1 = 3 := by norm_num [mExp]

/-- On the conjecture's new range `(3/2, 5/2]` the exponent is `m ∈ [3/2, 2)`, never `3`. -/
theorem mExp_new_range {γ : ℝ} (h1 : 3/2 < γ) (h2 : γ ≤ 5/2) :
    3/2 ≤ mExp γ ∧ mExp γ < 2 := by
  have hpos : 0 < γ - 1/2 := by linarith
  unfold mExp
  constructor
  · rw [le_div_iff₀ hpos]; linarith
  · rw [div_lt_iff₀ hpos]; linarith

/-! ## 2. Constants and the ratio `r = L1 / Lcl` -/

/-- One-bound-state constant (d = 1); attained by `(γ² - 1/4) sech²`. -/
noncomputable def L1 (γ : ℝ) : ℝ :=
  Gamma (γ + 1) / (sqrt π * Gamma (γ + 1/2) * (γ + 1/2)) * ((γ - 1/2) / (γ + 1/2)) ^ (γ - 1/2)

/-- Semiclassical constant (d = 1). -/
noncomputable def Lcl (γ : ℝ) : ℝ := Gamma (γ + 1) / (2 * sqrt π * Gamma (γ + 3/2))

noncomputable def r (γ : ℝ) : ℝ := 2 * ((γ - 1/2) / (γ + 1/2)) ^ (γ - 1/2)

private lemma ratio_algebra {A G s a X : ℝ} (hG : G ≠ 0) (hs : s ≠ 0) (ha : a ≠ 0) :
    A / (s * G * a) * X = 2 * X * (A / (2 * s * (a * G))) := by
  rw [div_mul_eq_mul_div, ← mul_div_assoc,
    div_eq_div_iff (mul_ne_zero (mul_ne_zero hs hG) ha)
      (mul_ne_zero (mul_ne_zero two_ne_zero hs) (mul_ne_zero ha hG))]
  ring

theorem L1_eq_r_mul_Lcl {γ : ℝ} (hγ : 1/2 < γ) : L1 γ = r γ * Lcl γ := by
  have ha : 0 < γ + 1/2 := by linarith
  have hΓ : Gamma (γ + 3/2) = (γ + 1/2) * Gamma (γ + 1/2) := by
    rw [show γ + 3/2 = (γ + 1/2) + 1 by ring, Gamma_add_one ha.ne']
  unfold L1 Lcl r
  rw [hΓ]
  exact ratio_algebra (Gamma_pos_of_pos ha).ne' (sqrt_pos.mpr pi_pos).ne' ha.ne'

theorem r_three_halves : r (3/2) = 1 := by norm_num [r]

theorem r_five_halves : r (5/2) = 8/9 := by norm_num [r, rpow_two]

/-- With `t = γ - 1/2`: `r γ = 2 · exp (phi t)`. -/
noncomputable def phi (t : ℝ) : ℝ := t * (log t - log (t + 1))

theorem r_eq_exp {γ : ℝ} (hγ : 1/2 < γ) : r γ = 2 * exp (phi (γ - 1/2)) := by
  have ht : 0 < γ - 1/2 := by linarith
  have ht1 : 0 < γ - 1/2 + 1 := by linarith
  unfold r phi
  rw [show γ + 1/2 = γ - 1/2 + 1 by ring, rpow_def_of_pos (div_pos ht ht1),
    log_div ht.ne' ht1.ne']
  ring_nf

theorem phi_hasDerivAt {x : ℝ} (hx : 0 < x) :
    HasDerivAt phi (1 * (log x - log (x + 1)) + x * (x⁻¹ - 1 / (x + 1))) x := by
  have hx1 : x + 1 ≠ 0 := by positivity
  have hl1 : HasDerivAt (fun y => log (y + 1)) (1 / (x + 1)) x :=
    ((hasDerivAt_id x).add_const 1).log hx1
  exact (hasDerivAt_id x).mul ((hasDerivAt_log hx.ne').sub hl1)

theorem phi_deriv_neg {x : ℝ} (hx : 0 < x) :
    1 * (log x - log (x + 1)) + x * (x⁻¹ - 1 / (x + 1)) < 0 := by
  have hx1 : 0 < x + 1 := by linarith
  have hq1 : x / (x + 1) ≠ 1 := by
    intro h
    rw [div_eq_one_iff_eq hx1.ne'] at h
    linarith
  have key := log_lt_sub_one_of_pos (div_pos hx hx1) hq1
  rw [log_div hx.ne' hx1.ne'] at key
  have e : x * (x⁻¹ - 1 / (x + 1)) = 1 - x / (x + 1) := by
    rw [mul_sub, mul_inv_cancel₀ hx.ne', mul_one_div]
  rw [e]
  linarith

theorem phi_strictAntiOn : StrictAntiOn phi (Set.Ioi 0) := by
  apply strictAntiOn_of_deriv_neg (convex_Ioi 0)
  · intro x hx
    exact (phi_hasDerivAt hx).continuousAt.continuousWithinAt
  · intro x hx
    rw [interior_Ioi] at hx
    rw [(phi_hasDerivAt hx).deriv]
    exact phi_deriv_neg hx

/-- `r` is strictly decreasing on all of `(1/2, ∞)`. -/
theorem r_strictAntiOn : StrictAntiOn r (Set.Ioi (1/2)) := by
  intro a ha b hb hab
  have ha' : (1:ℝ)/2 < a := ha
  have hb' : (1:ℝ)/2 < b := hb
  rw [r_eq_exp ha', r_eq_exp hb']
  have h := phi_strictAntiOn (Set.mem_Ioi.mpr (by linarith : (0:ℝ) < a - 1/2))
    (Set.mem_Ioi.mpr (by linarith : (0:ℝ) < b - 1/2)) (by linarith : a - 1/2 < b - 1/2)
  have := exp_lt_exp.mpr h
  linarith

/-- Why `(3/2, 5/2]` is new: `L1 < Lcl` for `γ > 3/2`. -/
theorem r_lt_one {γ : ℝ} (hγ : 3/2 < γ) : r γ < 1 := by
  have h := r_strictAntiOn (Set.mem_Ioi.mpr (by norm_num : (1:ℝ)/2 < 3/2))
    (Set.mem_Ioi.mpr (by linarith : (1:ℝ)/2 < γ)) hγ
  rwa [r_three_halves] at h

theorem one_lt_r {γ : ℝ} (h1 : 1/2 < γ) (h2 : γ < 3/2) : 1 < r γ := by
  have h := r_strictAntiOn (Set.mem_Ioi.mpr h1)
    (Set.mem_Ioi.mpr (by norm_num : (1:ℝ)/2 < 3/2)) h2
  rwa [r_three_halves] at h

/-- `r γ > 2/e` for every `γ > 1/2`. With `2/e > 1/2` this gives `Lcl < 2·L1`:
large-coupling potentials (Neumann ratio → `Lcl`) and parts of `V` far from the boundary
(ratio `≤ L_γ = Lcl` for `γ ≥ 3/2`) can never beat the half-soliton. -/
theorem two_exp_neg_one_lt_r {γ : ℝ} (hγ : 1/2 < γ) : 2 * exp (-1) < r γ := by
  rw [r_eq_exp hγ]
  have ht : 0 < γ - 1/2 := by linarith
  set t := γ - 1/2
  have hq : (t + 1) / t ≠ 1 := by
    intro h
    rw [div_eq_one_iff_eq ht.ne'] at h
    linarith
  have key := log_lt_sub_one_of_pos (by positivity) hq
  have e : (t + 1) / t - 1 = 1 / t := by
    rw [div_sub_one ht.ne']; ring
  rw [log_div (show t + 1 ≠ 0 by positivity) ht.ne', e] at key
  have hlt : t * (log (t + 1) - log t) < 1 := by
    have := mul_lt_mul_of_pos_left key ht
    rwa [mul_one_div_cancel ht.ne'] at this
  have hphi : phi t = -(t * (log (t + 1) - log t)) := by unfold phi; ring
  have := exp_lt_exp.mpr (show -1 < phi t by rw [hphi]; linarith)
  linarith

theorem half_lt_two_exp_neg_one : (1:ℝ)/2 < 2 * exp (-1) := by
  rw [exp_neg, ← div_eq_mul_inv, lt_div_iff₀ (exp_pos 1)]
  linarith [exp_one_lt_d9]

/-- Task: closed form at `γ = 1` (Read–Schulz's constant). -/
theorem L1_one : L1 1 = 4 / (3 * sqrt 3 * π) := by
  sorry

/-- Task: closed form at `γ = 2`. -/
theorem L1_two : L1 2 = 16 / (15 * π) * (3/5 : ℝ) ^ (3/2 : ℝ) := by
  sorry

/-- Task: the earlier numerics' `0.49007`. -/
theorem two_L1_one_bounds : 0.49006 < 2 * L1 1 ∧ 2 * L1 1 < 0.49008 := by
  sorry

/-- Task: the earlier numerics' `0.31559`. -/
theorem two_L1_two_bounds : 0.31559 < 2 * L1 2 ∧ 2 * L1 2 < 0.31561 := by
  sorry

/-! ## 3. Upper bound from Exner–Laptev–Usman, CMP 326 (2014), eq. (1.6)

`e₁ = |E₁|^γ` (Neumann ground state), `S = Σ_{n≥2} |Eₙ|^γ`, `M = ∫₀^∞ V^{γ+1/2}`,
`lcl = Lcl γ`, `l1 = L1 γ`.
* `hELU`: ELU (1.6), scalar Neumann, `γ ≥ 3/2`: `½ e₁ + S ≤ lcl · M`.
* `hOne`: the Neumann ground state is the ground state of the even extension, so the sharp
  whole-line one-bound-state bound gives `e₁ ≤ l1 · ∫_ℝ = 2 · l1 · M`. -/

/-- Known bound on the new range: `L^N_γ ≤ Lcl + L1`, strictly better than `2·Lcl`. -/
theorem neumann_upper_ELU {e₁ S M lcl l1 : ℝ}
    (hELU : e₁ / 2 + S ≤ lcl * M) (hOne : e₁ ≤ 2 * l1 * M) :
    e₁ + S ≤ (lcl + l1) * M := by
  linarith

/-- A potential beating `2·L1` must nearly saturate the one-bound-state bound:
`e₁ > 2(2·l1 - lcl)·M`, i.e. `e₁ / (2·l1·M) > 2 - 1/r(γ)`. -/
theorem beating_needs_big_ground_state {e₁ S M lcl l1 : ℝ}
    (hELU : e₁ / 2 + S ≤ lcl * M) (hbeat : 2 * l1 * M < e₁ + S) :
    2 * (2 * l1 - lcl) * M < e₁ := by
  linarith

theorem threshold_five_halves : 2 - 1 / r (5/2) = 7/8 := by
  rw [r_five_halves]; norm_num

/-! ## 4. Abstract (a)–(d)

Bound states of the even extension `Ṽ(x) = V(|x|)` are indexed by `all`; the even ones
(= Neumann states) by `ev ⊆ all`; `e i = |E_i|^γ ≥ 0`; `Mhalf = ∫₀^∞ V^{γ+1/2}`. -/

/-- Mass doubling for the even extension. -/
theorem even_extension_mass (V : ℝ → ℝ) (p : ℝ) :
    ∫ x, V |x| ^ p = 2 * ∫ x in Set.Ioi 0, V x ^ p :=
  integral_comp_abs (f := fun x => V x ^ p)

/-- (a) `L^N_γ ≤ 2 L_γ`. -/
theorem fact_a {ι : Type*} (all ev : Finset ι) (hsub : ev ⊆ all) (e : ι → ℝ)
    (he : ∀ i ∈ all, 0 ≤ e i) (Lγ Mhalf : ℝ)
    (hLT : ∑ i ∈ all, e i ≤ Lγ * (2 * Mhalf)) :
    ∑ i ∈ ev, e i ≤ 2 * Lγ * Mhalf :=
  calc ∑ i ∈ ev, e i ≤ ∑ i ∈ all, e i :=
        Finset.sum_le_sum_of_subset_of_nonneg hsub (fun i hi _ => he i hi)
    _ ≤ Lγ * (2 * Mhalf) := hLT
    _ = 2 * Lγ * Mhalf := by ring

section BestConstant
variable {P : Type*} (S M : P → ℝ)

/-- `C` is an admissible constant: `S V ≤ C · M V` for every potential `V`. -/
def Admissible (C : ℝ) : Prop := ∀ V, S V ≤ C * M V

/-- (b) one test potential with `S V₀ ≥ c · M V₀` and `M V₀ > 0` forces every admissible
`C ≥ c`. -/
theorem fact_b {C c : ℝ} (hC : Admissible S M C) (V₀ : P) (hM : 0 < M V₀)
    (hV₀ : c * M V₀ ≤ S V₀) : c ≤ C :=
  le_of_mul_le_mul_right (hV₀.trans (hC V₀)) hM

/-- (c) the squeeze. -/
theorem fact_c {LN l1 : ℝ} (hbest : IsLeast {C | Admissible S M C} LN)
    (hup : Admissible S M (2 * l1)) (V₀ : P) (hM : 0 < M V₀)
    (hV₀ : 2 * l1 * M V₀ ≤ S V₀) : LN = 2 * l1 :=
  le_antisymm (hbest.2 hup) (fact_b S M hbest.1 V₀ hM hV₀)

/-- (d) an extra positive contribution makes the bound strict. -/
theorem fact_d {C l1 δ : ℝ} (hC : Admissible S M C) (V₀ : P) (hM : 0 < M V₀)
    (hδ : 0 < δ) (hV₀ : S V₀ = 2 * l1 * M V₀ + δ) : 2 * l1 < C := by
  by_contra hcon
  have h1 := hC V₀
  have h2 : C * M V₀ ≤ 2 * l1 * M V₀ := mul_le_mul_of_nonneg_right (not_lt.mp hcon) hM.le
  linarith

end BestConstant

/-! ## 5. Pöschl–Teller facts behind (b) and (d)

`ν(ν+1) sech²` has bound states `E_k = -(ν-k)²` (`k < ν`) with parity `(-1)^k`. -/

theorem pt_coupling (γ : ℝ) : (γ - 1/2) * (γ - 1/2 + 1) = γ^2 - 1/4 := by ring

theorem k2_bound_iff (γ : ℝ) : 2 < γ - 1/2 ↔ 5/2 < γ := by
  constructor <;> intro h <;> linarith

/-- Even Pöschl–Teller eigenfunction `ψ₀ = sech^ν`. -/
noncomputable def psi0 (ν y : ℝ) : ℝ := cosh y ^ (-ν)

/-- Even Pöschl–Teller eigenfunction `ψ₂ = sech^(ν-2) ((2ν-1) tanh² - 1)`. -/
noncomputable def psi2 (ν y : ℝ) : ℝ := cosh y ^ (2 - ν) * ((2*ν - 1) * tanh y ^ 2 - 1)

/-- Task: `-ψ₀'' - ν(ν+1) sech² ψ₀ = -ν² ψ₀`. -/
theorem pt_ground_state (ν x : ℝ) :
    -deriv (deriv (psi0 ν)) x - ν * (ν + 1) / cosh x ^ 2 * psi0 ν x = -ν^2 * psi0 ν x := by
  sorry

/-- Task: `-ψ₂'' - ν(ν+1) sech² ψ₂ = -(ν-2)² ψ₂`. -/
theorem pt_second_even_state (ν x : ℝ) :
    -deriv (deriv (psi2 ν)) x - ν * (ν + 1) / cosh x ^ 2 * psi2 ν x
      = -(ν - 2)^2 * psi2 ν x := by
  sorry

/-- Task: `ψ₂ ∈ L²(0, ∞)` when `ν > 2`, so `-(ν-2)²` is a genuine Neumann eigenvalue. -/
theorem pt_second_even_state_sq_integrable {ν : ℝ} (hν : 2 < ν) :
    MeasureTheory.IntegrableOn (fun x => psi2 ν x ^ 2) (Set.Ioi 0) := by
  sorry

/-- Task: within the one-state sech² family, `ν = a = γ - 1/2` is optimal (weighted AM–GM,
`Real.geom_mean_le_arith_mean2_weighted` with weights `a/(a+1)`, `1/(a+1)`). -/
theorem sech2_family_opt {a ν : ℝ} (ha : 0 < a) (hν : 0 < ν) :
    ν ^ a / (ν + 1) ^ (a + 1) ≤ a ^ a / (a + 1) ^ (a + 1) := by
  sorry

/-! ## 6. The earlier numerics, exactly

γ = 3 (ν = 5/2): Neumann levels −25/4, −1/4; the soliton's k = 2 level multiplies its ratio by
`1 + (1/25)³`. γ = 5 (ν = 9/2): levels −81/4, −25/4, −1/4; factor `1 + (25/81)⁵ + (1/81)⁵`. -/

theorem soliton_bonus_gamma3 : ((1/4 : ℝ) / (25/4)) ^ 3 = 64 / 10^6 := by norm_num

theorem soliton_bonus_gamma5 :
    (28/10^4 : ℝ) < ((25/4 : ℝ) / (81/4)) ^ 5 + ((1/4 : ℝ) / (81/4)) ^ 5 ∧
    ((25/4 : ℝ) / (81/4)) ^ 5 + ((1/4 : ℝ) / (81/4)) ^ 5 < 281/10^5 := by
  norm_num

end HalflineLt
