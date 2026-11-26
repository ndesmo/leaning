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

Dead ends: none yet.

Next ideas, ranked:
1. Reproduce the Wang–Wang finite computation for 205, then run it at 195. Identify which part
   blows up, and whether symmetry or the reduction above cuts it down.
2. Recover or re-prove "Prop. 3": complements B of prime size p in tilings of ℤ_{np}. The
   candidate tools are Sands' and Tijdeman's replacement theorems and the Hajós property, using
   that 585 = 3²·5·13 has the form p²qr. Then the kper NONE results become a theorem modulo the
   computation.
3. Widen kper to non-cyclic G of order 195p (ℤ_3² × ℤ_65 for p = 3, and so on) and to |B| = p²,
   pq.
4. A second, independent implementation of the kper class, for example a SAT encoding, so the
   NONE results are double-checked.
