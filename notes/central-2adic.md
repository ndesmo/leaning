# NOTES: 2-adic valuation of central coefficients of (1+x+…+x¹⁵)ⁿ

Problem P2 of `PROBLEMS.md`, issue #22. Slug `central-2adic`.

Labels: [Lean], [Lean | hyp: …], [paper: ref, Thm], [preprint: ref, Thm], [standard: ref],
[numerical ± err], [conjecture], [own argument, unreviewed]. See `.claude/skills/prove/SKILL.md`.

Reference: **[A402341]** OEIS A402341, "Central (largest) coefficient of (1 + x + x^2 + ... +
x^15)^n", author Sajid Khan Hussain, Nov 17 2026, status approved, revision #13 (Nov 17 2026
10:25:10; the last revision as of 2026-11-26). https://oeis.org/A402341

## Statement

Let a(n) = [x^⌊15n/2⌋] (1 + x + … + x¹⁵)ⁿ and s₂ = binary digit sum (OEIS A000120).

**Target (comment of [A402341], verbatim):** "Conjecture: for even n, the 2-adic valuation of a(n)
equals A000120(15*n/2). Verified for n <= 1500." [conjecture]

That is: for every even n ≥ 0, v₂(a(n)) = s₂(15n/2).

**Natural generalization (ours, not in the entry).** For q = 2^r and even n,
v₂([x^{(q−1)n/2}] (1 + … + x^{q−1})ⁿ) = s₂((q−1)n/2). [conjecture; numerical support below]
For q = 2 this is Kummer's theorem for C(n, n/2) (see Literature, L3).

## Setting

- Exact formula ([A402341] %F, also A077042, A273975, Bollinger–Burchard property d)):
  a(n) = Σ_{j=0..⌊h/16⌋} (−1)^j C(n,j) C(n−1+h−16j, n−1), h = ⌊15n/2⌋, n ≥ 1.
- 1 + x + … + x¹⁵ = (1+x)(1+x²)(1+x⁴)(1+x⁸), so
  a(n) = Σ_{i+2j+4k+8l = 15n/2} C(n,i) C(n,j) C(n,k) C(n,l). [standard]
- By Kummer's theorem (L3), s₂(15n/2) = v₂(C(15n, 15n/2)) for even n, so the conjecture says
  v₂(a(n)) = v₂(C(15n, 15n/2)). [standard + own argument, unreviewed (one line)]
- Mod 2, 1 + … + x¹⁵ ≡ (1+x)¹⁵, which gives the odd case proved in the entry (L1).
- Symmetric-variable form (the entry's third %F): with u = x^{1/2} + x^{−1/2},
  x^{−1/2}(1+x) = u, x^{−1}(1+x²) = u² − 2, x^{−2}(1+x⁴) = u⁴ − 4u² + 2,
  x^{−4}(1+x⁸) = u⁸ − 8u⁶ + 20u⁴ − 16u² + 2 (each factor is the previous squared minus 2). So
  x^{−15n/2}(1+…+x¹⁵)ⁿ = f(u)ⁿ with f(u) = u(u²−2)(u⁴−4u²+2)(u⁸−8u⁶+20u⁴−16u²+2), and since the
  x⁰-coefficient of u^m is C(m, m/2) for even m, a(n) = Σ_m c(n,m) C(m, ⌊m/2⌋),
  c(n,m) = [u^m] f(u)ⁿ, m ≡ n (mod 2). The top term m = 15n has c = 1 and is C(15n, ⌊15n/2⌋).
  [A402341 %F] + [own argument, unreviewed: the derivation above; formula also checked exactly
  for n ≤ 120 by `dominant_term.py`]

## Claims ledger

| Claim | Label | Where |
|---|---|---|
| For even n, v₂(a(n)) = s₂(15n/2) | [conjecture] ([A402341]: "Verified for n <= 1500") | Statement |
| a(n) is odd iff n = (16^k − 1)/15 for some k ≥ 0 | [A402341 comment, proof given there; not yet re-checked by /review] | Literature, L1 |
| Conjecture holds for every even n ≤ 4000 | [numerical, exact mod 2^48, no undetermined case; Python, not Lean] | Numerics, N1 |
| Analogue v₂ = s₂((q−1)n/2) holds for all even n ≤ 2000 when q = 4, 8, 32, 64, and for even n ≤ 300 when q = 2 | [numerical, exact mod 2^48; Python, not Lean] | Numerics, N2 |
| The analogue fails for q = 3, 6, 12 (first failures n = 2) | [numerical, exact] | Numerics, N2 |
| For odd n, v₂(a(n)) − s₂(⌊15n/2⌋) takes values from −11 to 10 for n ≤ 4000 (no simple equality) | [numerical, exact mod 2^48] | Numerics, N3 |
| a(n) = Σ_m c(n,m) C(m, ⌊m/2⌋) with c(n,m) = [u^m] f(u)ⁿ | [A402341 %F] + [own argument, unreviewed]; checked exactly n ≤ 120 | Setting |
| Termwise dominance: for every even n ≤ 120 and every m < 15n with c(n,m) ≠ 0, v₂(c(n,m) C(m, m/2)) > s₂(15n/2) (excess ≥ 1) | [numerical, exact integers; Python] | Numerics, N4 |
| q = 4 carry inequality t + v₂(C(n,t)) + s₂(3n/2 − t) > s₂(3n/2) for even n ≤ 2000, 1 ≤ t ≤ n | [numerical, exact] | Numerics, N5; A1 |
| Termwise dominance for all even n implies the conjecture | [own argument, unreviewed] (the top term has valuation exactly s₂(15n/2) by Kummer, every other term strictly more) | Attack ideas, A1 |

## Literature (2026-11-26)

**L1. The entry itself.** Retrieved 2026-11-26 in OEIS internal format
(`https://oeis.org/search?q=id:A402341&fmt=text`). Verbatim:
- %N: "Central (largest) coefficient of (1 + x + x^2 + ... + x^15)^n."
- %C: "a(n) is the size of a largest antichain in the product of n chains of 16 elements each (de
  Bruijn, Tengbergen, and Kruyswijk)."
