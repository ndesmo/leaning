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

/-- Closed form at `γ = 1` (Read–Schulz's constant). -/
theorem L1_one : L1 1 = 4 / (3 * sqrt 3 * π) := by
  have hG32 : Gamma (1 + 1 / 2) = sqrt π / 2 := by
    rw [show (1:ℝ) + 1 / 2 = 1 / 2 + 1 by norm_num, Gamma_add_one (s := 1 / 2) (by norm_num),
      Gamma_one_half_eq]
    ring
  have hroot : (((1:ℝ) - 1 / 2) / (1 + 1 / 2)) ^ ((1:ℝ) - 1 / 2) = 1 / sqrt 3 := by
    rw [show ((1:ℝ) - 1 / 2) / (1 + 1 / 2) = 3⁻¹ by norm_num,
      show (1:ℝ) - 1 / 2 = 1 / 2 by norm_num, ← sqrt_eq_rpow, sqrt_inv, one_div]
  have h3 : sqrt (3:ℝ) ≠ 0 := by positivity
  have hpi : sqrt π ≠ 0 := (sqrt_pos.mpr pi_pos).ne'
  unfold L1
  rw [one_add_one_eq_two, Gamma_two, hG32, hroot]
  conv_rhs => rw [← mul_self_sqrt pi_pos.le]
  field_simp
  ring

/-- Closed form at `γ = 2`. -/
theorem L1_two : L1 2 = 16 / (15 * π) * (3/5 : ℝ) ^ (3/2 : ℝ) := by
  have hG3 : Gamma (2 + 1) = 2 := by
    rw [Gamma_add_one (s := 2) (by norm_num), Gamma_two]; norm_num
  have hG52 : Gamma (2 + 1 / 2) = 3 / 4 * sqrt π := by
    rw [show (2:ℝ) + 1 / 2 = (1 / 2 + 1) + 1 by norm_num,
      Gamma_add_one (s := 1 / 2 + 1) (by norm_num), Gamma_add_one (s := 1 / 2) (by norm_num),
      Gamma_one_half_eq]
    ring
  have hbase : ((2:ℝ) - 1 / 2) / (2 + 1 / 2) = 3 / 5 := by norm_num
  have hexp : (2:ℝ) - 1 / 2 = 3 / 2 := by norm_num
  have hpi : sqrt π ≠ 0 := (sqrt_pos.mpr pi_pos).ne'
  unfold L1
  rw [hG3, hG52, hbase, hexp]
  conv_rhs => rw [← mul_self_sqrt pi_pos.le]
  field_simp
  ring

/-- The earlier numerics' `0.49007`. -/
theorem two_L1_one_bounds : 0.49006 < 2 * L1 1 ∧ 2 * L1 1 < 0.49008 := by
  have hs1 : (1.7320508 : ℝ) < sqrt 3 := by rw [lt_sqrt (by norm_num)]; norm_num
  have hs2 : sqrt 3 < (1.7320509 : ℝ) := by rw [sqrt_lt' (by norm_num)]; norm_num
  have hlo : (1.7320508 : ℝ) * 3.141592 < sqrt 3 * π :=
    mul_lt_mul'' hs1 pi_gt_d6 (by norm_num) (by norm_num)
  have hhi : sqrt 3 * π < (1.7320509 : ℝ) * 3.141593 :=
    mul_lt_mul'' hs2 pi_lt_d6 (sqrt_nonneg 3) pi_pos.le
  have hpos : 0 < 3 * (sqrt 3 * π) := by positivity
  rw [L1_one, show 2 * (4 / (3 * sqrt 3 * π)) = 8 / (3 * (sqrt 3 * π)) by ring]
  constructor
  · rw [lt_div_iff₀ hpos]; linarith
  · rw [div_lt_iff₀ hpos]; linarith

/-- The earlier numerics' `0.31559`. -/
theorem two_L1_two_bounds : 0.31559 < 2 * L1 2 ∧ 2 * L1 2 < 0.31561 := by
  have hr : (3/5 : ℝ) ^ (3/2 : ℝ) = 3/5 * sqrt (3/5) := by
    rw [show (3/2 : ℝ) = 1 + 1/2 by norm_num, rpow_add (by norm_num), rpow_one, ← sqrt_eq_rpow]
  have hq1 : (0.7745966 : ℝ) < sqrt (3/5) := by rw [lt_sqrt (by norm_num)]; norm_num
  have hq2 : sqrt (3/5) < (0.7745967 : ℝ) := by rw [sqrt_lt' (by norm_num)]; norm_num
  have hpos : 0 < 25 * π := by positivity
  rw [L1_two, hr,
    show 2 * (16 / (15 * π) * (3/5 * sqrt (3/5))) = 32 * sqrt (3/5) / (25 * π) by ring]
  constructor
  · rw [lt_div_iff₀ hpos]; linarith [pi_lt_d6]
  · rw [div_lt_iff₀ hpos]; linarith [pi_gt_d6]

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

theorem psi0_hasDerivAt (ν y : ℝ) :
    HasDerivAt (psi0 ν) (sinh y * (-ν) * cosh y ^ (-ν - 1)) y :=
  (hasDerivAt_cosh y).rpow_const (Or.inl (cosh_pos y).ne')

theorem deriv_psi0 (ν : ℝ) : deriv (psi0 ν) = fun y => sinh y * (-ν) * cosh y ^ (-ν - 1) :=
  funext fun y => (psi0_hasDerivAt ν y).deriv

theorem dpsi0_hasDerivAt (ν y : ℝ) :
    HasDerivAt (fun y => sinh y * (-ν) * cosh y ^ (-ν - 1))
      (cosh y * (-ν) * cosh y ^ (-ν - 1) +
        sinh y * (-ν) * (sinh y * (-ν - 1) * cosh y ^ (-ν - 1 - 1))) y :=
  ((hasDerivAt_sinh y).mul_const (-ν)).mul
    ((hasDerivAt_cosh y).rpow_const (p := -ν - 1) (Or.inl (cosh_pos y).ne'))

/-- `ψ₀ = sech^ν` solves `-ψ'' - ν(ν+1) sech² ψ = -ν² ψ`. -/
theorem pt_ground_state (ν x : ℝ) :
    -deriv (deriv (psi0 ν)) x - ν * (ν + 1) / cosh x ^ 2 * psi0 ν x = -ν^2 * psi0 ν x := by
  have hc : cosh x ≠ 0 := (cosh_pos x).ne'
  have h1 : cosh x ^ (-ν - 1) = cosh x ^ (-ν) / cosh x := rpow_sub_one hc (-ν)
  have h2 : cosh x ^ (-ν - 1 - 1) = cosh x ^ (-ν) / cosh x / cosh x := by
    rw [rpow_sub_one hc, h1]
  have hs : sinh x ^ 2 = cosh x ^ 2 - 1 := by rw [cosh_sq]; ring
  rw [deriv_psi0, (dpsi0_hasDerivAt ν x).deriv, h1, h2]
  unfold psi0
  have key : sinh x * (-ν) * (sinh x * (-ν - 1) * (cosh x ^ (-ν) / cosh x / cosh x)) =
      ν * (ν + 1) * cosh x ^ (-ν) * sinh x ^ 2 / cosh x ^ 2 := by ring
  rw [key, hs]
  field_simp
  ring

/-- `ψ₂ = ψ₀ · (2(ν-1) sinh² - 1)`. -/
theorem psi2_eq (ν : ℝ) :
    psi2 ν = fun y => psi0 ν y * (2 * (ν - 1) * (sinh y * sinh y) - 1) := by
  funext y
  have hc : 0 < cosh y := cosh_pos y
  have hc' : cosh y ≠ 0 := hc.ne'
  have e1 : cosh y ^ (2 - ν) = cosh y ^ 2 * cosh y ^ (-ν) := by
    rw [show (2:ℝ) - ν = 2 + -ν by ring, rpow_add hc, rpow_two]
  have e2 : cosh y ^ 2 * ((2 * ν - 1) * (sinh y / cosh y) ^ 2 - 1) =
      (2 * ν - 1) * sinh y ^ 2 - cosh y ^ 2 := by
    field_simp
  unfold psi2 psi0
  rw [e1, tanh_eq_sinh_div_cosh]
  calc cosh y ^ 2 * cosh y ^ (-ν) * ((2 * ν - 1) * (sinh y / cosh y) ^ 2 - 1)
      = cosh y ^ (-ν) * (cosh y ^ 2 * ((2 * ν - 1) * (sinh y / cosh y) ^ 2 - 1)) := by ring
    _ = cosh y ^ (-ν) * ((2 * ν - 1) * sinh y ^ 2 - cosh y ^ 2) := by rw [e2]
    _ = cosh y ^ (-ν) * (2 * (ν - 1) * (sinh y * sinh y) - 1) := by rw [cosh_sq]; ring

theorem hasDerivAt_q (ν y : ℝ) :
    HasDerivAt (fun y => 2 * (ν - 1) * (sinh y * sinh y) - 1)
      (2 * (ν - 1) * (cosh y * sinh y + sinh y * cosh y)) y :=
  (((hasDerivAt_sinh y).mul (hasDerivAt_sinh y)).const_mul (2 * (ν - 1))).sub_const 1

theorem hasDerivAt_dq (ν y : ℝ) :
    HasDerivAt (fun y => 2 * (ν - 1) * (cosh y * sinh y + sinh y * cosh y))
      (2 * (ν - 1) * (sinh y * sinh y + cosh y * cosh y + (cosh y * cosh y + sinh y * sinh y)))
      y :=
  (((hasDerivAt_cosh y).mul (hasDerivAt_sinh y)).add
    ((hasDerivAt_sinh y).mul (hasDerivAt_cosh y))).const_mul (2 * (ν - 1))

theorem psi2_hasDerivAt (ν y : ℝ) :
    HasDerivAt (psi2 ν)
      (sinh y * (-ν) * cosh y ^ (-ν - 1) * (2 * (ν - 1) * (sinh y * sinh y) - 1) +
        cosh y ^ (-ν) * (2 * (ν - 1) * (cosh y * sinh y + sinh y * cosh y))) y := by
  rw [psi2_eq]
  exact (psi0_hasDerivAt ν y).mul (hasDerivAt_q ν y)

theorem deriv_psi2 (ν : ℝ) : deriv (psi2 ν) = fun y =>
    sinh y * (-ν) * cosh y ^ (-ν - 1) * (2 * (ν - 1) * (sinh y * sinh y) - 1) +
      cosh y ^ (-ν) * (2 * (ν - 1) * (cosh y * sinh y + sinh y * cosh y)) :=
  funext fun y => (psi2_hasDerivAt ν y).deriv

theorem deriv2_psi2 (ν y : ℝ) : deriv (deriv (psi2 ν)) y =
    (cosh y * (-ν) * cosh y ^ (-ν - 1) +
        sinh y * (-ν) * (sinh y * (-ν - 1) * cosh y ^ (-ν - 1 - 1))) *
          (2 * (ν - 1) * (sinh y * sinh y) - 1) +
      sinh y * (-ν) * cosh y ^ (-ν - 1) * (2 * (ν - 1) * (cosh y * sinh y + sinh y * cosh y)) +
    (sinh y * (-ν) * cosh y ^ (-ν - 1) * (2 * (ν - 1) * (cosh y * sinh y + sinh y * cosh y)) +
      cosh y ^ (-ν) * (2 * (ν - 1) *
        (sinh y * sinh y + cosh y * cosh y + (cosh y * cosh y + sinh y * sinh y)))) := by
  rw [deriv_psi2]
  exact (((dpsi0_hasDerivAt ν y).mul (hasDerivAt_q ν y)).add
    ((psi0_hasDerivAt ν y).mul (hasDerivAt_dq ν y))).deriv

/-- `ψ₂` solves `-ψ'' - ν(ν+1) sech² ψ = -(ν-2)² ψ`. With `B = cosh^(-ν-2)` every term is a
polynomial in `sinh`, `cosh`, `B`, and the identity holds modulo `cosh² = sinh² + 1`. -/
theorem pt_second_even_state (ν x : ℝ) :
    -deriv (deriv (psi2 ν)) x - ν * (ν + 1) / cosh x ^ 2 * psi2 ν x
      = -(ν - 2)^2 * psi2 ν x := by
  have hc : cosh x ≠ 0 := (cosh_pos x).ne'
  have hA1 : cosh x ^ (-ν - 1) = cosh x * cosh x ^ (-ν - 2) := by
    have e : cosh x ^ (-ν - 1) = cosh x ^ ((-ν - 2) + 1) := by ring_nf
    rw [e, rpow_add_one hc]; ring
  have hA2 : cosh x ^ (-ν - 1 - 1) = cosh x ^ (-ν - 2) := by ring_nf
  have hA : cosh x ^ (-ν) = cosh x ^ 2 * cosh x ^ (-ν - 2) := by
    have e : cosh x ^ (-ν) = cosh x ^ ((-ν - 2) + 1 + 1) := by ring_nf
    rw [e, rpow_add_one hc, rpow_add_one hc]; ring
  rw [deriv2_psi2, psi2_eq]
  simp only [psi0]
  rw [hA2, hA1, hA]
  have hV : ν * (ν + 1) / cosh x ^ 2 *
      (cosh x ^ 2 * cosh x ^ (-ν - 2) * (2 * (ν - 1) * (sinh x * sinh x) - 1)) =
      ν * (ν + 1) * cosh x ^ (-ν - 2) * (2 * (ν - 1) * (sinh x * sinh x) - 1) := by
    rw [div_mul_eq_mul_div, div_eq_iff (pow_ne_zero 2 hc)]; ring
  rw [hV]
  linear_combination (cosh x ^ (-ν - 2) *
    (ν * (ν + 1) * (2 * (ν - 1) * (sinh x * sinh x) - 1) - 4 * (ν - 1) * cosh x ^ 2)) *
      cosh_sq x

/-- `ψ₂ ∈ L²(0, ∞)` when `ν > 2`, so `-(ν-2)²` is a genuine Neumann eigenvalue: `ψ₂²` is
dominated by `(2ν-1)² 4^ν e^{-(2ν-4)x}`. -/
theorem pt_second_even_state_sq_integrable {ν : ℝ} (hν : 2 < ν) :
    MeasureTheory.IntegrableOn (fun x => psi2 ν x ^ 2) (Set.Ioi 0) := by
  have hb : 0 < 2 * ν - 4 := by linarith
  have hint : MeasureTheory.IntegrableOn
      (fun x => (2 * ν - 1) ^ 2 * exp (2 * ν * log 2) * exp (-(2 * ν - 4) * x)) (Set.Ioi 0) :=
    MeasureTheory.Integrable.const_mul (exp_neg_integrableOn_Ioi 0 hb) _
  have hcont : Continuous fun x => psi2 ν x ^ 2 := by
    have hA : Continuous fun y => cosh y ^ (-ν) :=
      continuous_cosh.rpow_const fun y => Or.inl (cosh_pos y).ne'
    simp only [psi2_eq, psi0]
    fun_prop
  refine MeasureTheory.Integrable.mono' hint hcont.aestronglyMeasurable ?_
  refine (MeasureTheory.ae_restrict_iff' measurableSet_Ioi).mpr
    (MeasureTheory.ae_of_all _ fun x hx => ?_)
  have hx' : 0 < x := hx
  have hC : 0 < cosh x := cosh_pos x
  have hCx : cosh x ≤ exp x := by
    rw [cosh_eq]; linarith [exp_le_exp.mpr (show -x ≤ x by linarith)]
  have hlog : x - log 2 ≤ log (cosh x) := by
    have h2 : exp x / 2 ≤ cosh x := by rw [cosh_eq]; linarith [exp_pos (-x)]
    have := log_le_log (by positivity) h2
    rwa [log_div (exp_pos x).ne' two_ne_zero, log_exp] at this
  have hA2 : (cosh x ^ (-ν)) ^ 2 ≤ exp (-(2 * ν) * (x - log 2)) := by
    rw [rpow_def_of_pos hC, ← exp_natCast_mul]
    apply exp_le_exp.mpr
    push_cast
    nlinarith [mul_le_mul_of_nonneg_left hlog (by linarith : (0:ℝ) ≤ 2 * ν)]
  have hS : sinh x * sinh x ≤ cosh x ^ 2 := by rw [cosh_sq]; nlinarith
  have hC1 : 1 ≤ cosh x ^ 2 := by rw [cosh_sq]; nlinarith [sq_nonneg (sinh x)]
  have hq : (2 * (ν - 1) * (sinh x * sinh x) - 1) ^ 2 ≤ ((2 * ν - 1) * cosh x ^ 2) ^ 2 := by
    have hn : 0 ≤ (ν - 1) * (cosh x ^ 2 - sinh x * sinh x) :=
      mul_nonneg (by linarith) (by linarith)
    apply sq_le_sq'
    · nlinarith [mul_self_nonneg (sinh x)]
    · nlinarith [mul_self_nonneg (sinh x)]
  have hC4 : (cosh x ^ 2) ^ 2 ≤ exp (4 * x) := by
    calc (cosh x ^ 2) ^ 2 = cosh x ^ 4 := by ring
      _ ≤ exp x ^ 4 := pow_le_pow_left₀ hC.le hCx 4
      _ = exp (4 * x) := by rw [← exp_natCast_mul]; norm_num
  have hexp : exp (-(2 * ν) * (x - log 2)) * exp (4 * x) =
      exp (2 * ν * log 2) * exp (-(2 * ν - 4) * x) := by
    rw [← exp_add, ← exp_add]; congr 1; ring
  show ‖psi2 ν x ^ 2‖ ≤ (2 * ν - 1) ^ 2 * exp (2 * ν * log 2) * exp (-(2 * ν - 4) * x)
  rw [Real.norm_eq_abs, abs_of_nonneg (sq_nonneg _), psi2_eq]
  simp only [psi0]
  calc (cosh x ^ (-ν) * (2 * (ν - 1) * (sinh x * sinh x) - 1)) ^ 2
      = (cosh x ^ (-ν)) ^ 2 * (2 * (ν - 1) * (sinh x * sinh x) - 1) ^ 2 := by ring
    _ ≤ exp (-(2 * ν) * (x - log 2)) * ((2 * ν - 1) ^ 2 * exp (4 * x)) := by
        apply mul_le_mul hA2 _ (sq_nonneg _) (exp_pos _).le
        calc _ ≤ ((2 * ν - 1) * cosh x ^ 2) ^ 2 := hq
          _ = (2 * ν - 1) ^ 2 * (cosh x ^ 2) ^ 2 := by ring
          _ ≤ (2 * ν - 1) ^ 2 * exp (4 * x) := by gcongr
    _ = (2 * ν - 1) ^ 2 * exp (2 * ν * log 2) * exp (-(2 * ν - 4) * x) := by
        rw [mul_assoc ((2 * ν - 1) ^ 2), ← hexp]; ring

/-- Within the one-state sech² family, `ν = a = γ - 1/2` is optimal (weighted AM–GM with
weights `a/(a+1)`, `1/(a+1)`). -/
theorem sech2_family_opt {a ν : ℝ} (ha : 0 < a) (hν : 0 < ν) :
    ν ^ a / (ν + 1) ^ (a + 1) ≤ a ^ a / (a + 1) ^ (a + 1) := by
  have ha1 : 0 < a + 1 := by linarith
  have ha1' : a + 1 ≠ 0 := ha1.ne'
  have hw := geom_mean_le_arith_mean2_weighted (w₁ := a / (a + 1)) (w₂ := 1 / (a + 1))
    (p₁ := ν / a) (p₂ := 1) (by positivity) (by positivity) (by positivity) (by norm_num)
    (by field_simp)
  rw [one_rpow, mul_one,
    show a / (a + 1) * (ν / a) + 1 / (a + 1) * 1 = (ν + 1) / (a + 1) by field_simp] at hw
  have hpow := rpow_le_rpow (by positivity) hw ha1.le
  rw [← rpow_mul (by positivity), div_mul_cancel₀ a ha1', div_rpow hν.le ha.le,
    div_rpow (by positivity) ha1.le] at hpow
  rw [div_le_div_iff₀ (by positivity) (by positivity)] at hpow ⊢
  linarith

/-! ## 6. The earlier numerics, exactly

γ = 3 (ν = 5/2): Neumann levels −25/4, −1/4; the soliton's k = 2 level multiplies its ratio by
`1 + (1/25)³`. γ = 5 (ν = 9/2): levels −81/4, −25/4, −1/4; factor `1 + (25/81)⁵ + (1/81)⁵`. -/

theorem soliton_bonus_gamma3 : ((1/4 : ℝ) / (25/4)) ^ 3 = 64 / 10^6 := by norm_num

theorem soliton_bonus_gamma5 :
    (28/10^4 : ℝ) < ((25/4 : ℝ) / (81/4)) ^ 5 + ((1/4 : ℝ) / (81/4)) ^ 5 ∧
    ((25/4 : ℝ) / (81/4)) ^ 5 + ((1/4 : ℝ) / (81/4)) ^ 5 < 281/10^5 := by
  norm_num

/-! ## 7. Task 5: the endpoint γ = 3/2 and the approach from above

Self-contained pieces of the argument in `NOTES.md` (Task 5). Spectral and scattering facts
enter as hypotheses. -/

/-- Uniqueness skeleton at `γ = 3/2`. For the even extension the trace formula reads
`S_even + S_odd + T = (3/16) · 2M`, where the Dirichlet sum `S_odd` and the scattering term `T`
are `≥ 0`. If the Neumann sum attains `(3/8) M`, both vanish: the extension is reflectionless
with no odd bound states. -/
theorem uniqueness_skeleton {Se So T M : ℝ} (htrace : Se + So + T = 3 / 16 * (2 * M))
    (hSo : 0 ≤ So) (hT : 0 ≤ T) (heq : Se = 3 / 8 * M) : So = 0 ∧ T = 0 := by
  constructor <;> linarith

/-- A potential with a single Neumann bound state satisfies the conjectured bound: its sum is
`|E₁|^γ`, which the one-bound-state bound controls. -/
theorem single_state_ok {ι : Type*} (ev : Finset ι) (e : ι → ℝ) (i₀ : ι) (hev : ev = {i₀})
    {l1 M : ℝ} (hOne : e i₀ ≤ 2 * l1 * M) : ∑ i ∈ ev, e i ≤ 2 * l1 * M := by
  rw [hev, Finset.sum_singleton]; exact hOne

theorem continuousOn_r : ContinuousOn r (Set.Ioi (1/2)) := by
  have hphi : ContinuousOn phi (Set.Ioi 0) :=
    fun x hx => (phi_hasDerivAt hx).continuousAt.continuousWithinAt
  have hsub : ContinuousOn (fun γ : ℝ => γ - 1/2) (Set.Ioi (1/2)) :=
    (continuous_id.sub continuous_const).continuousOn
  have hmaps : Set.MapsTo (fun γ : ℝ => γ - 1/2) (Set.Ioi (1/2)) (Set.Ioi 0) := by
    intro γ hγ
    have : (1:ℝ)/2 < γ := hγ
    show (0:ℝ) < γ - 1/2
    linarith
  have h : ContinuousOn (fun γ => 2 * exp (phi (γ - 1/2))) (Set.Ioi (1/2)) :=
    continuousOn_const.mul (continuous_exp.comp_continuousOn (hphi.comp hsub hmaps))
  exact h.congr fun γ hγ => r_eq_exp hγ

/-- The counterexample threshold `2 - 1/r(γ)` tends to `1` as `γ ↓ 3/2`. -/
theorem threshold_tendsto_one :
    Filter.Tendsto (fun γ => 2 - 1 / r γ) (nhdsWithin (3/2) (Set.Ioi (3/2))) (nhds 1) := by
  have hc : ContinuousAt r (3/2) :=
    continuousOn_r.continuousAt (Ioi_mem_nhds (by norm_num))
  have hr0 : r (3/2) ≠ 0 := by rw [r_three_halves]; norm_num
  have h : ContinuousAt (fun γ => 2 - 1 / r γ) (3/2) :=
    continuousAt_const.sub (continuousAt_const.div hc hr0)
  have hv : (2:ℝ) - 1 / r (3/2) = 1 := by rw [r_three_halves]; norm_num
  exact (h.tendsto.mono_left nhdsWithin_le_nhds).mono_right (le_of_eq (congrArg nhds hv))

/-- Step 2 of the near-3/2 argument: for γ close enough to `3/2` from above, any potential
beating `2·L1` has ground-state efficiency above `1 - η` (with
`beating_needs_big_ground_state`). -/
theorem threshold_eventually_gt (η : ℝ) (hη : 0 < η) :
    ∀ᶠ γ in nhdsWithin (3/2) (Set.Ioi (3/2)), 1 - η < 2 - 1 / r γ :=
  threshold_tendsto_one.eventually (lt_mem_nhds (by linarith))

/-- Localization bookkeeping for Step 5: the near part is bounded with the one-bound-state
constant, the far part with the whole-line constant `lcl`, and the two masses overlap by at most
`η`. Far mass is paid for at the rate `2·l1 - lcl`, which is `> 0` by `two_exp_neg_one_lt_r`. -/
theorem localization_bookkeeping {S Sn Sf M Mn Mf l1 lcl η : ℝ} (hl1 : 0 ≤ l1)
    (hS : S ≤ Sn + Sf) (hn : Sn ≤ 2 * l1 * Mn) (hf : Sf ≤ lcl * Mf) (hM : Mn + Mf ≤ M + η) :
    S ≤ 2 * l1 * M + 2 * l1 * η - (2 * l1 - lcl) * Mf := by
  nlinarith [mul_le_mul_of_nonneg_left hM (by linarith : (0:ℝ) ≤ 2 * l1)]

/-- At `ν = 2` (γ = 5/2) the even zero-energy solution `ψ₂ = 3 tanh² - 1` is bounded but does not
decay: the even sector is resonant, which is why (d) starts exactly at γ = 5/2. -/
theorem resonance_at_five_halves :
    (∀ x, -deriv (deriv (psi2 2)) x - 2 * (2 + 1) / cosh x ^ 2 * psi2 2 x = 0) ∧
      ∀ x, |psi2 2 x| ≤ 2 := by
  refine ⟨fun x => by simpa using pt_second_even_state 2 x, fun x => ?_⟩
  have ht := abs_tanh_lt_one x
  have h2 : tanh x ^ 2 < 1 := by nlinarith [abs_nonneg (tanh x), sq_abs (tanh x)]
  have h0 : 0 ≤ tanh x ^ 2 := sq_nonneg _
  unfold psi2
  rw [show (2:ℝ) - 2 = 0 by norm_num, rpow_zero, one_mul, abs_le]
  constructor <;> nlinarith

/-- Superadditivity of `t ↦ t^p` on `[0, ∞)` for `p ≥ 1` (Mathlib has it for `ℝ≥0`). -/
theorem real_add_rpow_le {p : ℝ} (hp : 1 ≤ p) {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) :
    a ^ p + b ^ p ≤ (a + b) ^ p := by
  lift a to NNReal using ha
  lift b to NNReal using hb
  exact_mod_cast NNReal.add_rpow_le_rpow_add a b hp

/-- Tangent-line bound for `t ↦ t^p`, `p ≥ 2`: `a^p + p a^{p-1} b + b^p ≤ (a + b)^p`. Integrated
with `a = V_sol`, `b = W ≥ 0`, it says that adding `W` to the soliton raises the mass by at least
the first-order term `p ∫ V_sol^{p-1} W` plus the full self-mass `∫ W^p`. The first-order term is
exactly what the ground state can gain (Euler–Lagrange at the soliton), so the self-mass of a
distant tail stays available to pay for its bound states. -/
theorem add_rpow_ge_tangent {p : ℝ} (hp : 2 ≤ p) {a b : ℝ} (ha : 0 ≤ a) (hb : 0 ≤ b) :
    a ^ p + p * a ^ (p - 1) * b + b ^ p ≤ (a + b) ^ p := by
  have hp0 : 0 < p := by linarith
  let f : ℝ → ℝ := fun t => (a + t) ^ p - a ^ p - p * a ^ (p - 1) * t - t ^ p
  have hderiv : ∀ t, 0 < t →
      HasDerivAt f (1 * p * (a + t) ^ (p - 1) - p * a ^ (p - 1) * 1 - p * t ^ (p - 1)) t := by
    intro t ht
    exact (((((hasDerivAt_id t).const_add a).rpow_const
      (Or.inl (add_pos_of_nonneg_of_pos ha ht).ne')).sub_const (a ^ p)).sub
      ((hasDerivAt_id t).const_mul (p * a ^ (p - 1)))).sub
      (hasDerivAt_rpow_const (Or.inl ht.ne'))
  have e0 : Continuous fun t : ℝ => a + t := continuous_const.add continuous_id
  have e1 : Continuous fun t : ℝ => (a + t) ^ p := e0.rpow_const fun _ => Or.inr hp0.le
  have e2 : Continuous fun t : ℝ => t ^ p := continuous_id.rpow_const fun _ => Or.inr hp0.le
  have e3 : Continuous fun t : ℝ => p * a ^ (p - 1) * t := continuous_const.mul continuous_id
  have hcont : Continuous f := ((e1.sub continuous_const).sub e3).sub e2
  have hmono : MonotoneOn f (Set.Ici 0) := by
    apply monotoneOn_of_deriv_nonneg (convex_Ici 0) hcont.continuousOn
    · rw [interior_Ici]
      exact fun t ht => (hderiv t ht).differentiableAt.differentiableWithinAt
    · rw [interior_Ici]
      intro t ht
      rw [(hderiv t ht).deriv]
      have h := real_add_rpow_le (show 1 ≤ p - 1 by linarith) ha (le_of_lt ht)
      nlinarith [mul_le_mul_of_nonneg_left h hp0.le]
  have h0 : f 0 = 0 := by
    simp only [f, add_zero, mul_zero, zero_rpow hp0.ne', sub_self]
  have hb' := hmono (Set.mem_Ici.mpr le_rfl) (Set.mem_Ici.mpr hb) hb
  rw [h0] at hb'
  simp only [f] at hb'
  linarith

end HalflineLt
