# NOTES: minimum modulus for valid residue sets (Fonollosa, Conjecture 1)

Problem P3 of `PROBLEMS.md`, issue #86 (part of #23). Slug `min-modulus`.

Labels: [Lean], [Lean | hyp: …], [paper: ref, Thm], [preprint: ref, Thm], [standard: ref],
[numerical ± err], [conjecture], [own argument, unreviewed]. See `.claude/skills/prove/SKILL.md`.

Reference: **[Fon26]** José A. R. Fonollosa, "Minimum modulus for the unique multiset-sum
problem", arXiv:2607.08366, v1 9 Jul 2026, v2 14 Jul 2026 (no v3 as of 2026-11-27), math.CO,
8 pages, unrefereed. https://arxiv.org/abs/2607.08366 (read: abs page and HTML v2).

## Statement

Fix n ≥ 2. A = {a_0 < … < a_{n−1}} ⊆ ℤ_N, p := Σ a_i mod N. A is **valid mod N** if the only
k ∈ ℤ_{≥0}^n with Σ k_i = n and Σ k_i a_i ≡ p (mod N) is k = (1, …, 1).

**Target, Conjecture 1 of [Fon26] (§1):** "For every n ≥ 2 and every N < 2^n − 2^floor(log_2 n),
no set of n residues is valid mod N;" [conjecture] [preprint: Fon26, Conj. 1]

