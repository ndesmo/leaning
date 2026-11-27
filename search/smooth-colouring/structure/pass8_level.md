# Pass 8: bounding the level in (b_i^p)

Status: written 2026-11-27 (explorer pass 8). Not /reviewed. Each claim is labelled. Scripts and
outputs are in `pass8_level/`. Notation is as in `composite_B.md`. T = T_n ⊂ Z^k is the set of
exponent vectors of 1..n, and m = n/p. A partition 𝒫 of T into m blocks of size p is
**separated** if some homomorphism g: Z^k → Z_m is constant on blocks and takes distinct values
on distinct blocks. M is the lattice of within-block differences, Γ = Z^k/M, Γ_p is the p-primary
torsion of Γ, and ḡ: Γ → Z_m is the map induced by g. "Level 0" means a homomorphism
ψ: Z^k → Z_p × Z_m that is bijective on T. When p ∤ m this group is Z_n, so level 0 is outcome (a).

## 0. Verdict

- **I did not prove a bound.** What I did:
  - an exact formula for the level of a given partition (Prop. 1, proved);
  - a conjectured lemma (Lemma K, or the weaker Lemma S) that would bound the level by
    v_p(n/p);
  - strong numerical support for both, with no counterexample found.
- **The conjectured bound is level ≤ v_p(n/p).** For n = 195 we have v_p(195/p) = 0 for every
  p ∈ {3, 5, 13}. So Lemma S for T_195 would turn **every** (b_i^p) into (a), and FP90 excludes
  (a). Every periodic tiling whose m_π is a power of a single prime would then be excluded. The
  existing level-1 searches are consistent with this, though not needed for it.
- **The bound matches all data.** Every [n] case where level 1 fails but a higher level succeeds
  needs **exactly** level v_p(n/p):
  - n = 162, p = 3: level 3 = v_3(54);
  - n = 189, p = 3: level 2 = v_3(63);
  - n = 184, p = 2: level 2 = v_2(92) (new this pass);
  - n = 176, p = 2: level 3 = v_2(88) (new this pass; level 2 is NONE, level 3 FOUND).
  So the bound would be sharp. A bound in terms of log_p n alone would not be.

## 1. Exact level of a partition [own argument, unreviewed]

**Prop. 1.** Fix a separated partition 𝒫, a separating g, and f: M → Z_p with f(x − y) ≠ 0 for all
x ≠ y in a common block. Let i ≥ 0. Then the following are equivalent:
- there is F: Z^k → Z_{p^{i+1}} with F|_M = ι∘f, where ι: Z_p ≅ p^iZ_{p^{i+1}} (so that (F, g)
  is a level-i solution);
- f vanishes on M ∩ p^{i+1}Z^k.

Consequences:
- The least such i is at most **e(𝒫) := log_p exp(Γ_p) = max_r v_p(d_r)**, the maximum over the
  nonzero elementary divisors d_r of M.
- If Γ_p = 0, any admissible f gives level 0.

