import Mathlib
import Proofs.WeaklyConsecutive

/-!
# Weakly consecutive sequences: class lemma, window lemma, coprime ends, prime powers

Progress note (issue #81): A6.0 (a) class lemma, A6.0 (b) reversal, A6.1 window lemma with its
corollary, A6.2 coprime ends with its corollary, and A6.3 (Conjecture 5.2 for prime powers and
`k = 1`) of `notes/weakly-consecutive.md` are all proved, for every `k`. Nothing is left in this
unit; the next unit is #82 (slice lemma A7.1, Theorem A7.2), which can build on these lemmas.

Notation as in `Proofs/WeaklyConsecutive.lean`: `σ : Equiv.Perm (Fin k)`, the 0-indexed position
`i : Fin k` stands for the position `i + 1 ∈ [k]` and `σ i` for the value `σ i + 1 ∈ [k]`.
So `T_m = {i : m ∣ σ i + 1}`, `pos(m) = σ.symm ⟨m - 1, _⟩`, the positions `1` and `k` are
`⟨0, _⟩` and `⟨k - 1, _⟩`, and the value `1` is `⟨0, _⟩`. Reversal `R(σ)(i) = σ(k + 1 − i)` is
`Fin.revPerm.trans σ`.
-/

namespace WeaklyConsecutiveEnds

open WeaklyConsecutive

variable {k : ℕ} {σ : Equiv.Perm (Fin k)}

/-- Definition 1.1 used with a natural modulus and a congruence of positions. -/
lemma dvd_of_modEq (h : IsWeaklyConsecutive σ) {i j : Fin k} {m : ℕ}
    (hm : m ∣ (σ i : ℕ) + 1) (hij : (i : ℕ) ≡ j [MOD m]) : m ∣ (σ j : ℕ) + 1 := by
  have h1 : (m : ℤ) ∣ (((i : ℕ) + 1 : ℕ) : ℤ) - (((j : ℕ) + 1 : ℕ) : ℤ) := by
    have := Nat.ModEq.dvd hij.symm
    push_cast
    simpa using this
  exact Int.natCast_dvd_natCast.mp (h i j m (Int.natCast_dvd_natCast.mpr hm) h1)

lemma card_filter_fin (n : ℕ) (P : ℕ → Prop) [DecidablePred P] :
    (Finset.univ.filter (fun i : Fin n => P i)).card = ((Finset.range n).filter P).card := by
  rw [← Nat.Iio_eq_range, ← Fin.map_valEmbedding_univ, Finset.filter_map, Finset.card_map]
  rfl

lemma card_modEq_fin (n m : ℕ) (hm : 0 < m) (v : ℕ) :
    (Finset.univ.filter (fun i : Fin n => (i : ℕ) ≡ v [MOD m])).card =
      n / m + if v % m < n % m then 1 else 0 := by
  rw [card_filter_fin n (· ≡ v [MOD m]), ← Nat.count_eq_card_filter_range,
    Nat.count_modEq_card n hm v]

/-- `|T_m| = ⌊k/m⌋`: `σ` is a bijection, and `[k]` has `⌊k/m⌋` multiples of `m`. -/
lemma card_T (σ : Equiv.Perm (Fin k)) (m : ℕ) :
    (Finset.univ.filter (fun i : Fin k => m ∣ (σ i : ℕ) + 1)).card = k / m := by
  have : (Finset.univ.filter (fun i : Fin k => m ∣ (σ i : ℕ) + 1)) =
      (Finset.univ.filter (fun v : Fin k => m ∣ (v : ℕ) + 1)).map σ.symm.toEmbedding := by
    ext i
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, Finset.mem_map_equiv,
      Equiv.symm_symm]
  rw [this, Finset.card_map, card_filter_fin k (fun e => m ∣ e + 1), Nat.card_multiples]

