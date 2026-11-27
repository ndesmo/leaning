# NOTES: colouring ℤ⁺ with n colours so that a, 2a, …, na are distinct, n = 195

Problem P11 of `PROBLEMS.md`, moonshot issue #31. Slug `smooth-colouring`. Search code and its
README are in `search/smooth-colouring/`.

Labels: [paper: ref, Thm], [preprint: ref, Thm], [numerical: …], [own argument, unreviewed],
[conjecture].

## Statement

n is *satisfactory* if ℤ⁺ can be coloured with n colours so that for every a the numbers
a, 2a, …, na get n different colours. Source: Caicedo–Chartier–Pach, "Coloring the n-smooth
numbers with n colors", EJC 28(1) (2021) #P1.34, arXiv:1902.00446; and MathOverflow 26358.

**Target:** is 195 satisfactory?

## Known

- A *multiplicative* colouring is a homomorphism (ℤ⁺, ·) → G, |G| = n, that is injective on
  {1..n}. One gives a satisfactory colouring. CCP find one for every n < 195, and none exists at
  n = 195 [paper: CCP]. Our exhaustive search agrees [numerical: search/…/multiplicative].
- Forcade–Pollington conjectured that a group G admitting a "group map" injective on {1..k} must be
  abelian. Campbell, arXiv:2610.12087 (8 Oct 2026), claims a proof [preprint, unread beyond the
  abstract].
- **Wang–Wang, arXiv:2609.15081 (14 Sep 2026)** [preprint: Thm 1.1]:
  - χ(B205) = 206, so n = 205 is not satisfactory;
  - χ(B208) = 208, via ℤ104 × ℤ2;
  - 212 ≤ χ(B211) ≤ 213.
  - They state n₀ ∈ {195, 205} and 195 ≤ χ(B195) ≤ 196, so **195 is open in that paper**.
  - Method: reduce an arbitrary tiling to a periodic one, then to a finite computation (Section 4).
- Open check 2026-11-25: one extended web search. It found only CCP, Wang–Wang, Campbell and this
  project's own issue. Nothing resolves 195.

## Exploration journal

### 2026-11-25: pass 1 (resumed after an interrupted start)

The interrupted first pass left the multiplicative search, its scan output up to n = 250 and an
unbuilt `periodic/kper.rs`. Its README, which held the "Prop. 3" that kper relies on, was lost.

Strategies this pass:
1. **Literature recheck.** Found Wang–Wang and Campbell (above). The area is now active: Wang–Wang
   came within one case of n₀. An agent read their Section 4 to find why their method does not
   settle 195; see the entry below.
2. **Periodic tilings of index p**, using `kper.rs`, which needed a one-line borrow fix to build.
   - The class tested: φ: ℤ⁺ → ℤ_{np}, p ‖ n, injective on {1..n}, with φ(a) − φ(b) ∉
     qℤ_{np} \ nℤ_{np} for all distinct a, b ≤ n, where q = n/p. Each such φ gives a colouring by
     the tiling φ([n]) ⊕ {0, q, …, (p−1)q}.
   - Sanity: solutions found at n = 12 (p = 3) and n = 30 (p = 5). An independent checker
     (`check_tiling_colouring.py`, written from the definition) accepts them as genuine colourings,
     with blocks checked for x ≤ 2000.
   - Control: n = 205 gives NONE for p = 5 and p = 41. This is consistent with Wang–Wang.
   - **n = 195: NONE for p = 3, 5 and 13.** Each search finished in about 2 s with complete=true
     [numerical: single search, no second implementation yet]. This rules out only the class
     coded; that class is complete for size-p complements only if the lost Prop. 3 is true.
   - Partial recovery of Prop. 3 [own argument, unreviewed]. The dilation theorem gives
     A ⊕ tB = G for t coprime to p. With B = {0, q, …, (p−1)q}, the union of the sets t(B − B) is
     qℤ_N \ nℤ_N. So kper's class is exactly the tilings by this B; that B is general is not
     shown.
3. **Structural reduction (sketch)** [own argument, unreviewed]. Suppose φ: ℤ^k → G is injective
   on S, and A ⊕ B = G with A = φ(S), |G| = 195m and gcd(m, 195) = 1. Tijdeman's dilation theorem,
   in its finite-abelian form, gives mA ⊕ B = G. I recall this as Sands' theorem in Szabó–Sands,
   *Factoring groups into subsets*; the citation is still to be checked.
   - mA lies in mG, a subgroup of order 195.
   - The sum mA + B is direct, so x ↦ mx is injective on A and mA = mG.
   - Then m·φ is a multiplicative colouring at n = 195, which is impossible.
   - **So a periodic tiling must have a period index 195m with gcd(m, 195) > 1.** This is probably
     the content of Wang–Wang Lemma 4.4 ("coprime period extension"); compare when their text is
     read.

