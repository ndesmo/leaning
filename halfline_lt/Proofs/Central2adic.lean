import Mathlib

/-!
# The 2-adic valuation of central coefficients of `(1 + x + ⋯ + x^(q-1))ⁿ`, `q = 2^r`

Notes: `notes/central-2adic.md` (issue #22, Lean unit #66). Target: the conjecture in OEIS
A402341 ("for even n, the 2-adic valuation of a(n) equals A000120(15*n/2)") and its
generalization to every `q = 2^r`, proved in the notes' Attack, S0–S5.

**Progress note (2026-11-27).** Complete: `central_2adic` (the Theorem of the notes' Attack, all
`r ≥ 1`, all even `n`) and `a402341_conjecture` (its `q = 16` case) are proved, with no `sorry`.
Nothing left for issue #66. The hypothesis `1 ≤ r` is kept because the notes state it; the proof
does not use it (for `r = 0` both sides are `0`).

Method (a reorganisation of the notes' S0–S5 that is easier to formalize; the mathematics
is the same). Write `s₂` for the binary digit sum.
* `G 0 = 1`, `G (j+1) = G j ^ 2 - 2 W^(2^j)` in `ℤ[W]`: `G j` is the reversed polynomial of
  `g_j(u) = 2 T_{2^j}(u/2)` in `w = u⁻²` (`g_0 = u`), so `F r = ∏_{j<r} G j` is the reversed
  polynomial of `f = u g_1 ⋯ g_{r-1}`, and `c(n, (q-1)n - 2t) = [w^t] (F r)ⁿ`.
* S0 (u-form) becomes a ring-hom identity in `ℤ⟦X⟧`: with `B = 1 + X` (a unit) and
  `z = X B⁻²`, `B^(2^j) G_j(z) = 1 + X^(2^j)` (`G_eval`), hence
  `B^(2^r - 1) F_r(z) = 1 + X + ⋯ + X^(2^r - 1)` (`F_eval`), and
  `[X^N] B^(2N) S(z) = ∑_{t ≤ N} [w^t]S · C(2(N-t), N-t)` (`coeff_extract`).
* S1–S4 become a divisibility property of coefficients. `WG R`: `2^(s₂ t) ∣ [w^t] R` for all
  `t`; `SG R`: `2^(s₂ t + 1) ∣ [w^t] R` for all `t ≥ 1`. `WG` and `SG` are closed under
  products (subadditivity of `s₂`), `WG R → SG (R^2)` (`WG.sq`), and `WG (G j)` by induction
  on `j`. So for even `n = 2m`, `(F r)ⁿ = ((F r)²)^m` satisfies `SG`; this replaces the
  multiset grouping of S3 (the factor 2 in S3 case B, m = 1, comes from squaring).
* S5: the `t = 0` term is `C(2N, N)`, of valuation exactly `s₂ N` (Kummer); every other term is
  divisible by `2^(s₂ N + 1)`.
-/

namespace Central2adic

open Polynomial

/-- Binary digit sum (OEIS A000120). -/
abbrev s₂ (n : ℕ) : ℕ := (Nat.digits 2 n).sum

/-! ### Digit sums -/

lemma s₂_add_le (a b : ℕ) : s₂ (a + b) ≤ s₂ a + s₂ b := by
  have hp : Nat.Prime 2 := Nat.prime_two
  have : Fact (Nat.Prime 2) := ⟨hp⟩
  have ha := Nat.Prime.sub_one_mul_multiplicity_factorial (n := a) hp
  have hb := Nat.Prime.sub_one_mul_multiplicity_factorial (n := b) hp
  have hab := Nat.Prime.sub_one_mul_multiplicity_factorial (n := a + b) hp
  have heq := Nat.add_choose_mul_factorial_mul_factorial a b
  have hle : multiplicity 2 a.factorial + multiplicity 2 b.factorial ≤
      multiplicity 2 (a + b).factorial := by
    have hc : (a + b).choose b ≠ 0 := (Nat.choose_pos (by omega)).ne'
    rw [← heq, Nat.multiplicity_mul (mul_ne_zero hc (Nat.factorial_ne_zero _))
      (Nat.factorial_ne_zero _), Nat.multiplicity_mul hc (Nat.factorial_ne_zero _)]
    omega
  simp only [Nat.add_one_sub_one, one_mul] at ha hb hab
  have h1 := Nat.digit_sum_le 2 a
  have h2 := Nat.digit_sum_le 2 b
  have h3 := Nat.digit_sum_le 2 (a + b)
  simp only [s₂]
  omega

@[simp] lemma s₂_zero : s₂ 0 = 0 := by simp [s₂]

lemma s₂_two_mul (n : ℕ) : s₂ (2 * n) = s₂ n := by
  rcases Nat.eq_zero_or_pos n with rfl | hn
  · rfl
  · simp only [s₂]
    rw [Nat.digits_def' (by norm_num) (by omega)]
    simp

lemma s₂_two_pow (j : ℕ) : s₂ (2 ^ j) = 1 := by
  induction j with
  | zero => decide
  | succ j ih => rw [pow_succ, mul_comm, s₂_two_mul, ih]

lemma s₂_pos {n : ℕ} (hn : n ≠ 0) : 1 ≤ s₂ n := by
  by_contra h
  have h0 : s₂ n = 0 := by omega
  have hl := Nat.getLast_digit_ne_zero 2 hn
  have hmem := List.getLast_mem (Nat.digits_ne_nil_iff_ne_zero (b := 2) (n := n) |>.mpr hn)
  exact hl (List.sum_eq_zero_iff.mp h0 _ hmem)

/-! ### Divisibility of coefficients (S1–S4) -/

/-- Weakly good: `2^(s₂ t)` divides the `t`-th coefficient, for every `t`. -/
def WG (R : ℤ[X]) : Prop := ∀ t, (2 : ℤ) ^ s₂ t ∣ R.coeff t

/-- Strongly good: `2^(s₂ t + 1)` divides the `t`-th coefficient, for every `t ≥ 1`. -/
def SG (R : ℤ[X]) : Prop := ∀ t, 1 ≤ t → (2 : ℤ) ^ (s₂ t + 1) ∣ R.coeff t

lemma WG.mul {P Q : ℤ[X]} (hP : WG P) (hQ : WG Q) : WG (P * Q) := by
  intro t
  rw [coeff_mul]
  refine Finset.dvd_sum fun x hx => ?_
  rw [Finset.HasAntidiagonal.mem_antidiagonal] at hx
  have h := s₂_add_le x.1 x.2
  rw [hx] at h
  exact (pow_dvd_pow 2 h).trans (by rw [pow_add]; exact mul_dvd_mul (hP _) (hQ _))

lemma WG.sub {P Q : ℤ[X]} (hP : WG P) (hQ : WG Q) : WG (P - Q) := fun t => by
  rw [coeff_sub]; exact dvd_sub (hP t) (hQ t)

lemma WG_one : WG 1 := fun t => by
  rw [coeff_one]
  split_ifs with h
  · subst h; simp
  · exact dvd_zero _

lemma SG.add {P Q : ℤ[X]} (hP : SG P) (hQ : SG Q) : SG (P + Q) := fun t ht => by
  rw [coeff_add]; exact dvd_add (hP t ht) (hQ t ht)

lemma SG.WG {P : ℤ[X]} (hP : SG P) : WG P := fun t => by
  rcases Nat.eq_zero_or_pos t with rfl | ht
  · rw [s₂_zero, pow_zero]; exact one_dvd _
  · exact (pow_dvd_pow 2 (Nat.le_succ _)).trans (hP t ht)

lemma SG.mul {P Q : ℤ[X]} (hP : SG P) (hQ : SG Q) : SG (P * Q) := by
  intro t ht
  rw [coeff_mul]
  refine Finset.dvd_sum fun x hx => ?_
  rw [Finset.HasAntidiagonal.mem_antidiagonal] at hx
  rcases Nat.eq_zero_or_pos x.1 with h1 | h1
  · have : x.2 = t := by omega
    rw [this]; exact dvd_mul_of_dvd_right (hQ t ht) _
  rcases Nat.eq_zero_or_pos x.2 with h2 | h2
  · have : x.1 = t := by omega
    rw [this]; exact dvd_mul_of_dvd_left (hP t ht) _
  have h := s₂_add_le x.1 x.2
  rw [hx] at h
  refine (pow_dvd_pow 2 (by omega : s₂ t + 1 ≤ (s₂ x.1 + 1) + (s₂ x.2 + 1))).trans ?_
  rw [pow_add]; exact mul_dvd_mul (hP _ h1) (hQ _ h2)

lemma SG_one : SG 1 := fun t ht => by
  rw [coeff_one]
  split_ifs with h
  · omega
  · exact dvd_zero _

lemma SG.pow {P : ℤ[X]} (hP : SG P) (m : ℕ) : SG (P ^ m) := by
  induction m with
  | zero => simpa using SG_one
  | succ m ih => rw [pow_succ]; exact ih.mul hP

/-- Truncation `∑_{i<d} r_i W^i`. -/
noncomputable def truncW (R : ℤ[X]) (d : ℕ) : ℤ[X] :=
  ∑ i ∈ Finset.range d, C (R.coeff i) * X ^ i

lemma coeff_truncW (R : ℤ[X]) (d t : ℕ) :
    (truncW R d).coeff t = if t < d then R.coeff t else 0 := by
  simp only [truncW, finsetSum_coeff, coeff_C_mul_X_pow]
  rw [Finset.sum_ite_eq]
  simp [Finset.mem_range]

lemma WG.tr {R : ℤ[X]} (hR : WG R) (d : ℕ) : WG (truncW R d) := fun t => by
  rw [coeff_truncW]; split_ifs
  · exact hR t
  · exact dvd_zero _

/-- The squaring step: the square of a weakly good polynomial is strongly good. This is where
the extra factor `2` of S3 comes from. -/
lemma WG.sq {R : ℤ[X]} (hR : WG R) : SG (R ^ 2) := by
  have key : ∀ d, SG (truncW R d ^ 2) := by
    intro d
    induction d with
    | zero => intro t ht; simp [truncW]
    | succ d ih =>
      have hsplit : truncW R (d + 1) = truncW R d + C (R.coeff d) * X ^ d := by
        simp [truncW, Finset.sum_range_succ]
      have hexp : truncW R (d + 1) ^ 2 = truncW R d ^ 2 +
          (C (2 * R.coeff d) * X ^ d * truncW R d + C (R.coeff d ^ 2) * X ^ (2 * d)) := by
        rw [hsplit]; simp only [map_mul, map_pow, map_ofNat]; ring
      rw [hexp]
      refine ih.add (SG.add ?_ ?_)
      · intro t ht
        rw [mul_assoc, coeff_C_mul, coeff_X_pow_mul']
        split_ifs with hdt
        · have h := s₂_add_le d (t - d)
          rw [Nat.add_sub_cancel' hdt] at h
          refine (pow_dvd_pow 2 (by omega : s₂ t + 1 ≤ 1 + s₂ d + s₂ (t - d))).trans ?_
          rw [pow_add, pow_add, pow_one]
          exact mul_dvd_mul (mul_dvd_mul_left 2 (hR d)) (hR.tr d _)
        · rw [mul_zero]; exact dvd_zero _
      · intro t ht
        rw [coeff_C_mul_X_pow]
        split_ifs with h
        · subst h
          have hd : d ≠ 0 := by omega
          have := s₂_pos hd
          rw [s₂_two_mul]
          refine (pow_dvd_pow 2 (by omega : s₂ d + 1 ≤ s₂ d * 2)).trans ?_
          rw [pow_mul]; exact pow_dvd_pow_of_dvd (hR d) 2
        · exact dvd_zero _
  have := key (R.natDegree + 1)
  have hR' : truncW R (R.natDegree + 1) = R := by
    rw [truncW]; exact (as_sum_range_C_mul_X_pow R).symm
  rwa [hR'] at this

/-- `G 0 = 1`, `G (j+1) = G j ^ 2 - 2 W^(2^j)`: the polynomial in `w = u⁻²` with
`g_j(u) = u^(2^j) G_j(u⁻²)`, where `g_0 = u` and `g_{j+1} = g_j² - 2`. -/
noncomputable def G : ℕ → ℤ[X]
  | 0 => 1
  | j + 1 => G j ^ 2 - 2 * X ^ (2 ^ j)

/-- `F r = ∏_{j<r} G j`, the polynomial in `w` attached to `f = u g_1 ⋯ g_{r-1}`. -/
noncomputable def F (r : ℕ) : ℤ[X] := ∏ j ∈ Finset.range r, G j

lemma WG_G (j : ℕ) : WG (G j) := by
  induction j with
  | zero => exact WG_one
  | succ j ih =>
    refine ih.sq.WG.sub fun t => ?_
    rw [show (2 : ℤ[X]) = C 2 by simp, coeff_C_mul_X_pow]
    split_ifs with h
    · rw [h, s₂_two_pow, pow_one]
    · exact dvd_zero _

lemma WG_F (r : ℕ) : WG (F r) := by
  induction r with
  | zero => simpa [F] using WG_one
  | succ r ih => rw [F, Finset.prod_range_succ]; exact ih.mul (WG_G r)

lemma eval_zero_G (j : ℕ) : (G j).eval 0 = 1 := by
  induction j with
  | zero => simp [G]
  | succ j ih => simp [G, ih]

lemma eval_zero_F (r : ℕ) : (F r).eval 0 = 1 := by
  simp [F, eval_prod, eval_zero_G]

/-! ### The u-form (S0) as an identity of power series -/

lemma isUnit_B : IsUnit (1 + PowerSeries.X : PowerSeries ℤ) := by
  rw [PowerSeries.isUnit_iff_constantCoeff]; simp

/-- `B = 1 + X` as a unit of `ℤ⟦X⟧`. -/
noncomputable def B : (PowerSeries ℤ)ˣ := isUnit_B.unit

lemma B_val : (B : PowerSeries ℤ) = 1 + PowerSeries.X := rfl

/-- `z = X (1 + X)⁻²`. -/
noncomputable def z : PowerSeries ℤ := PowerSeries.X * ((B⁻¹ : (PowerSeries ℤ)ˣ) : PowerSeries ℤ) ^ 2

lemma Bz (m : ℕ) : (B : PowerSeries ℤ) ^ (2 * m) * z ^ m = PowerSeries.X ^ m := by
  rw [z, mul_pow, ← pow_mul, mul_comm (PowerSeries.X ^ m), ← mul_assoc, ← mul_pow,
    mul_comm 2 m, Units.mul_inv, one_pow, one_mul]

lemma G_eval (j : ℕ) :
    (B : PowerSeries ℤ) ^ (2 ^ j) * aeval z (G j) = 1 + PowerSeries.X ^ (2 ^ j) := by
  induction j with
  | zero => simp [G, B_val]
  | succ j ih =>
    have h2 : (B : PowerSeries ℤ) ^ (2 ^ (j + 1)) = ((B : PowerSeries ℤ) ^ (2 ^ j)) ^ 2 := by
      rw [← pow_mul, pow_succ]
    have hX : (B : PowerSeries ℤ) ^ (2 ^ (j + 1)) * z ^ (2 ^ j) = PowerSeries.X ^ (2 ^ j) := by
      rw [pow_succ, mul_comm _ 2, Bz]
    simp only [G, map_sub, map_mul, map_pow, aeval_X, map_ofNat]
    calc (B : PowerSeries ℤ) ^ 2 ^ (j + 1) * (aeval z (G j) ^ 2 - 2 * z ^ 2 ^ j)
        = ((B : PowerSeries ℤ) ^ (2 ^ j) * aeval z (G j)) ^ 2
          - 2 * ((B : PowerSeries ℤ) ^ (2 ^ (j + 1)) * z ^ (2 ^ j)) := by rw [h2]; ring
      _ = 1 + PowerSeries.X ^ 2 ^ (j + 1) := by rw [ih, hX, pow_succ 2 j, pow_mul]; ring

lemma F_eval (r : ℕ) : (B : PowerSeries ℤ) ^ (2 ^ r - 1) * aeval z (F r) =
    ∑ i ∈ Finset.range (2 ^ r), PowerSeries.X ^ i := by
  induction r with
  | zero => simp [F]
  | succ r ih =>
    have he : 2 ^ (r + 1) - 1 = (2 ^ r - 1) + 2 ^ r := by
      have := Nat.one_le_two_pow (n := r); rw [pow_succ]; omega
    rw [F, Finset.prod_range_succ, map_mul, he, pow_add]
    calc (B : PowerSeries ℤ) ^ (2 ^ r - 1) * (B : PowerSeries ℤ) ^ 2 ^ r *
          (aeval z (∏ j ∈ Finset.range r, G j) * aeval z (G r))
        = ((B : PowerSeries ℤ) ^ (2 ^ r - 1) * aeval z (F r)) *
          ((B : PowerSeries ℤ) ^ 2 ^ r * aeval z (G r)) := by rw [F]; ring
      _ = ∑ i ∈ Finset.range (2 ^ (r + 1)), PowerSeries.X ^ i := by
        rw [ih, G_eval, pow_succ, mul_two, Finset.sum_range_add, mul_add, mul_one,
          Finset.sum_mul]
        congr 1
        refine Finset.sum_congr rfl fun i _ => ?_
        rw [← pow_add, add_comm]

lemma coeff_extract_monomial (t : ℕ) (c : ℤ) (N : ℕ) :
    PowerSeries.coeff N ((B : PowerSeries ℤ) ^ (2 * N) * aeval z (monomial t c)) =
      ∑ b ∈ Finset.range (N + 1), (monomial t c).coeff b * ((2 * (N - b)).choose (N - b) : ℤ) := by
    have hz : z ^ t = PowerSeries.X ^ t * ((B⁻¹ : (PowerSeries ℤ)ˣ) : PowerSeries ℤ) ^ (2 * t) := by
      rw [z, mul_pow, ← pow_mul, mul_comm 2 t]
    rw [aeval_monomial, hz, mul_left_comm, ← Algebra.smul_def, map_smul, smul_eq_mul]
    by_cases htN : t ≤ N
    · rw [Finset.sum_eq_single t (fun b _ hb => by rw [coeff_monomial_of_ne _ hb, zero_mul])
        (fun h => absurd (Finset.mem_range.mpr (by omega)) h), coeff_monomial_same]
      congr 1
      have hB : (B : PowerSeries ℤ) ^ (2 * N) =
          (B : PowerSeries ℤ) ^ (2 * (N - t)) * (B : PowerSeries ℤ) ^ (2 * t) := by
        rw [← pow_add]; congr 1; omega
      have hu : (B : PowerSeries ℤ) ^ (2 * t) *
          ((B⁻¹ : (PowerSeries ℤ)ˣ) : PowerSeries ℤ) ^ (2 * t) = 1 := by
        rw [← mul_pow, Units.mul_inv, one_pow]
      have hpoly : (B : PowerSeries ℤ) ^ (2 * (N - t)) =
          (((X + 1 : ℤ[X]) ^ (2 * (N - t)) : ℤ[X]) : PowerSeries ℤ) := by
        rw [B_val, Polynomial.coe_pow, Polynomial.coe_add, Polynomial.coe_X, Polynomial.coe_one,
          add_comm]
      have hcalc : (B : PowerSeries ℤ) ^ (2 * N) *
          (PowerSeries.X ^ t * ((B⁻¹ : (PowerSeries ℤ)ˣ) : PowerSeries ℤ) ^ (2 * t)) =
          PowerSeries.X ^ t * (B : PowerSeries ℤ) ^ (2 * (N - t)) := by
        rw [hB]
        calc (B : PowerSeries ℤ) ^ (2 * (N - t)) * (B : PowerSeries ℤ) ^ (2 * t) *
              (PowerSeries.X ^ t * ((B⁻¹ : (PowerSeries ℤ)ˣ) : PowerSeries ℤ) ^ (2 * t))
            = PowerSeries.X ^ t * (B : PowerSeries ℤ) ^ (2 * (N - t)) *
              ((B : PowerSeries ℤ) ^ (2 * t) *
                ((B⁻¹ : (PowerSeries ℤ)ˣ) : PowerSeries ℤ) ^ (2 * t)) := by ring
          _ = _ := by rw [hu, mul_one]
      rw [hcalc, PowerSeries.coeff_X_pow_mul', ite_eq_left htN, hpoly, Polynomial.coeff_coe,
        coeff_X_add_one_pow]
    · rw [Finset.sum_eq_zero fun b hb => by
        rw [coeff_monomial_of_ne _ (by rw [Finset.mem_range] at hb; omega), zero_mul]]
      rw [mul_left_comm, PowerSeries.coeff_X_pow_mul', ite_eq_right htN, mul_zero]

/-- Coefficient extraction: `[X^N] (1+X)^(2N) S(z) = ∑_{t ≤ N} [w^t] S · C(2(N-t), N-t)`. This
is `[x⁰] u^m = C(m, m/2)` of S0 after clearing denominators. -/
lemma coeff_extract (S : ℤ[X]) (N : ℕ) :
    PowerSeries.coeff N ((B : PowerSeries ℤ) ^ (2 * N) * aeval z S) =
      ∑ t ∈ Finset.range (N + 1), S.coeff t * ((2 * (N - t)).choose (N - t) : ℤ) := by
  induction S using Polynomial.induction_on' with
  | add p q hp hq =>
    rw [map_add, mul_add, map_add, hp, hq, ← Finset.sum_add_distrib]
    refine Finset.sum_congr rfl fun t _ => ?_
    rw [coeff_add, add_mul]
  | monomial t c => exact coeff_extract_monomial t c N

/-- `1 + X + ⋯ + X^(k-1)` as a power series. -/
lemma coe_geom (k : ℕ) : ((∑ i ∈ Finset.range k, (X : ℤ[X]) ^ i : ℤ[X]) : PowerSeries ℤ) =
    ∑ i ∈ Finset.range k, PowerSeries.X ^ i := by
  induction k with
  | zero => simp
  | succ k ih =>
    rw [Finset.sum_range_succ, Polynomial.coe_add, ih, Polynomial.coe_pow, Polynomial.coe_X,
      Finset.sum_range_succ]

/-- S0: `a_q(2m) = ∑_{t ≤ N} c_t C(2(N-t), N-t)` with `N = (q-1)m`, `c_t = [w^t] (F r)^(2m)`. -/
lemma main_identity (r m : ℕ) :
    ((∑ i ∈ Finset.range (2 ^ r), (X : ℤ[X]) ^ i) ^ (2 * m)).coeff ((2 ^ r - 1) * m) =
      ∑ t ∈ Finset.range ((2 ^ r - 1) * m + 1), ((F r) ^ (2 * m)).coeff t *
        ((2 * ((2 ^ r - 1) * m - t)).choose ((2 ^ r - 1) * m - t) : ℤ) := by
  rw [← coeff_extract, ← Polynomial.coeff_coe]
  congr 1
  rw [map_pow, Polynomial.coe_pow, coe_geom, show 2 * ((2 ^ r - 1) * m) = (2 ^ r - 1) * (2 * m) by
    ring, pow_mul (B : PowerSeries ℤ), ← mul_pow, F_eval]

/-- Kummer for central binomials: `v₂(C(2M, M)) = s₂ M`. -/
lemma multiplicity_central (M : ℕ) : multiplicity 2 ((2 * M).choose M) = s₂ M := by
  have h := sub_one_mul_multiplicity_choose_eq_sub_sum_digits (p := 2) (k := M) (n := 2 * M)
    (by omega)
  rw [show 2 * M - M = M by omega, two_mul M] at h
  have h2 : (Nat.digits 2 (M + M)).sum = s₂ M := by rw [← two_mul]; exact s₂_two_mul M
  rw [h2] at h
  rw [two_mul]; simpa using h

lemma central_dvd (M : ℕ) : (2 : ℤ) ^ s₂ M ∣ ((2 * M).choose M : ℤ) := by
  have : 2 ^ s₂ M ∣ (2 * M).choose M := by
    rw [multiplicity_dvd_iff_le (Nat.choose_pos (by omega)).ne', multiplicity_central]
  exact_mod_cast this

lemma central_not_dvd (M : ℕ) : ¬ (2 : ℤ) ^ (s₂ M + 1) ∣ ((2 * M).choose M : ℤ) := by
  have : ¬ 2 ^ (s₂ M + 1) ∣ (2 * M).choose M := by
    rw [multiplicity_dvd_iff_le (Nat.choose_pos (by omega)).ne', multiplicity_central]; omega
  exact_mod_cast this

/-- S5: the `t = 0` term has valuation exactly `s₂ N`, every other term more. -/
lemma sum_val (N : ℕ) (c : ℕ → ℤ) (h0 : c 0 = 1) (h : ∀ t, 1 ≤ t → (2 : ℤ) ^ (s₂ t + 1) ∣ c t) :
    (2 : ℤ) ^ s₂ N ∣ ∑ t ∈ Finset.range (N + 1), c t * ((2 * (N - t)).choose (N - t) : ℤ) ∧
    ¬ (2 : ℤ) ^ (s₂ N + 1) ∣
      ∑ t ∈ Finset.range (N + 1), c t * ((2 * (N - t)).choose (N - t) : ℤ) := by
  rw [Finset.sum_range_succ', h0, one_mul, Nat.sub_zero]
  have hrest : (2 : ℤ) ^ (s₂ N + 1) ∣ ∑ t ∈ Finset.range N,
      c (t + 1) * ((2 * (N - (t + 1))).choose (N - (t + 1)) : ℤ) := by
    refine Finset.dvd_sum fun t ht => ?_
    rw [Finset.mem_range] at ht
    have hs := s₂_add_le (t + 1) (N - (t + 1))
    rw [show t + 1 + (N - (t + 1)) = N by omega] at hs
    refine (pow_dvd_pow 2 (by omega : s₂ N + 1 ≤ (s₂ (t + 1) + 1) + s₂ (N - (t + 1)))).trans ?_
    rw [pow_add]
    exact mul_dvd_mul (h _ (by omega)) (central_dvd _)
  refine ⟨dvd_add ((pow_dvd_pow 2 (Nat.le_succ _)).trans hrest) (central_dvd N), fun hd => ?_⟩
  exact central_not_dvd N ((dvd_add_right hrest).mp hd)

/-! ### Main theorem (S5) -/

/-- **Theorem** (notes `central-2adic.md`, Attack): "For r ≥ 1, q = 2^r and every even n ≥ 0,
v₂(a_q(n)) = s₂((q−1)n/2)", where `a_q(n) = [x^((q−1)n/2)] (1 + x + ⋯ + x^(q−1))ⁿ` and `s₂` is
the binary digit sum. -/
theorem central_2adic (r n : ℕ) (_hr : 1 ≤ r) (hn : Even n) :
    padicValNat 2 (((∑ i ∈ Finset.range (2 ^ r), (X : ℕ[X]) ^ i) ^ n).coeff
      ((2 ^ r - 1) * n / 2)) = (Nat.digits 2 ((2 ^ r - 1) * n / 2)).sum := by
  obtain ⟨m, rfl⟩ := hn
  rw [← two_mul, show (2 ^ r - 1) * (2 * m) / 2 = (2 ^ r - 1) * m by
    rw [mul_left_comm, Nat.mul_div_cancel_left _ two_pos]]
  set N := (2 ^ r - 1) * m with hN
  set a := ((∑ i ∈ Finset.range (2 ^ r), (X : ℕ[X]) ^ i) ^ (2 * m)).coeff N with ha
  have hcast : (a : ℤ) = ((∑ i ∈ Finset.range (2 ^ r), (X : ℤ[X]) ^ i) ^ (2 * m)).coeff N := by
    have : ((∑ i ∈ Finset.range (2 ^ r), (X : ℕ[X]) ^ i) ^ (2 * m)).map (Nat.castRingHom ℤ) =
        (∑ i ∈ Finset.range (2 ^ r), (X : ℤ[X]) ^ i) ^ (2 * m) := by
      simp [Polynomial.map_pow, Polynomial.map_sum]
    rw [← this, coeff_map]; rfl
  have hSG : SG ((F r) ^ (2 * m)) := by
    rw [pow_mul]; exact (WG_F r).sq.pow m
  have h0 : ((F r) ^ (2 * m)).coeff 0 = 1 := by
    rw [coeff_zero_eq_eval_zero, eval_pow, eval_zero_F, one_pow]
  obtain ⟨hdvd, hndvd⟩ := sum_val N (fun t => ((F r) ^ (2 * m)).coeff t) h0 hSG
  rw [← main_identity, ← hcast] at hdvd hndvd
  have hdvd' : 2 ^ s₂ N ∣ a := by exact_mod_cast hdvd
  have hndvd' : ¬ 2 ^ (s₂ N + 1) ∣ a := by exact_mod_cast hndvd
  have ha0 : a ≠ 0 := by rintro h; rw [h] at hndvd'; exact hndvd' (dvd_zero _)
  rw [Nat.padicValNat_def]
  rw [multiplicity_dvd_iff_le ha0] at hdvd' hndvd'
  show multiplicity 2 a = s₂ N
  omega

/-- **The A402341 conjecture** ([A402341], comment): "for even n, the 2-adic valuation of a(n)
equals A000120(15*n/2)", where `a(n) = [x^⌊15n/2⌋] (1 + x + ⋯ + x^15)ⁿ`. -/
theorem a402341_conjecture (n : ℕ) (hn : Even n) :
    padicValNat 2 (((∑ i ∈ Finset.range 16, (X : ℕ[X]) ^ i) ^ n).coeff (15 * n / 2)) =
      (Nat.digits 2 (15 * n / 2)).sum :=
  central_2adic 4 n (by norm_num) hn

end Central2adic
