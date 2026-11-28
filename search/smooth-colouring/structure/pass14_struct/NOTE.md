# Pass 14 (structural): the mixed case m_π = 15 when H is cyclic

Status: written 2026-11-28 by a pass-14 subagent. Not reviewed. Scripts and outputs are in this
directory. Notation is as in `../pass13_mixed.md`:
- G = H × Z13, with H = G_3 × G_5 and |H| = 225;
- B' ⊆ H, |B'| = 15, aperiodic;
- T is split into 13 fibres T_k, and A_k = φ_H(T_k) ⊆ H satisfies A_k ⊕ B' = H for every k ∈ Z13.

Labels: [own argument, unreviewed]; [cited, read] means the quoted text was read in the source;
[unverified citation] means memory only; [numerical] gives the script.

## Verdict

The conjecture "mixed ⇒ some (c_{x,y})" is **not proved**. What is proved, conditional on one
unverified citation (Sands: Z_{p²q²} and Z_{p^n q} are good groups), is a **complete classification
of the mixed case when H is cyclic** (G_3 = Z9 and G_5 = Z25, so G ≅ Z_2925):

> **Theorem 4.** Suppose H ≅ Z9 × Z25 and B' is aperiodic. Then one of the following holds.
> 1. A periodic replacement B'' exists, with A ⊕ B'' = G. Prop 1 of pass 13 then reduces this to
>    the prime-|B| case, which is closed (or excluded).
> 2. Every fibre A_k is a coset of P = 3Z9 × 5Z25. This is (c_{2,2}) through G, with ψ = φ.
> 3. **(residual R)** S_{B'} = {3, 5}, and every fibre is, up to translation, a set of one of these
>    two shapes:
>    - C_s = {(3i + s_j, 5j) : i ∈ Z3, j ∈ Z5}, with s ∈ Z9^5;
>    - D_t = {(3i, 5j + t_i)}, with t ∈ Z25^3.
>
>    These are exactly the Prop-2 families of pass 13. If Φ_45 ∤ B', only C_s shapes occur. If
>    Φ_75 ∤ B', only D_t shapes occur.

So for cyclic H, the open gap is no longer "an arbitrary aperiodic B'". It is the explicit
configuration R, in which the fibres are Hajós-shifted grids. Prop 6 gives a sufficient lattice
condition for (c) in the pure-C_s part of R.

If H is non-cyclic (G_3 = Z3² or G_5 = Z5²), nothing here applies. The order-36 analogues
Z4 × Z3² and Z2² × Z3² have pairs of aperiodic factors (pass 13, `exp1_order36.out`), so an
argument of this kind cannot work there.

I did not find a counterexample to the conjecture (option (c) of the brief). Option (b), the
replacement trick, works exactly in case 1 and provably fails in R (Prop 5(ii)).

## 1. Cited results

**[cited, read]** Coven–Meyerowitz, *Tiling the integers with translates of one finite set*,
J. Algebra 212 (1999). Read in the HTML rendering at https://arxiv.org/html/math/9802122v1; the
displayed formulas were missing from that rendering.
- "Let S_A be the set of prime powers s such that the s-th cyclotomic polynomial Φ_s(x) divides A(x)."
- Theorem B1: "If A tiles the integers, then A(x) satisfies (T1)."
- Theorem B2: "If A tiles the integers and #A has at most two prime factors, then A(x) satisfies (T2)."
- (T1) and (T2) are quoted from Łaba–Londner's restatement (https://arxiv.org/html/2106.14044v3,
  Thm 1.1):
  - (T1): "A(1)=∏_{s∈S_A}Φ_s(1)";
  - (T2): "if s_1,…,s_k∈S_A are powers of different primes, then Φ_{s_1…s_k}(X) divides A(X)."
- Tiling criterion, Łaba–Londner eq. (1.2): A ⊕ B = Z_M iff "|A||B|=M and Φ_s(X) | A(X)B(X) for all
  s|M, s≠1".

  This is also elementary. 1_A * 1_B = 1 iff Â·B̂ vanishes off the trivial character. Characters of
  the same order d are Galois-conjugate, so Â vanishes at one of them iff it vanishes at all of them,
  iff Φ_d | A(x).

**[cited, read; not used, but a route to removing the unverified citation below]** CM Lemma 2.4,
"essentially Theorem 4 of" Sands, Proc. Edinburgh Math. Soc. 22 (1977): "Let A⊕C=ℤ be a tiling of
period n such that A is finite, 0∈A∩C, and n has one or two prime factors. Then there is a prime
factor p of n such that either A⊂pℤ or C⊆pℤ."