/-- **A6.0 (a), class lemma** (`notes/weakly-consecutive.md`, Attack ideas A6.0 (a)). "Let σ be a
WCS of length k ≥ 1 and m ∈ [k]. T_m = {i ∈ [k] : i ≡ pos(m) (mod m)}, and |T_m| = ⌊k/m⌋." -/
theorem class_lemma (h : IsWeaklyConsecutive σ) {m : ℕ} (hm1 : 1 ≤ m) (hmk : m ≤ k) :
    (∀ i : Fin k, m ∣ (σ i : ℕ) + 1 ↔ (i : ℕ) ≡ (σ.symm ⟨m - 1, by omega⟩ : ℕ) [MOD m]) ∧
    (Finset.univ.filter (fun i : Fin k => m ∣ (σ i : ℕ) + 1)).card = k / m := by
  set p := σ.symm ⟨m - 1, by omega⟩ with hp_def
  have hp : m ∣ (σ p : ℕ) + 1 := by
    simp only [hp_def, Equiv.apply_symm_apply]
    rw [Nat.sub_add_cancel hm1]
  have hsub : Finset.univ.filter (fun i : Fin k => (i : ℕ) ≡ p [MOD m]) ⊆
      Finset.univ.filter (fun i : Fin k => m ∣ (σ i : ℕ) + 1) := by
    intro j hj
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hj ⊢
    exact dvd_of_modEq h hp hj.symm
  have hcard : (Finset.univ.filter (fun i : Fin k => m ∣ (σ i : ℕ) + 1)).card ≤
      (Finset.univ.filter (fun i : Fin k => (i : ℕ) ≡ p [MOD m])).card := by
    rw [card_T, card_modEq_fin k m (by omega)]
    omega
  have heq := Finset.eq_of_subset_of_card_le hsub hcard
  refine ⟨fun i => ?_, card_T σ m⟩
  have := Finset.ext_iff.mp heq i
  simp only [Finset.mem_filter, Finset.mem_univ, true_and] at this
  exact this.symm

/-- **A6.0 (a), consequence.** "For every i ∈ T_m, T_m is the class of i mod m inside [k]". -/
theorem class_of_mem (h : IsWeaklyConsecutive σ) {m : ℕ} (hm1 : 1 ≤ m) (hmk : m ≤ k)
    {i : Fin k} (hi : m ∣ (σ i : ℕ) + 1) :
    ∀ j : Fin k, m ∣ (σ j : ℕ) + 1 ↔ (j : ℕ) ≡ i [MOD m] := by
  have hc := (class_lemma h hm1 hmk).1
  have hi' := (hc i).mp hi
  intro j
  rw [hc j]
  exact ⟨fun hj => hj.trans hi'.symm, fun hj => hj.trans hi'⟩

/-- **A6.0 (b), reversal** ([GSK24] Rule 3, re-proved). "R(σ)(i) = σ(k + 1 − i) is a WCS." -/
theorem reversal (h : IsWeaklyConsecutive σ) : IsWeaklyConsecutive (Fin.revPerm.trans σ) := by
  intro i j m hi hij
  simp only [Equiv.trans_apply, Fin.revPerm_apply] at hi ⊢
  apply h _ _ m hi
  have e : (((Fin.rev i : ℕ) + 1 : ℕ) : ℤ) - (((Fin.rev j : ℕ) + 1 : ℕ) : ℤ) =
      -((((i : ℕ) + 1 : ℕ) : ℤ) - (((j : ℕ) + 1 : ℕ) : ℤ)) := by
    simp only [Fin.val_rev]
    have := i.isLt
    have := j.isLt
    omega
  rw [e]
  exact dvd_neg.mpr hij

lemma window_left (h : IsWeaklyConsecutive σ) (i : Fin k) {m : ℕ} (hm2 : 2 ≤ m) (hmk : m ≤ k)
    (hdiv : m ∣ (σ i : ℕ) + 1) : k % m < (i : ℕ) + 1 := by
  have hcls := class_of_mem h (by omega) hmk hdiv
  have hT : Finset.univ.filter (fun j : Fin k => m ∣ (σ j : ℕ) + 1) =
      Finset.univ.filter (fun j : Fin k => (j : ℕ) ≡ i [MOD m]) :=
    Finset.filter_congr (fun j _ => hcls j)
  have hc := card_T σ m
  rw [hT, card_modEq_fin k m (by omega)] at hc
  have := Nat.mod_le (i : ℕ) m
  split_ifs at hc with hlt
  · omega
  · omega

