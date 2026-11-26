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
   - Status at the end of this pass: **309 of 776 classes NONE, no EXISTS.** The remaining classes
     are slow: with `dil=1` and generic B, D0 has hundreds of elements, so a node costs about 100×
     more. The 20 processes were left running, one output line per class in `out/m3_*.txt`, with
     limit = 10⁹ nodes per class (TIMEOUT if hit).
   - Labels: [numerical: single implementation, so far]. A NONE here is not evidence against 195
     (see item 4); only an EXISTS matters. `check_general.py` (independent, from the definition) is
     ready for any hit and passes on n = 12.

Dead ends:
- `periodic/kper_indep.py` (a pure-Python cross-check of kper) is far too slow at n = 195; it did
  not finish n = 205 in about 40 min. gtile replaced it.
- Excluding 195 by bounded periodic searches is ruled out as a proof strategy until a three-prime
  analogue of Wang–Wang §4.3–4.4 exists. Do not spend passes on null searches for that purpose.

Next ideas, ranked:
1. **Finish the m = 3 sweep.**
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
