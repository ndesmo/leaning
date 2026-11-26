import Mathlib

/-!
# Weakly consecutive sequences: Conjecture 5.2 of [GSK24] for small lengths

[GSK24] T. Garrison, C. Seiler, A. Knowles, "Weakly Consecutive Sequences", arXiv:2401.09497.

Definition 1.1 of [GSK24]: a permutation `σ` of `[k] = {1, …, k}` is *weakly consecutive* if for
all `i, j ∈ [k]` and all integers `m`, `m ∣ σ(i)` and `m ∣ (i − j)` imply `m ∣ σ(j)`.
Conjecture 5.2 of [GSK24]: every weakly consecutive `σ` has `σ(1) = 1` or `σ(k) = 1`.

Indexing. We use `σ : Equiv.Perm (Fin k)`. The 0-indexed `i : Fin k` stands for the position
`i + 1 ∈ [k]`, and `σ i : Fin k` stands for the value `σ i + 1 ∈ [k]`. The definition below writes
these shifts out explicitly, so it is Definition 1.1 verbatim with `m` ranging over all of `ℤ`.
The value `1` is `0 : Fin k`; the positions `1` and `k` are `0` and `k - 1 : Fin k`.

Method. `level k n` is a backtracking enumeration of the partial sequences of length `n`
(stored last value first) all of whose pairs pass the Definition 1.1 test for `m ∈ [2, k]`.
The pair test is `gcd(d, a) = gcd(d, b)` for values `a ≠ b` at distance `d`, which for
values in `[1, k]` is equivalent to the Definition 1.1 test for all `m` (`pairOK_of_wc` proves
the direction used). `mem_level` proves that every weakly consecutive `σ` survives the pruning
(completeness), so a kernel evaluation (`decide +kernel`, no `native_decide`) of `check k` proves
the conjecture for that `k`. Soundness of the enumerator is not needed for the conjecture and is
not proved here, so the file does not prove the counts `N(k)`.
-/

namespace WeaklyConsecutive

/-- Definition 1.1 of [GSK24], with 1-indexed positions `i + 1` and values `σ i + 1`. -/
def IsWeaklyConsecutive {k : ℕ} (σ : Equiv.Perm (Fin k)) : Prop :=
  ∀ (i j : Fin k) (m : ℤ), m ∣ (((σ i : ℕ) + 1 : ℕ) : ℤ) →
    m ∣ (((i : ℕ) + 1 : ℕ) : ℤ) - (((j : ℕ) + 1 : ℕ) : ℤ) → m ∣ (((σ j : ℕ) + 1 : ℕ) : ℤ)

/-- The pair test: 0-indexed values `a ≠ b` (1-indexed `a + 1`, `b + 1`) at positions distance
`d` apart. For values in `[1, k]` the equality `gcd(d, a + 1) = gcd(d, b + 1)` is exactly the
Definition 1.1 test in both directions (`pairOK_of_wc` proves the direction needed here). -/
def pairOK (a b d : ℕ) : Bool :=
  !(Nat.beq a b) && Nat.beq (Nat.gcd d (a + 1)) (Nat.gcd d (b + 1))

/-! The enumerator is written with the recursors `List.rec` and `Nat.rec` directly (hence
`noncomputable`: it is only ever evaluated by the kernel). This is much faster under kernel
reduction than the equation-compiler versions, which go through `brecOn`. -/

/-- `compat v l d`: the new value `v` passes the pair test against every entry of `l`, where
`l` lists earlier values, nearest first, the head being at distance `d`. -/
noncomputable def compat (v : ℕ) (l : List ℕ) : ℕ → Bool :=
  @List.rec ℕ (fun _ => ℕ → Bool) (fun _ => true) (fun w _ ih d => pairOK v w d && ih (d + 1)) l

