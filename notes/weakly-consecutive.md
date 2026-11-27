# NOTES: weakly consecutive sequences start or end with 1

Problem P1 of `PROBLEMS.md`, issue #21. Slug `weakly-consecutive`.

Labels: [Lean], [Lean | hyp: …], [paper: ref, Thm], [preprint: ref, Thm], [standard: ref],
[numerical ± err], [conjecture], [own argument, unreviewed]. See `.claude/skills/prove/SKILL.md`.

Reference: **[GSK24]** T. Garrison, C. Seiler, A. Knowles, "Weakly Consecutive Sequences",
arXiv:2401.09497 v1 (17 Jan 2024, 14 pages, math.CO / math.NT; PDF dated October 2023).
https://arxiv.org/abs/2401.09497. Unrefereed preprint: no journal version found, and the first
author's homepage still lists it as a preprint (2026-11-25).

## Statement

**Target (Conjecture 5.2 of [GSK24]).** Let k ≥ 1 and let σ be a permutation of [k] = {1, …, k}
such that for all i, j ∈ [k] and all integers m, if m ∣ σ(i) and m ∣ (i − j) then m ∣ σ(j). Then
σ(1) = 1 or σ(k) = 1. [conjecture]

## Setting

- σ is a *WCS* ("weakly consecutive sequence") of length k. Only m ∈ [2, k] matter: m = 1 is
  vacuous, and for m > k no value is divisible by m. Negative m reduce to |m|.
- N(k) = number of WCS of length k. OEIS A395372 (Charles R Greathouse IV, 20 Apr 2026),
  "Number of weakly consecutive sequences of length n", cites only [GSK24] and has no comment on
  Conjecture 5.2.
- Reversal R(σ)(i) = σ(k − i + 1) maps WCS to WCS ([GSK24] Rule 3), so the target is symmetric
  under i ↦ k + 1 − i.

## Claims ledger