- %C: "a(n) is odd if and only if n = (16^k - 1)/15 for some k >= 0, i.e., n = 0, 1, 17, 273,
  4369, ... Proof: modulo 2, 1 + x + ... + x^15 == (1+x)^15, so a(n) == binomial(15*n,
  floor(15*n/2)) (mod 2). By Lucas's theorem, binomial(N, floor(N/2)) is odd iff N = 0 or N = 2^m
  - 1, and 15*n = 2^m - 1 holds iff 4 | m."
- %C: "Conjecture: for even n, the 2-adic valuation of a(n) equals A000120(15*n/2). Verified for n
  <= 1500."
- %D: "N. G. de Bruijn, Ca. van Ebbenhorst Tengbergen, and D. Kruyswijk, On the set of divisors of a
  number, Nieuw Archief voor Wiskunde (2) 23 (1951), 191-193."
- %H: b-file "Table of n, a(n) for n = 0..829" (by the author).
- %F: "a(n) ~ 16^n * sqrt(2/(85*Pi*n))."; "a(n) = Sum_{j=0..floor(h/16)} (-1)^j * binomial(n,j) *
  binomial(n-1+h-16*j, n-1) with h = floor(15*n/2), n >= 1."; "a(n) = Sum_{m>=0, m==n (mod 2)}
  c(n,m)*binomial(m, floor(m/2)), where c(n,m) is the coefficient of u^m in
  (u*(u^2-2)*(u^4-4*u^2+2)*(u^8-8*u^6+20*u^4-16*u^2+2))^n."
- %Y: "Row 16 of A077042." and "Cf. A005190, A005191, A018901, A025012, A025013, A025014, A025015,
  A201549, A201550, A201551, A201552, A225779, A273975."
- %K nonn,easy,new. %A "_Sajid Khan Hussain_, Nov 17 2026". Programs by Kotesovec, Marcus.
- A search subagent read the history page (https://oeis.org/history?seq=A402341): revisions #4–#13
  all dated Nov 17 2026 (edits by Marcus, Kotesovec, De Vlieger); discussion only "Asymptotics is
  correct." and a reference request; nothing on the 2-adic conjecture. Revisions #1–#3 not shown.
- Remark on the odd-case proof: "binomial(N, floor(N/2)) is odd iff N = 0 or N = 2^m − 1" is
  Lucas's theorem (⌊N/2⌋ ≤ N bitwise iff N's binary digits are all 1); and 15n = 2^m − 1 needs
  15 | 2^m − 1, i.e. 4 | m. We have not yet re-derived this formally; the attack stage should.

**L2. Sibling OEIS entries** (all retrieved 2026-11-26 in internal format). None states a 2-adic
valuation result or conjecture:
- A005190 "Central quadrinomial coefficients: largest coefficient of (1 + x + x^2 + x^3)^n."
  (q = 4; %C "The maximal coefficient is that of x^[3n/2]."; bisections A005721, A005723). No
  2-adic comment. A005721 (= A005190(2n), per the search subagent) has formulas only, e.g. "a(n) =
  Sum_{k = 0..2*n} binomial(2*n, k)*binomial(6*n-2*k, 3*n-k)*(-2)^k" (Peter Bala, Dec 01 2025, as
  relayed by the subagent).