**[cited, secondary sources only — pass 15, see `../pass15_sands/CITATION.md`]** Sands, Acta Math.
Acad. Sci. Hungar. 8 (1957) and "On the factorisation of finite abelian groups II", ibid. 13 (1962)
153–169 (the 1962 paper completes the classification); also Szabó–Sands (2009). A cyclic
group Z_N is *good*, meaning every factorization has a periodic factor, iff N divides one of
p^n q, p²q², p²qr, pqrs. Only two instances are used here: Z225 = Z_{3²5²} and Z75 = Z_{3·5²}
(the latter is the p^n q case, de Bruijn).

Numerical consistency check of the analogue Z36 = Z_{2²3²} [numerical, `cyclic_classify.py`]:
- all 6-subsets containing 0 were enumerated;
- 0 factorizations Z36 = B ⊕ C with |B| = |C| = 6 have both factors aperiodic.

## 2. Elementary lemmas

Throughout, H = Z9 × Z25 ≅ Z225. Characters of order d correspond to the divisors d | 225.
Put g3 = (3,0) and g5 = (0,5), the generators of the order-3 and order-5 subgroups.

**Lemma 1 (periodicity in terms of zeros).** [own argument, unreviewed; standard]
X ⊆ Z_N satisfies X + N/p = X iff Φ_d | X(x) for every d | N with v_p(d) = v_p(N).

*Proof.* X + g = X iff X̂(χ)(χ(g) − 1) = 0 for all χ. For g = N/p, χ(g) ≠ 1 iff p^{v_p(N)} divides
ord χ. ∎

In Z225, this gives:
- g3-periodic ⇔ Φ_9, Φ_45, Φ_225 all divide X;
- g5-periodic ⇔ Φ_25, Φ_75, Φ_225 all divide X.

**Lemma 1' (quotient invariance).** [own argument, unreviewed]
Φ_3Φ_15Φ_75 | X(x) iff the multiset image of X in H/⟨g3⟩ ≅ Z3 × Z25 is invariant under (1,0).
The same holds with 3 and 5 exchanged.

*Proof.* The characters of order d ∈ {3, 15, 75} are exactly the characters of Z75 = H/⟨g3⟩ that are
nontrivial on the subgroup ⟨25⟩ ≅ ⟨(1,0)⟩. A function on Z75 is invariant under ⟨25⟩ iff its Fourier
transform vanishes on those characters. ∎

**Lemma 2 (replacement).** [own argument, unreviewed; classical Hajós-type]
Suppose A ⊕ B = G, A + g = A, and π: G → G/⟨g⟩ is the quotient map. Let B̃ ⊆ G be any set with
|B̃| = |B| and π(B̃) = π(B). Then A ⊕ B̃ = G.

*Proof.*
1. Since A + g = A, we can write A = A_0 ⊕ ⟨g⟩. So A_0 ⊕ ⟨g⟩ ⊕ B = G, and π is injective on B.
2. Hence A + B̃ = A_0 + π^{-1}(π(B̃)) = A_0 + π^{-1}(π(B)) = A_0 + ⟨g⟩ + B = G.
3. The sizes match, |A||B̃| = |G|, so the sum is direct. ∎

Use with many fibres: if every A_k has the same period g, then B' can be replaced by any B'' with
π(B'') = π(B') bijectively. In particular, if π(B') has a period h̄, and h̄ lifts to an element h of
the same order, then B'' = (a lift of a set of orbit representatives) ⊕ ⟨h⟩ is periodic. Prop 1 of
pass 13 then applies.

[numerical, `replace_check.py`, outputs `replace_check_{2_3,3_2}.out`] On Z36:
- 90 + 936 aperiodic tiles B with S_B = {p, q²} were tested;
- in every case the lifted B'' is periodic and tiles with **every** complement of B.

**Lemma 3 (Z25).** [own argument, unreviewed]
1. If E ⊆ Z25, |E| = 5, and Φ_25 | E(x), then E is a coset of 5Z25.
2. If X ⊕ Y = Z25 with |X| = |Y| = 5, then one of X, Y is a coset of 5Z25.

*Proof.*
1. Let ζ be a primitive 25th root of unity. Then 1, ζ, …, ζ⁴ is a basis of Q(ζ) over Q(ζ^5).
   Write Σ_{e∈E} ζ^e = Σ_r ζ^r σ_r, where σ_r is a sum of distinct 5th roots of unity. The sum is 0,
   so every σ_r = 0. A sum of distinct 5th roots of unity vanishes only if it is empty or complete.
   Since |E| = 5, E is one full residue class mod 5.