/-- **A6.1, window lemma** (`notes/weakly-consecutive.md`, Attack ideas A6.1). "Let σ be a WCS,
i ∈ [k], m ∈ [2, k] with m ∣ σ(i). Then s_m < i and s_m < k + 1 − i", where `s_m = k mod m`.
Here the position `i` is `(i : ℕ) + 1`. -/
theorem window (h : IsWeaklyConsecutive σ) (i : Fin k) {m : ℕ} (hm2 : 2 ≤ m) (hmk : m ≤ k)
    (hdiv : m ∣ (σ i : ℕ) + 1) :
    k % m < (i : ℕ) + 1 ∧ k % m < k + 1 - ((i : ℕ) + 1) := by
  refine ⟨window_left h i hm2 hmk hdiv, ?_⟩
  have := window_left (reversal h) (Fin.rev i) hm2 hmk
    (by simpa only [Equiv.trans_apply, Fin.revPerm_apply, Fin.rev_rev] using hdiv)
  rw [Fin.val_rev] at this
  have := i.isLt
  omega

/-- **A6.1, corollary (end values), first half.** "σ(1) ∣ k". -/
theorem first_dvd (h : IsWeaklyConsecutive σ) (hk : 0 < k) : (σ ⟨0, hk⟩ : ℕ) + 1 ∣ k := by
  rcases Nat.lt_or_ge ((σ ⟨0, hk⟩ : ℕ) + 1) 2 with hd | hd
  · rw [show (σ ⟨0, hk⟩ : ℕ) + 1 = 1 by omega]
    exact one_dvd k
  · have := window_left h ⟨0, hk⟩ hd (by have := (σ ⟨0, hk⟩).isLt; omega) dvd_rfl
    exact Nat.dvd_of_mod_eq_zero (by simpa using this)

/-- **A6.1, corollary (end values), second half.** "σ(k) ∣ k". -/
theorem last_dvd (h : IsWeaklyConsecutive σ) (hk : 0 < k) :
    (σ ⟨k - 1, by omega⟩ : ℕ) + 1 ∣ k := by
  have := first_dvd (reversal h) hk
  have e : Fin.rev (⟨0, hk⟩ : Fin k) = ⟨k - 1, by omega⟩ := by
    ext
    simp [Fin.val_rev]
  simpa only [Equiv.trans_apply, Fin.revPerm_apply, e] using this

/-- **A6.2, coprime ends** (`notes/weakly-consecutive.md`, Attack ideas A6.2). "For every WCS,
gcd(σ(1), σ(k)) = 1." -/
theorem coprime_ends (h : IsWeaklyConsecutive σ) (hk : 0 < k) :
    Nat.gcd ((σ ⟨0, hk⟩ : ℕ) + 1) ((σ ⟨k - 1, by omega⟩ : ℕ) + 1) = 1 := by
  set g := Nat.gcd ((σ ⟨0, hk⟩ : ℕ) + 1) ((σ ⟨k - 1, by omega⟩ : ℕ) + 1) with hg_def
  by_contra hg
  have hg0 : 0 < g := Nat.gcd_pos_of_pos_left _ (Nat.succ_pos _)
  have hgk : g ≤ k :=
    (Nat.le_of_dvd (Nat.succ_pos _) (Nat.gcd_dvd_left _ _)).trans
      (by have := (σ ⟨0, hk⟩).isLt; omega)
  have hcls := class_of_mem h (i := ⟨0, hk⟩) (by omega) hgk (Nat.gcd_dvd_left _ _)
  have hmod : (k - 1) ≡ 0 [MOD g] := (hcls ⟨k - 1, by omega⟩).mp (Nat.gcd_dvd_right _ _)
  have h1 : g ∣ k - 1 := (Nat.modEq_zero_iff_dvd).mp hmod
  have h2 : g ∣ k := (Nat.gcd_dvd_left _ _).trans (first_dvd h hk)
  have h3 : g ∣ k - (k - 1) := Nat.dvd_sub h2 h1
  rw [show k - (k - 1) = 1 by omega] at h3
  exact hg (Nat.dvd_one.mp h3)

