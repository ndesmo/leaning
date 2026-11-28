# Pass 13: the mixed case m_π = 15 (two primes of π dividing |B|)

Status: written 2026-11-28 (explorer pass 13), not reviewed. Code and outputs: `pass13_mixed/`.
Notation as in `prime_B_reduction.md` and `composite_B.md`. After Lemma A (pass2.md) and dilation by
t = 13 (coprime to 15), a periodic tiling with m_π = 15 is: G = H × Z13, H = G_3 × G_5, |H| = 225,
B' ⊆ H, |B'| = 15, and the 13 fibres A_k ⊆ H (k ∈ Z13) satisfy A_k ⊕ B' = H, |A_k| = 15.

**Verdict in one line.** The reduction splits into "B' periodic" (closed, Prop. 1) and "B' aperiodic"
(open). In the open case, **no argument that only uses homomorphisms of G can work**: there are
group-level complements that no homomorphism handles (Prop. 2, proved by hand), and verified small
analogues (n = 30, |B| = 6) where no homomorphism of G gives (a), (b^p), (b^q) or the new mixed
family (c). In every one of those analogues the *partition-level* form of (c) (Theorem 3') does
hold. So the natural next search family is (c_{x,y}) below, and the natural conjecture is
"mixed ⇒ (c)". Neither is proved.

## 1. Prop. 1: periodic B' is closed  [own argument, unreviewed]

Let A ⊕ B' = G be as above (or for any m_π), and suppose B' + g = B' for some g ≠ 0. Then B' is a
union of ⟨g⟩-cosets, so ord g divides |B'|, and B' = B'' ⊕ ⟨g⟩. Hence A ⊕ B'' ⊕ ⟨g⟩ = G. Passing to
Ḡ = G/⟨g⟩, every coset is uniquely ā + b̄'', so Ā ⊕ B̄'' = Ḡ, the quotient map is injective on A,
and φ̄ = (G → Ḡ)∘φ is a homomorphism injective on T with |B̄''| = |B'|/ord g.

For m_π = 15, ord g ∈ {3, 5, 15}:
- 15: |B̄''| = 1, so φ̄: T → Ḡ is a bijection onto a group of order 195, which is cyclic: (a).
- 3: |B̄''| = 5 is prime, so `prime_B_reduction.md` gives (a) or (b_1^5).
- 5: likewise (a) or (b_1^3).

All three are excluded (CCP/FP90 for (a); passes 2–3 for (b_1^p) [numerical: single implementation]).
More generally, **a period of B' of order d reduces m_π to m_π/d**. Inducting on |B'| and using
Theorem 2 of `composite_B.md`, the remaining gap is exactly: **B' aperiodic and m_π mixed.**

## 2. New family (c) and its finite form

> **(c_{x,y})** (x, y ≥ 1): there is a homomorphism ψ: Z^44 → Z_{3^x} × Z_{5^y} × Z13, injective on T,
> such that every fibre ψ(T) ∩ (Z_{3^x} × Z_{5^y} × {k}) is a coset of P_{x,y} × {k}, where
> P_{x,y} = 3^{x−1}Z_{3^x} × 5^{y−1}Z_{5^y} is the order-15 subgroup.

Facts [own argument, unreviewed; each is a few lines]:
- (c_{x,y}) is a periodic tiling with |B| = 3^{x−1}5^{y−1}, using B = transversal of P_{x,y} × {0}
  (as in Theorem 1 of `composite_B.md`).
- Monotone: (c_{x,y}) ⇒ (c_{x+1,y}) and (c_{x,y+1}), via x ↦ 3x or x ↦ 5x as in Theorem 1.
- (a) ⇒ (c_{1,1}). Conversely (c_{1,1}) is (a), by counting: 195 points in a group of order 195.
- (c_{x,1}) ⇒ (b_{x−1}^3) (or (a) when x = 1): put ψ' = (ψ_3, (ψ_5, ψ_13)) into Z_{3^x} × Z65. Over each
  (j, k) the fibre is (u_k + P_3) × {(j,k)}. Symmetrically (c_{1,y}) ⇒ (b_{y−1}^5).
  So the known NONE results exclude (c_{x,1}) for x ≤ 5 and (c_{1,y}) for y ≤ 4.
- (b_i^p) does **not** obviously imply any (c). The Z13-fibre of a (b^3)-solution is
  ∪_j (u_{j,k} + P_3) × {j}, and this is a P_3 × P_5-coset only if the u_{j,k} agree mod P_3. So (c)
  with x, y ≥ 2 is a **genuinely new** family. Its smallest member, (c_{2,2}), lives in G = Z9 × Z25 × Z13 ≅ Z_2925.

**Theorem 3' (finite reformulation)** [own argument, unreviewed; identical to Theorem 3 of
`composite_B.md` with Z_p replaced by Z15 ⊂ Q/Z]. These are equivalent:
- (c_{x,y}) holds for some x, y ≥ 1;
- there are:
  - a partition 𝒫 of T into 13 blocks of size 15;
  - a homomorphism ψ_K: Z^44 → Z13 that is constant on blocks and takes distinct values on distinct blocks;
  - a homomorphism f: M → Z15, where M is the lattice spanned by within-block differences, that
    is injective on every block.