- A025013 "Central octonomial coefficients: largest coefficient of (1+x+...+x^7)^n." (q = 8). No
  2-adic comment.
- A077042 (square array, rows = q; Bottomley 2002), A273975 (all coefficients; Zabolotskii 2016,
  revised Nov 17 2026, keyword "changed" (its %Y list does not mention A402341)), A201552, A005191,
  A018901, A025012, A025014, A025015, A201549, A201550, A201551, A225779: asymptotics, recurrences,
  formulas; no 2-adic statements.
- A000984 (central binomial): %F "A007814(a(n)) = A000120(n). - _Vladimir Shevelev_, Jul 20 2009"
  (the q = 2 case).
- A134660 (number of odd coefficients of (1+x+x²+x³)ⁿ) = 2^{s₂(3n)} per the search subagent;
  a parity count, not a valuation.
- The same author (Sajid Khan Hussain) has no other sibling entry among those cross-referenced.

**L3. Kummer / Legendre.** [standard: E. Kummer, J. Reine Angew. Math. 44 (1852); e.g. Granville,
"Arithmetic properties of binomial coefficients I", CMS Conf. Proc. 20 (1997)] v_p(C(a+b, a)) =
number of carries when adding a and b in base p; in particular v₂(C(2m, m)) = s₂(m). Multinomial
form (Wikipedia "Kummer's theorem", verbatim from the page source as relayed by the search
subagent): "ν_p binom(n; m_1,…,m_k) = (1/(p−1)) ((Σ_{i=1}^k S_p(m_i)) − S_p(n))". Primary source
suggested: D. Singmaster, "Divisibility of binomial and multinomial coefficients by primes and prime
powers", Fibonacci Assoc. 18th Anniv. Vol. (1980) 98–113 (not accessed).

**L4. Lucas-type congruence for (1+…+x^{k−1})ⁿ.** R. C. Bollinger, C. L. Burchard, "Lucas's
theorem and some related results for extended Pascal triangles", Amer. Math. Monthly 97 (1990)
198–204. Original not accessed (JSTOR). Statement quoted second-hand from R. Meštrović, "Lucas'
theorem: its generalizations, extensions and applications (1878–2014)", arXiv:1409.3820, pp. 39–40
(pdftotext; spot-checked by us, symbols partly lost): with (1 + x + … + x^{k−1})^n =
Σ_m C_k(n, m) x^m, "if p is a prime, and if n = n0 + n1p + · · · + nsp^s and m = m0 + m1p + · · · +
msp^s are the p-adic expansions of n and m, then (108) Ck(n, m) ≡ Σ_{r0,...,rs} Π_{i=0}^{s}
Ck(ni, ri) (mod p), where the sum is taken over all (s + 1)-tuples (r0, r1, . . . , rs) such that
i) m = r0 + r1p + · · · + rsp^s and ii) 0 ≤ ri ≤ (k − 1)ni for each i = 0, 1, . . . , s; if m is not
representable in this form, then certainly Ck(n, m) ≡ 0 (mod p)." Mod p only; gives parity, not
v₂. [paper: Bollinger–Burchard 1990, Thm 1, via Meštrović's survey; verify against the original
before citing]

**L5. Same-shape results for the infinite product ∏(1 − x^{2^j}).** (Background; different
object, but the identical "v₂ = v₂(binomial)" shape and 2-adic recurrence methods.)
- M. Gawron, P. Miska, M. Ulas, "Arithmetic properties of coefficients of power series expansion of
  ∏_{n=0}^∞(1−x^{2^n})^t (with an Appendix by Andrzej Schinzel)", arXiv:1703.01955 v1 (6 Mar 2017),
  no journal ref on arXiv. Theorem 3.3 (read by a subagent in the HTML version, not quoted
  verbatim because of tool limits): for k ∈ ℕ and all n, ν₂(t_{2^k}(n)) = ν₂(C(n+2^k−1, 2^k−1)),
  where t_m(n) = [x^n] ∏(1−x^{2^j})^m. [preprint: GMU17, Thm 3.3; verbatim text still to be
  extracted]
- Z. Shen, "Powers of the Thue–Morse Series: 2-Adic Valuations and Automatic Odd Parts",
  arXiv:2609.16966 (15 Sep 2026). Theorem 1.1 (pdftotext by the search subagent; ν and binomial
  garbled): "Let r ≥ 1 and put m = 2^r. For every n ≥ 0, ν2(tm(n)) = ν2 C(n+m−1, m−1). Moreover,
  for every s ≥ 1, the sequence (odd(tm(n)) mod 2^s)_{n≥0} is 2-automatic." Method: the
  functional equation T(x) = (1 − x)T(x²). [preprint: Shen 2026, Thm 1.1]