/-- `extFrom l n acc`: prepend to `acc` every extension `v :: l` with `v < n` that passes. -/
noncomputable def extFrom (l : List ℕ) (n : ℕ) : List (List ℕ) → List (List ℕ) :=
  @Nat.rec (fun _ => List (List ℕ) → List (List ℕ)) (fun acc => acc)
    (fun v ih acc => ih (bif compat v l 1 then (v :: l) :: acc else acc)) n

/-- All passing one-step extensions (values `< k`) of all partial sequences in `L`. -/
noncomputable def step (k : ℕ) (L : List (List ℕ)) : List (List ℕ) :=
  @List.rec (List ℕ) (fun _ => List (List ℕ)) [] (fun l _ ih => extFrom l k ih) L

/-- Surviving partial sequences of length `n` (last value first). -/
noncomputable def level (k n : ℕ) : List (List ℕ) :=
  @Nat.rec (fun _ => List (List ℕ)) [[]] (fun _ L => step k L) n

/-- The target property of a full sequence: it starts or ends with the value `0`. -/
def good (l : List ℕ) : Bool := l.head? == some 0 || l.getLast? == some 0

/-- Every list in `L` is `good`. -/
noncomputable def allGood (L : List (List ℕ)) : Bool :=
  @List.rec (List ℕ) (fun _ => Bool) true (fun l _ ih => good l && ih) L

/-- Every surviving full sequence of length `k` starts or ends with the value `0`. -/
noncomputable def check (k : ℕ) : Bool := allGood (level k k)

/-- `check k` for all `k ∈ [1, K]`. -/
noncomputable def checksUpTo (K : ℕ) : Bool :=
  @Nat.rec (fun _ => Bool) true (fun n ih => ih && check (n + 1)) K

lemma mem_extFrom_of_mem {l x : List ℕ} :
    ∀ (n : ℕ) {acc : List (List ℕ)}, x ∈ acc → x ∈ extFrom l n acc := by
  intro n
  induction n with
  | zero => intro acc h; exact h
  | succ n ih =>
    intro acc h
    show x ∈ extFrom l n (bif compat n l 1 then (n :: l) :: acc else acc)
    apply ih
    cases compat n l 1
    · exact h
    · exact List.mem_cons_of_mem _ h

lemma mem_extFrom {l : List ℕ} {v : ℕ} (hv : compat v l 1 = true) :
    ∀ (n : ℕ) {acc : List (List ℕ)}, v < n → (v :: l) ∈ extFrom l n acc := by
  intro n
  induction n with
  | zero => intro acc h; omega
  | succ n ih =>
    intro acc h
    show v :: l ∈ extFrom l n (bif compat n l 1 then (n :: l) :: acc else acc)
    rcases Nat.lt_succ_iff_lt_or_eq.mp h with h | rfl
    · exact ih h
    · apply mem_extFrom_of_mem
      rw [hv]
      exact List.mem_cons_self

lemma mem_step {k v : ℕ} {l : List ℕ} (hv : v < k) (hc : compat v l 1 = true) :
    ∀ L : List (List ℕ), l ∈ L → (v :: l) ∈ step k L := by
  intro L
  induction L with
  | nil => intro h; simp at h
  | cons l' L ih =>
    intro h
    show v :: l ∈ extFrom l' k (step k L)
    rcases List.mem_cons.mp h with rfl | h
    · exact mem_extFrom hc k hv
    · exact mem_extFrom_of_mem k (ih h)