4. **Wang–Wang, read in full by an agent** (v1, the only version; the promised ancillary code is
   not on arXiv). Their §7, verbatim: "The missing step at 195 is a reduction of an arbitrary
   tiling by T_195 to a bounded finite search … Neither reduction has been established here for
   195=3·5·13".
   - Their periodicity step (§4.3, "q complete p-gons or p complete q-gons") and the quotient
     bound (Lemma 4.5, two primes only) both need |A| = pq.
   - For three primes, Lam–Leung shows vanishing sums of 195th roots of unity need not be unions
     of polygons, so these steps fail as stated.
   - Consequence: **for 195, a null periodic search proves nothing about non-existence.** Only a
     hit is decisive: a periodic tiling gives a colouring.
   - They also use the Horak–Kim dilation theorem (k·A tiles with the same complement when
     (k, |A|) = 1). It supports the reduction in item 3 to {3,5,13}-groups.
5. **General periodic search, m = 3** (`search/smooth-colouring/general/gtile.rs`, new).
   - The search: φ: ℤ⁺ → G with A = φ([195]) ⊕ B = G and |B| = 3, for G = ℤ_9×ℤ_5×ℤ_13 (cyclic,
     order 585) and G = ℤ_3×ℤ_3×ℤ_5×ℤ_13. It covers every B = {0, b1, b2} up to translation and
     componentwise units: 310 and 466 classes.
   - Pruning: A − A avoids t(B − B) for all t coprime to 3 (`dil=1`, by dilation). The primes in
     (97, 195] are placed by an exact cover of the holes. The symmetry is first-prime orbit-minimal
     under units fixing D0, with every uB tried at the leaf.
   - Bug caught and fixed mid-run: the first version tried only B itself at the leaf, which is
     unsound when uB ≠ B + c. Old outputs are kept in `out/old_unsound_sym/` and are not used.
   - Cross-check: with B = {0, 65, 130} (kper's class) gtile returns NONE after 2.1·10⁹ nodes in
     165 s, independently of kper. This is the second implementation for item 2.
   - Status at the end of this pass (third run, `gtile4`): **310 classes NONE, 4 TIMEOUT
     (10⁹ nodes, about 10 min each), about 462 not reached, no EXISTS.** The processes were then
     stopped.
     - All 310 NONE classes have leaves = 0. No smooth assignment survived, so the leaf-symmetry
       issue above never affected any result.
     - The TIMEOUT classes are progression-type B = {0, x, 2x}:
       - (1,0,0)-steps in ℤ_9×ℤ_5×ℤ_13;
       - in ℤ_3²×ℤ_5×ℤ_13, B = {0, (0,1,0,0), (0,2,1,0)}, {0, (0,1,0,0), (1,2,0,0)} and the
         subgroup {0, (0,1,0,0), (0,2,0,0)}. The subgroup case is the multiplicative case, which
         is known to be NONE.
       - For these B, D0 is small and the pruning is weak. The search needs kper's full stabiliser
         chain instead of first-prime symmetry only.
     - Run history: `out/old_unsound_sym/` (run 1, leaf bug) and `out/run2_slowleaf/` (run 2,
       uncounted leaf work). Neither run found an EXISTS.
   - Labels: [numerical: single implementation, so far]. A NONE here is not evidence against 195
     (see item 4); only an EXISTS matters. `check_general.py` (independent, from the definition) is
     ready for any hit and passes on n = 12.

Dead ends:
- `periodic/kper_indep.py` (a pure-Python cross-check of kper) is far too slow at n = 195; it did
  not finish n = 205 in about 40 min. gtile replaced it.
- Excluding 195 by bounded periodic searches is ruled out as a proof strategy until a three-prime
  analogue of Wang–Wang §4.3–4.4 exists. Do not spend passes on null searches for that purpose.

Next ideas, ranked:
1. **Finish the m = 3 sweep.** Port kper's stabiliser-chain symmetry and its threading into
   gtile. Skip B that are subgroup cosets (the multiplicative case). Then rerun the TIMEOUT
   classes and the ones not reached.
   - Collect `general/out/m3_*.txt`. If the processes died, rerun skipping the B already listed.
   - Speed up generic B: replace the `put` loop over D0 with a bitset OR, or use the full kper
     stabiliser chain. Then rerun the TIMEOUT classes with no limit.
   - Any EXISTS goes to `check_general.py`, then a Lean check by `decide` on the finite tiling.
2. **Existence search with m = 5 and m = 13** (G = ℤ_3×ℤ_25×ℤ_13, ℤ_3×ℤ_5²×ℤ_13, ℤ_3×ℤ_5×ℤ_169,
   and so on).
   - There are too many B to enumerate, so restrict to structured B. Following Wang–Wang (4.8),
     use box or arithmetic-progression B: {0, d, 2d, …} and products.
   - Use local search (simulated annealing on φ) rather than exhaustive DFS. The aim is a hit, not
     a proof of absence.
3. **The structural route to non-existence.** Try a three-prime analogue of the Wang–Wang
   periodicity step, using the Lam–Leung structure of vanishing sums of 195th roots of unity
   (sums of 3-, 5- and 13-gons, with signed combinations) applied to the invariant measure of a
   tiling. This is hard but it is the real gap; brief a subagent with §4.3 of arXiv:2609.15081.
4. Recover "Prop. 3" for kper; this matters less now that gtile covers kper's class directly.

### 2026-11-25: pass 2

Three parallel strategies. No hit, so no PR this pass.

1. **The |B| = 3 periodic case is closed** (`general/gtile5.rs`, `run5.sh`) [own argument,
   unreviewed] + [numerical: single implementation].
   - Reduction: G = H × Z65, with H the 3-Sylow subgroup (Z9 or Z3²). Coprime dilation
     (Tijdeman, with roles swapped: gcd(t, |B|) = 1 ⇒ A ⊕ tB = G) with t = 65 sends B into H.
     There 65 acts as an automorphism. So WLOG B ⊂ H, and A ⊕ B = G iff every H-coset meets A in
     a complement of B in H. Up to Aut(H) and translation, that leaves 5 classes:
     - Z9 {0,1,2}: searched, NONE.
     - Z9 {0,1,3}: no complement in Z9, NONE.
     - Z9 {0,3,6}: a subgroup, so the multiplicative case, NONE by CCP.
     - Z3² non-collinear: searched, NONE. Also by theory: every complement is a coset of
       K = ⟨(1,1)⟩, so A = A + K, and A ⊕ K' = G for another order-3 subgroup K'. That is the
       multiplicative case.
     - Z3² line: a subgroup, NONE.
   - gtile5 does exact fibre pruning over φ = (h, f) with h into H and f into Z65. The primes
     above 97 fill the remaining slots, so every surviving leaf is a genuine tiling.
     - Runs: `sh run5.sh 9 0,1,2 20 50000000000` (20/20 NONE, about 2.6·10⁹ nodes, about 20 s)
       and `sh run5.sh 3,3 0/0,1/0,0/1 16 50000000000` (16/16 NONE). Outputs are in
       `general/out/m3_pass2_gtile5_*.txt`.
     - Validation: gtile5 agrees with gtile4 on existence for n = 3m with m ≤ 27 (except 18), in
       both groups. Its witnesses at n = 21, 39 and 120 pass `check_general.py` (pass −B).
   - This subsumes the 4 TIMEOUT and about 462 unreached classes of pass 1. The files
     `general/out/m3_pass2_{cyc,nc}.txt` are abandoned gtile4 runs (TIMEOUT at 10⁸); ignore them.
   - **Claim:** no periodic tiling with |G| = 585 exists. As item 4 of pass 1 says, this does not
     bear on non-existence for 195.
   - **Still needed:** a second, independent checker for the Z9 {0,1,2} NONE, and /review of the
     reduction.
2. **Simulated annealing for |B| = 5 and 13** (`local/sa.rs`): a dead end.
   - Best collision counts: 20–25 for |B| = 5, and 261–265 for |B| = 13.
   - Calibration failed: with m = 1 the annealer cannot even find the known lattice colourings at
     n = 190, 196 and 198, where it stalls at 6–10 collisions.
   - **Dead end:** plain annealing is too weak here. Do not retry it without exact completion.
3. **Structural** (`structure/pass2.md`).
   - **Lemma A** [own argument, unreviewed]: T_195 tiles Z^44 periodically iff there is a
     {3,5,13}-group H, |H| = 195m with m > 1, and ψ: Z^44 → H injective on T, with ψ(T) ⊕ B = H.
     The verbatim Horak–Kim Thms 6 and 8 are quoted there.
   - There is no known periodicity theorem for T_195 in Z^44, and Greenfeld–Tao disprove the
     periodic tiling conjecture in high dimension. So the gap is exactly "tiling ⇒ periodic
     tiling".
   - Where Wang–Wang §4.3 breaks for three primes:
     - **O1, counting:** 3a + 5b + 13c = 195 has 109 solutions, only 3 of them pure.
     - **O2:** nonnegative tables that are not sums of polygons.

Next ideas, ranked:
1. **The pure-type question** (structure/pass2.md). Must every completely multiplicative
   χ: [195] → 𝕋 with Σ_{m≤195} χ(m)^k = 0 for all k coprime to 195 have at most one of A_3, A_5,
   A_13 nonzero? This is a finite search over coincidence patterns, which the primes above 97
   constrain strongly.
   - If yes, attempt a three-factor version of Wang–Wang (4.5) and Lemma 4.4.
   - If no, a mixed χ kills the spectral route.
2. **Exact search for |B| ∈ {5, 13} by the pass-2 reduction.** Dilate by t coprime to |B| to push
   B into the p-Sylow part, then run fibre-pruned DFS as in gtile5. Order 975 (Z25 or Z5²) first.
   - Unverified lead: if Sands' good-group classification covers Z975, one factor must be
     periodic, so A is a union of cosets. Check the literature.
3. An independent checker for the gtile5 NONE (Z9 {0,1,2}), then /review of the |B| = 3
   reduction. It is a clean negative result and could become a PR.

### 2026-11-25: pass 3

Two parallel strategies. There are verified findings, but none has passed /review yet, so there is
no PR this pass.

1. **Pure-type question: the answer is no** (`structure/pass3_puretype.md`).
   - The mixed character is χ(p) = e(w_p/195), with the weights in
     `structure/cert_N195_1_2_14.json`.
     - S_k = Σ_{m≤195} χ(m)^k = 0 for all 96 units k mod 195.
     - A_3 = 3, A_5 = 10 and A_13 = 182, so all three are nonzero. The structure is one 3-gon,
       two 5-gons and fourteen 13-gons. Primes in (97,195] fill the small polygons.
   - Checks:
     - [numerical: certificate checked by an independent script]. `puretype_check.py` reduces
       the sums exactly modulo Φ_195 in sympy.
     - A separate 10-line float check written by the main session, sharing no code with the
       search, gives max |S_k| = 4.7e-12.
   - Search: `puretype_search.py 1 2 14` (OR-tools CP-SAT, about 280 s).
   - Consequence: obstruction O1 is realised by an actual character. Condition (ii) plus
     multiplicativity does **not** force A_pA_q = 0. The Wang–Wang §4.3 spectral route can be
     saved only with extra input: (iii), the Frobenius congruences (iv), or positivity of σ_f̃.
     The question is not dead, but the cheap route is.
   - [own argument, unreviewed]: for μ_N-valued χ with N a {3,5,13}-number, the condition reduces
     to S_1 = 0 by Galois conjugation. Non-root-of-unity χ add nothing for mixed examples.
2. **Periodic tilings with |B| = 5 and |B| = 13 are closed** (`general/gtile6.rs`, `run6.sh`,
   `tiles_p2.py`, `out/m5_summary.txt`).
   - Reduction [own argument, unreviewed], as in pass 2: dilating by t = |K| gives B ⊂ H, the
     p-Sylow subgroup of order p². Then, by Rédei's theorem (factors of prime size; cited, not
     re-read), every complement of a non-subgroup B is a coset of an order-p subgroup.
     - H = Z_p²: closed by argument. Every fibre complements the line spanned by a difference in
       B − B, which reduces to the multiplicative case. This holds for p = 5 and 13.
     - H = Z_{p²}: every fibre is a coset of pZ_{p²}. This is one search per p.
   - n = 195 results, all 20/20 splits complete, no limit hit:
     - Z25 × Z39: NONE (3.0·10⁹ nodes).
     - Z169 × Z15: NONE (1.1·10¹⁰ nodes).
     - Z5² classes searched as well: NONE, which is redundant.
     - Labels: [numerical: single implementation]. Ext and coset modes share the search core.
   - Validation:
     - At p = 3, gtile6 agrees with gtile5 for n = 3m, m ≤ 64.
     - At p = 5, three implementations, gtile4 among them, agree that solutions exist for
       n = 5m, m ≤ 29, 5 ∤ m.
     - At p = 13, solutions exist for n = 13m, m ≤ 11.
     - Witnesses pass `check_general.py`.
     - Weakness: no NONE case was validated at p = 5. The planned control at n = 205 and 235 on
       Z5² was stopped.
   - With pass 2, every periodic class with |B| prime is now closed. Composite |B| ≥ 9 remains
     open. As before, this does not bear on non-existence for 195.