- Note the analogy: here ∏_{j<r}(1 + x^{2^j}) = (1 − x^{2^r})/(1 − x) satisfies
  F_r(x) = (1 + x)F_{r−1}(x²), a finite analogue of that functional equation.

**L6. Not relevant (checked).** Straub–Moll–Amdeberhan, "The p-adic valuation of k-central
binomial coefficients", Acta Arith. 140 (2009), arXiv:0811.2028 (coefficients of (1−k²x)^{−1/k});
D. M. Davis, "Some 2-adic Integers Related to the Odd Part of 2^e!", J. Integer Seq. 29 (2026),
Art. 26.3.1 (title and abstract read via pdftotext: about OEIS A359349); Boros–Moll–Shallit
arXiv:math/0308072; Deutsch–Sagan and Pan–Sun / Mikić (central trinomial, odd p or 3-adic).

**Search scope (2026-11-26).**
- OEIS: A402341 (entry, b-file, history), A077042, A273975, A201552, A005190, A005721, A005723,
  A005191, A018901, A025012–A025015, A201549–A201551, A225779, A174061, A000984; OEIS full-text
  searches "A402341", "central 2-adic A000120", "quadrinomial 2-adic", "octonomial". The search
  "A402341" returned only A402341 itself.
- Web search queries, including "A402341 OEIS central coefficient 2-adic
  valuation", "2-adic valuation central coefficient (1+x+...+x^{q-1})^n binary digit sum",
  "central coefficient (1+x+x^2+x^3)^n divisible power of 2", Bollinger–Burchard, Granville
  polynomial powers, compositions with bounded parts + valuation).
- arXiv API abstract searches: central coefficient(s) + valuation/2-adic/divisibility, largest
  coefficient + valuation, polynomial coefficients + valuation, central trinomial, quadrinomial,
  central multinomial, extended binomial, antichain + valuation, Lucas + polynomial powers,
  A402341.
- StackExchange API (MathOverflow and Math.SE): "central coefficient 2-adic",
  "1+x+x^2+x^3 coefficients power of 2", "A402341", and all posts since 2026-11-01 matching
  "2-adic", "central coefficient", "x^{15}", "binary digit sum coefficient".
- Not accessed: Bollinger–Burchard original; Singmaster 1980; Granville's polynomial-power formula
  (images only on the HTML page); full verbatim theorem text of GMU17; A402341 revisions #1–#3.

**Verdict.** Open: no proof, disproof or discussion of the conjecture (or of the q = 2^r
analogue) found in the works searched, as of 2026-11-26.

## Numerics

Scripts in `search/central-2adic/` (run with `python -I`):
- `check_v2.py [N] [q …] [--bfile PATH]`: computes a_q(n) mod 2^48 for n ≤ N by the recurrence
  P_n = P_{n−1}(1 − x^q)/(1 − x) (truncated at the final centre), cross-checks against the exact
  alternating-sum formula at ≥ 200 sampled n, and (q = 16) against the A402341 b-file.
- `dominant_term.py [N]`: exact c(n,m), checks the %F u-formula against the exact a(n), and
  tests termwise 2-adic dominance (A1).
- N5 was a one-line inline check, not saved as a script (q = 4 form of A1).

Results (2026-11-26):
- **N1.** `python -I check_v2.py 4000 16 --bfile b402341.txt`: cross-check OK at 220 n; all 830
  b-file terms agree mod 2^48; for every even n ≤ 4000, v₂(a(n)) = s₂(15n/2); no residue was 0 mod
  2^48. [numerical, exact mod 2^48]
- **N2.** `check_v2.py 2000 4 8 32 64`: analogue v₂ = s₂((q−1)n/2) holds for every even n ≤ 2000,
  q = 4, 8, 32, 64; `check_v2.py 300 2 4 8 16 32`: holds for even n ≤ 300 (q = 2 is Kummer).
  For q = 3, 6, 12 it fails (e.g. q = 3, n = 2: v₂ = 0, s₂(2) = 1; q = 6, n = 2: v₂ = 1,
  s₂(5) = 2), so the power-of-2 structure matters. [numerical]
