# Pass 9: Lemma S tested directly, and refuted for general downsets

Status: written 2026-11-27 (explorer pass 9, Lemma S strategy). Not /reviewed. Notation as in
`pass8_level.md`: T a finite downset of N^k with 0 ∈ T, |T| = p·m, g: Z^k → Z_m a homomorphism
whose fibres on T all have size p, M = ⟨x − y : x, y ∈ T, g(x) = g(y)⟩, Γ = Z^k/M.
Lemma S: exp(Γ_p) ≤ p^{v_p(m)}. Lemma K: ḡ injective on Γ_tors. Scripts and outputs are in
`pass9_lemmaS/` (commands below are run from there).

## 0. Verdict

1. **Lemma S and Lemma K, as stated in pass 8 (for all downsets), are false**
   [numerical, certified by an independent sympy check]. Counterexample (p = 2, m = 5, k = 5,
   |T| = 10): T = {0, e5, e4, 2e4, e3, e2, 2e2, e1, e1+e3, 2e1}, g = (1, 2, 4, 3, 3).
   - Fibres: {0, e1+e3}, {e1, 2e4}, {e2, 2e1}, {e3, 2e2}, {e4, e5}.
   - Γ = Z^5/M ≅ Z_10 (SNF 1,1,1,1,10), so Γ_2 = Z_2 ≠ 0 although 2 ∤ 5; ḡ kills Γ_2 (Lemma K
     fails too).
   - By hand: e5 = e4, e1 = 2e4, e2 = 2e1 = 4e4, e3 = 2e2 = 8e4 and e3 = −e1 = −2e4, so 10e4 = 0.
   - The **per-partition level bound fails too**: for this (𝒫, g) an admissible f exists and the
     minimal level is exactly 1 > v_2(5) = 0 (brute force over F: Z^5 → Z_2, Z_4). The set T
     itself does admit a level-0 bijection ψ: Z^5 → Z_10 (32 of them) via other partitions.
   - Certificate: `cex_downsets.json`; checker `cex_downset_check.py` (sympy SNF + brute force,
     shares no code with the search).
   - So the pass-8 corollary route ("Lemma S for downsets ⇒ level ≤ v_p(n/p)") cannot be proved
     from the downset property alone; any proof must use more structure of T_n.
2. **A second counterexample is midpoint-convex** (x, y ∈ T, (x+y)/2 ∈ Z^k ⇒ (x+y)/2 ∈ T), k = 6:
   T = {0, e6, e5, e4, e3, e3+e5, e2, e2+e6, e1, 2e1}, g = (1, 2, 4, 1, 4, 3), Γ ≅ Z ⊕ Z_2.
   So midpoint convexity does not rescue it.
3. **Refined conjecture S′ [conjecture]:** Lemma S holds for *shifted* downsets
   (x ∈ T, i < j, x_j > 0 ⇒ x − e_j + e_i ∈ T). T_n is shifted (replace a prime factor by a
   smaller prime), and so is every threshold set {x : w·x ≤ 1} with w sorted. Neither
   counterexample is shifted under any coordinate order (both contain 2e_a, 2e_b with
   e_a + e_b ∉ T).
4. **T_195 itself: no violation found, space NOT exhausted** (sampling only; §2).
5. No proof of S′. §3 records what is proved and where the argument stops.

## 1. Evidence table [numerical]

General / restricted downset classes, every g exhaustively for each sampled T
(`all_g` DFS over Z_m^k), violation = log_p exp(Γ_p) > v_p(m):

| class | runs (p, m, k) | pairs (T, g) | violations |
|---|---|---|---|
| random downsets | (2,5,6), (2,7,6–8), (2,5,5–8), (3,5,6), (3,5,8) | ~10^5 | yes, p = 2 and p = 3 |
| midpoint-convex | (2,7,7), (2,5,8) | ~4·10^4 | 108 + 48 |
| threshold w·x ≤ 1 | (2,5,5), (2,5,6), (2,7,6), (2,7,7), (3,5,6) | 429 786 | 0 |
| shifted | (2,5,6), (2,7,7), (2,5,8), (3,5,7), (2,4,6), (2,6,7), (3,3,7), (2,8,7), (3,2,8), (5,3,8) | 220 389 | 0 |

Commands: `python ds_highdim.py p m k trials seed`, `python ds_convex.py …`,
`python ds_threshold.py …`, `python ds_shifted.py …` (arguments as in the table; seeds in
`out/shifted_more.txt` and the journal). The shifted runs include p | m cases (m = 4, 6, 8, 3),
where the bound v_p(m) was also never exceeded.

**T_n exhaustive** (`lemS.py exh n p`, sweep output `out/exh_Tn_sweep.txt`): every g with all
fibres of size p on T_n (g(2) restricted to divisors of m — unit symmetry, which preserves M),
for **every n ≤ 42 and every prime p | n with p < n** (n = 44 was not finished): 0 violations. Largest: n = 42, p = 2:
371 699 maps g, all with Γ_2 = 0; n = 40, p = 2 (m = 20): 185 360 maps, max level 2 = v_2(20).
For p | m the bound v_p(m) is attained (n = 16, 24, 27, 32, 40, …).