Dead ends:
- The spectral route through condition (ii) alone is dead, because the mixed χ above satisfies
  it. Do not retry it without new input from (iii) or (iv), or from positivity.

Next ideas, ranked:
1. **Write up the prime-|B| result** (passes 2 and 3) as a clean negative result:
   - "no periodic tiling with |B| prime";
   - add an independent second checker for the Z9, Z25 and Z169 NONE results;
   - re-read Rédei's statement and the Tijdeman or Horak–Kim dilation statement;
   - then /review and a PR (`Part of #31`).
2. **Test the mixed χ against (iii), (iv) and positivity.** Can a σ_f̃-typical character be
   mixed? If (iv) or positivity excludes every mixed character, the spectral route revives.
3. **Composite |B|**: 9 (Z27, Z9×Z3, Z3³), 15 and 25. Rédei no longer applies. Try a
   Sands/good-group style factorisation argument first, then search.

### 2026-11-26: pass 4

Two parallel strategies. There is no PR this pass: the reduction has not passed /review, and no
second implementation has confirmed the searches.

1. **The prime-|B| reduction, written up rigorously** (`structure/prime_B_reduction.md`)
   [own argument, unreviewed].
   - Claim: suppose a periodic tiling has a period lattice of index 195p with p prime. Then either
     (a) a multiplicative colouring exists, which is excluded by Forcade–Pollington's computation
     as reported in CCP Thm 5.1, or (b) p ∈ {3, 5, 13} and φ: Z^44 → Z_{p²} × Z_{195/p} is
     injective on T with every fibre a coset of pZ_{p²}.
   - The only tool is dilation (D), proved in full in the note by the Frobenius argument in Z[G].
   - The new Lemma 1: if some d ∈ B − B has order p, then A ⊕ ⟨d⟩ = G, which gives (a). It
     disposes of H = Z_p² and of B' − B' ∩ pZ_{p²} ≠ {0} with no search. **Rédei is not needed**,
     and the Z3²/Z5² searches of passes 2 and 3 were redundant.
   - The journal's direction of dilation (dilate B, gcd(t, |B|) = 1) is correct. CCP do not prove
     "no multiplicative colouring at 195" themselves; they report FP90's search.
   - Brute force for p = 3, 5 (`structure/prime_B_bruteforce.py`, `.out`) found no counterexample
     to Lemma 1 or D.
   - The cited statements are now verbatim in §5, from secondary sources: Zhao–Yuan Prop. 2.1
     (Szabó–Sands Thm 7.12), Zhou Prop. 1 and Coven–Meyerowitz Lemma 2.2. Tijdeman's and Sands'
     originals were not read. Łaba–Londner and Tao state weaker versions (t coprime to |G|) and
     must not be cited for D.