lemma good_of_allGood {l : List ℕ} : ∀ L : List (List ℕ), allGood L = true → l ∈ L →
    good l = true := by
  intro L
  induction L with
  | nil => intro _ h; exact absurd h List.not_mem_nil
  | cons l' L ih =>
    intro hL h
    change (good l' && allGood L) = true at hL
    cases hg : good l'
    · rw [hg, Bool.false_and] at hL; exact Bool.noConfusion hL
    · rw [hg, Bool.true_and] at hL
      cases h with
      | head => exact hg
      | tail _ h => exact ih hL h

lemma check_of_checksUpTo {K : ℕ} (hK : checksUpTo K = true) {k : ℕ} (h1 : 1 ≤ k)
    (h2 : k ≤ K) : check k = true := by
  induction K with
  | zero => omega
  | succ K ih =>
    have hK' : checksUpTo K = true ∧ check (K + 1) = true := by
      simpa only [Bool.and_eq_true] using
        (show (checksUpTo K && check (K + 1)) = true from hK)
    rcases Nat.lt_succ_iff_lt_or_eq.mp (Nat.lt_succ_of_le h2) with h | rfl
    · exact ih hK'.1 (by omega)
    · exact hK'.2

/-- The values of `σ` as a function on `ℕ` (0 outside `[0, k)`). -/
def vals {k : ℕ} (σ : Equiv.Perm (Fin k)) (i : ℕ) : ℕ :=
  if h : i < k then (σ ⟨i, h⟩ : ℕ) else 0

/-- The first `n` values of `σ`, last first. -/
def pre {k : ℕ} (σ : Equiv.Perm (Fin k)) : ℕ → List ℕ
  | 0 => []
  | n + 1 => vals σ n :: pre σ n

lemma pairOK_of_wc {k : ℕ} {σ : Equiv.Perm (Fin k)} (h : IsWeaklyConsecutive σ)
    {n q : ℕ} (hq : q < n) (hn : n < k) :
    pairOK (vals σ n) (vals σ q) (n - q) = true := by
  have hqk : q < k := by omega
  simp only [vals, hn, hqk, ↓reduceDIte]
  set i : Fin k := ⟨n, hn⟩
  set j : Fin k := ⟨q, hqk⟩
  have hij : i ≠ j := by
    intro e; have := congrArg Fin.val e; simp [i, j] at this; omega
  have hne : (σ i : ℕ) ≠ (σ j : ℕ) := fun e => hij (σ.injective (Fin.ext e))
  have hd : ∀ g : ℕ, g ∣ n - q →
      (g : ℤ) ∣ (((i : ℕ) + 1 : ℕ) : ℤ) - (((j : ℕ) + 1 : ℕ) : ℤ) ∧
      (g : ℤ) ∣ (((j : ℕ) + 1 : ℕ) : ℤ) - (((i : ℕ) + 1 : ℕ) : ℤ) := by
    intro g hg
    have e : (((i : ℕ) + 1 : ℕ) : ℤ) - (((j : ℕ) + 1 : ℕ) : ℤ) = ((n - q : ℕ) : ℤ) := by
      simp [i, j]; omega
    have h1 : (g : ℤ) ∣ (((i : ℕ) + 1 : ℕ) : ℤ) - (((j : ℕ) + 1 : ℕ) : ℤ) := by
      rw [e]; exact Int.natCast_dvd_natCast.mpr hg
    refine ⟨h1, ?_⟩
    have := dvd_neg.mpr h1; simpa using this
  have g1 : Nat.gcd (n - q) ((σ i : ℕ) + 1) ∣ Nat.gcd (n - q) ((σ j : ℕ) + 1) := by
    refine Nat.dvd_gcd (Nat.gcd_dvd_left _ _) ?_
    have := h i j _ (Int.natCast_dvd_natCast.mpr (Nat.gcd_dvd_right _ _))
      (hd _ (Nat.gcd_dvd_left _ _)).1
    exact Int.natCast_dvd_natCast.mp this
  have g2 : Nat.gcd (n - q) ((σ j : ℕ) + 1) ∣ Nat.gcd (n - q) ((σ i : ℕ) + 1) := by
    refine Nat.dvd_gcd (Nat.gcd_dvd_left _ _) ?_
    have := h j i _ (Int.natCast_dvd_natCast.mpr (Nat.gcd_dvd_right _ _))
      (hd _ (Nat.gcd_dvd_left _ _)).2
    exact Int.natCast_dvd_natCast.mp this
  have := Nat.dvd_antisymm g1 g2
  simp only [pairOK, Bool.and_eq_true, Bool.not_eq_true', this]
  cases hb : Nat.beq (σ i : ℕ) (σ j : ℕ)
  · exact ⟨rfl, Nat.beq_refl _⟩
  · exact absurd (Nat.eq_of_beq_eq_true hb) hne

lemma compat_pre {k : ℕ} {σ : Equiv.Perm (Fin k)} (h : IsWeaklyConsecutive σ) {n : ℕ}
    (hn : n < k) : ∀ j d, j + d = n + 1 → 1 ≤ d → compat (vals σ n) (pre σ j) d = true := by
  intro j
  induction j with
  | zero => intro d _ _; rfl
  | succ j ih =>
    intro d hjd hd
    show (pairOK (vals σ n) (vals σ j) d && compat (vals σ n) (pre σ j) (d + 1)) = true
    rw [Bool.and_eq_true]
    refine ⟨?_, ih (d + 1) (by omega) (by omega)⟩
    have : d = n - j := by omega
    subst this
    exact pairOK_of_wc h (by omega) hn

/-- Completeness of the enumeration: every weakly consecutive `σ` survives the pruning. -/
lemma mem_level {k : ℕ} {σ : Equiv.Perm (Fin k)} (h : IsWeaklyConsecutive σ) :
    ∀ n, n ≤ k → pre σ n ∈ level k n := by
  intro n
  induction n with
  | zero => intro _; exact List.mem_singleton_self _
  | succ n ih =>
    intro hn
    show vals σ n :: pre σ n ∈ step k (level k n)
    exact mem_step
      (by unfold vals; rw [dif_pos (show n < k by omega)]; exact (σ _).isLt) (compat_pre h (by omega) n 1 (by omega) le_rfl) _
      (ih (by omega))

/-- If the kernel-checked enumeration `check k` succeeds, Conjecture 5.2 holds for length `k`. -/
theorem conj52_of_check (k : ℕ) (hk : 0 < k) (hc : check k = true)
    (σ : Equiv.Perm (Fin k)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, hk⟩ = ⟨0, hk⟩ ∨ σ ⟨k - 1, by omega⟩ = ⟨0, hk⟩ := by
  have getLast?_pre : ∀ n, (pre σ (n + 1)).getLast? = some (vals σ 0) := by
    intro n
    induction n with
    | zero => rfl
    | succ n ih => exact ih
  have := good_of_allGood _ hc (mem_level h k le_rfl)
  obtain ⟨k', rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
  simp only [good, Bool.or_eq_true, beq_iff_eq, getLast?_pre] at this
  simp only [pre, List.head?_cons, Option.some.injEq, vals] at this
  simp only [Nat.lt_add_one_iff, zero_le, ↓reduceDIte, lt_add_iff_pos_left] at this
  rcases this with h1 | h1
  · right; ext; simpa using h1
  · left; ext; simpa using h1

/-- Kernel evaluation of the enumerator for every length `k ∈ [1, 16]` (`decide +kernel`, so the
kernel itself reduces `checksUpTo 16` to `true`; no `native_decide`). -/
lemma checksUpTo_16 : checksUpTo 16 = true := by decide +kernel

/-- **Conjecture 5.2 of [GSK24] for `1 ≤ k ≤ 16`.** Every weakly consecutive permutation `σ` of
`[k]` has `σ(1) = 1` or `σ(k) = 1` (0-indexed: `σ 0 = 0` or `σ (k - 1) = 0`). -/
theorem conjecture_5_2_le_16 (k : ℕ) (hk : 0 < k) (hk16 : k ≤ 16)
    (σ : Equiv.Perm (Fin k)) (h : IsWeaklyConsecutive σ) :
    σ ⟨0, hk⟩ = ⟨0, hk⟩ ∨ σ ⟨k - 1, by omega⟩ = ⟨0, hk⟩ :=
  conj52_of_check k hk (check_of_checksUpTo checksUpTo_16 hk hk16) σ h

end WeaklyConsecutive