## 2. T_195 directly

Space: maps g: Z^44 → Z_m (m = 195/p) with every fibre on T_195 of size p. By Lemma R (§3) only
the 25 primes q ≤ 97 matter; the 19 primes 101…193 occur in exactly one number and only fill holes.

- **Random sampling** (`python lemS.py rand 195 p N seed out.json`, randomized DFS restarts,
  node cap 2·10^5 per restart): p = 3: 400 samples; p = 5: 600 samples; p = 13: 1000 samples. All have
  Γ_13 = 0. Outputs `out/rand195_p*.txt/json`.
- **Targeted search** (`python lemS_target.py rand 195 p 40 seed 100000`): every violation has a
  nonzero block-constant h: Z^k → F_p (Lemma E, §3), so this DFS assigns (h(q), g(q)) jointly
  and requires every g-class to have one h-value. Hits (g, h) do occur, but in every hit h lifts
  (Γ_p = 0). Earlier short runs (5 restarts, cap 2·10^5) gave 4 hits at p = 3 and 5 at p = 13, all with Γ_p = 0. The 40-restart run (`out/target195.txt`) was killed at the time limit before it printed anything, so it does not count.
- **Exhausted: nothing** at n = 195. The searched space is a biased sample. The DFS with
  increasing-prime order and random value order is not uniform over the solution set.
- **Cross-check:** `check_indep.py` (sympy `factorint` + `smith_normal_form`, full M from all
  pairs, no singleton reduction) agrees per sample with `lemS.py` on 1600 T_n samples with
  nonzero exponents (n = 24, 32 at p = 2; n = 27 at p = 3; n = 40 at p = 5) and on the first 100
  T_195 samples per p (`out/rand195_p*.txt`).

## 3. What is proved, and where it stops [own argument, unreviewed]

**Lemma R (singleton reduction).** Suppose coordinate q is nonzero at exactly one point of T,
namely e_q, and e_q lies in block B. Then the torsion of Γ is unchanged if we delete e_q from T
and keep only the relations among B ∖ {e_q}.
*Proof.* B has p ≥ 2 points, so choose b_0 ∈ B ∖ {e_q} and use the generators b − b_0 (b ∈ B)
for the B-relations. v = e_q − b_0 is the only generator of M with a nonzero q-coordinate, and
that coordinate is 1. So Z^k = Zv ⊕ {x_q = 0} and M = Zv ⊕ M', where M' is generated by the
remaining generators, all of which lie in {x_q = 0}. Hence Γ ≅ Z^{k−1}/M'. M' is exactly the
relation lattice of T ∖ {e_q} with the induced blocks (B ∖ {e_q} keeps its relations b − b_0).
Iterating over all singleton coordinates gives the reduction. When a block consists only of
singletons, the last one leaves a free Z summand, which carries no torsion. ∎ This justifies the 25-prime reduction at n = 195 and the hole-filling in `lemS.py`.

**Lemma E.** Γ_p = 0 iff every F_p-linear h: Z^k → F_p that is constant on blocks is the
reduction of a Z-linear H: Z^k → Z that is constant on blocks.
*Proof.* Γ = Z^r ⊕ Tor. Hom(Γ, F_p) = F_p^r ⊕ Hom(Tor, F_p). The image of Hom(Γ, Z) is the
first summand, and Hom(Tor, F_p) = 0 iff p ∤ |Tor|. ∎
Equivalently, h|_T = φ∘g for some φ: Z_m → F_p with φ(0) = 0, and the downset gives partial
additivity: φ(g(x) + g(e_i)) = φ(g(x)) + φ(g(e_i)) whenever x, x + e_i ∈ T.

**Where it stops.**
- The counterexamples show that partial additivity plus equal fibres do not force h to lift. In
  cex1, φ is the parity character of the Z_10 = Z_2 × Z_5 structure. It is additive along every
  edge x → x + e_i of T, but there is no rational lift.
- The obstruction uses chains 2e_a ~ e_b ("q² in the block of r") closed by a relation
  e_a + e_c ~ 0. Shiftedness forces e_a + e_b ∈ T whenever 2e_b ∈ T and a < b. This adds edges,
  hence more additivity constraints on φ. I could not turn this into a proof that φ lifts.
- Induction on |T| (removing a maximal element together with its block) fails as stated. The
  smaller set is generally not shifted, and g no longer has equal fibres on it.
- **Open:** S′ for shifted downsets with p ∤ m, or for T_n only. That is the exact statement the
  pass-8 corollary needs, and only for the partitions that carry an admissible f.

## 4. Consequences for the project

- The pass-8 "level ≤ v_p(n/p)" bound is not refuted for T_n: the T_n data and the shifted data
  are all consistent with it. Its proposed proof route is wrong in generality, though. "Downset"
  must be replaced by "shifted downset" (or T_n), and pass8_level.md §2 should say so.
- The n = 195 prime-power exclusion still rests on the explicit level-1/2/3 NONE searches, not on
  Lemma S.