Proof sketch. For (⇐), extend f to F: Z^44 → Q/Z, which is possible because Q/Z is divisible.
Project F onto its 3- and 5-primary parts, which still extends f because f takes values in Z15.
The image is finite cyclic, so it is Z_{3^x} × Z_{5^y}. Inside a block the values differ by nonzero
elements of (1/15)Z/Z, and there are 15 of them, so they form one coset of the order-15 subgroup.
For (⇒), take the blocks to be the ψ_13-fibres, and take f = ψ_{3,5} restricted to M. The Smith-form
bound of Theorem 3 carries over: for a given partition, x − 1 ≤ max v_3 and y − 1 ≤ max v_5 of the
nonzero elementary divisors of M.

**Search specification for a later pass.** Search (c_{2,2}) on G = Z9 × Z25 × Z13. Find φ: Z^44 → G,
injective on T, such that each of the 13 fibres over Z13 is a coset of 3Z9 × 5Z25. Equivalently:
reduced modulo 3Z9 × 5Z25, φ is constant on each Z13-fibre, and on each fibre it is a bijection onto
3Z9 × 5Z25 after translation. This is a coset-mode search like gtile7, with the coset modulus
made two-dimensional. Then go up to (c_{3,2}), (c_{2,3}), and so on. One NONE at (c_{x,y}) excludes
every (c_{x',y'}) with x' ≤ x and y' ≤ y.

## 3. Where a Theorem-2-type argument breaks  [proved by hand, own argument, unreviewed]

Theorem 2 produced one character χ of H that handles **every** complement of B' at once. For mixed
|B'| that is impossible in general:

**Prop. 2.** Let H = Z9 × Z25 and B' = {0,1,2} × {0,1,2,3,4}, which is aperiodic. For
s = (s_0, …, s_4) ∈ {0,1,2}^5, put C_s = {(3i + s_j, 5j) : i ∈ Z3, j ∈ Z5}.
- Then C_s ⊕ B' = H for every s.
- If s is not constant, then no homomorphism ρ: H → Q/Z is injective on C_s with ρ(C_s) a coset of
  the order-15 subgroup.

*Proof.* Tiling: C_s + B' = ∪_j (3Z9 + s_j + {0,1,2}) × (5j + {0..4}) = ∪_j Z9 × (5j + {0..4}) = H,
and the count is 15·15 = 225.