2. **Independent second checker for the three (b) NONE results**
   (`search/smooth-colouring/independent/`, CP-SAT): **inconclusive.**
   - The model is correct where it can be tested:
     - exact solution counts match brute force (n = 5, 6, 9, 10);
     - every positive control is solved: n = 3m for m ≤ 27 (including 18), n = 5m for m ≤ 28 with
       5 ∤ m, and n = 13m for m ≤ 11;
     - 61 witnesses pass `direct_check.py` and `check_general.py`.
   - At n = 195, all three cases return UNKNOWN after 1500 s (full model) and after 900 s
     (`--reduce`, primes > n/2 dropped). CP-SAT already times out on the positive control n = 145,
     p = 5, so it is too weak at proving infeasibility here.
   - **Dead end:** CP-SAT as the confirming checker. Do not retry without a much stronger
     formulation.

Next ideas, ranked:
1. **Independent exact DFS** (C or Rust, written from the definition in `prime_B_reduction.md` (b),
   not from gtile5/6). Use a different variable order, e.g. by largest prime first or by fibres,
   plus the `--reduce` completion argument. Validate on the same controls. Then run /review on the
   reduction and open a PR, "no periodic tiling of prime index 195p", `Part of #31`. The PR rests on
   the three searches, D, and FP90 as reported by CCP.