- **N3.** Odd n, q = 16, n ≤ 4000: d(n) = v₂(a(n)) − s₂(⌊15n/2⌋) ranges over −11..10; counts
  {−11:1, −10:1, −9:2, −8:4, −7:8, −6:16, −5:31, −4:62, −3:125, −1:125, 0:63, 1:281, 2:142,
  3:570, 4:288, 5:142, 6:73, 7:36, 8:18, 9:8, 10:4}; d = −2 never occurs. Small values:
  d(1) = −3, d(17) = −7 (the odd a(n)), d(3) = d(7) = 3. No conjecture proposed for odd n.
  [numerical]
- **N4.** `dominant_term.py 120`: the u-formula equals the exact a(n) for all n ≤ 120; for every
  even n ≤ 120, every term m < 15n has v₂(c(n,m) C(m, m/2)) ≥ s₂(15n/2) + 1 (minimum excess 1 to
  4). [numerical, exact integers]
- **N5.** q = 4 form of A1: t + v₂(C(n,t)) + s₂(3n/2 − t) > s₂(3n/2) holds for every even
  n ≤ 2000 and 1 ≤ t ≤ n (exact integers). [numerical]

## Attack ideas

- **A1. Termwise dominance in the u-expansion (best lead).** By N4, for even n the conjecture
  would follow from: for every even m < 15n, v₂(c(n,m)) + s₂(m/2) > s₂(15n/2). [own argument,
  unreviewed for the implication; the inequality is numerical for n ≤ 120]. The factor
  g_j(u) = 2T_{2^j}(u/2) (T = Chebyshev) has coefficients with known 2-adic valuations
  (u² − 2; u⁴ − 4u² + 2; u⁸ − 8u⁶ + 20u⁴ − 16u² + 2): lowering the degree by 2t costs a power of 2
  depending on t. Plan: bound v₂(c(n,m)) from below by a multinomial expansion of f(u)ⁿ, and bound
  s₂(15n/2) − s₂(m/2) ≤ (number of "borrows"), via Legendre. Try q = 4 first (f = u(u² − 2), so
  c(n, 3n − 2t) = (−2)^t C(n, t) exactly) — then the claim is
  t + v₂(C(n,t)) + s₂(3n/2 − t) > s₂(3n/2) for 1 ≤ t ≤ n, which is a clean carry inequality and
  should be provable outright; then q = 8, 16 and general q = 2^r.
- **A2. Kummer carries in the 4-fold product.** a(n) = Σ C(n,i)C(n,j)C(n,k)C(n,l) over
  i + 2j + 4k + 8l = 15n/2; v₂ of each term is a sum of carry counts. Identify the terms of minimal
  valuation and show their number is odd (2-adic cancellation control).
- **A3. Recursion F_r(x) = (1 + x)F_{r−1}(x²).** a_{2^r}(n) = Σ_i C(n, i) [x^{(c−i)/2}]
  F_{r−1}(x)ⁿ with c − i even, mirroring Gawron–Miska–Ulas / Shen's T(x) = (1−x)T(x²). Induction on
  r, with q = 2 (Kummer) as base, might go through if the off-centre coefficients
  [x^{c'}]F_{r−1}ⁿ also have controlled valuation — tabulate v₂ of off-centre coefficients first.
- **A4. 2-adic Lucas / Granville-type congruence mod 2^{s+1}.** Use
  1 + … + x^{15} = (1+x)^{15} · ∏ (1 − 2x·(…)/(1+x)^{…}) to compare a(n) with C(15n, 15n/2) modulo
  2^{s₂(15n/2)+1}; equivalent in spirit to A1.
- **First target.** Prove the q = 4 case (A005190, even n: v₂ = s₂(3n/2)) via A1, then q = 8,
  then q = 16. Lean: Mathlib has Kummer-type lemmas `Nat.factorization_choose`
  (`Mathlib/Data/Nat/Choose/Factorization.lean`) and `multiplicity_choose`
  (`Mathlib/NumberTheory/Padics/PadicVal/Basic.lean`); small cases can be checked by `decide`.

## Review

(none yet)

## Log

- **2026-11-26.** Literature stage (issue #22, branch `agent/central-2adic-literature`). Re-checked
  openness: A402341 still at revision #13 of 2026-11-17, no comment on the conjecture beyond the
  original; no proof found elsewhere (scope above). Quoted the entry verbatim and collected L2–L6.
  Numerics N1–N4 (scripts in `search/central-2adic/`): conjecture holds for even n ≤ 4000; the
  q = 2^r analogue holds for q = 4, 8, 32, 64 up to n = 2000 and fails for q = 3, 6, 12; termwise
  2-adic dominance of the top term in the u-formula holds for even n ≤ 120 (attack lead A1).
  [numerical, Python, not Lean] P2 marked `taken (#22)` in `PROBLEMS.md`; LEDGER entry added.
  /review not run on this stage.
