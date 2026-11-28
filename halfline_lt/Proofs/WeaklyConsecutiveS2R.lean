import Mathlib
import Proofs.WeaklyConsecutiveSlice

/-!
# Weakly consecutive sequences: Conjecture 5.2 for `k = s²·r`, `s ∣ r − 1`

Progress note (issue #96): A7.5 of `notes/weakly-consecutive.md` is proved: (i)
`conjecture_5_2_s_sq_mul_r` (`r ∤ s² − s + 1`), (ii) `conjecture_5_2_63` and
`conjecture_5_2_2107`, and the combined form of the issue, `conjecture_5_2_s_sq_mul_r'`.
Nothing is left in this unit.

Notation as in `Proofs/WeaklyConsecutive.lean`: `σ : Equiv.Perm (Fin k)`, the 0-indexed position
`i : Fin k` stands for the position `i + 1 ∈ [k]` and `σ i` for the value `σ i + 1 ∈ [k]`.
So the position `k − s + 1` is `⟨k - s, _⟩` and the position `s² − s + 1` is `⟨s ^ 2 - s, _⟩`.

Route. Steps 1, 2, 4 and 5 follow the notes. Step 3 (`σ(s² − s + 1) = k`) is proved, as A7.1
(iii) is in `Proofs/WeaklyConsecutiveSlice.lean`, without building the slice `υ`: with
`σ(s² − s + 1) = s²·u` (class lemma), the window lemma A6.1 at position `s² − s + 1` with modulus
`s²·u` gives `s²·(r mod u) = k mod (s²·u) < s² − s + 1`, so `u ∣ r`, and `u ≠ 1` since the value
`s²` sits at position `k − s + 1`. In step 5, `T_m = {m, 2m, …}` for `m ∣ k + 1` is proved from
the class lemma and the window lemma (`dvd_of_dvd_succ`), not by counting.
-/

namespace WeaklyConsecutiveS2R

open WeaklyConsecutive WeaklyConsecutiveEnds WeaklyConsecutiveSlice

variable {k : ℕ} {σ : Equiv.Perm (Fin k)}

/-- Step 1–4 core of A7.5: if `k = s²·r` (`s ∣ r − 1`, `(s, r) ≠ (2, 3)`), `1` is interior and
`σ(k) = r`, then `σ(k − s + 1) = s²` (step 2) and `σ(s² − s + 1) = k` (step 3). -/
lemma core {r s : ℕ} (hr : r.Prime) (hs : s.Prime) (hsr : s ∣ r - 1) (h23 : ¬ (s = 2 ∧ r = 3))
    (hk : k = s ^ 2 * r) (h : IsWeaklyConsecutive σ) (hk0 : 0 < k)
    (hp1 : 1 < (σ.symm ⟨0, hk0⟩ : ℕ) + 1) (hpk : (σ.symm ⟨0, hk0⟩ : ℕ) + 1 < k)
    (hd' : (σ ⟨k - 1, by omega⟩ : ℕ) + 1 = r) :
    ∃ (h2 : s ^ 2 - s < k),
      (σ ⟨k - s, by have := hs.two_le; omega⟩ : ℕ) + 1 = s ^ 2 ∧
      (σ ⟨s ^ 2 - s, h2⟩ : ℕ) + 1 = k := by
  have hs2 := hs.two_le
  have hr2 := hr.two_le
  have hsr' : s ≤ r - 1 := Nat.le_of_dvd (by omega) hsr
  have hss : s ≤ s ^ 2 := Nat.le_self_pow (by norm_num) s
  have hs4 : 4 ≤ s ^ 2 := by nlinarith
  have hS : s ^ 2 * 2 ≤ k := by rw [hk]; exact Nat.mul_le_mul_left _ hr2
  obtain ⟨hd2, -, hdk, -, hcop, -⟩ := interior_ends h hk0 hp1 hpk
  set d := (σ ⟨0, hk0⟩ : ℕ) + 1 with hd_def
  rw [hd'] at hcop
  -- Step 1: `d = s^c`, `c ∈ {1, 2}`.
  have hdS : d ∣ s ^ 2 := hcop.dvd_of_dvd_mul_right (hk ▸ hdk)
  obtain ⟨c, hc2, hc⟩ := (Nat.dvd_prime_pow hs).mp hdS
  obtain ⟨e, he, hediv, he2, hg⟩ := slice h hk0 hp1 hpk
  rw [hd'] at hg
  rw [← hd_def] at hediv hg
  interval_cases c
  · rw [pow_zero] at hc; omega
  · -- Step 2, α = 1: `e = s`.
    rw [pow_one] at hc
    have hKe : k / d = s * r := by
      rw [hc, hk, pow_two, mul_assoc, Nat.mul_div_cancel_left _ hs.pos]
    rw [hKe] at hediv
    have hre : ¬ r ∣ e := by
      intro hre
      rw [Nat.gcd_eq_right hre, hc] at hg
      have := Nat.le_of_dvd (by omega) hg
      omega
    have hcop' : Nat.Coprime e r := ((Nat.Prime.coprime_iff_not_dvd hr).mpr hre).symm
    have hes : e ∣ s := hcop'.dvd_of_dvd_mul_right hediv
    have hes' : e = s := ((Nat.Prime.eq_one_or_self_of_dvd hs e hes).resolve_left (by omega))
    have hpos1 : (σ ⟨k - s, by omega⟩ : ℕ) + 1 = s ^ 2 := by
      have : (⟨k - s, by omega⟩ : Fin k) = ⟨k - ((σ ⟨0, hk0⟩ : ℕ) + 1), by omega⟩ :=
        Fin.ext (by simp only; omega)
      rw [this, he, ← hd_def, hc, hes', pow_two]
    refine ⟨by omega, hpos1, ?_⟩
    -- Step 3: `σ(s² − s + 1) = k`.
    set j : Fin k := ⟨s ^ 2 - s, by omega⟩ with hj_def
    have hcls := class_of_mem h (i := ⟨k - s, by omega⟩) (m := s ^ 2) (by omega) (by omega)
      (by rw [hpos1])
    have hjS : s ^ 2 ∣ (σ j : ℕ) + 1 := by
      refine (hcls j).mpr ?_
      refine (Nat.modEq_iff_dvd' (show s ^ 2 - s ≤ k - s by omega)).mpr ?_
      show s ^ 2 ∣ k - s - (s ^ 2 - s)
      have : k - s - (s ^ 2 - s) = s ^ 2 * (r - 1) := by
        rw [Nat.mul_sub, mul_one, ← hk]; omega
      rw [this]; exact dvd_mul_right _ _
    obtain ⟨u, hu⟩ := hjS
    have hu0 : 0 < u := by
      rcases Nat.eq_zero_or_pos u with h0 | h0
      · rw [h0, mul_zero] at hu; omega
      · exact h0
    have hjk : (σ j : ℕ) + 1 ≤ k := (σ j).isLt
    have hw := (window h j (m := s ^ 2 * u) (by nlinarith) (by rw [← hu]; exact hjk) (by rw [hu])).1
    simp only [hj_def] at hw
    rw [hk, Nat.mul_mod_mul_left] at hw
    have hru : r % u = 0 := by
      by_contra hne
      have : s ^ 2 * 1 ≤ s ^ 2 * (r % u) := Nat.mul_le_mul_left _ (by omega)
      omega
    have hur : u ∣ r := Nat.dvd_of_mod_eq_zero hru
    rcases (Nat.Prime.eq_one_or_self_of_dvd hr u hur) with hu1 | hu1
    · exfalso
      rw [hu1, mul_one] at hu
      have : σ j = σ ⟨k - s, by omega⟩ := Fin.ext (by omega)
      have := congrArg Fin.val (σ.injective this)
      simp only [hj_def] at this
      have : s ^ 2 * 1 < s ^ 2 * r := Nat.mul_lt_mul_of_pos_left (by omega) (by omega)
      omega
    · rw [hu, hu1, hk]
  · -- Step 2, α = 2 is impossible: it forces `(s, r) = (2, 3)`.
    exfalso
    have hKe : k / d = r := by rw [hc, hk, Nat.mul_div_cancel_left _ (by omega)]
    rw [hKe] at hediv
    have her : e = r := (Nat.Prime.eq_one_or_self_of_dvd hr e hediv).resolve_left (by omega)
    rw [her, Nat.gcd_self, hc] at hg
    have hfac : s ^ 2 - 1 = (s - 1) * (s + 1) := by
      obtain ⟨t, rfl⟩ : ∃ t, s = t + 1 := ⟨s - 1, by omega⟩
      simp only [Nat.add_sub_cancel]
      ring_nf; omega
    rw [hfac] at hg
    rcases (Nat.Prime.dvd_mul hr).mp hg with h1 | h1
    · have := Nat.le_of_dvd (by omega) h1; omega
    · have hrs : r = s + 1 := le_antisymm (Nat.le_of_dvd (by omega) h1) (by omega)
      rcases hs.eq_two_or_odd' with h2 | h2
      · exact h23 ⟨h2, by omega⟩
      · have h2r : 2 ∣ r := by rw [hrs]; exact (Nat.odd_iff.mp h2 ▸ even_iff_two_dvd.mp
          (by obtain ⟨t, ht⟩ := h2; exact ⟨t + 1, by omega⟩))
        rcases (Nat.Prime.eq_one_or_self_of_dvd hr 2 h2r) with h | h <;> omega

/-- Reduction (steps 1 and reversal of A7.5): for `k = s²·r`, it suffices to rule out an interior
`1` with `σ(k) = r`. -/
lemma reduce {r s : ℕ} (hr : r.Prime) (hs : s.Prime) (hk : k = s ^ 2 * r) (hk0 : 0 < k)
    (P : ∀ τ : Equiv.Perm (Fin k), IsWeaklyConsecutive τ →
      1 < (τ.symm ⟨0, hk0⟩ : ℕ) + 1 → (τ.symm ⟨0, hk0⟩ : ℕ) + 1 < k →
      (τ ⟨k - 1, by omega⟩ : ℕ) + 1 = r → False)
    (σ : Equiv.Perm (Fin k)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, hk0⟩ = ⟨0, hk0⟩ ∨ σ ⟨k - 1, by omega⟩ = ⟨0, hk0⟩ := by
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
  have hk' : k = r * s ^ 2 := hk.trans (mul_comm _ _)
  replace hdk := hdk.trans (dvd_of_eq hk')
  replace hd'k := hd'k.trans (dvd_of_eq hk')
  by_cases hrd' : r ∣ (σ ⟨k - 1, by omega⟩ : ℕ) + 1
  · have hrd : ¬ r ∣ (σ ⟨0, hk0⟩ : ℕ) + 1 := fun h1 => hgcd1 r hr h1 hrd'
    have hsd := s_dvd_of_not_r_dvd hr hs hd2 hdk hrd
    have hsd' : ¬ s ∣ (σ ⟨k - 1, by omega⟩ : ℕ) + 1 := fun h2 => hgcd1 s hs hsd h2
    exact P σ h hp1 hpk' (eq_r_of_not_s_dvd hs hd'k hrd' hsd')
  · have hsd' := s_dvd_of_not_r_dvd hr hs hd'2 hd'k hrd'
    have hsd : ¬ s ∣ (σ ⟨0, hk0⟩ : ℕ) + 1 := fun h1 => hgcd1 s hs h1 hsd'
    have hrd : r ∣ (σ ⟨0, hk0⟩ : ℕ) + 1 := by
      by_contra hrd
      exact hsd (s_dvd_of_not_r_dvd hr hs hd2 hdk hrd)
    have hdr := eq_r_of_not_s_dvd hs hdk hrd hsd
    -- Reverse: `R(σ)(k) = σ(1) = r`, and `1` stays interior.
    have hrv := reversal h
    have hsymm : ((Fin.revPerm.trans σ).symm ⟨0, hk0⟩ : ℕ) = k - 1 - (σ.symm ⟨0, hk0⟩ : ℕ) := by
      simp [Fin.val_rev]
      omega
    have hlast : (Fin.revPerm.trans σ) ⟨k - 1, by omega⟩ = σ ⟨0, hk0⟩ := by
      simp only [Equiv.trans_apply, Fin.revPerm_apply]
      congr 1; ext; simp [Fin.val_rev]; omega
    exact P _ hrv (by rw [hsymm]; omega) (by rw [hsymm]; omega) (by rw [hlast]; exact hdr)

/-- Step 5 of A7.5: if `m ∈ [2, k]` and `m ∣ k + 1` (here as `k mod m = m − 1`), then
`T_m = {m, 2m, …}`: every position `j` with `m ∣ j` has `m ∣ σ(j)`. -/
lemma dvd_of_dvd_succ (h : IsWeaklyConsecutive σ) {m : ℕ} (hm2 : 2 ≤ m) (hmk : m ≤ k)
    (hmod : k % m = m - 1) (j : Fin k) (hj : m ∣ (j : ℕ) + 1) : m ∣ (σ j : ℕ) + 1 := by
  set p := σ.symm ⟨m - 1, by omega⟩ with hp_def
  have hpm : m ∣ (σ p : ℕ) + 1 := by
    rw [hp_def, Equiv.apply_symm_apply]; simp only; rw [Nat.sub_add_cancel (by omega)]
  have hcls := class_of_mem h (i := p) (by omega) hmk hpm
  have hc : (p : ℕ) % m = m - 1 := by
    have hlt : (p : ℕ) % m < m := Nat.mod_lt _ (by omega)
    by_contra hne
    have hck : (p : ℕ) % m < k := by omega
    have hdv := (hcls ⟨(p : ℕ) % m, hck⟩).mpr (Nat.mod_modEq _ _)
    have := (window h ⟨(p : ℕ) % m, hck⟩ hm2 hmk hdv).1
    simp only at this
    omega
  refine (hcls j).mpr ?_
  refine Nat.ModEq.add_right_cancel' 1 ?_
  refine (Nat.modEq_zero_iff_dvd.mpr hj).trans (Nat.modEq_zero_iff_dvd.mpr ?_).symm
  have := Nat.div_add_mod (p : ℕ) m
  exact ⟨(p : ℕ) / m + 1, by rw [hc] at this; rw [mul_add, mul_one]; omega⟩

/-- **A7.5 (i)** (`notes/weakly-consecutive.md`, Attack ideas A7.5). "Let r, s be distinct primes
with s ∣ r − 1 and k = s²·r. (i) If r ∤ s² − s + 1, every WCS of length k has σ(1) = 1 or
σ(k) = 1." (0-indexed: `σ 0 = 0` or `σ (k - 1) = 0`.) The hypothesis `r ≠ s` is stated as in
the notes; it follows from `s ∣ r − 1`, and the proof does not use it. -/
theorem conjecture_5_2_s_sq_mul_r {r s : ℕ} (hr : r.Prime) (hs : s.Prime) (_hrs : r ≠ s)
    (hsr : s ∣ r - 1) (hrs1 : ¬ r ∣ s ^ 2 - s + 1) (hk : k = s ^ 2 * r)
    (σ : Equiv.Perm (Fin k)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos⟩ =
        ⟨0, hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos⟩ ∨
      σ ⟨k - 1, by have := hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos; omega⟩ =
        ⟨0, hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos⟩ := by
  have hk0 : 0 < k := hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos
  have h23 : ¬ (s = 2 ∧ r = 3) := by
    rintro ⟨rfl, rfl⟩; exact hrs1 (by norm_num)
  refine reduce hr hs hk hk0 (fun τ hτ hp1 hpk hd' => ?_) σ h
  obtain ⟨h2, -, hv⟩ := core hr hs hsr h23 hk hτ hk0 hp1 hpk hd'
  -- Step 4: `T_r` is the class of position `k` mod `r`.
  have hcls := class_of_mem hτ (i := ⟨k - 1, by omega⟩) (m := r) (by have := hr.two_le; omega)
    (by rw [← hd']; exact (τ _).isLt) (by rw [hd'])
  have hrk : r ∣ k := hk ▸ dvd_mul_left r _
  have hmod := (hcls ⟨s ^ 2 - s, h2⟩).mp (by rw [hv]; exact hrk)
  have hdv := (Nat.modEq_iff_dvd' (by simp only; omega)).mp hmod
  simp only at hdv
  apply hrs1
  have hss : s ≤ s ^ 2 := Nat.le_self_pow (by norm_num) s
  have : k = (k - 1 - (s ^ 2 - s)) + (s ^ 2 - s + 1) := by omega
  exact (Nat.dvd_add_right hdv).mp (this ▸ hrk)

/-- **A7.5 (ii), k = 63** (`notes/weakly-consecutive.md`, Attack ideas A7.5). "(ii) The same holds
for k = 63 (s = 3, r = 7) …": every WCS of length 63 has σ(1) = 1 or σ(63) = 1. -/
theorem conjecture_5_2_63 (σ : Equiv.Perm (Fin 63)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, by norm_num⟩ = ⟨0, by norm_num⟩ ∨ σ ⟨62, by norm_num⟩ = ⟨0, by norm_num⟩ := by
  refine reduce (r := 7) (s := 3) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (fun τ hτ hp1 hpk hd' => ?_) σ h
  obtain ⟨_, hv, _⟩ := core (r := 7) (s := 3) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) hτ (by norm_num) hp1 hpk hd'
  -- Step 5: position 16 lies in `T_8` (8 ∣ 64) and in `T_9` (16 ≡ 1 − 3 mod 9).
  have h9 : 9 ∣ (τ ⟨15, by norm_num⟩ : ℕ) + 1 :=
    (class_of_mem hτ (i := ⟨60, by norm_num⟩) (m := 9) (by norm_num) (by norm_num)
      (by rw [hv]; norm_num) _).mpr (by decide)
  have h8 : 8 ∣ (τ ⟨15, by norm_num⟩ : ℕ) + 1 :=
    dvd_of_dvd_succ hτ (by norm_num) (by norm_num) (by norm_num) _ (by decide)
  have h72 : 72 ∣ (τ ⟨15, by norm_num⟩ : ℕ) + 1 :=
    Nat.Coprime.mul_dvd_of_dvd_of_dvd (by norm_num) h8 h9
  have := Nat.le_of_dvd (by omega) h72
  have := (τ ⟨15, by norm_num⟩).isLt
  omega

/-- **A7.5 (ii), k = 2107** (`notes/weakly-consecutive.md`, Attack ideas A7.5). "(ii) The same
holds for … k = 2107 (s = 7, r = 43)": every WCS of length 2107 has σ(1) = 1 or σ(2107) = 1. -/
theorem conjecture_5_2_2107 (σ : Equiv.Perm (Fin 2107)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, by norm_num⟩ = ⟨0, by norm_num⟩ ∨ σ ⟨2106, by norm_num⟩ = ⟨0, by norm_num⟩ := by
  refine reduce (r := 43) (s := 7) (by norm_num) (by norm_num) (by norm_num) (by norm_num)
    (fun τ hτ hp1 hpk hd' => ?_) σ h
  obtain ⟨_, hv, _⟩ := core (r := 43) (s := 7) (by norm_num) (by norm_num) (by norm_num)
    (by norm_num) (by norm_num) hτ (by norm_num) hp1 hpk hd'
  -- Step 5: position 680 lies in `T_68` (68 ∣ 2108) and in `T_49` (680 ≡ 1 − 7 mod 49).
  have h49 : 49 ∣ (τ ⟨679, by norm_num⟩ : ℕ) + 1 :=
    (class_of_mem hτ (i := ⟨2100, by norm_num⟩) (m := 49) (by norm_num) (by norm_num)
      (by rw [hv]; norm_num) _).mpr (by decide)
  have h68 : 68 ∣ (τ ⟨679, by norm_num⟩ : ℕ) + 1 :=
    dvd_of_dvd_succ hτ (by norm_num) (by norm_num) (by norm_num) _ (by decide)
  have hprod : 68 * 49 ∣ (τ ⟨679, by norm_num⟩ : ℕ) + 1 :=
    Nat.Coprime.mul_dvd_of_dvd_of_dvd (by norm_num) h68 h49
  have := Nat.le_of_dvd (by omega) hprod
  have := (τ ⟨679, by norm_num⟩).isLt
  omega

/-- **A7.5, combined** (issue #96). "Let r, s be distinct primes with s ∣ r − 1, and k = s²·r.
If r ∤ s² − s + 1, or k ∈ {63, 2107}, then every weakly consecutive sequence of length k has
σ(1) = 1 or σ(k) = 1." -/
theorem conjecture_5_2_s_sq_mul_r' {r s : ℕ} (hr : r.Prime) (hs : s.Prime) (hrs : r ≠ s)
    (hsr : s ∣ r - 1) (hk : k = s ^ 2 * r) (hcase : ¬ r ∣ s ^ 2 - s + 1 ∨ k = 63 ∨ k = 2107)
    (σ : Equiv.Perm (Fin k)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos⟩ =
        ⟨0, hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos⟩ ∨
      σ ⟨k - 1, by have := hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos; omega⟩ =
        ⟨0, hk ▸ Nat.mul_pos (pow_pos hs.pos 2) hr.pos⟩ := by
  rcases hcase with hc | rfl | rfl
  · exact conjecture_5_2_s_sq_mul_r hr hs hrs hsr hc hk σ h
  · exact conjecture_5_2_63 σ h
  · exact conjecture_5_2_2107 σ h

end WeaklyConsecutiveS2R