2. Test the mixed character against (iii), (iv) and positivity (pass 3 next idea 2).
3. Composite |B| = 9, 15, 25. Lemma 1 generalises: any d ∈ B − B whose order is coprime to
   |B|/ord(d) … needs thought. Try a Lemma-1-style reduction before any search.

### 2026-11-26: pass 5

Two parallel strategies. Both produced findings, but nothing has passed /review, so there is no
PR this pass.

1. **Independent second checker for case (b): agrees** (`independent/dfs2.rs`)
   [numerical: two independent implementations; dfs2 uses an unreviewed symmetry reduction].
   - Written from `prime_B_reduction.md` §3(b) without reading gtile5/6. It uses a pairwise
     reformulation (φ(r) ∉ F for 8098 difference vectors), forward checking, and the 19 primes
     > 97 left to a bijective completion step. Symmetry breaking is lex-leader under
     U(Z_{p²})×U(Z_K).
   - Validation:
     - exact counts match `brute_count.py` for n = 3, 6, 9 (p = 3) and n = 5, 10 (p = 5);
     - the asc, desc and greedy orders give identical counts at (24,3), (30,5) and (26,13);
     - 107 positive controls found a witness, and all 107 witnesses pass `direct_check.py`.
   - n = 195: COMPLETE-NONE for Z9×Z65, Z25×Z39 and Z169×Z15, about 10⁶ nodes and 15 s each.
     This agrees with gtile5/6.
   - **Gap:** the symmetry breaking was never tested against an exhaustive run on a NONE case. A
     280 s `--nosym` run at p = 13 did not finish.
   - New and unconfirmed: dfs2 says case (b) is NONE for n = 162 and n = 189 with p = 3, even
     though multiplicative colourings exist there. CP-SAT timed out on both. Cross-check these
     with gtile6.