*Proof.* Take a Smith basis e'_r of Z^k with M = ⊕ d_r Z e'_r, and put c_r = f(d_r e'_r).
- For d_r = 0 there is no condition.
- For d_r = p^v u with p ∤ u, we need p^v F(e'_r) = u^{-1}ι(c_r) ∈ p^iZ_{p^{i+1}}. This is
  solvable iff v ≤ i or c_r = 0.
- On the other hand, M ∩ p^{i+1}Z^k = ⊕ lcm(d_r, p^{i+1}) Z e'_r. On the generator with v ≤ i,
  f takes the value p^{i+1−v}c_r = 0. On the generator with v ≥ i+1 it takes the value c_r.
So both conditions say "c_r = 0 whenever v_p(d_r) ≥ i+1". ∎

This sharpens the Smith-form remark of `composite_B.md` §4: the minimal level depends only on
(𝒫, f), and it is controlled by the p-torsion of Γ. That torsion lives in a group determined by
the blocks alone.

**Lemma 2** [own argument, unreviewed; elementary]. Write [x] for the class of t(x) in Γ.
- If x, x' ∈ T, then [x] = [x'] iff x and x' lie in the same block. So π: T → Γ has the blocks as
  its fibres, and ḡ is a bijection from π(T) onto Z_m.
- Hence ker ḡ ∩ (π(T) − π(T)) = {0}.
- If p ∤ m, then ḡ(Γ_p) = 0, because p is invertible mod m. So no nonzero element of Γ_p is a
  difference [x] − [x'].

## 2. The conjectured lemma and what it gives

> **Pass 10:** Lemma S is false even for T_n: it fails at n = 54, p = 2
> (`pass10_sweep/cex_T54_p2.json`). The level bound would have to use the admissible f. See the journal.

**Lemma K (conjecture).** Let T be a finite downset of N^k containing 0, with |T| = p·m, and let
g: Z^k → Z_m have all fibres on T of size p. Then ḡ is injective on the torsion subgroup of
Γ = Z^k/M.

**Lemma S (weaker conjecture).** exp(Γ_p) ≤ p^{v_p(m)}.

Lemma K implies Lemma S, since then Γ_p embeds in the p-part of Z_m, which is Z_{p^{v_p(m)}}.

**Corollary (conditional)** [own argument, unreviewed, assuming Lemma S for T_n]:
- If (b_i^p) holds for some i, then (b_{v_p(n/p)}^p) holds, where level 0 means a bijective
  ψ: Z^k → Z_p × Z_{n/p}.
- For n = 195: (b_i^p) for some i implies (a).

*Proof.*
1. Theorem 3 of `composite_B.md` turns a (b_i^p) solution into (𝒫, g = ψ_K, f), with 𝒫 separated.
2. Lemma S gives e(𝒫) ≤ v_p(m).
3. Prop. 1 then gives a solution at level ≤ v_p(m).
4. If that level is below v_p(m), lift it with Theorem 1 of `composite_B.md`. Its step (a) ⇒ (b_1)
   works verbatim from level 0 to level 1. ∎

T_n is a downset, because a divisor of a number ≤ n is ≤ n. So the downset hypothesis applies.

**Where the proof breaks.**
- Lemma 2 rules out torsion classes of the form [x] − [x']. It says nothing about torsion classes
  that are not differences of points of T.
- I found no argument that turns the equal-fibre condition on g plus the downset property into
  control of those classes.
- Writing S = π(T) and W = ker ḡ, Lemma 2 shows that S ⊕ W = Γ is a tiling. Lemma K says that W is
  torsion-free. I could not derive this from the character identity
  Σ_{x∈T} χ([x]) = p·Ŝ(χ).
- **The downset hypothesis is essential.** Take T = {0, 4} ⊂ Z, p = 2, m = 1. Then M = 4Z,
  Γ = Z_4 lies in ker ḡ, and the minimal level is 2 > v_2(1) = 0. So any proof must use
  divisor-closure. Pure lattice or elementary-divisor arguments cannot suffice, because they do
  not see it.
- Lemma 2 does use the separation hypothesis. The example "blocks {a, 6a}, {b, 15b}, {c, 10c}"
  would need level ≥ 1 locally, but separation forces 2 into the block of 1, so it cannot occur.
  That is the only mechanism I can prove.

## 3. Numerical evidence

All exact and exhaustive within the stated range unless noted. Commands are run from
`structure/pass8_level/`.

**3a. Minimal level for every downset** [numerical: `downset_levels.py`, brute force over all g, F].
- Downsets tested:
  - N², size ≤ 18 for p = 2, ≤ 15 for p = 3 and 5, ≤ 14 for p = 7;
  - N³, size ≤ 12 for p = 2 and 3.
- **No case has minimal level > v_p(m).** Where level 0 was tested, every downset with p ∤ m that
  is solvable at any searched level is solvable at level 0. Level 0 was tested for:
  - N², p = 2, size ≤ 18;
  - N², p = 3, size ≤ 12 (a separate 300 s run, not saved);
  - N², p = 5, size ≤ 15;
  - N³, p = 2 and 3, size ≤ 12.
  For p = 7, and for N² with p = 3 at sizes 13–15, only levels ≥ 1 were run. There every solvable
  p ∤ m case is solvable at level 1.
- The 415 unsolvable p = 2, p ∤ m downsets of N² have no solution at levels 1–4 either.
- For p | m the maximal level v_p(m) is attained. Examples:
  - the chain {0..7}, p = 2, m = 4: level 2;
  - 55 downsets with m = 8: level 3.
- Commands, outputs `ds*.out`:
  - `python downset_levels.py 2 18 3 2 2 0`
  - `python downset_levels.py 2 18 4 2`
  - `python downset_levels.py 2 15 3 3`
  - `python downset_levels.py 2 15 2 5 5 0`
  - `python downset_levels.py 3 12 2 2,3 2 0`
  - `python downset_levels.py 3 12 3 2`
  - `python downset_levels.py 3 12 2 3`
  - `python downset_levels.py 2 14 3 2,3,5,7` (`ds2_14.out`)

**3b. Lemma S and Lemma K on downsets** [numerical: `saturation_test.py`, `kernel_test.py`].
- Every pair (T, g) with all fibres of size p was tested:
  - Lemma S: 5239 pairs (N², size ≤ 18, p = 2, 3, 5) and 26826 pairs (N³, size ≤ 12, p = 2, 3);
  - Lemma K: 1932 pairs (N², size ≤ 14, block sizes 2, 3, 4, 5).
- **0 violations.**
- Commands:
  - `python saturation_test.py 2 18 2,3,5` (`sat2_18.out`)
  - `python saturation_test.py 3 12 2,3` (`sat3.out`)
  - `python kernel_test.py 2 14 2,3,4,5`

**3c. Lemma K on real [n] witnesses** [numerical: `lemmaK_witness.py`, own Smith form
cross-checked against sympy's `smith_normal_form`].
- 165 witnesses: all dfs3 level-2/3 controls in `../independent/out/dfs3_w/`, the n = 162 level-3
  gtile7 witness, and this pass's n = 176 and n = 184 witnesses.
- In every case Lemma K holds: Γ_tors is cyclic, its order divides K = n/p, and ḡ is injective on
  it. Γ is finite in 126 cases, and then Γ ≅ Z_K.
- For n = 162: Γ_tors = Z_54, so e = 3. For n = 189: Γ_tors = Z_63, so e = 2. Both equal the
  observed minimal levels.
- 34 witnesses have their own F at a lower level than e(𝒫), for example level 0 with e = 2. So
  e(𝒫) is only an upper bound.
- A first version of this script had a bug: it read the torsion generators from the columns of V
  instead of the rows of V^{-1}. It reported 58 false failures. The bug is fixed and an assertion
  now checks that d·y ∈ M.
- These witnesses are biased: the searches found them. Lemma K for T_n is a statement about all
  separated partitions, and that is not tested.
- Command: `python lemmaK_witness.py runs/w162_hd81_gtile7.txt runs/*.json ../../independent/out/dfs3_w/*.json`
  (`lemmaK_witness.out`).

**3d. New [n] level data** [numerical: dfs3, single implementation, with symmetry breaking].
- Commands, from `../independent`:
  `./dfs3.exe N 2 --level L --threads 3 --split 2 --out ../structure/pass8_level/runs/w_N_2_LL.json`.
  Logs are in `runs/dfs3_*.txt`.
- Results:
  - n = 176, p = 2 (level 1 NONE in pass 6): level 2 NONE (3008/3008 tasks), level 3 FOUND.
  - n = 184, p = 2 (level 1 NONE): level 2 FOUND, level 3 FOUND.
- The level-4 runs were started but were not needed.
- Timing: the bound level ≤ v_p(m) was formulated before the n = 176 level-3 result came in, and
  that result met it with equality.

## 4. Next steps

1. Prove Lemma S, or Lemma K, for downsets. Possible routes:
   - induct on |T| by removing a maximal element together with its block;
   - or show directly that a downset partitioned by g into equal fibres makes W = ker ḡ
     torsion-free.
   Only the case p ∤ m (Γ_p = 0) is needed for n = 195.
2. Test Lemma S for T_195 itself on many separated partitions. Generate g with all fibres of size
   p by a relaxed search that drops f and keeps only the equal-fibre condition, then compute Γ_p.
   This tests the exact hypothesis needed, on the exact T.
3. If Lemma S holds, then the level-1 NONE searches for n = 195 become independent confirmations
   rather than the proof. Every m_π that is a power of a single prime is then excluded by FP90
   alone.

## Amendment (pass 9)

The proposed Lemma S and Lemma K are **false for general downsets**. The counterexample cex1 is in
`pass9_lemmaS.md` and its certificate is `pass9_lemmaS/cex_downsets.json`. It has p = 2, k = 5,
Γ ≅ Z_10 and a minimal level of 1 > v_2(5) = 0.

The conjecture is restricted to *shifted* downsets, called S′ there; T_n is shifted. Read every
use of "downset" in §2 as "shifted downset (e.g. T_n)". The corollary at n = 195 now depends on S′.
