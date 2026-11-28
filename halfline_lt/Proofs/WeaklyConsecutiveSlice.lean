import Mathlib
import Proofs.WeaklyConsecutiveEnds

/-!
# Weakly consecutive sequences: slice lemma, and Conjecture 5.2 for `k = r·s^b`, `s ∤ r − 1`

Progress note (issue #82): A7.1 (slice lemma, `slice`) with its mirror (`slice_mirror`) and
A7.2 (Conjecture 5.2 for `k = r·s^b`, `r, s` distinct primes, `b ≥ 1`, `s ∤ r − 1`,
`conjecture_5_2_r_mul_s_pow`), with its squarefree case `k = p·q`
(`conjecture_5_2_mul_primes`), of `notes/weakly-consecutive.md` are proved, for every such `k`.
Nothing is left in this unit.

Notation as in `Proofs/WeaklyConsecutive.lean`: `σ : Equiv.Perm (Fin k)`, the 0-indexed position
`i : Fin k` stands for the position `i + 1 ∈ [k]` and `σ i` for the value `σ i + 1 ∈ [k]`. So
`d = σ(1)` is `σ ⟨0, _⟩ + 1`, `d′ = σ(k)` is `σ ⟨k - 1, _⟩ + 1`, the position `k − d + 1` is
`⟨k - d, _⟩`, the position `d′` is `⟨d′ - 1, _⟩`, and `1 < pos(1) < k` reads
`1 < σ.symm ⟨0, _⟩ + 1 < k`.

Route. The notes prove `e ∣ K` (A7.1 (iii)) by building the slice `τ` and applying A6.1's
corollary to it. This file proves the same conclusion without building `τ`: the window lemma
A6.1 applied to `σ` itself at position `k − d + 1` with modulus `m = d·e` gives
`k mod (d·e) < d`, and `k mod (d·e) = d·(K mod e)` since `k = d·K`, so `K mod e = 0`.
The other steps follow the notes: (i) `d ∣ σ(k − d + 1)` from the class lemma A6.0 (a);
`e ≥ 2` since the value `d` sits at position 1 only; (iv) `g = gcd(e, d′)` divides both
`σ(k − d + 1)` and `σ(k)`, so by A6.0 (a) `g ∣ k − (k − d + 1) = d − 1` when `g ≥ 2`.
-/

namespace WeaklyConsecutiveSlice

open WeaklyConsecutive WeaklyConsecutiveEnds

variable {k : ℕ} {σ : Equiv.Perm (Fin k)}

/-- **A7.1, slice lemma** (`notes/weakly-consecutive.md`, Attack ideas A7.1). "Let σ be a WCS of
length k with 1 < pos(1) < k, d = σ(1), d′ = σ(k) …, and K = k/d. Then σ(k − d + 1) = d·e with
e ∣ K, e ≥ 2 and gcd(e, d′) ∣ d − 1." -/
theorem slice (h : IsWeaklyConsecutive σ) (hk : 0 < k)
    (hp1 : 1 < (σ.symm ⟨0, hk⟩ : ℕ) + 1) (hpk : (σ.symm ⟨0, hk⟩ : ℕ) + 1 < k) :
    ∃ e : ℕ, (σ ⟨k - ((σ ⟨0, hk⟩ : ℕ) + 1), by omega⟩ : ℕ) + 1 = ((σ ⟨0, hk⟩ : ℕ) + 1) * e ∧
      e ∣ k / ((σ ⟨0, hk⟩ : ℕ) + 1) ∧ 2 ≤ e ∧
      Nat.gcd e ((σ ⟨k - 1, by omega⟩ : ℕ) + 1) ∣ (σ ⟨0, hk⟩ : ℕ) + 1 - 1 := by
  obtain ⟨hd2, hd'2, hdk, hd'k, hcop, hmul⟩ := interior_ends h hk hp1 hpk
  set d := (σ ⟨0, hk⟩ : ℕ) + 1 with hd_def
  set d' := (σ ⟨k - 1, by omega⟩ : ℕ) + 1 with hd'_def
  obtain ⟨K, hK⟩ := hdk
  have hKpos : 0 < K := by
    rcases Nat.eq_zero_or_pos K with h0 | h0
    · rw [h0, mul_zero] at hK; omega
    · exact h0
  have hd'K : d' ∣ K := by
    rw [hK] at hmul
    exact Nat.dvd_of_mul_dvd_mul_left (by omega) hmul
  have hK2 : 2 ≤ K := le_trans hd'2 (Nat.le_of_dvd hKpos hd'K)
  have hdK : 2 * d ≤ k := by
    calc 2 * d ≤ d * K := by nlinarith
      _ = k := hK.symm
  set i : Fin k := ⟨k - d, by omega⟩ with hi_def
  -- (i) `d ∣ σ(k − d + 1)`: position `k − d + 1` is in the class of position 1 mod d.
  have hdi : d ∣ (σ i : ℕ) + 1 := by
    have hcls := class_of_mem h (i := ⟨0, hk⟩) (m := d) (by omega) (by omega) dvd_rfl
    refine (hcls i).mpr ?_
    refine (Nat.modEq_zero_iff_dvd).mpr ?_
    show d ∣ k - d
    exact Nat.dvd_sub (⟨K, hK⟩ : d ∣ k) dvd_rfl
  obtain ⟨e, he⟩ := hdi
  have he0 : e ≠ 0 := by rintro rfl; rw [mul_zero] at he; omega
  have he1 : e ≠ 1 := by
    rintro rfl
    rw [mul_one] at he
    have : σ i = σ ⟨0, hk⟩ := Fin.ext (by omega)
    have := congrArg Fin.val (σ.injective this)
    simp only [hi_def] at this
    omega
  have he2 : 2 ≤ e := by omega
  refine ⟨e, he, ?_, he2, ?_⟩
  · -- (iii) `e ∣ K`, by the window lemma at position `k − d + 1` with modulus `d·e`.
    have hde2 : 2 ≤ d * e := by nlinarith
    have hdek : d * e ≤ k := by have := (σ i).isLt; omega
    have hw := (window h i hde2 hdek (he ▸ dvd_rfl)).2
    simp only [hi_def] at hw
    rw [hK, Nat.mul_mod_mul_left] at hw
    have hdKd : d ≤ d * K := Nat.le_mul_of_pos_right d hKpos
    have hlt : d * (K % e) < d * 1 := by omega
    have := Nat.lt_of_mul_lt_mul_left hlt
    rw [Nat.div_eq_of_eq_mul_left (by omega) (hK.trans (mul_comm d K))]
    exact Nat.dvd_of_mod_eq_zero (by omega)
  · -- (iv) `gcd(e, d′) ∣ d − 1`.
    set g := Nat.gcd e d' with hg_def
    have hg0 : 0 < g := Nat.gcd_pos_of_pos_left _ (by omega)
    rcases Nat.lt_or_ge g 2 with hg | hg
    · rw [show g = 1 by omega]; exact one_dvd _
    have hgi : g ∣ (σ i : ℕ) + 1 := he ▸ Dvd.dvd.mul_left (Nat.gcd_dvd_left e d') d
    have hgk : g ≤ k :=
      (Nat.le_of_dvd (by omega) (Nat.gcd_dvd_right e d')).trans
        (by have := (σ ⟨k - 1, by omega⟩).isLt; omega)
    have hcls := class_of_mem h (i := i) (by omega) hgk hgi
    have hmod : (k - 1) ≡ (k - d) [MOD g] := (hcls ⟨k - 1, by omega⟩).mp (Nat.gcd_dvd_right e d')
    have := (Nat.modEq_iff_dvd' (by omega)).mp hmod.symm
    rwa [show k - 1 - (k - d) = d - 1 by omega] at this

/-- **A7.1, mirror** (`notes/weakly-consecutive.md`, Attack ideas A7.1, *Mirror*). "σ(d′) = d′·e′
with e′ ∣ k/d′, e′ ≥ 2, gcd(e′, d) ∣ d′ − 1", under the hypotheses of A7.1. -/
theorem slice_mirror (h : IsWeaklyConsecutive σ) (hk : 0 < k)
    (hp1 : 1 < (σ.symm ⟨0, hk⟩ : ℕ) + 1) (hpk : (σ.symm ⟨0, hk⟩ : ℕ) + 1 < k) :
    ∃ e' : ℕ, (σ ⟨(σ ⟨k - 1, by omega⟩ : ℕ) + 1 - 1, by omega⟩ : ℕ) + 1 =
        ((σ ⟨k - 1, by omega⟩ : ℕ) + 1) * e' ∧
      e' ∣ k / ((σ ⟨k - 1, by omega⟩ : ℕ) + 1) ∧ 2 ≤ e' ∧
      Nat.gcd e' ((σ ⟨0, hk⟩ : ℕ) + 1) ∣ (σ ⟨k - 1, by omega⟩ : ℕ) + 1 - 1 := by
  have hr := reversal h
  have hsymm : ((Fin.revPerm.trans σ).symm ⟨0, hk⟩ : ℕ) = k - 1 - (σ.symm ⟨0, hk⟩ : ℕ) := by
    simp [Fin.val_rev]
    omega
  have h0 : (Fin.revPerm.trans σ) ⟨0, hk⟩ = σ ⟨k - 1, by omega⟩ := by
    simp only [Equiv.trans_apply, Fin.revPerm_apply]
    congr 1
  have hlast : (Fin.revPerm.trans σ) ⟨k - 1, by omega⟩ = σ ⟨0, hk⟩ := by
    simp only [Equiv.trans_apply, Fin.revPerm_apply]
    congr 1; ext; simp [Fin.val_rev]; omega
  obtain ⟨e, he, hediv, he2, hg⟩ :=
    slice hr hk (by rw [hsymm]; omega) (by rw [hsymm]; omega)
  rw [h0, hlast] at hg
  rw [h0] at hediv
  simp only [h0] at he
  refine ⟨e, ?_, hediv, he2, hg⟩
  rw [← he]
  simp only [Equiv.trans_apply, Fin.revPerm_apply]
  refine congrArg (fun x : Fin k => (σ x : ℕ) + 1) (Fin.ext ?_)
  simp only [Fin.val_rev]
  have := (σ ⟨k - 1, by omega⟩).isLt
  omega

/-- A divisor `x ≥ 2` of `r·s^b` (`r`, `s` prime) not divisible by `r` is divisible by `s`. -/
lemma s_dvd_of_not_r_dvd {r s b x : ℕ} (hr : r.Prime) (hs : s.Prime) (hx2 : 2 ≤ x)
    (hx : x ∣ r * s ^ b) (hrx : ¬ r ∣ x) : s ∣ x := by
  have hcop : Nat.Coprime x r := ((Nat.Prime.coprime_iff_not_dvd hr).mpr hrx).symm
  obtain ⟨c, -, hc⟩ := (Nat.dvd_prime_pow hs).mp (hcop.dvd_of_dvd_mul_left hx)
  rcases Nat.eq_zero_or_pos c with h0 | h0
  · rw [h0, pow_zero] at hc; omega
  · rw [hc]; exact dvd_pow_self s h0.ne'

/-- A divisor of `r·s^b` (`r`, `s` prime) divisible by `r` and not by `s` equals `r`. -/
lemma eq_r_of_not_s_dvd {r s b x : ℕ} (hs : s.Prime)
    (hx : x ∣ r * s ^ b) (hrx : r ∣ x) (hsx : ¬ s ∣ x) : x = r := by
  have hcop : Nat.Coprime x (s ^ b) :=
    Nat.Coprime.pow_right b (((Nat.Prime.coprime_iff_not_dvd hs).mpr hsx).symm)
  exact Nat.dvd_antisymm (hcop.dvd_of_dvd_mul_right hx) hrx

/-- The closing step of A7.2: with `d = r`, `s ∣ d′`, `K = s^b`, the conclusion of A7.1 gives
`s ∣ r − 1`. -/
lemma closing {r s b e d' : ℕ} (hs : s.Prime) (he : e ∣ s ^ b) (he2 : 2 ≤ e) (hsd' : s ∣ d')
    (hg : Nat.gcd e d' ∣ r - 1) : s ∣ r - 1 := by
  obtain ⟨c, -, hc⟩ := (Nat.dvd_prime_pow hs).mp he
  have hc0 : c ≠ 0 := by rintro rfl; rw [pow_zero] at hc; omega
  have hse : s ∣ e := hc ▸ dvd_pow_self s hc0
  exact (Nat.dvd_gcd hse hsd').trans hg

/-- **A7.2, Theorem** (`notes/weakly-consecutive.md`, Attack ideas A7.2). "Let k = r·s^b with
r, s distinct primes, b ≥ 1 and s ∤ r − 1. Then every WCS of length k has σ(1) = 1 or
σ(k) = 1." (0-indexed: `σ 0 = 0` or `σ (k - 1) = 0`.) The hypotheses `r ≠ s` and `b ≥ 1` are
stated as in the notes; the proof does not use them (without them `k` is a prime or a prime
power, already covered by A6.3). -/
theorem conjecture_5_2_r_mul_s_pow {r s b : ℕ} (hr : r.Prime) (hs : s.Prime) (_hrs : r ≠ s)
    (_hb : 1 ≤ b) (hsr : ¬ s ∣ r - 1) (hk : k = r * s ^ b)
    (σ : Equiv.Perm (Fin k)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, hk ▸ Nat.mul_pos hr.pos (pow_pos hs.pos b)⟩ =
        ⟨0, hk ▸ Nat.mul_pos hr.pos (pow_pos hs.pos b)⟩ ∨
      σ ⟨k - 1, by have := hk ▸ Nat.mul_pos hr.pos (pow_pos hs.pos b); omega⟩ =
        ⟨0, hk ▸ Nat.mul_pos hr.pos (pow_pos hs.pos b)⟩ := by
  have hk0 : 0 < k := hk ▸ Nat.mul_pos hr.pos (pow_pos hs.pos b)
  by_contra hne
  rw [not_or] at hne
  have hp0 : (σ.symm ⟨0, hk0⟩ : ℕ) ≠ 0 := by
    intro e
    apply hne.1
    have : σ.symm ⟨0, hk0⟩ = ⟨0, hk0⟩ := Fin.ext e
    exact (congrArg σ this.symm).trans (σ.apply_symm_apply _)
  have hpk : (σ.symm ⟨0, hk0⟩ : ℕ) ≠ k - 1 := by
    intro e
    apply hne.2
    have : σ.symm ⟨0, hk0⟩ = ⟨k - 1, by omega⟩ := Fin.ext e
    exact (congrArg σ this.symm).trans (σ.apply_symm_apply _)
  have hp1 : 1 < (σ.symm ⟨0, hk0⟩ : ℕ) + 1 := by omega
  have hpk' : (σ.symm ⟨0, hk0⟩ : ℕ) + 1 < k := by have := (σ.symm ⟨0, hk0⟩).isLt; omega
  obtain ⟨hd2, hd'2, hdk, hd'k, hcop, -⟩ := interior_ends h hk0 hp1 hpk'
  have hgcd1 : ∀ p : ℕ, p.Prime → p ∣ (σ ⟨0, hk0⟩ : ℕ) + 1 →
      p ∣ (σ ⟨k - 1, by omega⟩ : ℕ) + 1 → False := fun p hp h1 h2 =>
    hp.one_lt.ne' (Nat.dvd_one.mp (hcop ▸ Nat.dvd_gcd h1 h2))
  replace hdk := hdk.trans (dvd_of_eq hk)
  replace hd'k := hd'k.trans (dvd_of_eq hk)
  by_cases hrd : r ∣ (σ ⟨0, hk0⟩ : ℕ) + 1
  · -- σ(1) = r and s ∣ σ(k): use A7.1.
    have hrd' : ¬ r ∣ (σ ⟨k - 1, by omega⟩ : ℕ) + 1 := fun h2 => hgcd1 r hr hrd h2
    have hsd' := s_dvd_of_not_r_dvd hr hs hd'2 hd'k hrd'
    have hsd : ¬ s ∣ (σ ⟨0, hk0⟩ : ℕ) + 1 := fun h1 => hgcd1 s hs h1 hsd'
    have hdr := eq_r_of_not_s_dvd hs hdk hrd hsd
    obtain ⟨e, -, hediv, he2, hg⟩ := slice h hk0 hp1 hpk'
    rw [hdr, hk, Nat.mul_div_cancel_left _ hr.pos] at hediv
    rw [hdr] at hg
    exact hsr (closing hs hediv he2 hsd' hg)
  · -- s ∣ σ(1); then σ(k) = r: use the mirror of A7.1.
    have hsd := s_dvd_of_not_r_dvd hr hs hd2 hdk hrd
    have hsd' : ¬ s ∣ (σ ⟨k - 1, by omega⟩ : ℕ) + 1 := fun h2 => hgcd1 s hs hsd h2
    have hrd' : r ∣ (σ ⟨k - 1, by omega⟩ : ℕ) + 1 := by
      by_contra hrd'
      exact hsd' (s_dvd_of_not_r_dvd hr hs hd'2 hd'k hrd')
    have hd'r := eq_r_of_not_s_dvd hs hd'k hrd' hsd'
    obtain ⟨e, -, hediv, he2, hg⟩ := slice_mirror h hk0 hp1 hpk'
    rw [hd'r, hk, Nat.mul_div_cancel_left _ hr.pos] at hediv
    rw [hd'r] at hg
    exact hsr (closing hs hediv he2 hsd hg)

/-- **A7.2, squarefree case** (`notes/weakly-consecutive.md`, Attack ideas A7.2, *Squarefree
k = pq*). "(p < q primes): take r = p, s = q; then 1 ≤ p − 1 < q, so q ∤ p − 1." So Conjecture
5.2 holds for every `k = p·q` with `p < q` primes. -/
theorem conjecture_5_2_mul_primes {p q : ℕ} (hp : p.Prime) (hq : q.Prime) (hpq : p < q)
    (hk : k = p * q) (σ : Equiv.Perm (Fin k)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, hk ▸ Nat.mul_pos hp.pos hq.pos⟩ = ⟨0, hk ▸ Nat.mul_pos hp.pos hq.pos⟩ ∨
      σ ⟨k - 1, by have := hk ▸ Nat.mul_pos hp.pos hq.pos; omega⟩ =
        ⟨0, hk ▸ Nat.mul_pos hp.pos hq.pos⟩ := by
  have hsr : ¬ q ∣ p - 1 := fun hd =>
    absurd (Nat.le_of_dvd (by have := hp.two_le; omega) hd) (by omega)
  exact conjecture_5_2_r_mul_s_pow hp hq hpq.ne (le_refl 1) hsr (by rw [hk, pow_one]) σ h

end WeaklyConsecutiveSlice