2. **Prime-power |B| reduces to one cyclic search per level** (`structure/composite_B.md`)
   [own argument, unreviewed].
   - Thm 2: suppose the {3,5,13}-part of |B| is p^a. Then (a) holds or (b_a^p) holds, where
     (b_i^p) means ψ: Z^44 → Z_{p^{i+1}}×Z_{195/p}, injective, with every fibre a coset of
     p^iZ_{p^{i+1}}. The proof needs no Rédei and no Lemma 1. Its key step, Lemma C, gives a
     character χ in supp B̂' that kills every fibre's Fourier transform; Lemma V then says
     vanishing p-term sums of p-power roots of unity are μ_p-cosets.
   - Thm 1: the levels are nested, so one NONE at level a excludes every level ≤ a. Lemmas C and P
     were checked exhaustively on all groups of order p², p³ with p ∈ {3, 5}, which covers every
     C ⊕ B = H with |C| = p, about 88k pairs in Z3³ (`composite_bruteforce.out`). No
     counterexample.
   - gtile7 (gtile6 with coset mode extended to Z_{p^{i+1}}; regression identical to gtile6 at
     hd = 9). Positive controls found solutions at hd = 27 and hd = 125, but no hd = 81 controls
     were run. NONE results, all 20/20 splits [numerical: single implementation]:
     - Z27×Z65 (1.4·10¹⁰ nodes);
     - Z125×Z39 (3.4·10¹⁰ nodes);
     - Z81×Z65 (about 1.7·10¹¹ nodes).
   - Consequence, if Thm 2 and these searches hold: there is no periodic tiling whose
     {3,5,13}-part of |B| is 3, 9, 27, 5, 25 or 13. That last case is level 1, from pass 3.

Dead ends:
- Thm 2's argument fails for mixed {3,5,13}-part (for example |B| = 15): the characters χ_q
  map fibres onto unions of μ_q-cosets, and those cosets can repeat, so χ_q is not injective.

Next ideas, ranked:
1. **/review** `composite_B.md` together with `prime_B_reduction.md`. Close the dfs2 symmetry gap
   with a nosym run on a small NONE case (n = 162 if gtile6 confirms it NONE). Then open a PR:
   "no periodic tiling with |B| a prime power p^a, p = 3 with a ≤ 3, p = 5 with a ≤ 2, p = 13
   with a = 1" (`Part of #31`). Before that, run hd = 81 positive controls and dfs2 at level 2.
2. Bound the level through Thm 3 (the lattice M from block differences). If the primes > 97 force
   unimodular directions, a finite set of levels would suffice, and every prime-power |B| would
   be closed.