/-- **A6.2, corollary.** "If 1 < p < k [p = pos(1)], then σ(1) and σ(k) are both ≥ 2 …, so
d = σ(1) and d′ = σ(k) are coprime divisors of k, both ≥ 2, and d·d′ ∣ k." -/
theorem interior_ends (h : IsWeaklyConsecutive σ) (hk : 0 < k)
    (hp1 : 1 < (σ.symm ⟨0, hk⟩ : ℕ) + 1) (hpk : (σ.symm ⟨0, hk⟩ : ℕ) + 1 < k) :
    2 ≤ (σ ⟨0, hk⟩ : ℕ) + 1 ∧ 2 ≤ (σ ⟨k - 1, by omega⟩ : ℕ) + 1 ∧
    (σ ⟨0, hk⟩ : ℕ) + 1 ∣ k ∧ (σ ⟨k - 1, by omega⟩ : ℕ) + 1 ∣ k ∧
    Nat.Coprime ((σ ⟨0, hk⟩ : ℕ) + 1) ((σ ⟨k - 1, by omega⟩ : ℕ) + 1) ∧
    ((σ ⟨0, hk⟩ : ℕ) + 1) * ((σ ⟨k - 1, by omega⟩ : ℕ) + 1) ∣ k := by
  have ne : ∀ j : Fin k, (j : ℕ) ≠ (σ.symm ⟨0, hk⟩ : ℕ) → 2 ≤ (σ j : ℕ) + 1 := by
    intro j hj
    by_contra hlt
    apply hj
    have : σ j = ⟨0, hk⟩ := Fin.ext (by simp only; omega)
    rw [← this, Equiv.symm_apply_apply]
  have hc := coprime_ends h hk
  exact ⟨ne _ (by simp only; omega), ne _ (by simp only; omega), first_dvd h hk, last_dvd h hk,
    hc, Nat.Coprime.mul_dvd_of_dvd_of_dvd hc (first_dvd h hk) (last_dvd h hk)⟩

/-- **A6.3, prime powers** (`notes/weakly-consecutive.md`, Attack ideas A6.3). "If k = q^a is a
prime power (q prime, a ≥ 1), or k = 1, every WCS of length k has σ(1) = 1 or σ(k) = 1." Both
cases are `k = q ^ a` with `a ≥ 0` (`a = 0` is `k = 1`). -/
theorem conjecture_5_2_prime_pow {q a : ℕ} (hq : q.Prime) (σ : Equiv.Perm (Fin (q ^ a)))
    (h : IsWeaklyConsecutive σ) :
    σ ⟨0, pow_pos hq.pos a⟩ = ⟨0, pow_pos hq.pos a⟩ ∨
      σ ⟨q ^ a - 1, by have := pow_pos hq.pos a; omega⟩ = ⟨0, pow_pos hq.pos a⟩ := by
  have hk := pow_pos hq.pos a
  by_contra hne
  rw [not_or] at hne
  have qdvd : ∀ j : Fin (q ^ a), σ j ≠ ⟨0, hk⟩ → (σ j : ℕ) + 1 ∣ q ^ a → q ∣ (σ j : ℕ) + 1 := by
    intro j hj hd
    obtain ⟨e, -, he⟩ := (Nat.dvd_prime_pow hq).mp hd
    have e0 : e ≠ 0 := by
      rintro rfl
      apply hj
      exact Fin.ext (by simp only; simp at he; omega)
    rw [he]
    exact dvd_pow_self q e0
  have h1 := qdvd _ hne.1 (first_dvd h hk)
  have h2 := qdvd _ hne.2 (last_dvd h hk)
  have := Nat.dvd_gcd h1 h2
  rw [coprime_ends h hk] at this
  exact hq.one_lt.ne' (Nat.dvd_one.mp this)

end WeaklyConsecutiveEnds