The bound is attained: {2^k − 1 : 0 ≤ k ≤ n−1} is valid mod 2^n − 2^⌊log₂ n⌋
[preprint: Fon26, Thm A; author's Lean proof `nmin_eq` in jarfo/min-modulus, not re-checked here].
So Conjecture 1 says the least valid modulus over all n-sets is exactly 2^n − 2^⌊log₂ n⌋:
2, 6, 12, 28, 60, 124, 248, 504, … for n = 2, 3, 4, … .

**Note on the sub-issue.** For n = 8 the bound is 2^8 − 2^3 = **248**, not 252 (252 = 2^8 − 2^2).
Issue #87 ("certify n = 8, every N < 252") should read N < 248: {2^k − 1 : k < 8} is valid
mod 248 (N3 below), so "no valid set for N < 252" is false.
[numerical, exact; and arithmetic]

## Setting

- Translation invariance: replacing A by A + t shifts both sides by n·t, so WLOG 0 ∈ A; scaling by
  a unit of ℤ_N also preserves validity. [own argument, reviewed 2026-11-27 (one line each)]
- [Fon26] Lemma 1 (§3), quoted: "A is valid mod N if and only if no balanced c has N | V(c)."
  Here c = k − (1, …, 1), "balanced" means c_i ≥ −1, Σ c_i = 0, c ≠ 0, and (for a_i = 2^i − 1)
  V(c) := Σ c_i 2^i. [preprint: Fon26, Lemma 1] (as relayed; see Literature caveat)

## Claims ledger

| Claim | Label | Where |
|---|---|---|
| Conjecture 1 (all n ≥ 2) | [conjecture] [preprint: Fon26, Conj. 1] | Statement |
| {2^k − 1} is valid mod 2^n − 2^⌊log₂ n⌋ and invalid mod every smaller N' ≥ 2 | [preprint: Fon26, Thms A, B]; Lean proof by the author (jarfo/min-modulus), not re-checked here | L1 |
| Conjecture 1 holds for n ≤ 7 | [preprint: Fon26, §7, CP-SAT infeasibility certificates] (certificates not re-checked here) | L1 |
| No counterexample for n ≤ 13 | [preprint: Fon26, §7, solver and GPU search, not a certificate] | L1 |
| Every valid n-family in a finite abelian group G has \|G\| ≥ 2^{n−1}; hence N ≥ 2^{n−1} | [preprint: Inal, OSF 10.17605/OSF.IO/C58Q9] (not accessed; reported by jarfo/min-modulus, Sun16z/min-modulus-gap and vasilyshablov/Special_Project, each with a Lean proof, none re-checked here) | L3 |
| Conjecture 1 for n = 3, 4, 5 (kernel) and n = 6 (`native_decide`); N ≥ 2^{n−1} + 2^{n−1}/(72(n−1)√((n−1)ln n)) for n ≥ 3 | [preprint: Sun16z/min-modulus-gap README, Zenodo 10.5281/zenodo.24586140] (Lean per the README, 2026-11-27; not re-checked here) | L4 |
| Least valid modulus over all n-sets is 2, 6, 12, 28 for n = 2, 3, 4, 5 (matches conjecture) | [numerical, exact exhaustive search; Python, not Lean] | N1 |
| {2^k − 1} has least valid modulus 2^n − 2^⌊log₂ n⌋ for 2 ≤ n ≤ 9 | [numerical, exact; Python] | N2 |
| Issue #87's bound 252 should be 248 | [numerical, exact] + arithmetic | Statement |
| Conjecture 1 not found resolved for n ≥ 8 in the works searched | [conjecture]; literature search, scope as recorded | Literature, Verdict |
| Validity is invariant under translation and under scaling by a unit of ℤ_N | [own argument, reviewed 2026-11-27] | Setting |
| [Fon26] Lemma 1: A valid mod N iff no balanced c has N \| V(c) | [preprint: Fon26, Lemma 1] (as relayed) | Setting |
| formal-conjectures `min_modulus` matches [Fon26] Conjecture 1 (no mismatch of substance) | [own argument, unreviewed] | L2 |
| {2^k − 1 : k < 8} is valid mod 248 | [numerical, exact] | N3 |

## Literature (2026-11-27)

Caveat: the fetch agent could quote at most 125 characters per passage from the arXiv HTML, so
long statements of [Fon26] below are verbatim fragments, joined as the agent relayed them. The
definition is cross-checked against the formal-conjectures Lean text (L2), which is quoted in full.
Spot-check of Fon26 §6 against the HTML directly: not done.

**L1. [Fon26].**
- Abstract: "Fix n >= 2. A set A = {a_0 < a_1 < ... < a_{n-1}} of n residues in Z_N is "valid
  mod N" if the all-ones multiset is the only size-n multiset drawn from A whose sum is
  p := sum_i a_i (mod N)." Also: "We conjecture that no size-n residue set admits a smaller valid
  modulus."
- §2 Definition: "A is valid mod N if the only k ≥ 0 with sum_i k_i = n and sum_i k_i a_i ≡ p
  (mod N) is k = (1,1,...,1)." (relayed as condensed from a display) Multisets: "A size-n multiset
  with elements from A is encoded by its multiplicity vector k = (k_0,...,k_{n-1}) ∈ Z_{≥0}^n with
  sum_i k_i = n."
- Conjecture 1 (§1): "For every n ≥ 2 and every N < 2^n − 2^floor(log_2 n), no set of n residues
  is valid mod N;" … "that is, the super-increasing set attains the least valid modulus over all
  size-n sets."
- Theorem A (§5, upper bound): A = {2^k − 1 : 0 ≤ k ≤ n−1}, m := ⌊log₂ n⌋, is valid mod
  N = 2^n − 2^m for every n ≥ 2. Key step, Lemma 4: "Let 0 ≤ t ≤ n−1 and N_t := 2^n − 2^t. Then
  for every M ≥ 0, s_min(M+N_t) ≥ s_min(M)+1." Lemma 3: "s_min(M) = floor(M/2^{n−1}) +
  popcount(M mod 2^{n−1})" (s_min = least number of coins 2^0, …, 2^{n−1} summing to M).
- Theorem B (§6, the fixed set only): "For every n ≥ 2 and every 2 ≤ N' < 2^n − 2^m, the
  super-increasing set is invalid mod N'." Via Proposition 1: "For an integer V ≠ 0 there is a
  balanced c with V(c) = V if and only if," with M := V + (2^n − 1), "n ≤ M and s_min(M) ≤ n."
  Lemma 2: "No balanced c has V(c) = 0." The paper proves no lower bound for arbitrary sets.
- §1 values: "2, 6, 12, 28, 60, 124, 248, 504, 1016, 2040, 4088, 8184" for n = 2, …, 13.
- §7 computation: "This certifies Conjecture 1 outright for n ≤ 7;" (CP-SAT, A left free, "one
  infeasibility certificate per modulus"); "for n ≤ 13, extensive solver- and GPU-search finds
  valid sets at N = 2^n − 2^m and none below, and every minimal-modulus solution found
  canonicalizes, under translation and unit scaling, to the super-increasing set."
- Open problems (relayed as §8, "Problem 1"; the task brief called this §7): "Global optimality
  (Conjecture 1): prove that no size-n residue set is valid below 2^n − 2^floor(log_2 n)." "Even
  an exponential lower bound N_min ≥ c^n valid for all sets appears to be open." "The case
  analysis of Section 6 uses the binary structure of the fixed set throughout; a set-free argument
  would need a different mechanism." Problem 2: "Is the minimal-modulus solution unique up to
  translation and unit scaling for all n?" Problem 4: whether 2^{n−1} is the least order over all
  finite abelian groups "is open"; Proposition 2: "If g_0,…,g_{n−1} ∈ (Z_2)^k have unique multiset
  sums, then k ≥ n−1." Cited group bound: "(2n choose n)/2^n ∼ 2^n/sqrt(pi n)" from the companion
  paper arXiv:2607.09949 (not fetched).
- Motivation: "Since the cost is governed by N, one wants the smallest modulus for which some
  exponent set has this property." (computing the permanent by a size-N transform)

**L2. formal-conjectures** `FormalConjectures/Arxiv/2607.08366/MinModulus.lean` (read via the
GitHub API 2026-11-27; last commit d9f6ffa8, 2026-10-29). Definition and target, verbatim:

```lean
def IsValidMod (A : Finset (ZMod N)) : Prop :=
  ∀ m : ZMod N → ℕ, ∑ a ∈ A, m a = #A → ∑ a ∈ A, (m a : ZMod N) * a = ∑ a ∈ A, a →
    ∀ a ∈ A, m a = 1

def minModulus (n : ℕ) : ℕ := 2 ^ n - 2 ^ (Nat.log 2 n)

@[category research open, question, AMS 11]
theorem min_modulus :
    ∀ n N : ℕ, 2 ≤ n → 0 < N → N < minModulus n →
      ∀ A : Finset (ZMod N), #A = n → ¬ IsValidMod A := by
  sorry
```

Theorem A is there as `exists_isValidMod_minModulus`, tagged `research solved` with a
`formal_proof` link to jarfo/min-modulus. Mismatch check against [Fon26]: none of substance.
The Lean adds `0 < N` (the file explains that `ZMod 0 = ℤ` would make `{1, 2}` valid); for N < n
there is no n-element Finset, so those N are vacuous in both; `Nat.log 2 n` = ⌊log₂ n⌋; a
multiplicity function on ZMod N restricted to A is the paper's vector k.
[own argument, unreviewed]

**L3. Inal, OSF preprint 10.17605/OSF.IO/C58Q9 (Jul 2026)**, not accessed. As reported by
jarfo/min-modulus (README, `MinModulus/AbelianMin.lean`, commits 2026-07-22/24) and by
vasilyshablov/Special_Project (README, 2026-10-09): |G| ≥ 2^{n−1} for every finite abelian G
carrying a valid n-family, equality iff G ≅ (ℤ/2)^{n−1}. This answers [Fon26] Problem 4 and gives
N ≥ 2^{n−1} for cyclic G. 2^{n−1} ≥ (√2)^n for n ≥ 2, so if Inal's bound holds (not re-checked
here), the §8 remark that an exponential lower bound "appears to be open" is out of date. Vasilyshablov's README gives a one-paragraph proof
("anchor argument": for fixed j the 2^{n−1} elements t + Σ_{i∈S}(g_j − g_i), S ⊆ [n]∖{j}, are
pairwise distinct). s66lem/conjectures (README 2026-11-25) claims the same plus
N ≥ 2^{n−1} + ⌈n/gcd(2, N)⌉ − 1. [none re-checked here]

**L4. Sun16z/min-modulus-gap** (created 2026-11-27 10:21 UTC, pushed 12:59 UTC; Zenodo
10.5281/zenodo.24586140; AI-assisted, per its README). Claims, Lean-checked per the README, none
re-checked here: for n ≥ 3 and valid A ⊆ ℤ_N, N ≥ 2^{n−1} + 2^{n−1}/(72(n−1)√((n−1) ln n));
Conjecture 1 for n = 3, 4 (conceptual), n = 5 (`decide +kernel`, 47,081 cases at N = 24..27),
n = 6 (`native_decide`, N = 42..59). Its README: "It does **not** resolve the full Conjecture 1".
formal-conjectures issue #8415 and PR #8416 (both opened 2026-11-27, open) propose adding the
n = 3, 4 and lower-bound variants.

**L5. Others seen.** Kuberwastaken/c5-k4 (2026-08-14): bounded search, "NO COUNTEREXAMPLE". Many
mirrors/audits of the formal-conjectures file (BoltonBailey, tadamcz, LeanPool, competemath, …);
not read.

**Search scope (2026-11-27).** arXiv abs page of 2607.08366 (versions); arXiv HTML v2 full text;
web search "unique multiset-sum" minimum modulus Fonollosa (found only the paper and unrelated
unique-sums papers); GitHub API: formal-conjectures file, its commit history, issues/PRs matching
"2607.08366" and "MinModulus"; `gh search repos min-modulus`; `gh search code 2607.08366` (first
30 hits); READMEs of jarfo/min-modulus (commit list), Sun16z/min-modulus-gap,
s66lem/conjectures, vasilyshablov/Special_Project, Kuberwastaken/c5-k4.
Not accessed: Inal's OSF preprint; companion arXiv:2607.09949; v1 of [Fon26]; Semantic
Scholar/Google Scholar citation lists; MathOverflow.

**Verdict.** No resolution of Conjecture 1 for n ≥ 8 found in the works searched (scope above)
(n ≤ 7 by the paper's CP-SAT certificates; n ≤ 6 also by third-party Lean). Claimed general lower
bound (L3, L4, not re-checked): 2^{n−1}(1 + o(1)), about half the conjecture. The area is crowded:
several groups have posted related work (L3–L5), one on 2026-11-27 itself. Sub-issue #88 (general lower bound) overlaps L3/L4 directly;
any bound we prove must beat 2^{n−1} + 2^{n−1}/(72(n−1)√((n−1) ln n)) to be worth stating.
Novelty of anything we prove is at most "not found in the works searched".

## Numerics

Script `search/min-modulus/minmod.py` (run `python -I minmod.py 5`, about 1 s). Exhaustive over
sets containing 0 (translation, Setting) and all multiplicity vectors.

- **N1.** Least N for which some n-set is valid mod N: n = 2: 2; n = 3: 6; n = 4: 12; n = 5: 28.
  All equal 2^n − 2^⌊log₂ n⌋; the first valid set found (lexicographic) is {0, 1, 3, …, 2^{n−1}−1}.
  [numerical, exact]
- **N2.** For A = {2^k − 1}, the least N at which A mod N has n distinct elements and is valid is
  2^n − 2^⌊log₂ n⌋ for every 2 ≤ n ≤ 9. Agrees with [Fon26] Thms A and B. [numerical, exact]
- **N3.** In particular {2^k − 1 : k < 8} is valid mod 248 (N2 at n = 8). Whether it stays valid at
  249–251 was not checked, but validity at 248 already shows the conjecture's threshold is 248.
  [numerical, exact]
- Scale for n = 8: naive enumeration has C(247, 7) ≈ 1.0·10^13 sets per modulus, so #87 needs
  heavy symmetry reduction (translation, unit scaling, negation) and pruning (Sun16z's prefix
  pruning, L4) or a SAT/CP certificate.

## Attack ideas

- **#87, n = 8, every N < 248.** The paper's CP-SAT certifies n ≤ 7; L4 does n ≤ 6 in Lean.
  N < 2^7 = 128 is covered by L3's claimed bound; L3's reported equality case (|G| = 2^{n−1} only
  for G ≅ (ℤ/2)^{n−1}) also excludes the cyclic N = 128. L4's additive term is
  128/(72·7·√(7 ln 8)) ≈ 0.07, so it too gives only N ≥ 129. Relying on these claimed, not
  re-checked results (L3 alone suffices), the range to do is 129 ≤ N ≤ 247; unconditionally it is
  8 ≤ N ≤ 247.
  (a) Prefix-pruned search over sorted differences 0 < b_1 < … < b_7 < N, as in L4, with
  witnesses (a second multiplicity vector) per leaf, exported as a certificate that a small
  checker (Lean `decide` on chunks, or a verified checker) re-validates. (b) Reduce by unit
  scaling: WLOG gcd(b_1, N) or a chosen difference is normalised. (c) Use the L3/L4 structure
  (2-torsion quotient reduction) to discard N with a large 2-part first.
  Risk: Sun16z went from n = 5 to n = 6 within hours; n = 7, 8 may follow soon. Check before
  starting.
- **#88, general lower bound.** The anchor argument (L3) gives 2^{n−1} distinct elements; the
  conjecture needs about twice that. Leads: count the anchor sets for two anchors j ≠ j' jointly
  and bound their overlap; use the doubles {2(g_j − g_i)}, which s66lem uses for +n/2; Fourier
  (L4's MGF method). Any result must beat L4 to be worth stating.

## Review

- **2026-11-27.** Two independent reviewers (mathematics; claims and citations).
  - M1/C1 (L3, "2^{n−1} = c^n with c = 2" false): fixed; now "2^{n−1} ≥ (√2)^n for n ≥ 2, so if
    Inal's bound holds (not re-checked here), the §8 remark is out of date".
  - M2 (L3's equality case already excludes N = 128): fixed; Attack ideas and LEDGER MM2 now give
    129 ≤ N ≤ 247 from L3 alone, attributed to the claimed, not re-checked results.
  - C2 (Verdict overclaims): fixed; "open for every n ≥ 8" → "no resolution … found in the works
    searched"; lower bound marked claimed, not re-checked; "three independent AI-assisted groups"
    → "several groups have posted related work (L3–L5)".
  - C3 (LEDGER "still open for n ≥ 8"): fixed; now "not found resolved for n ≥ 8 in the works
    searched (notes, Search scope)".
  - C4 (L4 row label invalid): fixed; now [preprint: Sun16z/min-modulus-gap README, Zenodo
    10.5281/zenodo.24586140], not re-checked.
  - C5 (missing ledger rows): fixed; rows added for the openness verdict, translation/unit-scaling
    invariance (now [own argument, reviewed 2026-11-27], checked by the mathematics reviewer),
    Lemma 1, the L2 match check (still unreviewed) and N3.
  - C6 (LEDGER MM2 conditional range): fixed; MM2 states that N < 129 rests on Inal's/L3's claimed
    bound, not re-checked, and that the unconditional target is 8 ≤ N < 248.
  - C7 (PROBLEMS P3 "is known"): fixed; now "is claimed (Inal, OSF preprint, not accessed; reported
    with Lean proofs by third parties, not re-checked)".
  - C8 (PROBLEMS P3 scout lines): fixed; Conjecture 1 quoted as in notes L1, §7 → §8, openness
    evidence marked superseded 2026-11-27, "N < 252" → "N < 248 (corrected 2026-11-27; the scout
    wrote 252)".

## Log

- **2026-11-27.** Literature + setup stage (issue #86, part of #23, branch
  `agent/min-modulus-setup`). Openness re-checked: no v3 of [Fon26]; formal-conjectures still tags
  `min_modulus` `research open` (last commit 2026-10-29); open issue #8415 and PR #8416 there
  (2026-11-27) add n = 3, 4 and a lower bound, not the full conjecture. Found prior lower-bound work
  (Inal 2^{n−1}; Sun16z 2^{n−1}(1 + Θ(1/(n^{3/2}√log n))); n ≤ 6 in Lean) that makes the paper's
  "exponential lower bound appears to be open" out of date. Numerics N1–N3: conjecture holds for
  n ≤ 5 by exhaustive search. Found that #87's bound should be N < 248, not 252.
  [numerical, Python, not Lean] P3 marked `taken (#23)` in `PROBLEMS.md`; LEDGER entry added.