3. Mixed |B| = 15: a two-character argument (χ_3, χ_5, χ_3χ_5 in supp B̂').
4. The spectral route with (iii), (iv) or positivity (pass 3, idea 2).

### 2026-11-26: pass 6

Two parallel strategies: closing the dfs2 symmetry gap, and an independent adversarial read of the
two reduction notes. There is no PR this pass. The read was a single referee subagent, not the
formal /review, and the fixes it asks for have not been applied yet.

1. **dfs2 symmetry gap: closed for p = 3** (`independent/out/symgap_summary.txt`)
   [numerical: two independent implementations].
   - gtile6 agrees with dfs2 on every new case:
     - NONE for n = 162 and 189 (p = 3), and for n = 176 and 184 (p = 2);
     - EXISTS for n = 156, 159, 165, 186 and 192 (p = 3), and for n = 174 and 178 (p = 2).
     - Outputs are in `general/out/x*_p*.txt`.
   - Scan with symmetry (`scan_small.sh`): every n ≤ 160 is FOUND for every p ∈ {2,3,5,7,11,13}.
     The only NONE cases up to n = 200 are 162 and 189 (p = 3), 176 and 184 (p = 2), and 195.
   - Exhaustive **no-symmetry** runs are NONE at n = 162 (p = 3, 6.8·10⁷ nodes), n = 176 (p = 2)
     and **n = 195 (p = 3)**.
     - The n = 195 run had 1.7·10⁸ nodes over all 208632 split-2 tasks, in three resumed runs.
       `dfs2_dump.rs` (a copy of dfs2 with `--from`) did the resuming.
     - Coverage was merged from the logs: `out/nosym_n195_p3_coverage.txt`, with per-task node
       counts in `out/nosym_n195_p3_tasks.txt.gz`.
     - So the p = 3 result at 195 does not depend on the symmetry breaking.
   - Exact orbit test (`symcheck.py`) on 17 small FOUND cases with p ∈ {2,3,5,7,13}: all pass.
     - The symmetric solution set is exactly the lex-minimal orbit representatives of the
       no-symmetry set.
     - The orbit sizes sum to the no-symmetry count.
     - The no-symmetry set is closed under the group.
     - Results are in `out/symcheck_small.txt`.
   - Still open: p = 5 and 13 at n = 195 rely on symmetry, which is now supported by the orbit test.
     The no-symmetry run at n = 189 was not done (estimated over 10 min).
2. **Referee read of `prime_B_reduction.md` and `composite_B.md`.** Verdict: both **pass with
   fixes**. There is nothing fatal and no gap that needs a new argument. Tests are in
   `structure/review_pass6/`.
   - Checked correct:
     - D, with the right direction: the dilated set has size coprime to t;
     - Lemma 1 and Q;
     - Steps 1 and 2a–2d;
     - Lemmas V and C, and Thm 1 and Thm 2;
     - removal of the part of |B| coprime to 195 (`pass2.md` Lemma A);
     - coverage: m_π = 1, a prime power, or mixed (the stated gap).
   - Brute force of the abstract Thm 2 claim, with 195 replaced by n = 6 or 10, found no failures
     in 18 groups.
     - Only one coprime-part case was tested (Z30, n = 6), and several planned groups never ran.
     - Negative control: Z36 with n = 6 and m_π = 6 mixed gives 14 failures, so the single-prime
       hypothesis is really needed.
   - Fixes to apply:
     - prime note §0: "m = 1 or composite";
     - state squarefree 195 as a hypothesis in §3;
     - 2b: the fibres are "up to translation";
     - Lemma 1: say why kd ≠ 0;
     - composite note: drop the redundant "(or (a))";
     - state the quantifier via Per(L);
     - Thm 3 Smith form: handle d_r = 0;
     - record the sampled Lemma C/P result.
   - **New observation (referee):** (a) ⇒ (b_i^p), so the NONE results at level ≥ 1 already
     exclude multiplicative colourings at 195. That gives an independent recheck of FP90, though
     from a single implementation per level above 1.

Next ideas, ranked:
1. Apply the referee's fixes. Run hd = 81 positive controls for gtile7. Then run the formal /review
   and open the PR "no periodic tiling with |B| a prime power, levels as in pass 5", `Part of #31`.
   Label it [own argument, reviewed] together with [numerical: two implementations at level 1,
   one at levels 2 and 3].
2. dfs2 at level 2 (Z27×Z65, Z125×Z39), as a second implementation for gtile7.
3. Bound the level via Thm 3 (pass 5, idea 2).
4. Mixed |B| = 15 (pass 5, idea 3).

### 2026-11-27: pass 7

Two parallel strategies: applying the referee's fixes together with the missing gtile7 controls,
and a second independent implementation at levels 2 and 3. Both completed. There is no PR this
pass, because the formal /review has still not been run on the reduction notes.

1. **Referee fixes applied** to `structure/prime_B_reduction.md` and `structure/composite_B.md`.
   Each file now ends with a "Revision (pass 7)" section.
   - All eight fixes from pass 6 are in. None turned out to be wrong when re-derived.
   - Two changes go slightly beyond wording:
     - Thm 3's Smith form now handles d_r = 0: the bound ranges over the nonzero d_r only.
     - The quantifier now goes through m(Λ) = m(Per(L))·[Per(L):Λ].
   - §6 now records the sampled Lemma C/P result: no counterexample on Z81, Z27×Z3, Z9², Z9×Z3²
     and Z3⁴. **The p = 5 groups Z125, Z25×Z5 and Z5³ were never tested.**
2. **hd = 81 positive controls for gtile7** (`general/out/m27_hd81_controls.txt`).
   - gtile7.exe was rebuilt first.
   - Controls: n = 30, 60, 99, 120 and 150 give EXISTS on all 20 splits; n = 180 gives EXISTS on 7
     splits and hit the time limit on the rest.
   - 19 witnesses really use the level-3 residues: their H-values lie outside 27Z81. All 19 pass
     `check_general.py`. A perturbed witness is rejected.
   - **n = 162, p = 3 is NONE at levels 1 and 2 but EXISTS at level 3.**
     - Level 1: two implementations (pass 6).
     - Level 2: gtile7 gives 20/20 NONE, and dfs3 also gives NONE (item 3).
     - Level 3: gtile7 finds a witness, 2.4·10⁹ nodes, which passes `check_general.py` and a
       direct check of its fibres.
     - So the level hierarchy is strict, and a NONE at low levels says nothing about higher
       levels. This makes idea 2 below (bounding the level) essential.
3. **dfs3, an independent search at levels 2 and 3** (`independent/dfs3.rs`). It extends dfs2 with
   `--level i` and shares no code with gtile7 [numerical: two independent implementations; dfs3
   uses symmetry breaking].
   - Validation:
     - At level 1 it reproduces dfs2 exactly, node counts included.
     - Exact counts match `brute_count3.py` on 13 tiny cases at levels 2 and 3.
     - The greedy, asc and desc orders agree.
     - The orbit test (`symcheck3.py`) passes on 18 cases.
     - 159 level-2 controls and 58 level-3 controls are FOUND, and every witness passes
       `direct_check3.py`.
     - The 107 level-1 witnesses, lifted to each higher level, are accepted; perturbed copies are
       rejected.
   - Also found: n = 189 has a level-2 witness, although it is NONE at level 1.
   - n = 195 results, all tasks done, agreeing with gtile7:
     - Z27×Z65: NONE, 2.1·10⁶ nodes;
     - Z125×Z39: NONE, 2.0·10⁶ nodes;
     - Z81×Z65: NONE, 5.2·10⁶ nodes.
     Commands are in `independent/out/dfs3_n195_*.txt`.
   - Gaps:
     - None of the n = 195 runs at levels 2 and 3 was repeated without symmetry breaking.
     - p = 13 has only 3 controls at level 2.
     - Level 3 has controls only for p = 3.
     - Z625×Z39 (p = 5, level 3) was not run.

Dead ends: none new.

Next ideas, ranked:
1. Run the formal **/review** on both reduction notes, then open the PR "no periodic tiling with
   |B| a prime power: p = 3 with a ≤ 3, p = 5 with a ≤ 2, p = 13 with a = 1" (`Part of #31`). The
   searches now have two implementations at every level. Before the PR, if there is time, rerun the
   dfs3 Z27×Z65 case without symmetry (`--nosym`).
2. **Bound the level** via Thm 3, the lattice of block differences. The n = 162 result shows this
   is essential: any full exclusion of prime-power |B| needs a finite bound on the level.
3. Extend the levels: Z243×Z65 and Z625×Z39 with dfs3, and Z13³×Z15 at level 2.
4. Mixed |B| = 15: a two-character argument (pass 5, idea 3).

### 2026-11-27: pass 8

Two parallel strategies: a symmetry-free rerun plus level extensions (computation), and a
structural bound on the level. There is no PR this pass: the formal /review has still not been run
(the budget ran out).

1. **Z27×Z65 (p = 3, level 2) at n = 195 is NONE without the lex-leader symmetry breaking**
   [numerical: dfs3 with `--nosym --first`; 9.09·10⁶ nodes, all 586589 tasks].
   - A pure `--nosym` run was projected at about 3 h, so it was not done.
   - Instead, dfs3 got a new flag, `--first`, which restricts only the first variable (prime 2) to
     orbit representatives of U(Z27)×U(Z65). The representatives come from a separate script,
     `orbit_reps3.py`.
   - This is sound because every group element γ is an automorphism of G that fixes F, so γ∘φ is
     a solution exactly when φ is.
   - Checks:
     - `firstcheck3.py` passes on 9 small cases: the `--first` solution set equals the nosym set
       filtered on its first value, and its orbit closure equals the full nosym set.
     - `symcheck3.py` passes at n = 21, 24, 27 and 30.
   - Commands are in `independent/out/pass8_runs.txt`.
2. **Z625×Z39 (p = 5, level 3) at n = 195: incomplete.** 8994 of 11149 split-2 tasks finished, with
   no solution. To resume, use the command in `pass8_runs.txt`; expect about 6.5 min of setup.
   - The 12 p = 5 level-3 controls are all FOUND, but they are weak: each is a lift of a level-2
     solution.
   - Z243×Z65 (level 4) was not run.
3. **Level bound, structural** (`structure/pass8_level.md`, scripts in `structure/pass8_level/`).
   - Prop. 1 [own argument, unreviewed]: for fixed partition data, the minimal level is the least
     i such that f vanishes on M ∩ p^{i+1}Z^k. So the level is at most log_p exp(Γ_p).
   - **Conjectured sharp bound [conjecture]: level ≤ v_p(n/p).** It reduces to Lemma S:
     exp(Γ_p) ≤ p^{v_p(n/p)} for a downset T and a g whose fibres on T all have size p.
     - At n = 195, v_p(195/p) = 0 for every p | 195. So Lemma S would turn every (b_i^p) into (a),
       and FP90/CCP would then exclude all periodic tilings whose m_π is a single prime power.
   - Evidence [numerical: single implementation]:
     - Every [n] case where level 1 fails but a higher level succeeds needs exactly v_p(n/p):
       162 needs 3, 189 needs 2, 184 needs 2, and 176 needs 3. The n = 176 data (level 2 NONE,
       level 3 FOUND) is new this pass and was predicted before the run.
     - The exhaustive downset brute force in N² and N³ found no violation, and the bound is
       attained.
     - Lemma K, which implies Lemma S, holds in all 165 real witnesses.
   - Where the argument breaks: Lemma 2 rules out only those torsion classes that are differences
     of points of T. An equivalent goal is to show that W = ker ḡ is torsion-free in the tiling
     S ⊕ W = Γ.
   - The downset hypothesis is essential: T = {0, 4}, p = 2 needs level 2.

Dead ends: a pure `--nosym` run at level 2 is too slow for one pass (about 3 h).

Next ideas, ranked:
1. **Test Lemma S directly on T_195.** Search for maps g whose fibres on T_195 all have size p,
   with no f, and compute Γ_p for each. Then try to prove Lemma S for downsets, by induction on
   |T| or by showing W is torsion-free. If it holds, the prime-power |B| family is closed at 195.
2. Run the formal /review on the reduction notes plus Prop. 1, then open the finite-level PR
   (`Part of #31`).
3. Finish Z625×Z39 at level 3 (resume), then Z243×Z65 at level 4.
4. Mixed |B| = 15.