No ρ: suppose ρ works. Then all differences of ρ(C_s) lie in (1/15)Z/Z. Pick j, j' with
δ = s_j − s_{j'} ≢ 0 (mod 3). The difference ρ(δ, 5(j − j')) lies in (1/15)Z, and ρ(0, 5(j − j'))
lies in (1/5)Z because it is killed by 5. So ρ(δ, 0) ∈ (1/15)Z ∩ (1/9)Z = (1/3)Z. Since δ is a unit
mod 9, ρ(1, 0) ∈ (1/3)Z, so ρ(3, 0) = 0. But (s_0, 0) and (s_0 + 3, 0) are both in C_s, which
contradicts injectivity. ∎

The same holds in Z4 × Z9 with B' = {0,1} × {0,1,2}. Exhaustively [numerical, `exp1_order36.py`,
output `exp1_order36.out`], counting aperiodic tiles B' of size 6 that have a complement with no
such ρ:

| H | aperiodic tiles B' of size 6 | with a complement that has no ρ |
|---|---|---|
| Z4 × Z9 | 8802 | 1020 |
| Z2² × Z9 | 20556 | 702 |
| Z4 × Z3² | 32808 | 888 |
| Z2² × Z3² | 74160 | 0 |

The same run, on these order-36 groups:
- every complement of an aperiodic B' is periodic in Z4 × Z9 and Z2² × Z9;
- in Z4 × Z3² and Z2² × Z3², 108 aperiodic B' each have an aperiodic complement;
- complements occur with period orders {2}, {3} and {2, 3, 6} for the same B'. This is the
  "different fibres, different periods" phenomenon.

**Consequence.** If a reduction of the mixed case exists, it must use the arithmetic of T (the
lattice M, and in particular the freedom on sparse primes), not just homomorphisms of G.

## 4. Small analogues: n = 30, |B| = 6 (p, q = 2, 3, K = Z5)

`exp2_tn.py` searches for tilings of the following form:
- H of order 36, with an aperiodic tile B' chosen (by seed) among those having a complement with
  no common ρ;
- φ: Z^10 → G = H × Z5 with φ(T_30) − φ(T_30) avoiding (B' − B') × {0}. Since |A||B'| = |G|, this
  packing condition is the same as A ⊕ B' = G.

It uses random-restart DFS (env RESTARTS) and returns the first solution of each restart.

Each solution is tested for the reductions a proof would produce **through G**:
- (a);
- (c): a hom u: G → Z_{exp H} and a hom w: G → Z5 such that every w-fibre has size 6 and is mapped
  by u onto a coset of the order-6 subgroup;
- (b^2) and (b^3), in the same way.

`verify.py` is an independent checker written from the definitions. It shares no code with the search.
- It recomputes A with sympy.factorint.
- It checks injectivity and A ⊕ B' = G by computing all |A||B'| sums.
- It re-decides (a), (c), (b^2) and (b^3) by enumerating **all** homomorphisms G → Z_N from
  generator images. The fibration w ranges over every hom, not only the projection.
- It asserts agreement with the search's flags.

All 410 tilings below pass, and the flags agree.

[numerical: two implementations (exp2_tn.py and verify.py), output `pass13_mixed/verify.out`]

| file (H, B'-seed) | tilings | (c) through G | (b^2) | (b^3) | **none of (a),(b),(c) through G** |
|---|---|---|---|---|---|
| exp2_n30_4x9_1.json (DFS, no restarts) | 200 | 104 | 0 | 0 | **96** |
| exp2_n30_4x9_1_r.json | 30 | 18 | 0 | 0 | **12** |
| exp2_n30_4x9_2_r.json | 30 | 7 | 0 | 30 | 0 |
| exp2_n30_4x9_3_r.json | 30 | 16 | 0 | 0 | **14** |
| exp2_n30_2x2x9_{1,2}_r.json | 60 | 35 | 0 | 60 | 0 |
| exp2_n30_4x3x3_{1,2}_r.json | 60 | 43 | 60 | 0 | 0 |

(a) through G never occurs.

**So genuinely mixed tilings, in the through-G sense, exist at n = 30.** There are 122 of them, each
verified twice. Since no hom of G gives (a) or (b) either, the prime-|B| theorem also implies that
Per(L) of these tilings still has index 30·6 [consistency, not a separate check].

**How they arise (one example inspected by hand, `exp2_n30_4x9_1.json`).**
- φ(2) = (0,0,1), and 27 of the 30 points lie in the subgroup S = 2Z4 × 3Z9 × Z5 ≅ Z30. That is a
  multiplicative colouring.
- The points 19, 23 and 29 (free primes) form a coset X of ⟨(0,3,0)⟩ inside one K-fibre, and they
  are moved off S by (0,1,0). This is legal because ⟨(0,3)⟩ + B' = {0,1} × Z9 is invariant under
  (0,1): a Hajós-type shift.
- The shifted fibre is exactly a C_s-type complement of Prop. 2, so no homomorphism of G sees it.

**Partition-level test (Theorem 3', not through G).** `t5_partition.py` computes a Z-basis of M by
Hermite normal form (sympy), enumerates Hom(M, Z2) and Hom(M, Z3), and looks for f = (f2, f3)
bijective on every K-fibre. It reports **T5c true for every tiling tested**:
- the first 12 DFS tilings, 10 of them through-G mixed;
- all 90 Z4 × Z9 restart tilings, including the 26 through-G mixed ones;
- the 30 tilings of exp2_n30_2x2x9_1_r;
- the 30 tilings of exp2_n30_4x3x3_1_r.

That is 162 in all. [numerical: single implementation; the positives are not independently re-checked]
For the shift examples this is expected: f is free on the singleton directions e_19, e_23, e_29.

**n = 105, |B| = 15, H = Z9 × Z25, B' = {0,1,2} × {0..4}** (the exact analogue of Prop. 2, K = Z7):
the random-restart DFS found no solution in 10 × 30 s. Solutions certainly exist (for example
A = 3Z9 × 5Z25 × Z7 composed with a multiplicative colouring of 105), so this is a search failure,
not a NONE. Not pursued.

**Not done:** n = 6 and n = 15 (K trivial). There "(c) through the partition" is just (a) for the whole
of T, which always holds for n < 195, so they carry no information.

## 5. What a small-n test can and cannot show

For n < 195, (a) holds for *some* homomorphism (Forcade–Pollington), so an implication "tiling ⇒ (a)
or (b) or (c)" is never falsifiable at small n. The meaningful small-n question is structural: does
the *given* tiling's own data yield the structure?
- Through G: **no** (§4, verified).
- Through the partition and M (Theorem 3'): **yes** in all 162 samples.

The samples are biased toward "first solution found by DFS", which tends to mean a multiplicative
colouring plus shifts of sparse primes.

## 6. Conjecture and next steps

[conjecture] Mixed-case reduction: if (*) holds with m_π mixed (two primes; at 195 also three), then
the K-fibre partition admits f as in Theorem 3', so (c_{x,y}) (or its three-prime analogue) holds.
Evidence: §4 only (n = 30 analogue, 162 samples, no counterexample).

Next:
1. Implement the (c_{2,2}) search on Z9 × Z25 × Z13 (spec in §2). It is the cheapest new exclusion.
   Positive controls: n = 30 with p, q = 2, 3, and n = 105.
2. Make the n = 105 analogue run: seed the DFS from a multiplicative colouring and apply random
   Hajós shifts and re-solves, rather than blind DFS. Then test T5c with CP-SAT, since the rank of M
   is about 27 and enumerating Hom(M, Z5) is too big.
3. Hunt for T5c failures at n = 30 among less "shift-like" tilings: for example, forbid φ(2) ∈ K, or
   require two K-fibres with complements of different period types that use no free primes.
4. Try to prove the conjecture in the sub-case where every non-subgroup fibre differs from a coset of
   a fixed order-15 subgroup only on points of sparse primes (> 97). This is the mechanism seen in §4.

## Reproduction (from `search/smooth-colouring/structure/pass13_mixed/`)

- `python exp1_order36.py 2 3 > exp1_order36.out` (about 1 min).
- `RESTARTS=30 python exp2_tn.py 30 2 3 4,9 <seed> 20` for seed = 1, 2, 3, and likewise with
  `2,2,9` and `4,3,3` for seeds 1 and 2 (seconds each; logs `exp2_n30_*_r.log` for the latter two
  groups). Without RESTARTS: `python exp2_tn.py 30 2 3 4,9 1 120 200` (the 200-tiling DFS file).
- `python verify.py <json>` for each `exp2_n30_*.json` (output `verify.out`).
- `python t5_partition.py <json> [limit]` (outputs `t5_more.out`; the Z4 × Z9 runs were printed to the console).
- n = 105: `BPRIME='[[0,0],[0,1],[0,2],[0,3],[0,4],[1,0],[1,1],[1,2],[1,3],[1,4],[2,0],[2,1],[2,2],[2,3],[2,4]]' RESTARTS=10 python exp2_tn.py 105 3 5 9,25 grid 30`.
- Python 3 with sympy 1.14. Everything is single-threaded, with at most 4 runs in parallel.