2. Φ_25 divides X or Y, so part 1 applies to that factor. ∎

## 3. Theorem 4: the case analysis  [own argument, unreviewed; relies on CM and on Sands (unverified)]

Each A_k and B' tiles Z225, hence tiles Z. Both have size 15 = 3·5, which has two prime factors.

By CM Theorem B1 and the tiling criterion, S_{B'} and S_{A_k} partition {3, 9, 5, 25}. By T1, each
contains exactly one power of 3 and one power of 5. By T2, each also has Φ_{3^α5^β} for its pair.
Each composite d ∈ {15, 45, 75, 225} divides B' or A_k.

**(i) S_{B'} = {9, 25}: impossible.**
1. By T2, Φ_225 | B'.
2. B' is aperiodic, so by Lemma 1, Φ_45 ∤ B' and Φ_75 ∤ B'.
3. Then every complement C has Φ_45 and Φ_75, and S_C = {3, 5}. So C has neither Φ_9 nor Φ_25, and
   by Lemma 1 C is aperiodic.
4. This gives a factorization of Z225 with both factors aperiodic, which contradicts Sands.

**(ii) S_{B'} = {3, 25} (the case {9, 5} is symmetric): closed.**
1. By T2, Φ_75 | B'. Since B' is aperiodic, Lemma 1 gives Φ_225 ∤ B'.
2. So every A_k has Φ_225 and S_{A_k} = {9, 5}. By T2, Φ_45 | A_k.
3. By Lemma 1, every A_k is g3-periodic. Write A_k = A_k'' ⊕ ⟨g3⟩. In Z75 = H/⟨g3⟩, this gives
   Ā_k'' ⊕ B̄' = Z75.
4. If B̄' has a period of order 5, it lifts to an element of order 5 (the 5-part splits off). By
   Lemma 2 we get a periodic B'', which is outcome 1.
5. If B̄' has a period of order 3, it is (1,0). Then B̄' = Z3 × E, where E is the image of B' in Z25,
   with 5 points, each hit 3 times. Φ_25 | B' gives Φ_25 | E, so by Lemma 3, E is a coset of 5Z25.
   Then B̄' has the order-5 period (0,5), and step 4 applies.
6. Otherwise B̄' is aperiodic. Since Z75 is good, every Ā_k'' (5 points) is a coset of the order-5
   subgroup. So A_k = π^{-1}(Ā_k'') is a coset of P, which is outcome 2.

**(iii) S_{B'} = {3, 5}.** By T2, Φ_15 | B'. Every A_k has S = {9, 25} and Φ_225.
- If Φ_45 ∤ B', then Φ_45 | A_k, so A_k is g3-periodic.
- If Φ_75 ∤ B', then A_k is g5-periodic.
- If both fail to divide B', every A_k is a coset of P (outcome 2).
- If both divide B', each A_k is still periodic, because Z225 is good and B' is aperiodic.

*Shape of a g3-periodic fibre that is not a P-coset, when Φ_75 | B'.*
1. By Lemma 1', B̄' ⊆ Z3 × Z25 is (1,0)-invariant. As a set it is Z3 × E, with E the image of B'
   in Z25 (5 points).
2. In Z75, Ā_k'' ⊕ Z3 × E = Z75. Reducing mod Z3 gives Ã_k'' ⊕ E = Z25.
3. S_{B'} ∌ 25, so E is not a coset of 5Z25 (Lemma 3, part 1). By Lemma 3, part 2, Ã_k'' is a
   coset of 5Z25.
4. So A_k ⊆ Z9 × (c + 5Z25), and it meets each of the 5 rows in one ⟨g3⟩-coset. That is
   A_k = (0, c) + C_s.

Symmetrically, a g5-periodic fibre is a D_t. Under Φ_45 ∤ B' only C_s fibres occur, and under
Φ_75 ∤ B' only D_t fibres occur. ∎

[numerical, `cyclic_classify.py 2 3`, output `cyclic_classify_2_3.out`] On the Z36 analogue
(p, q = 2, 3), every prediction holds exhaustively:

| S_B | Φ_{p²q} \| B, Φ_{pq²} \| B | complement types | count of aperiodic tiles B containing 0 |
|---|---|---|---|
| {4, 9} | (any) | none | 0 |
| {2, 9} | (F, T) | p-periodic only | 90 |
| {3, 4} | (T, F) | q-periodic only | 936 |
| {2, 3} | (F, F) | P-cosets only | 7020 |
| {2, 3} | (F, T) | P-cosets and C_s-shapes | 270 |
| {2, 3} | (T, F) | P-cosets and D_t-shapes | 468 |
| {2, 3} | (T, T) | P-cosets, C_s- and D_t-shapes | 18 |

No complement violated the C_s or D_t shape test.

## 4. Prop 5: what replacement can and cannot do in R  [own argument, unreviewed]

(i) In case (ii) of §3, replacement (Lemma 2) always produces a periodic B'' unless every fibre is a
P-coset. This was checked numerically on Z36: 1026 of 1026 tiles.

(ii) In R with only C_s fibres (Φ_45 ∤ B', Φ_75 | B'), no periodic B'' with π(B'') = π(B') exists.
1. A period of B'' must have order 3 or 5.
2. Order 3 is impossible: the only order-3 subgroup is ⟨g3⟩, and π is injective on B''.
3. Order 5 would need π(B'') = Z3 × E to be invariant under some (0, 5w). Then E would be a coset
   of 5Z25, which is excluded.

[numerical: all 270 + 468 analogue tiles on Z36 have no order-q period mod ⟨g_p⟩, per
`replace_check_*.out`]

Because R contains C_s fibres (and D_t fibres, in the doubly case), Prop 2 of pass 13 shows that no
homomorphism of G gives (c) in general. So R is a genuine residual: the arithmetic of T is needed.

## 5. Prop 6: a sufficient lattice condition in the pure-C_s part of R  [own argument, unreviewed]

Suppose every fibre is (0, c_k) + C_{s^{(k)}} or a P-coset. Let M be the lattice spanned by the
within-fibre differences of T, as in Theorem 3' of pass 13. The 15 points of a fibre split into
5 "rows" of 3 points, with equal φ_5 and φ_3 differing by multiples of 3.

Claim: if there is a homomorphism f_3: M → Z3 that is injective on every row triple, then (c_{x,y})
holds for some x, y.

*Proof.*
1. All within-fibre differences have φ_5 ∈ 5Z25. So f_5 := φ_5/5 is a well-defined homomorphism
   M → Z5, and it is bijective from the rows of each fibre onto Z5.
2. Then f = (f_3, f_5): M → Z15 is injective on every fibre.
3. Theorem 3' of pass 13 now gives (c_{x,y}). ∎

The naive candidate f_3 = φ_3/3 is defined only on M_3 = M ∩ φ_3^{-1}(3Z9). It never extends to M
when some s^{(k)} is non-constant mod 3. To see this, take v ∈ M \ M_3. Then 3v ∈ M_3 and
φ_3(3v)/3 ≡ φ_3(v) ≢ 0 (mod 3), whereas an extension would need f_3(3v) = 3f_3(v) = 0. This is
Prop 2 of pass 13 again.

The corrected candidate is f_3 = φ_3/3 + λ, where λ: M_3 → Z3 vanishes on the row-difference
lattice R and has λ(3v) = −φ_3(v). It exists iff **3v ∉ R + 3M_3**. This is a finite
linear-algebra test over F_3 for any given tiling. It is the natural check to run on the pass-13
n = 30 and n = 105 samples, and it is the precise form of next step 4 in pass 13. In the free-prime
examples it holds trivially. A failure of it, together with a failure of every other f_3, would be
the counterexample shape for the "own partition" form of the conjecture.

## 6. What remains

1. **R at 195, cyclic H.** Either prove the existence of f_3 (Prop 6) from the arithmetic of T_195,
   or treat the doubly case, where both C_s and D_t fibres are present and neither φ_5/5 nor φ_3/3 is
   defined on M. Alternatively, search R directly. It is a much smaller family than "all aperiodic
   B'": S_{B'} = {3, 5}, with fibres of two explicit shapes.
2. **Non-cyclic H** (Z3² × Z25, Z9 × Z5², Z3² × Z5²). These are not good groups, and aperiodic
   complements exist in the analogues. This is untouched.
3. Remove the Sands dependence:
   - either derive the periodicity used in (i) and (iii) from CM Lemma 2.4 (verified quote) by the
     usual subgroup recursion,
   - or check Z225 directly. Size-15 tiles of Z225 are characterised by T1 and T2 (CM Corollary), so
     they could be enumerated by their zero sets.

## Reproduction (from this directory; single-threaded, Python 3, a few seconds each)

- `python cyclic_classify.py 2 3 > cyclic_classify_2_3.out`
- `python replace_check.py 2 3 > replace_check_2_3.out`; `python replace_check.py 3 2 > replace_check_3_2.out`