| Claim | Label | Where |
|---|---|---|
| Conjecture 5.2: every WCS has σ(1) = 1 or σ(k) = 1 | [conjecture] | Statement |
| Conjecture 5.1 (4 seeds, 3 rules generate every WCS) verified by computer up to k = 500 | [preprint: GSK24, §5] (authors' claim, not re-run) | Literature |
| Conjecture 5.1 implies Conjecture 5.2 | [preprint: GSK24, §5] (stated: check on the seeds, preserved by the rules) | Literature |
| σ is a WCS iff S_m^σ = T_m^σ for all m ∈ [k] | [preprint: GSK24, Lemma 2.2] | Literature |
| For a WCS, m ∈ [k] and every x ∈ [k] with m ∣ x, σ^{-1}(x) ∈ [(k mod m) + 1, k − (k mod m)] (in particular for x = m) | [preprint: GSK24, Lemma 2.3, read with m ∣ x] + [own argument, unreviewed: the reading and a re-derivation] | Literature, item 4 |
| Division slices D_d(σ) of a WCS are WCS | [preprint: GSK24, Lemma 2.4] + [own argument, unreviewed: the reading m = k] | Literature, item 5 |
| Reversal preserves WCS | [preprint: GSK24, Rule 3]; re-proved from Def. 1.1 [own argument, unreviewed] | Literature; Attack ideas, A6.0 (b) |
| Class lemma: for a WCS and m ∈ [k], T_m is the residue class of σ^{-1}(m) mod m inside [k], of size ⌊k/m⌋ (direction WCS ⇒ classes of GSK24 Lemma 2.2) | [own argument, unreviewed] | Attack ideas, A6.0 (a) |
| Conjecture 5.2 holds for every k ≤ 16: every WCS σ of [k] (Def. 1.1 verbatim, m ∈ ℤ) has σ(1) = 1 or σ(k) = 1 (`conjecture_5_2_le_16`) | [Lean] (`halfline_lt/Proofs/WeaklyConsecutive.lean`; kernel `decide +kernel` on a pruned enumerator proved complete, no `native_decide`) | Log 2026-11-25 (Lean) |
| N(k) for k = 1..23 is 1, 2, 2, 4, 4, 4, 4, 4, 8, 16, 16, 4, 4, 2, 2, 8, 8, 8, 8, 4, 12, 16, 16, and no WCS with 16 < k ≤ 23 violates Conjecture 5.2 | [numerical, exact enumeration, Python, not Lean] (the counts are not proved in Lean for any k: the enumerator's soundness is not formalized) | Log 2026-11-25 |
| σ^{-1}(1) is the unique position not in ⋃_{p ≤ k prime} T_p; so Conjecture 5.2 ⇔ for every WCS the prime classes T_p cover {2, …, k − 1} | [own argument, unreviewed] | Attack ideas, A1 |
| T_m ∩ T_n = T_{lcm(m,n)} if lcm(m,n) ≤ k, and = ∅ otherwise | [own argument, unreviewed] | Attack ideas, A2 |
| For every m ∈ (k/2, k] (prime or not), T_m = {σ^{-1}(m)} and σ^{-1}(m) ∈ [k − m + 1, m] | [preprint: GSK24, Lemmas 2.2, 2.3] + [own argument, unreviewed] | Attack ideas, A3 |
| For every m ∈ (k/3, k/2] (prime or not), T_m = {ρ, ρ + m} with ρ ∈ (k − 2m, m], and σ^{-1}(m) ∈ {ρ, ρ + m} | [preprint: GSK24, Lemma 2.2] + [own argument, unreviewed] | Attack ideas, A3 |
| For odd k, every even value sits at an even position, so σ^{-1}(1) is odd | [preprint: GSK24, Lemmas 2.2, 2.3] + [own argument, unreviewed] | Attack ideas, A3 |
| If Conjecture 5.2 holds for all lengths ≤ ⌊k/2⌋, then for every WCS of length k and every d ∈ [2, k], σ^{-1}(d) is the first or the last element of T_d | [preprint: GSK24, Lemma 2.4] + [own argument, unreviewed] | Attack ideas, A4 |
| Window lemma: if m ∈ [2, k] divides σ(i) then k mod m < min(i, k + 1 − i); hence σ(1) ∣ k and σ(k) ∣ k | [own argument, unreviewed] (GSK24 input re-proved, A6.0, A8) | Attack ideas, A6.1 |
| gcd(σ(1), σ(k)) = 1 for every WCS; so if 1 < σ^{-1}(1) < k, σ(1) and σ(k) are coprime divisors of k, both ≥ 2 | [own argument, unreviewed] (GSK24 input re-proved, A6.0, A8) | Attack ideas, A6.2 |
| Conjecture 5.2 holds when k is a prime power (or k = 1) | [own argument, unreviewed] (GSK24 input re-proved, A6.0, A8) | Attack ideas, A6.3 |
| σ is a WCS iff σ(i) = λ(Y + i) for some integer Y (unique mod lcm(1..k)), λ(N) = lcm{m ∈ [k] : m ∣ N}; and iff (a) λ ≤ k on [Y + 1, Y + k] and (b) (Y mod m) + (k mod m) < m for all m ∈ [2, k] | [preprint: GSK24, Lemma 2.2] + [own argument, unreviewed] | Attack ideas, A6.4 |
| For m ∈ [2, k] dividing k + 1, T_m = {m, 2m, …}; hence gcd(σ^{-1}(1), k + 1) = 1 | [preprint: GSK24, Lemma 2.2] + [own argument, unreviewed] (via A6.4) | Attack ideas, A6.4 |
| gcd(σ(i), i − σ^{-1}(1)) = 1 for all i ≠ σ^{-1}(1) | [own argument, unreviewed] | Attack ideas, A6.4 |
| A6.1, A6.2 and the Y-form, k + 1 and unit-class parts of A6.4 hold on every WCS with k ≤ 20; enumerating Y mod lcm(1..k) gives exactly N(k) WCS for k ≤ 13 | [numerical, Python, not Lean] | Log 2026-11-25 (attack) |
| Class sizes + compatibility alone admit an interior 1 (e.g. k = 8, 12); adding disjointness of coprime prime-power classes with product > k excludes it for k ≤ 18, primes only do not (k = 6, 14) | [numerical, Python, not Lean] | Attack ideas, A6.5 |
| Slice lemma: if 1 < σ^{-1}(1) < k, d = σ(1), d′ = σ(k), then σ(k − d + 1) = d·e with e ∣ k/d, e ≥ 2 and gcd(e, d′) ∣ d − 1; mirror: σ(d′) = d′·e′ with e′ ∣ k/d′, e′ ≥ 2, gcd(e′, d) ∣ d′ − 1 | [own argument, unreviewed] (GSK24 input re-proved, A6.0, A7.1 (ii), A8) | Attack ideas, A7.1 |
| Conjecture 5.2 holds for k = r·s^b (r, s distinct primes, b ≥ 1) with s ∤ r − 1; in particular for every squarefree k = pq and every k = 2·s^b | [own argument, unreviewed] (GSK24 input re-proved, A6.0, A8) | Attack ideas, A7.2 |
| General form of the slice lemma (σ(1) = d ≥ 2, k/d ≥ 2 ⇒ d ∣ σ(k − d + 1), e ∣ k/d, e ≥ 2, gcd(σ(k − d + 1), σ(k)) ∣ d − 1, and the mirror) holds on every WCS with k ≤ 20 | [numerical, Python, not Lean] (`search/weakly-consecutive/wc_slice_check.py`) | Log 2026-11-26 |
| Conjecture 5.2 holds for k = 4r, r ≥ 5 prime (with k = 12 from Lean: for every k = 4r, r an odd prime) | [own argument, unreviewed] (k = 12 part: [Lean]) | Attack ideas, A7.4 |
| No WCS of length 4r with σ(1) ∈ {2, 4}, σ(4r) = r for r = 3, 5, 7 | [numerical, Python, not Lean] (`search/weakly-consecutive/wc_4r_check.py`) | Attack ideas, A7.4 |
| Conjecture 5.2 holds for k = s²·r (r, s distinct primes, s ∣ r − 1) when r ∤ s² − s + 1, and for k = 63 and k = 2107 (generalizes A7.4: s = 2) | [own argument, unreviewed] | Attack ideas, A7.5 |
| For primes s < 60, the pairs with s ∣ r − 1 and r ∣ s² − s + 1 are (2, 3), (3, 7), (7, 43), (13, 157); A7.5's k + 1 step closes 63 and 2107, not 12 or 26533 | [numerical, Python, not Lean] (`search/weakly-consecutive/wc_s2r_check.py`) | Attack ideas, A7.5 |
| Conjecture 5.2 for the remaining k with two distinct prime factors: p^a q^b with a, b ≥ 2, or r·s^b with s ∣ r − 1 and b ≥ 3, or b = 2 with r ∣ s² − s + 1 not closed by A7.5 (e.g. 2^b·r, b ≥ 3; 26533) | [conjecture] | Attack ideas, A7.3, A7.4, A7.5 |
| Conjecture 5.2 for k with at least three distinct prime factors | [conjecture] | Attack ideas, A6.5 |

## Literature (2026-11-25)

Read through a fetch subagent (ar5iv/arXiv HTML and the abs page of arXiv:2401.09497); the
statements below that the proof would use (Def. 2.1, Lemmas 2.2–2.4, Conjecture 5.3) were then
re-fetched directly from https://arxiv.org/html/2401.09497. The fetch tool limits verbatim quotes
to about 125 characters, so long statements are given as consecutive verbatim pieces, and the
Rule statements and §4 results are summaries, marked as such. All items are [preprint: GSK24].

1. **Definition 1.1** (§1): "We say σ is weakly consecutive if, for all i,j∈[k] and integers m,
   if m|σ(i) and m|(i−j), then m|σ(j)." The setting, as quoted by the scout: "Let σ:[k]→[k] be a
   permutation …".
2. **Definition 2.1** (§2): "Given a permutation σ over [k] and an m∈[k], define the sets of
   indices" "S_m^σ = {i∈[k] : i ≡ σ^{-1}(m) mod m} and T_m^σ = {i∈[k] : m | σ(i)}."
3. **Lemma 2.2** (§2): "Let σ be a permutation over [k]. Then, σ is weakly consecutive if and
   only if" "S_m^σ = T_m^σ for all m∈[k]." Proof idea (summary): S ⊆ T, |S| ≥ ⌊k/m⌋ = |T|.
4. **Lemma 2.3** (§2): "Let σ be a weakly consecutive sequence of length k. For any x∈[k],
   σ^{-1}(x) lies between" "(k mod m)+1 and k−(k mod m), inclusive."
   - *Hypothesis check.* m is not bound in the statement. The proof (summary: otherwise
     |S_m| = ⌊k/m⌋ + 1 > |T_m|) works for every x that is a multiple of m (then σ^{-1}(x) ∈ T_m),
     so we read it with **m ∣ x**; below it is used with x = m. This reading is ours
     [own argument, unreviewed]. Re-derived: write
     k = qm + s with 0 ≤ s < m; the class of a position r mod m meets [k] in q + 1 points if its
     least positive representative is ≤ s, and in q points otherwise. By Lemma 2.2 this class is
     T_m, of size q, so σ^{-1}(m) ≡ ρ (mod m) with ρ ∈ [s + 1, m]; in particular
     σ^{-1}(m) ∉ [1, s], and by the same count from the right end, σ^{-1}(m) ∉ [k − s + 1, k].
     The same holds for every point of T_m, hence for σ^{-1}(x) whenever m ∣ x (a one-line
     corollary: the count above is about the class, not the point).
     [own argument, unreviewed]
5. **Lemma 2.4** (§2): "Fix d∈[m]. Let ℓ be the least index such that d|σ(ℓ). Then the
   permutation" "D_d(σ): [⌊m/d⌋] → [⌊m/d⌋]" "defined by" "D_d(σ)(i) = σ(ℓ+(i−1)d)/d" "is weakly
   consecutive." Here m is again unbound; from context σ is a WCS of length k and we read
   **m = k**. This reading is ours [own argument, unreviewed], not stated in [GSK24].
6. **Starting sequences and rules** (§1.1, §3; summaries, not verbatim):
   - SS1: the identity, any k. SS2: k = p − 1, p prime; σ(k) = 1, σ(i) = i + 1 otherwise.
     SS3: k = 2p or 2p + 1 with p, p + 2 prime (a double swap). SS4: k = 2p − 1 with p, 2p + 1,
     p + 2 prime; σ(k) = 1, σ(k − 1) = 2, σ(p) = p, σ(p − 2) = p + 2, σ(i) = i + 2 otherwise.
   - Rule 1 (twin prime swap, q, q + 2 prime, ⌈k/2⌉ < q ≤ k; stated in §3 for sequences with q,
     q + 2 in their SS4 positions, so not for an arbitrary WCS; see the paper for the exact
     hypotheses). Rule 2 (prime power swap), with
     hypothesis quoted verbatim: "Let σ be a weakly consecutive sequence, and prime p and integer
     c≥1 such that p^c≤k<p^c+p^{c-1}." It swaps the values p^c and p^{c−1}; the printed formula
     has a typo (p^{x−1} for p^{c−1}). Rule 3: reversal.
   - Lemma 3.1: the three rules commute.
7. **Conjecture 5.1** (§5): "Any WCS can be derived from one of the four starting sequences by
   applying the three rules." "Moreover, for k≥12, the starting sequence and rule applications
   are unique up to reordering the rules." "We have verified this by computer calculation up to
   k=500."
8. **Conjecture 5.2** (§5): "Any WCS either begins or ends with the term 1 (in other
   words, σ(1)=1 or σ(k)=1). Surprisingly, we have not been able to prove this conjecture by
   working straight from the definition." Its derivation from 5.1: "If Conjecture 5.1 is true,
   it implies certain properties of WCS's" "by simply checking that they hold on the starting
   sequences and are preserved by the rules."
9. **Conjecture 5.3** (§5): "Let σ be a WCS. Then each m<k/2 appears as either one of the first
   m or last m terms of the sequence; in other words" "σ^{-1}(m) ∈ [1,m] ∪ [k−m+1,k]." The paper says 5.2 with
   Lemma 2.4 implies 5.3.
10. Other conjectures (§5): 5.4 (N(k) a power of 2 unless k = 2p − 1 with p, 2p + 1, p + 2
    prime), 5.5, 5.6. Table 1 lists all WCS of length ≤ 8; Table 2 gives N(k) for k ≤ 100.
    §4 (Theorem 1.2 = Cor. 4.2, Thm 4.1, Thm 4.8) is about the size of N(k) (large values infinitely often, Cor. 4.2;
    small values infinitely often, Thm 4.8), via the
    number of prime-power intervals I_{p,c} = [p^c, p^c + p^{c−1}) containing k, and does not
    bear on 5.2. The bibliography (7 items) is classical number theory only.

**What a proof of 5.2 can cite.** Lemma 2.2 (the residue-class characterization), Lemma 2.3 (read
with m ∣ x and used with x = m, re-derived above, so it can be proved inline instead of cited), Lemma 2.4 (slices, for an
induction on k) and Rule 3 (reversal). All three lemmas have short elementary proofs, so a proof
should re-prove them (and Lean should formalize them) rather than rely on the preprint. Nothing in
[GSK24] constrains the position of the value 1 directly.

### Search scope (2026-11-25)

- arXiv API: `all:"weakly consecutive"`, `ti:"weakly consecutive"`,
  `abs:"weakly consecutive" AND abs:permutation`: only 2401.09497. Author searches
  `au:Garrison_Thomas`, `au:Seiler_Chris`: besides 2401.09497, only 2403.12195 (PackIt!) and
  2609.01998 (Mondrian art problem, 2 Sep 2026), neither about WCS. `au:Knowles_A` with math:
  unrelated.
- OpenAlex (W4391046639): cited_by_count 0, not published. zbMATH Open "weakly consecutive": the
  paper only. Crossref: no journal version.
- Web search (paper title with authors; the conjecture's wording "begins or ends with the term 1",
  "σ(1)=1"): only the paper and mirrors.
- MathOverflow and Math.StackExchange (Stack Exchange API, "weakly consecutive"): 0 results.
- OEIS: A395372 (counts only, no conjecture discussion); the keyword search found nothing else.
- **Not accessed:** Semantic Scholar (HTTP 429), Google Scholar (bot wall).

**Verdict.** Conjectures 5.1 and 5.2 are open as far as these searches show: no proof,
counterexample or citing work was found in the sources above, other than OEIS A395372,
which links the paper and lists the counts but does not discuss Conjecture 5.2.

## Attack ideas

Write T_m = T_m^σ and pos(v) = σ^{-1}(v). For a WCS, T_m is the residue class of pos(m) mod m
inside [k], of size ⌊k/m⌋ (Lemma 2.2).

- **A1. Covering reformulation.** [own argument, unreviewed] For i ≠ pos(1), σ(i) ≥ 2 has a prime
  factor p ≤ k, and i ∈ T_p. pos(1) lies in no T_m (m ≥ 2). So pos(1) is the unique point of [k]
  missed by the prime classes T_p (p ≤ k prime), and Conjecture 5.2 says: for every WCS these
  classes cover {2, …, k − 1}. This is a covering-system (Jacobsthal-type) statement with the
  extra size constraints |T_p ∩ [k]| = ⌊k/p⌋ and the lcm constraints in A2.
- **A2. Compatibility.** [own argument, unreviewed] T_m ∩ T_n is the set of positions whose value
  is divisible by lcm(m, n): it is T_{lcm(m,n)} if lcm(m, n) ≤ k, and empty otherwise. So for
  coprime m, n with mn > k the two classes are disjoint inside [k]. This is not automatic: as
  residue classes mod m and mod n they meet (CRT) in one residue class mod mn, which can have a
  point in [k] since mn > k only bounds it to at most one; the WCS property (no value in [k] is
  divisible by lcm(m, n) > k) is what forces that class to miss [k].
  This is a constraint on the pair (pos(m) mod m, pos(n) mod n) worth exploiting for large coprime pairs (a suggestion, not a claim).
- **A3. Large primes and small moduli.** [own argument, unreviewed] Primality is not used in the
  first two bullets: they hold for every m in the stated ranges.
  - For m ∈ (k/2, k], T_m = {pos(m)} and pos(m) ∈ [k − m + 1, m] (Lemma 2.3, with k mod m = k − m).
  - For m ∈ (k/3, k/2], T_m = {ρ, ρ + m}, both in [k], where its least element ρ lies in
    (k − 2m, m], and pos(m) ∈ {ρ, ρ + m}. Proof: 2m ≤ k < 3m, so ⌊k/m⌋ = 2. By Lemma 2.2, T_m is
    the residue class of pos(m) mod m inside [k], of size 2; with least element ρ ∈ [1, m] its
    points in [k] are ρ, ρ + m, …, so size 2 means ρ + m ≤ k < ρ + 2m, i.e. ρ > k − 2m (and
    ρ + m ≤ k holds since ρ ≤ m ≤ k − m). pos(m) ∈ T_m by definition.
  - m = 2, k odd: T_2 is the class with least representative 2, i.e. the even positions, so every
    even value sits at an even position and pos(1) is odd. For k even both parities are possible
    a priori.
  - Plan: suppose 2 ≤ pos(1) ≤ k − 1. For each value v > k/2, T_v is a singleton: no other
    value shares v's class (first bullet), though pos(v) itself may still lie anywhere in
    [k − v + 1, v]. Already for v ∈ (k/3, k/2], |T_v| = 2 (second bullet), and its least element
    ρ ranges over (k − 2v, v]. The values with small prime factors fill whole residue
    classes. Count the positions in [2, k − 1] left uncovered by the small-prime classes and show
    the large primes cannot cover all but one of them unless the gap is at an end.
- **A4. Induction through slices.** [preprint: GSK24, Lemma 2.4] + [own argument, unreviewed]
  Strong induction on k. For d ∈ [2, k] the slice D_d(σ) is a WCS of length ⌊k/d⌋ < k, and its
  value 1 is the position of d within T_d. So the induction hypothesis gives: pos(d) is the first
  or the last element of T_d, for every d ≥ 2. (This is Conjecture 5.3's mechanism.) Only lengths
  ⌊k/d⌋ ≤ ⌊k/2⌋ are used, so the stronger form holds: if Conjecture 5.2 holds for all lengths
  ≤ ⌊k/2⌋ (length 1 is trivial), then for every WCS of length k, pos(d) is extreme in T_d for all d ∈ [2, k]. What remains
  for the inductive step is to locate the value 1 itself, using these rigid positions for all
  d ≥ 2 at once, e.g. for the primes d in A3.
- **A5. Lean.** The definition is decidable; check Conjecture 5.2 for small k by `decide` /
  `native_decide` (or a verified enumeration) and formalize Lemmas 2.2–2.4 as the reusable base.
  The Python counts below must be re-done in Lean before any page uses them.
- **A6. Attack (2026-11-25).** Result (own argument, unreviewed; /review of A6.1–A6.5 found no mathematical error, see Review; A6.0 was added on 2026-11-27, see Review of that date): Conjecture 5.2
  for k a prime power (A6.3), and in general an interior 1 forces σ(1), σ(k) to be coprime divisors of k, both ≥ 2. The full
  conjecture is **not** proved; the gap is in A6.5. Notation as above: T_m = {i ∈ [k] : m ∣ σ(i)},
  p = pos(1), s_m = k mod m. The direction "WCS ⇒ classes" of Lemma 2.2 of [GSK24] and Rule 3
  (reversal) are used throughout; both are re-proved in A6.0, so A6.1–A6.3 and A7 do not rest on
  the preprint (citation check #80, A8).
  - **A6.0. Class lemma and reversal.** [own argument, unreviewed] (Added 2026-11-27, #80.)
    Let σ be a WCS of length k ≥ 1 and m ∈ [k].
    - *(a) Class lemma.* T_m = {i ∈ [k] : i ≡ pos(m) (mod m)}, and |T_m| = ⌊k/m⌋. Consequently,
      for every i ∈ T_m, T_m is the class of i mod m inside [k]; any two points of T_m are
      congruent mod m. *Proof.* Write S_m = {i ∈ [k] : i ≡ pos(m) (mod m)} (pos(m) exists since
      m ∈ [k]). S_m ⊆ T_m: for j ∈ S_m, m ∣ σ(pos(m)) = m and m ∣ pos(m) − j, so m ∣ σ(j) by
      Def. 1.1. |T_m| = ⌊k/m⌋: σ is a bijection of [k], so T_m is in bijection (via σ) with the
      multiples of m in [k], of which there are ⌊k/m⌋. |S_m| ≥ ⌊k/m⌋: the ⌊k/m⌋ disjoint blocks
      [jm + 1, (j + 1)m] (0 ≤ j < ⌊k/m⌋) lie in [k], and each contains exactly one integer of each
      residue class mod m. So ⌊k/m⌋ ≤ |S_m| ≤ |T_m| = ⌊k/m⌋, and S_m = T_m. The consequence holds
      because a residue class is the class of each of its members. ∎ Edge cases: m = 1 gives
      T_1 = S_1 = [k]; m = k gives T_k = S_k = {pos(k)}; k = 1 has only m = 1. Only this direction
      of [GSK24] Lemma 2.2 is used (the converse is not needed in A6.1–A6.3, A7.1–A7.2).
    - *(b) Reversal.* R(σ)(i) = σ(k + 1 − i) is a WCS. *Proof.* R(σ) is a permutation of [k]. If
      m ∣ R(σ)(i) = σ(k + 1 − i) and m ∣ i − j, then m ∣ (k + 1 − j) − (k + 1 − i) = i − j,
      so m ∣ σ(k + 1 − j) = R(σ)(j) by Def. 1.1. ∎ R maps position i to k + 1 − i, keeps the
      multiset of values, swaps σ(1) and σ(k), and keeps "1 < pos(1) < k". (This is [GSK24] Rule 3,
      re-proved.)
  - **A6.1. Window lemma.** [own argument, unreviewed] Let σ be a WCS, i ∈ [k], m ∈ [2, k] with
    m ∣ σ(i). Then s_m < i and s_m < k + 1 − i. *Proof.* T_m is the class of i mod m inside [k]
    and has ⌊k/m⌋ = (k − s_m)/m points (A6.0 (a)). If i ≤ s_m, the class of i contains the ⌊k/m⌋ + 1
    points i + jm, j = 0, …, ⌊k/m⌋, all in [k] (the last is i + ⌊k/m⌋·m ≤ s_m + k − s_m = k), a
    contradiction. The other inequality follows by reversal (A6.0 (b)), which
    maps position i to k + 1 − i and keeps the values. ∎ (This is Lemma 2.3 of [GSK24] read with m ∣ x,
    i.e. for the whole class T_m (our reading, Literature item 4): every member of the class has the same residue mod m.
    The proof above does not use Lemma 2.3; it is a remark on the relation only.)
    - *Corollary (end values).* σ(1) ∣ k and σ(k) ∣ k: every divisor m ≥ 2 of σ(1) has
      s_m < 1, i.e. m ∣ k; take m = σ(1) (if σ(1) ≥ 2). Same for σ(k).
  - **A6.2. Coprime ends.** [own argument, unreviewed] For every WCS, gcd(σ(1), σ(k)) = 1.
    *Proof.* Let h = gcd(σ(1), σ(k)). If h ≥ 2 (then h ≤ σ(1) ≤ k, so h ∈ [2, k]), positions 1 and
    k both lie in T_h, a single residue class mod h (A6.0 (a)), so h ∣ k − 1; and h ∣ σ(1) ∣ k by A6.1. So h ∣ gcd(k, k − 1) = 1. ∎
    - *Corollary.* If 1 < p < k, then σ(1) and σ(k) are both ≥ 2 (the value 1 occurs once), so
      d = σ(1) and d′ = σ(k) are **coprime divisors of k, both ≥ 2**, and d·d′ ∣ k.
  - **A6.3. Prime powers.** [own argument, unreviewed] *If k = q^a is a prime power (q prime,
    a ≥ 1), or k = 1, every WCS of length k has σ(1) = 1 or σ(k) = 1.* *Proof.* k = 1 is trivial.
    Otherwise, if 1 < p < k, A6.2 gives coprime divisors d, d′ ≥ 2 of q^a; both are divisible by
    q, contradiction. If p ∈ {1, k} there is nothing to prove. ∎ This covers k = 2, 3, 4, 5, 7, 8,
    9, 11, 13, 16, 17, 19, 23, 25, 27, … . Not found in [GSK24] (which says it could not prove 5.2
    from the definition) nor in the works searched (Literature, search scope). Hypotheses used:
    the WCS property (through the class lemma A6.0 (a), in A6.1 and in A6.2's "positions 1 and k lie in T_h"),
    the uniqueness of the value 1, and that k is a prime power. A small, decidable Lean target
    for later: A6.1 and A6.2 from the definition, then A6.3.
  - **A6.4. Single-residue form and other necessary conditions.** [own argument, unreviewed]
    - *Reformulation.* Let L = lcm(1, …, k) and λ(N) = lcm{m ∈ [k] : m ∣ N}. A permutation σ of
      [k] is a WCS iff there is an integer Y with σ(i) = λ(Y + i) for all i ∈ [k]; Y is then
      unique mod L. *Proof.* (⇐) λ(N) ∣ N, and for m ∈ [k], m ∣ λ(N) ⇔ m ∣ N. So if m ∣ σ(i)
      and m ∣ i − j then m ≤ σ(i) ≤ k, m ∣ Y + i, hence m ∣ Y + j and m ∣ σ(j). (⇒) For each
      m ∈ [k], T_m is a nonempty residue class c_m mod m (Lemma 2.2), and m ∣ n ≤ k gives
      T_n ⊆ T_m, so c_n ≡ c_m (mod m). By the CRT pick X ≡ c_Q (mod Q) for each maximal prime
      power Q ≤ k. For m = ∏ q^{e_q} ∈ [k], m ∣ σ(i) iff q^{e_q} ∣ σ(i) for all q, so
      T_m = ⋂ T_{q^{e_q}} = {i : i ≡ X (mod m)}. Thus the divisors in [k] of σ(i) are exactly the
      m ∈ [k] dividing i − X; their lcm is σ(i). Put Y = −X. Uniqueness: T_m fixes Y mod m. ∎
    - *Window criterion.* With J = [Y + 1, Y + k], i ↦ λ(Y + i) is a permutation of [k] iff
      (a) λ(N) ≤ k for every N ∈ J, and (b) for every m ∈ [2, k], J contains exactly ⌊k/m⌋
      multiples of m, i.e. (Y mod m) + s_m < m. *Proof.* Under (a), #{i : m ∣ λ(Y + i)} is the
      number of multiples of m in J; (b) makes it ⌊k/m⌋ for all m, and downward induction on m
      gives that each v ∈ [k] is taken exactly once. The count of multiples of m in J is
      ⌊(Y + k)/m⌋ − ⌊Y/m⌋ = ⌊k/m⌋ + [(Y mod m) + s_m ≥ m]. ∎ In this form Conjecture 5.2 says:
      the unique element of J with no prime factor ≤ k is Y + 1 or Y + k.
    - *Divisors of k + 1.* If m ∈ [2, k] divides k + 1, then s_m = m − 1, so (b) forces
      Y ≡ 0 (mod m), i.e. T_m = {m, 2m, …}. Hence gcd(p, k + 1) = 1 (a prime q ∣ gcd(p, k + 1)
      would divide Y + p = the rough element). For k odd this is A3's "p is odd".
    - *Unit classes.* gcd(σ(i), i − p) = 1 for all i ≠ p (if m ∣ σ(i) and m ∣ i − p then
      m ∣ σ(p) = 1). So, relative to the position of 1, every T_m is a class of units mod m.
    - *Interior case, more.* If 1 < p < k with d = σ(1), d′ = σ(k) as in A6.2, then
      Y ≡ −1 (mod d) and Y ≡ 0 (mod d′), so p ≢ 1 (mod q) for every prime q ∣ d and q′ ∤ p for
      every prime q′ ∣ d′; and the slices D_d(σ) and D_{d′}(σ) (Lemma 2.4) are WCS of lengths k/d
      and k/d′ that start, resp. end, with 1, so they give no contradiction by themselves.
  - **A6.5. Gap.** [conjecture] Open as a proof: k with at least two distinct prime factors (k = 6, 10, 12,
    14, 15, 18, 20, …). These k are verified numerically for k ≤ 23 (Python, Log), and [GSK24]
    reports checking Conjecture 5.1, which implies 5.2, up to k = 500. What remains is to exclude a WCS with 1 < p < k, σ(1) = d, σ(k) = d′,
    where d, d′ ≥ 2 are coprime divisors of k with d·d′ ∣ k (and the congruences of A6.4 hold). Approaches
    tried and why they fail:
    - *Class sizes alone (the counting plan of A3).* The system "each T_m is a residue class mod
      m of size ⌊k/m⌋, compatible under divisibility, not containing p" does **not** force
      p ∈ {1, k}: by exhaustive search it has solutions with interior p for k = 4, 6, 7, 8, …, 20
      (e.g. k = 8, p ∈ {2, 4, 5, 7}; k = 12, every p ∈ [2, 11]). [numerical, Python, not Lean]
      So a proof must use more than this system, for example that the classes cover every position other than p (A6.3 uses this
      at positions 1 and k) or the disjointness T_m ∩ T_n = ∅ for lcm(m, n) > k (A2).
    - *Which disjointness is needed.* Adding to the size system the disjointness of T_Q, T_{Q′}
      for coprime prime powers Q, Q′ ≤ k with QQ′ > k excludes every interior p for k ≤ 18. (The full system, i.e. sizes + compatibility +
      T_m ∩ T_n = ∅ whenever lcm(m, n) > k, is equivalent to WCS [own argument, unreviewed]: if λ(N) > k for some N ∈ J, let
      M be the largest divisor of N in [k] and n ∈ [k] a divisor of N not dividing M; then
      lcm(M, n) > k, so disjointness gives (a) of A6.4. So it excludes interior p for k ≤ 20 by
      the enumeration, [own argument, unreviewed] + [numerical, Python, not Lean].) With primes only instead of prime powers, interior p survive at k = 6 and
      k = 14 (the search range of this run was not recorded; a reviewer re-ran it for k ≤ 14 and
      found exactly k = 6, 14; k = 19, 20 are not claimed for the prime-power pairs); with only pairs involving a power
      of 2, or only pairs of values > k/2, they survive for most k ≤ 20. [numerical, Python, not
      Lean] So the size system plus prime-only disjointness is not enough (k = 6, 14); with the
      prime-power pairs added it suffices for k ≤ 18.
    - *Ends only.* A6.1–A6.2 use only positions 1 and k. The analogous statements for
      positions 2 and k − 1 (divisors of σ(2) divide k or k − 1, by A6.1) did not give a
      contradiction in the interior case by hand; the next step would be to push A6.1 inward
      together with the induction hypothesis of A4 (pos(d) extreme in T_d), which was not
      completed.
    - *Update 2026-11-26.* Part of this gap is closed by A7.2 below (k = r·s^b with s ∤ r − 1,
      including every squarefree k = pq); what is left for two prime factors is A7.3.
- **A7. Two distinct prime factors (#68).** (2026-11-26.) Notation as in A6. New ingredient
  compared with A6.5: the slice D_d through position 1 (Lemma 2.4 of [GSK24], re-proved inline
  for this slice) is a WCS of length k/d that *starts* with 1, so A6.1 applied to the slice constrains
  the value at the last point of T_d; A6.2's gcd argument then compares that point with
  position k.
  - **A7.1. Slice lemma.** [own argument, unreviewed] (GSK24 Lemmas 2.2 and 2.4 re-proved: A6.0,
    (ii) below; see A8.) Let σ be a WCS of length k with
    1 < pos(1) < k, d = σ(1), d′ = σ(k) (coprime divisors of k, both ≥ 2, d·d′ ∣ k: A6.2), and
    K = k/d (so K ≥ d′ ≥ 2). Then σ(k − d + 1) = d·e with **e ∣ K, e ≥ 2 and gcd(e, d′) ∣ d − 1**.
    *Proof.* (i) T_d is the class of position 1 mod d inside [k] (A6.0 (a), as 1 ∈ T_d); since d ∣ k it is
    {1, 1 + d, …, 1 + (K − 1)d}, whose last point is k − d + 1, and these K positions carry exactly
    the K multiples of d in [k]. So τ(i) = σ(1 + (i − 1)d)/d is a permutation of [K].
    (ii) τ is a WCS: if m ∣ τ(i) and m ∣ i − j, then md ∣ σ(1 + (i − 1)d) and md divides the
    position difference (i − j)d, so md ∣ σ(1 + (j − 1)d) by Def. 1.1, i.e. m ∣ τ(j). (This is
    [GSK24] Lemma 2.4 for this slice.) (iii) τ(1) = σ(1)/d = 1 and K ≥ 2, so e := τ(K) ≥ 2, and
    A6.1's corollary applied to τ gives e ∣ K. (iv) g := gcd(de, d′) = gcd(e, d′) since
    gcd(d, d′) = 1. If g ≥ 2 (g ≤ d′ ≤ k, so g ∈ [2, k]), positions k − d + 1 and k both lie in T_g,
    one residue class mod g (A6.0 (a)), so g ∣ (k) − (k − d + 1) = d − 1. ∎ (Edge cases: K = 1, i.e.
    d = k, cannot occur, since d·d′ ∣ k with d′ ≥ 2; and k − d + 1 ≠ k since d ≥ 2.)
    - *Mirror.* Applying A7.1 to the reversal (A6.0 (b); it swaps σ(1) and σ(k) and maps position
      k − d′ + 1 to d′): σ(d′) = d′·e′ with e′ ∣ k/d′, e′ ≥ 2, gcd(e′, d) ∣ d′ − 1.
      [own argument, unreviewed]
    - The general form (no interior 1 assumed: σ(1) = d ≥ 2 and k/d ≥ 2; then (i)–(iii) hold
      verbatim and (iv) reads gcd(σ(k − d + 1), σ(k)) ∣ d − 1), with its mirror, holds on every
      WCS with k ≤ 20. [numerical, Python, not Lean] (`search/weakly-consecutive/wc_slice_check.py`; for the
      interior case itself numerics are vacuous, since no WCS with k ≤ 23 has an interior 1.)
  - **A7.2. Theorem.** [own argument, unreviewed] (no GSK24 lemma used beyond A6.0; see A8.) *Let k = r·s^b with r, s distinct primes,
    b ≥ 1 and s ∤ r − 1. Then every WCS of length k has σ(1) = 1 or σ(k) = 1.* *Proof.* Suppose
    1 < pos(1) < k. By A6.2, σ(1) and σ(k) are coprime divisors of k, both ≥ 2. Each value is ≥ 2
    and has only the primes r, s; by coprimality no prime divides both, so if one value were
    divisible by both r and s the other would be 1. Hence one value is a power of r dividing k,
    i.e. r itself, and the other is s^β with 1 ≤ β ≤ b. Reversal (A6.0 (b))
    keeps the WCS property and the interiority of pos(1) and swaps σ(1), σ(k), so we may assume
    σ(1) = r, σ(k) = s^β. Apply A7.1 with d = r, d′ = s^β, K = s^b: e ∣ s^b and e ≥ 2 give s ∣ e,
    so s ∣ gcd(e, s^β) ∣ r − 1, contradicting s ∤ r − 1. ∎
    - *Squarefree k = pq* (p < q primes): take r = p, s = q; then 1 ≤ p − 1 < q, so q ∤ p − 1.
      (With r = q the hypothesis can fail, e.g. 2 ∣ 3 − 1 for k = 6, which is why the
      orientation matters.) Together with A6.3: Conjecture 5.2 holds for every prime power k and
      every squarefree k = pq. [own argument, unreviewed]
    - *Covered k ≤ 100 with two distinct prime factors* (`search/weakly-consecutive/wc_slice_check.py`): 6, 10, 14, 15,
      18, 21, 22, 26, 33, 34, 35, 38, 39, 45, 46, 50, 51, 54, 55, 57, 58, 62, 65, 69, 74, 75, 77,
      82, 85, 86, 87, 91, 93, 94, 95, 98, 99. This includes every k = 2·s^b (r = 2, s odd) and
      every pq. [own argument, unreviewed] (A7.2) + list computed by `search/weakly-consecutive/wc_slice_check.py`
      [numerical, Python, not Lean]
    - Hypotheses used: Def. 1.1 (in A7.1 (ii)), the class lemma A6.0 (a), A6.1,
      A6.2, reversal (A6.0 (b)), uniqueness of the value 1, the factorization of k. The steps are small and
      decidable-flavoured; a Lean version needs the class lemma A6.0 (a), A6.1, A6.2 and the slice WCS fact.
  - **A7.3. Remaining gap (two prime factors).** [conjecture] Not proved: k = p^a q^b not of the
    form in A7.2, i.e. (a) a, b ≥ 2 (36, 72, 100, …), or (b) k = r·s^b with b ≥ 2 and
    s ∣ r − 1 (squarefree k is always covered). Family (b) contains every 2^b·r with b ≥ 2 and r
    an odd prime (12, 20, 24, 28, 40, …) and e.g. 63 = 7·3². The uncovered k ≤ 100 are 12, 20,
    24, 28, 36, 40, 44, 48, 52, 56, 63, 68, 72, 76, 80, 88, 92, 96, 100 (superseded for k = 4r by A7.4: see the Update below). Up to reversal and naming, an interior 1 then has σ(1) = p^α,
    σ(k) = q^β (1 ≤ α ≤ a, 1 ≤ β ≤ b), and A7.1 with its mirror gives only:
    e ∣ p^{a−α}q^b, gcd(e, q^β) ∣ p^α − 1; e′ ∣ p^a q^{b−β}, gcd(e′, p^α) ∣ q^β − 1. In
    particular α = a forces q ∣ p^a − 1 and β = b forces p ∣ q^b − 1. [own argument, unreviewed]
    These do not close the case: for k = 12 with (σ(1), σ(12)) = (4, 3), e = 3 and e′ = 2
    satisfy them (3 ∣ 3, 2 ∣ 4, gcd(3, 3) ∣ 3, gcd(2, 4) ∣ 2). [own argument, unreviewed]
    - *What closes small cases by hand.* For k = 12 with (σ(1), σ(12)) = (2, 3): A7.1 forces e = 2
      (e ∣ 6, 3 ∤ e), so σ(11) = 4, T_4 = {3, 7, 11}; then T_12 = {3}, T_8 = {7} (window [5, 8]),
      T_6 = {3, 9}, so σ(9) = 6 (T_12 = {3}); pos(9) = 6 (window [4, 9] in T_3 = {3, 6, 9, 12}
      leaves {6, 9}, and position 9 is odd, so in T_2 with σ(9) even, indeed σ(9) = 6), pos(10) = 5
      (T_2 is the odd positions; 5 is the only free odd position in the window [3, 10], since 3,
      7, 9 are taken), and the singleton T_7 must lie in the window [6, 7], both of whose
      positions are taken: contradiction. [own argument, unreviewed] So this argument closes the
      sub-case through a large prime (7 ∈ (k/2, k], A3). The step that would close A7.3: a
      general way to combine A7.1 with the singleton classes of primes in (k/2, k] (A3), or a
      second slice (e.g. D_e on positions of T_{de}) that again
      starts or ends with a known value; not found.
    - *Update 2026-11-27.* The sub-family k = 4r (r an odd prime) is closed: A7.4 (r ≥ 5, own
      argument, unreviewed) and the Lean check (r = 3). Still open in A7.3: (a) and (b) with
      k ≠ 4r. The uncovered k ≤ 100 are now (a) 36, 72, 100 and (b) 24, 40, 48, 56, 63, 80, 88, 96.
    - *Update 2026-11-27 (later).* A7.5 closes k = s²·r (s ∣ r − 1) except when r ∣ s² − s + 1,
      and also k = 63 and 2107 among those exceptions (own argument, unreviewed). Still open in
      (b): b ≥ 3, and b = 2 exceptions such as 26533 = 13²·157. The uncovered k ≤ 100 are now
      (a) 36, 72, 100 and (b) 24, 40, 48, 56, 80, 88, 96 (all 2^b·r with b ≥ 3).
  - **A7.4. k = 4r (2026-11-27, #68).** [own argument, unreviewed] *Let r ≥ 5 be a prime and
    k = 4r. Then every WCS of length k has σ(1) = 1 or σ(k) = 1.* With k = 12 (r = 3) from the
    Lean check k ≤ 16 ([Lean], `conjecture_5_2_le_16`), Conjecture 5.2 holds for every k = 4r, r an
    odd prime (20, 28, 44, 52, 68, 76, 92, … are newly covered by a proof in these notes; they were already
    verified numerically, k ≤ 23 here and k ≤ 500 in [GSK24] (authors' claim); 4r is family (b) of
    A7.3 with s = 2, b = 2). No GSK24 lemma is used beyond those re-proved in A6.0, A7.1 (ii) and
    step 3 (Lemma 2.4, for the slices).
    *Proof.* Suppose 1 < pos(1) < k.
    1. (End values.) By A6.2, d = σ(1) and d′ = σ(k) are coprime divisors of 4r, both ≥ 2. The
       divisors ≥ 2 of 4r are 2, 4, r, 2r, 4r; a coprime pair of them is {2, r} or {4, r} (2r and
       4r share a factor with every other one). Reversal (A6.0 (b)) keeps the WCS property and
       the interiority of pos(1) and swaps σ(1), σ(k), so we may assume d = 2^α (α ∈ {1, 2}), d′ = r.
    2. (α = 1 and σ(k − 1) = 4.) A7.1 applies (1 < pos(1) < k, d, d′ as there; K = k/d = 4r/2^α):
       σ(k − d + 1) = d·e with e ∣ K, e ≥ 2, gcd(e, r) ∣ d − 1. If α = 2: K = r, so e = r and
       r = gcd(r, r) ∣ 3, i.e. r = 3, excluded. So α = 1, K = 2r, e ∈ {2, r, 2r}, and gcd(e, r) ∣ 1
       rules out r, 2r: e = 2, i.e. σ(4r − 1) = 4.
    3. (σ(3) = 4r.) 4 ≤ k and 4 ∣ σ(4r − 1), so by A6.0 (a) T_4 is the residue class of 4r − 1
       mod 4 inside [k], of size ⌊k/4⌋ = r: T_4 = {3, 7, …, 4r − 1} (exactly r points, so the
       class lemma's count is consistent), and these r positions carry exactly the r multiples
       4, 8, …, 4r of 4 in [k]. So υ(i) = σ(4i − 1)/4 is a permutation of [r]. It is a WCS (as in
       A7.1 (ii)): if m ∣ υ(i) and m ∣ i − j, then 4m ∣ σ(4i − 1) and 4m ∣ (4i − 1) − (4j − 1), so
       4m ∣ σ(4j − 1) by Def. 1.1, i.e. m ∣ υ(j). Now υ(r) = σ(4r − 1)/4 = 1, and r ≥ 2, so
       υ(1) ≠ 1; A6.1's corollary (σ(1) ∣ k for every WCS) applied to υ gives υ(1) ∣ r, so
       υ(1) = r, i.e. σ(3) = 4r.
    4. (Contradiction.) r ≤ k and r ∣ σ(k), so by A6.0 (a) T_r is the residue class of k = 4r
       mod r inside [k], i.e. {r, 2r, 3r, 4r}. But r ∣ σ(3) = 4r, so 3 ∈ T_r and r ∣ 3: r = 3,
       excluded. ∎
    - *Edge cases audited.* Step 2 uses A7.1 only in its stated (interior) form. Step 3 needs
      4 ∈ [2, k] and r ≥ 2 (υ has length r ≥ 5, so its first and last positions differ). Step 4
      needs 3 ∉ {r, 2r, 3r, 4r}, true for r ≥ 5 (fails exactly for r = 3: for k = 12 with
      (σ(1), σ(12)) = (2, 3), steps 2–3 give σ(11) = 4, σ(3) = 12, which is consistent; A7.3
      closes that sub-case by a different hand argument, and (4, 3) is not excluded by step 2
      since r = 3 ∣ 3). The mirror of A7.1 is not used. Hypotheses used: Def. 1.1, A6.0 (a), (b),
      A6.1 (corollary), A6.2, A7.1, uniqueness of the value 1, primality of r.
    - *Numerics.* [numerical, Python, not Lean] `search/weakly-consecutive/wc_4r_check.py`
      (backtracking with σ(1) = 2^α, α = 1, 2, and σ(k) = r fixed) finds no WCS for k = 12, 20,
      28; r = 11 (k = 44) did not finish in 5 minutes. (k = 12, 20 were already covered by the
      exhaustive k ≤ 23 enumeration.) These are consistent with A7.4 but not part of the proof.
    - *Failed extension to k = 2^b·r, b ≥ 3.* [own argument, unreviewed] The same chain gives
      σ(1) = 2^α, σ(k) = r (up to reversal), and A7.1: σ(k − 2^α + 1) = 2^α·e, e ∣ 2^{b−α}r,
      gcd(e, r) ∣ 2^α − 1. If r ∤ 2^α − 1 then e = 2^c (1 ≤ c ≤ b − α); the slice of
      T_{2^{α+c}} (class of k − 2^α + 1, length L = 2^{b−α−c}r, ending with 1) gives
      σ(j) = 2^{α+c}f with j = 2^α(2^c − 1) + 1, f ∣ L, f ≥ 2. The step-4 contradiction needs
      r ∣ f, but f may be a power of 2 when b − α − c ≥ 1 (for b = 2, α = c = 1 this is
      L = r, which forced f = r). Iterating the slice (now one starting with 1 at position j)
      did not close it in this stage. Also open: r ∣ 2^α − 1 (e.g. r = 3, 7) and A7.3 (a).
  - **A7.5. k = s²·r (2026-11-27, #68).** [own argument, unreviewed] *Let r, s be distinct
    primes with s ∣ r − 1 and k = s²·r. (i) If r ∤ s² − s + 1, every WCS of length k has
    σ(1) = 1 or σ(k) = 1. (ii) The same holds for k = 63 (s = 3, r = 7) and k = 2107 (s = 7,
    r = 43), where r ∣ s² − s + 1.* For s = 2 this is A7.4 (s² − s + 1 = 3, so (i) is k = 4r,
    r ≥ 5). If s ∤ r − 1, k = s²·r is already covered by A7.2. Newly covered k ≤ 100: only 63;
    the next new ones are 117, 171, 275, 279, 333, … (list from `search/weakly-consecutive/wc_s2r_check.py`,
    [numerical, Python, not Lean]). No GSK24 lemma is used beyond those re-proved in A6.0 and
    A7.1 (ii).
    *Proof.* Suppose 1 < pos(1) < k. Note r > s (r ≡ 1 mod s, r ≠ 1).
    1. (End values.) By A6.2, d = σ(1), d′ = σ(k) are coprime divisors of s²r, both ≥ 2. One of
       them is not divisible by s; being ≥ 2 and coprime to the other, it is r, and then the
       other is s or s² (s²r, sr, r share a factor with r). By reversal (A6.0 (b)) we may assume
       d = s^α (α ∈ {1, 2}), d′ = r.
    2. (α = 1, σ(k − s + 1) = s².) By A7.1, σ(k − d + 1) = d·e with e ∣ K = s^{2−α}r, e ≥ 2,
       gcd(e, r) ∣ s^α − 1. If α = 2: K = r, e = r, so r ∣ s² − 1 = (s − 1)(s + 1); r ∤ s − 1
       (0 < s − 1 < r), so r ∣ s + 1, and r > s gives r = s + 1, i.e. (s, r) = (2, 3), which
       satisfies r ∣ s² − s + 1 = 3 and is not k = 63 or 2107; so α = 2 is excluded in (i) and
       (ii). So α = 1, K = sr, e ∈ {s, r, sr}, and gcd(e, r) ∣ s − 1 < r rules out r, sr:
       e = s, σ(k − s + 1) = s².
    3. (Slice of T_{s²}, for (i).) s² ≤ k and s² ∣ σ(k − s + 1), so by A6.0 (a) T_{s²} is the
       class of k − s + 1 ≡ 1 − s (mod s²) inside [k] (as s² ∣ k): {s²i − s + 1 : 1 ≤ i ≤ r},
       r points carrying the r multiples of s² in [k]. So υ(i) = σ(s²i − s + 1)/s² is a
       permutation of [r], and a WCS by the argument of A7.1 (ii) (if m ∣ υ(i), m ∣ i − j, then
       s²m divides σ(s²i − s + 1) and the position difference s²(i − j), so s²m ∣ σ(s²j − s + 1)).
       υ(r) = 1 and r ≥ 2, so υ(1) ≠ 1, and A6.1's corollary gives υ(1) ∣ r: υ(1) = r, i.e.
       σ(s² − s + 1) = k.
    4. (Contradiction for (i).) r ∣ σ(k), so T_r is the class of k ≡ 0 (mod r) in [k],
       {r, 2r, …, s²r}. As r ∣ σ(s² − s + 1) = k, r ∣ s² − s + 1, against the hypothesis of (i).
    5. (Divisors of k + 1, for (ii).) Let m ∈ [2, k] divide k + 1. [1, k + 1] contains exactly
       (k + 1)/m points of each class mod m, and k + 1 ≡ 0, so the class 0 has (k + 1)/m − 1 =
       ⌊k/m⌋ points in [k] and every other class has (k + 1)/m. By A6.0 (a) T_m is a class of
       size ⌊k/m⌋, so T_m = {m, 2m, …}. (This is the k + 1 part of A6.4, re-proved from A6.0 (a)
       only.) Since s ∣ k, gcd(m, s) = 1. If some j ∈ [k] lies in T_m ∩ T_{s²}, then σ(j) is
       divisible by m·s² (coprime factors), which is impossible when m·s² > k. By step 2 and A6.0 (a) (s² ∈ [k], s² ∣ k), as in step 3,
       T_{s²} = {j ∈ [k] : j ≡ 1 − s (mod s²)}. For k = 63: m = 8 ∣ 64, 8·9 = 72 > 63, and
       j = 16 = 2·8 satisfies 16 ≡ −2 (mod 9). For k = 2107: m = 68 ∣ 2108 = 68·31,
       68·49 = 3332 > 2107, and j = 680 = 10·68 satisfies 680 + 6 = 686 = 14·49. Contradiction. ∎
    - *Edge cases audited.* Step 1 uses s prime (divisors of s²r). Step 3 needs the class to
      start at s² − s + 1 ≥ 1 (true) and r ≥ 2 so υ's ends differ. Step 4 needs r ∤ s² − s + 1,
      which is exactly where (i) stops; for s = 2 it is r ≠ 3, matching A7.4. Step 5 uses step 2 and
      the first sentence of step 3 (the class of T_{s²}), not step 3's slice or step 4. The mirror of A7.1 is not used. Hypotheses used: Def. 1.1, A6.0 (a), (b), A6.1
      (corollary), A6.2, A7.1, uniqueness of the value 1, primality of r and s, s ∣ r − 1.
    - *Remaining exceptions.* [numerical, Python, not Lean] For primes s < 60 the pairs with
      s ∣ r − 1 and r ∣ s² − s + 1 are (s, r) = (2, 3), (3, 7), (7, 43), (13, 157); step 5 (some
      m ∣ k + 1 with m·s² > k and a multiple of m in [k] that is ≡ 1 − s mod s²) applies to
      k = 63 and 2107 but not to k = 12 (Lean covers it) nor k = 26533 = 13²·157, which stays
      open (`search/weakly-consecutive/wc_s2r_check.py`).
    - *Not attempted.* b ≥ 3 (k = s^b·r, the failed extension of A7.4 applies verbatim) and A7.3 (a).
- **A8. Citation check (#80) (2026-11-27).** Finishing item 2 for A6.1–A6.3 and A7.1–A7.2. Each
  [GSK24] ingredient these steps used is now re-proved in the notes, so none is cited; the only
  thing taken from the paper is Definition 1.1 itself (the statement of the problem, quoted
  verbatim in Literature item 1). No fetch of arXiv:2401.09497 was needed. All re-proofs are
  [own argument, unreviewed].
  - *A6.1 (window lemma).* Uses: T_m is the class of i mod m with ⌊k/m⌋ points ([GSK24] Lemma 2.2,
    direction WCS ⇒ classes): re-proved in A6.0 (a). Reversal ([GSK24] Rule 3): re-proved in
    A6.0 (b). Lemma 2.3: not used (A6.1 is its own derivation; the relation to Lemma 2.3 read with
    m ∣ x is a remark). Corollary σ(1), σ(k) ∣ k: from A6.1 only.
  - *A6.2 (coprime ends).* Uses: positions 1 and k in T_h are congruent mod h (Lemma 2.2):
    A6.0 (a), with h ∈ [2, k] checked; σ(1) ∣ k: A6.1. Nothing cited.
  - *A6.3 (prime powers).* Uses A6.2 and uniqueness of the value 1 only. Nothing cited.
  - *A7.1 (slice lemma).* (i) T_d is the class of 1 mod d (Lemma 2.2): A6.0 (a). (ii) the slice τ is
    a WCS ([GSK24] Lemma 2.4 for the slice through position 1): re-proved in (ii) from Def. 1.1,
    so the reading m = k of Lemma 2.4 (Literature item 5) is not needed. (iii) e ∣ K: A6.1's
    corollary applied to τ. (iv) congruence of positions k − d + 1 and k mod g (Lemma 2.2):
    A6.0 (a). Mirror: reversal, A6.0 (b). Lemma 2.3: not used (the old label listed it because
    A6.1 is its relative). Nothing cited.
  - *A7.2 (k = r·s^b, s ∤ r − 1).* Uses A6.2, reversal (A6.0 (b)), A7.1 and the factorization of k.
    Lemma 2.2 enters only through A6.0; Lemma 2.3 is not used. Nothing cited.
  - *Checked edge cases.* k = 1 (no m ∈ [2, k]; A6.3 trivial); m = k in A6.0 (T_k a singleton);
    m = 1 (T_1 = [k]); in A7.1, d = k (K = 1) is excluded by d·d′ ∣ k, d′ ≥ 2, so K ≥ 2 and
    τ(K) ≠ τ(1) = 1; the gcds h, g in A6.2 and A7.1 (iv) are ≤ k, so A6.0 applies to them. Author's
    re-check, not a /review: no error found in A6.1–A6.3, A7.1–A7.2.
  - *Not covered by this check.* The other rows of the Claims ledger that cite [GSK24] (A3, A4,
    A6.4, and the paper's own claims in Literature) keep their labels.

## Review

### 2026-11-25: literature stage, `/review` (two independent subagents)

Mathematics reviewer (brute-forced every claim for k ≤ 23 and checked them by hand): no blocking
problems. Two wording findings, both fixed:
- M1. A3: "T_p = {pos(p), pos(p) ± p}" read as three elements. Fixed: T_p = {ρ, ρ + p} with
  ρ ∈ (k − 2p, p] and pos(p) ∈ {ρ, ρ + p}.
- M2. A2: "as residue classes mod mn they meet" was imprecise. Fixed: the classes mod m and mod n
  meet in a residue class mod mn, which has no point in [k].

Claims and citation reviewer (checked the quotes against the arXiv HTML, plus Table 2 and OEIS
A395372): seven wording findings, all fixed:
- C1. The verdict and LEDGER said no citing work was found, but OEIS A395372 links the paper.
  Fixed in both places.
- C2. The quote of Conjecture 5.3 dropped "in other words". Restored.
- C3. "p. 12" for Conjecture 5.2 was not checked against the PDF. Dropped.
- C4. The §4 summary said only "how large N(k) can be", but Thm 4.8 is about small values. Fixed.
- C5. The claims-ledger row for large primes lacked p ≤ k. Fixed to p ∈ (k/2, k].
- C6. "[idea]" is not a claim label. Replaced with "(a suggestion, not a claim)".
- C7. The Rule 1 summary omitted its SS4 setting. Added a caveat pointing to the paper.

The search was not re-run by the reviewer; the openness verdict stays limited to the stated
scope.

### 2026-11-25: attack stage (A6), `/review` (two independent subagents)

Mathematics reviewer (re-derived A6.1–A6.4 and re-ran a brute force for k ≤ 14 that matched every
number it covers): no mathematical error. Five wording findings, all fixed:
- M1. Preamble: the Lemma 2.2 sketch also needs that every residue class mod m has ≥ ⌊k/m⌋ points
  in [k]. Added.
- M2. A6.1: it is Lemma 2.3 extended from pos(m) to the whole class T_m, not Lemma 2.3 itself.
  Reworded.
- M3. A6.5: "full system" was undefined and its equivalence to WCS unproved. Defined, and the
  one-line proof via the A6.4 window criterion added.
- M4. A6.5: the search ranges of the relaxations were not stated. Stated what is known; the range of
  the primes-only run was not recorded, so the note says so instead of guessing.
- M5. A6.5: the gap omitted the numerical status. Added (k ≤ 23 here; [GSK24] reports k ≤ 500),
  and d·d′ ∣ k.

Claims reviewer: one blocking finding and three wording findings, all fixed:
- C1 (blocks). LEDGER row WC1a said prime-power k "done". Now "own argument, unreviewed".
- C2. "Any proof must use …" and "a proof … needs the prime-power pairs" over-read the numerics on
  one relaxation. Weakened to statements about that relaxation.
- C3. The ledger row said the window criterion was enumerated separately. It was not; row now
  records only the Y-enumeration.
- C4. The k + 1 row rests on Lemma 2.2 too; label now includes it. A6.1 row now also cites
  Lemma 2.3, and reversal is justified from the definition.

### 2026-11-25: issue #52 (review points left open when PR #49 merged), `/review` (two independent subagents)

The seven points from the last reviewer-loop comment on PR #49, all fixed:
1. FIX. A3's second bullet had no ledger label. Now proved inline (⌊k/m⌋ = 2 and Lemma 2.2) and
   given its own ledger row, [own argument, unreviewed].
2. The m = k reading of Lemma 2.4 (and the reading of Lemma 2.3) is ours. Labelled
   [own argument, unreviewed] in the ledger and in Literature items 4 and 5.
3. "The intended reading is x = m" was too strong. Now: the argument works for every x with
   m ∣ x; used with x = m.
4. A3 never uses primality. Both bullets and the ledger row now state every m in the range.
5. "Pinned to a single position" holds only for values > k/2. A3's plan now says so.
6. A2's CRT sentence. Now says the CRT class mod mn can have one point in [k] and the WCS property
   is what empties it.
7. A4. The stronger induction form (lengths ≤ ⌊k/2⌋) is stated, in the prose and the ledger.

`/review` of these changes. Mathematics reviewer (brute force over all permutations, k ≤ 9; it used
the divisibility-class form, not Def. 1.1 verbatim): no problems; one nit (length 1 trivial).
Claims reviewer: three wording findings, all fixed:
- C1. A6.1 still said "Lemma 2.3 extended to the whole class", which now contradicts the m ∣ x
  reading. Reworded. (The historical M2 entry above is left as it was.)
- C2. The m ∣ x extension was only one sentence. It now says it is a corollary of the class count.
- C3 (with the mathematics nit). A4: added "length 1 is trivial".

### 2026-11-26: reviewer-loop comment on PR #63 (3 minor findings, all fixed)

- R1. A3 Plan said each v > k/2 "is pinned to a single position" and values in (k/3, k/2] "have
  two candidate positions". That overstates the bullets. Fixed: T_v is a singleton (pos(v) still
  free in [k − v + 1, v]); |T_v| = 2 with ρ ranging over (k − 2v, v].
- R2. Claims-ledger row for m ∈ (k/2, k] cited only Lemma 2.3; T_m = {σ^{-1}(m)} uses Lemma 2.2.
  Fixed: label now cites Lemmas 2.2, 2.3.
- R3. Claims-ledger row for Lemma 2.3 stated the window only for σ^{-1}(m). Fixed: now stated for
  every x with m ∣ x, as in Literature item 4 and A6.1.

### 2026-11-26: attack stage A7 (#68), `/review` (two independent subagents)

Nine wording and label findings, no mathematical error; all fixed:
1. Claims-ledger row for the remaining k lacked b ≥ 2 in "r·s^b with s ∣ r − 1". Fixed: b ≥ 2
   added, as in A7.3.
2. A7.3: "the sub-case closes only through a large prime" claimed no other route exists. Fixed:
   now "this argument closes the sub-case through a large prime".
3. A7.3 k = 12 hand check: the window for 9 left {6, 9} without excluding 9, and "last odd
   position" for 10 was wrong. Fixed: σ(9) = 6 (T_6 = {3, 9}, T_12 = {3}) and 9 is odd, so
   pos(9) = 6; position 5 is the only free odd position in [3, 10].
4. A7 intro: "pins the value" overstated A6.1. Fixed: "constrains the value".
5. LEDGER WC1a listed prime-power k (A6.3) as progress on two prime factors. Fixed: moved to its
   own row WC1c.
6. A7.1 and A7.2 (headers and claims-ledger rows) cited only the own argument. Fixed: labelled
   [preprint: GSK24, Lemmas 2.2, 2.3] + [own argument, unreviewed]; A7.1 also cites Lemma 2.4,
   re-proved inline.
7. A7.2 "Covered k ≤ 100" list was labelled own argument only. Fixed: own argument (A7.2) + list
   computed by `search/weakly-consecutive/wc_slice_check.py` [numerical, Python, not Lean].
8. LEDGER "Approaches that failed" said the slice constraints are satisfiable "in the uncovered
   cases" and k = 12 closes "only via" 7. Fixed: "in at least one uncovered case (k = 12,
   (4, 3))", and the hand check closes it "using" the singleton class of 7; "only" dropped (also
   in A7.3, see 2).
9. A6.5: the "full system is equivalent to WCS" parenthesis had no label. Fixed: the equivalence
   is [own argument, unreviewed], and the k ≤ 20 consequence that argument + [numerical, Python,
   not Lean].

### 2026-11-27: citation check (#80), `/review` (two independent subagents)

Mathematics reviewer (A6.0–A6.3, A7.1–A7.2, A8 against Def. 1.1; re-derived the covered k ≤ 100
list): no mathematical error, no silent use of a GSK24 result, A7.2's case split exhaustive.
Claims reviewer: every dropped GSK24 label rests on a re-proof in the notes; cross-references
resolve. Wording findings, all fixed:
1. A6.1 "blocks [i + jm]" are points, not blocks. Fixed.
2. A7.2 "Coprimality puts r and s in different ones" was compressed. Spelled out.
3. A7.2 hypotheses line "a Lean version needs Lemma 2.2" read as a citation. Now "the class lemma A6.0 (a)".
4. A6 header's "/review found no mathematical error" read as covering A6.0, added later. Scoped to A6.1–A6.5.
5. A8, A7.2 bullet contradicted A8's own statement that Lemma 2.3 is unused. Fixed.
6. A8 "No error found" read like a review finding. Now marked as the author's re-check.

### 2026-11-27: attack stage A7.4 (#68, k = 4r), `/review` (two independent subagents)

Mathematics reviewer: no mathematical error; every step, hypothesis (interior 1, d·d′ ∣ k, K ≥ 2,
coprimality), the slice construction and the edge cases (r = 2, 3, position collisions) checked;
`wc_4r_check.py` re-run. Claims reviewer: labels, the Lean coverage of k = 12
(`conjecture_5_2_le_16`), the script's scope and the uncovered-k lists all recomputed and correct.
Wording findings, all fixed:
1. A7.4 header said no GSK24 lemma is used beyond A6.0, but Lemma 2.4 (slices) is used, re-proved
   in A7.1 (ii) and step 3. Fixed: the sentence now names them. The A7.2 header ("see A8") is left
   as is: A8 records the A7.1 (ii) re-proof.
2. "20, 28, 44, … are new" read as a novelty claim; these k were already verified numerically
   (k ≤ 23 here, k ≤ 500 in [GSK24]). Fixed: "newly covered by a proof in these notes", with that
   caveat.
3. The e.g. lists after "(b) for k ≠ 4r" (notes A7.3 Update and LEDGER.md) included 36, 72, 100,
   which are family (a). Fixed: split into (a) and (b).
4. The original A7.3 list of uncovered k ≤ 100 still contained the 4r values. Fixed: marked as
   superseded for k = 4r by A7.4.

### 2026-11-27: attack stage A7.5 (#68, k = s²·r), `/review` (two independent subagents)

No mathematical error found; two wording points, both fixed:
1. Step 5 attributed T_{s²} = {j ≡ 1 − s (mod s²)} to step 2 alone, and the edge-case note said step 5
   does not use steps 3–4. Fixed: it comes from step 2 with A6.0 (a), as in step 3's first sentence;
   the note now says so.
2. `wc_s2r_check.py` defaulted to s < 200 (slow; did not finish in 120 s) while the claims cite s < 60.
   Fixed: the default bound is now 60, matching the stated output.

## Log

- **2026-11-25.** Literature stage. Re-checked openness (search scope above): nothing found after
  the scout or beyond it; P1 marked `taken` in `PROBLEMS.md`. Extracted Def. 1.1, Def. 2.1,
  Lemmas 2.2–2.4, Conjectures 5.1–5.3 from [GSK24]; noted the unbound m in Lemmas 2.3 and 2.4
  and the intended readings. Brute-force sanity check (throwaway Python backtracking script over
  m ∈ [2, k], not committed): N(k) for k = 1..23 is 1, 2, 2, 4, 4, 4, 4, 4, 8, 16, 16, 4, 4, 2,
  2, 8, 8, 8, 8, 4, 12, 16, 16, matching [GSK24] Table 2 (as reported) and OEIS A395372 where
  they overlap; no WCS with k ≤ 23 violates Conjecture 5.2. A second, independent script by a
  search subagent gave the same counts for k ≤ 22. [numerical, exact enumeration; not Lean]
- **2026-11-25.** `/review` done (9 wording findings, all fixed; see Review). PR #49 opened.
- **2026-11-25.** Lean (issue #47). `halfline_lt/Proofs/WeaklyConsecutive.lean` states
  Def. 1.1 on `Equiv.Perm (Fin k)` with the 1-indexing shifts written out and m ranging over ℤ
  (`IsWeaklyConsecutive`), and proves `conjecture_5_2_le_16`: Conjecture 5.2 for 1 ≤ k ≤ 16.
  [Lean] Method: a backtracking enumerator over partial sequences that prunes with the pair test
  gcd(d, σ(i)) = gcd(d, σ(j)) for positions at distance d (implied by Def. 1.1: take
  m = either gcd); completeness (every WCS survives) is proved, and the kernel evaluates the
  enumerator by `decide +kernel`. Written with `List.rec`/`Nat.rec` directly: the
  equation-compiler version was ~10× slower in the kernel. `check.ps1` on the file: CLEAN, 162 s
  (all of k = 1..16 in one `decide +kernel`). One-off single-k runs (not committed) were erratic:
  k = 15 alone 429 s, k = 16 alone 137 s; k = 17 did not finish in 20 min, so going further needs
  stronger pruning (e.g. a Lean proof of Lemma 2.3, or the residue-class structure of Lemma 2.2)
  or a smaller search space. Counts N(k) are not proved (soundness of the enumerator not
  formalized).
- **2026-11-25.** PR #57 opened (issue #47). `/review` not run (budget); left to the reviewer loop.
- **2026-11-25.** Attack stage (issue #48). Own arguments (unreviewed) for the window lemma,
  coprime ends, and Conjecture 5.2 for prime-power k (A6.1–A6.3), plus a single-residue
  reformulation of WCS (A6.4). Full conjecture not proved; gap: k with two or more distinct prime
  factors (A6.5). Throwaway Python scripts, not committed: backtracking enumeration of all WCS for
  k ≤ 20 (counts as in the earlier log line), a check of A6.1, A6.2 and the Y-form, k + 1 and unit-class parts of A6.4 on all of them, an
  enumeration of Y mod lcm(1..k) for k ≤ 13 (count equals N(k)), and a residue-system search for
  the relaxations in A6.5. [numerical, Python, not Lean]
- **2026-11-25.** Attack stage `/review` done (1 blocking + 8 wording findings, all fixed; see
  Review). PR opened for #48.
- **2026-11-25.** Issue #52: fixed the seven review points left open on PR #49 (see Review);
  `/review` done (3 wording findings + 1 nit, all fixed).
- **2026-11-26.** Addressed the reviewer-loop comment on PR #63 (3 minor findings, all fixed;
  see Review).
- **2026-11-26.** Attack stage for issue #68 (two distinct prime factors). Own arguments
  (unreviewed): slice lemma A7.1 and Conjecture 5.2 for k = r·s^b with s ∤ r − 1 (A7.2), which
  includes every squarefree k = pq and every 2·s^b. Gap A7.3: p^a q^b with a, b ≥ 2, or r·s^b
  with b ≥ 2 and s ∣ r − 1 (e.g. 12, 20, 36, 63). `search/weakly-consecutive/wc_slice_check.py` (kept in the repo, run with `python -I`):
  re-enumerates all WCS for k ≤ 20 (counts as in the 2026-11-25 line), checks the general
  form of A7.1 and its mirror on all of them (no failures), and lists the covered k ≤ 100.
  [numerical, Python, not Lean] `/review` (two subagents) found no mathematical error; 9 wording/label findings fixed (Review section).
- 2026-11-27: opened PR #69 for the A7 attack stage (#68).
- **2026-11-27.** Citation check (#80, finishing item 2) for A6.1–A6.3 and A7.1–A7.2: added A6.0
  (class lemma = Lemma 2.2 direction WCS ⇒ classes, and reversal = Rule 3, both from Def. 1.1)
  and A8 (step-by-step list). Every GSK24 ingredient of these steps is now re-proved; their
  labels drop the [preprint: GSK24 …] part and stay [own argument, unreviewed]. No fetch needed.
- **2026-11-27.** `/review` of the citation check: no mathematical error; 6 wording findings fixed (Review).
- **2026-11-27.** Attack stage for #68 on A7.3: A7.4 proves Conjecture 5.2 for k = 4r, r ≥ 5
  prime (own argument, unreviewed; A6.2 + A7.1 force σ(1) = 2, σ(k − 1) = 4 up to reversal, the
  slice of T_4 then forces σ(3) = 4r, contradicting T_r = multiples of r); k = 12 is in the Lean
  check. `search/weakly-consecutive/wc_4r_check.py`: no WCS with σ(1) ∈ {2, 4}, σ(4r) = r for
  r = 3, 5, 7 [numerical, Python, not Lean]. Extension to 2^b·r, b ≥ 3, failed (A7.4). Not yet reviewed.
- **2026-11-27.** Attack stage for #68 on A7.3 (b), b = 2: A7.5 runs A7.4's chain for k = s²·r,
  s ∣ r − 1 (σ(1) = s, σ(k − s + 1) = s², σ(s² − s + 1) = k up to reversal), contradicting
  T_r = multiples of r unless r ∣ s² − s + 1; for k = 63 and 2107 a divisor m of k + 1 with
  T_m = multiples of m meets T_{s²} with m·s² > k (own argument, unreviewed). Newly covered
  k ≤ 100: 63. `search/weakly-consecutive/wc_s2r_check.py` lists the exceptions for s < 60
  [numerical, Python, not Lean]; 26533 = 13²·157 stays open. Not attempted: b ≥ 3, A7.3 (a). Not yet reviewed.
