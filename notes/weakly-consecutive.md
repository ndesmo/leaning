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
| For a WCS and m ∈ [k], σ^{-1}(m) ∈ [(k mod m) + 1, k − (k mod m)] | [preprint: GSK24, Lemma 2.3, read with x = m] + [own argument, unreviewed: the reading and a re-derivation] | Literature, item 4 |
| Division slices D_d(σ) of a WCS are WCS | [preprint: GSK24, Lemma 2.4, read with m = k] | Literature, item 5 |
| Reversal preserves WCS | [preprint: GSK24, Rule 3] | Literature |
| Conjecture 5.2 holds for every k ≤ 16: every WCS σ of [k] (Def. 1.1 verbatim, m ∈ ℤ) has σ(1) = 1 or σ(k) = 1 (`conjecture_5_2_le_16`) | [Lean] (`halfline_lt/Proofs/WeaklyConsecutive.lean`; kernel `decide +kernel` on a pruned enumerator proved complete, no `native_decide`) | Log 2026-11-25 (Lean) |
| N(k) for k = 1..23 is 1, 2, 2, 4, 4, 4, 4, 4, 8, 16, 16, 4, 4, 2, 2, 8, 8, 8, 8, 4, 12, 16, 16, and no WCS with 16 < k ≤ 23 violates Conjecture 5.2 | [numerical, exact enumeration, Python, not Lean] (the counts are not proved in Lean for any k: the enumerator's soundness is not formalized) | Log 2026-11-25 |
| σ^{-1}(1) is the unique position not in ⋃_{p ≤ k prime} T_p; so Conjecture 5.2 ⇔ for every WCS the prime classes T_p cover {2, …, k − 1} | [own argument, unreviewed] | Attack ideas, A1 |
| T_m ∩ T_n = T_{lcm(m,n)} if lcm(m,n) ≤ k, and = ∅ otherwise | [own argument, unreviewed] | Attack ideas, A2 |
| For a prime p ∈ (k/2, k], T_p = {σ^{-1}(p)} and σ^{-1}(p) ∈ [k − p + 1, p] | [preprint: GSK24, Lemma 2.3] + [own argument, unreviewed] | Attack ideas, A3 |
| For odd k, every even value sits at an even position, so σ^{-1}(1) is odd | [preprint: GSK24, Lemmas 2.2, 2.3] + [own argument, unreviewed] | Attack ideas, A3 |
| If Conjecture 5.2 holds for all lengths < k, then for every WCS of length k and every d ∈ [2, k], σ^{-1}(d) is the first or the last element of T_d | [preprint: GSK24, Lemma 2.4] + [own argument, unreviewed] | Attack ideas, A4 |

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
     |S_m| = ⌊k/m⌋ + 1 > |T_m|) shows the intended reading is **x = m**. Re-derived: write
     k = qm + s with 0 ≤ s < m; the class of a position r mod m meets [k] in q + 1 points if its
     least positive representative is ≤ s, and in q points otherwise. By Lemma 2.2 this class is
     T_m, of size q, so σ^{-1}(m) ≡ ρ (mod m) with ρ ∈ [s + 1, m]; in particular
     σ^{-1}(m) ∉ [1, s], and by the same count from the right end, σ^{-1}(m) ∉ [k − s + 1, k].
     [own argument, unreviewed]
5. **Lemma 2.4** (§2): "Fix d∈[m]. Let ℓ be the least index such that d|σ(ℓ). Then the
   permutation" "D_d(σ): [⌊m/d⌋] → [⌊m/d⌋]" "defined by" "D_d(σ)(i) = σ(ℓ+(i−1)d)/d" "is weakly
   consecutive." Here m is again unbound; from context σ is a WCS of length k and **m = k**.
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

**What a proof of 5.2 can cite.** Lemma 2.2 (the residue-class characterization), Lemma 2.3 (with
x = m, re-derived above, so it can be proved inline instead of cited), Lemma 2.4 (slices, for an
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
  coprime m, n with mn > k the two classes are disjoint inside [k], although as residue classes
  mod m and mod n they meet in a residue class mod mn (CRT), which has no point in [k].
  This is a constraint on the pair (pos(m) mod m, pos(n) mod n) worth exploiting for large coprime pairs (a suggestion, not a claim).
- **A3. Large primes and small moduli.** [own argument, unreviewed]
  - For a prime p ∈ (k/2, k], T_p = {pos(p)} and pos(p) ∈ [k − p + 1, p] (Lemma 2.3).
  - For a prime p ∈ (k/3, k/2], T_p = {ρ, ρ + p}, both in [k], where its least
    element ρ lies in (k − 2p, p], and pos(p) ∈ {ρ, ρ + p}.
  - m = 2, k odd: T_2 is the class with least representative 2, i.e. the even positions, so every
    even value sits at an even position and pos(1) is odd. For k even both parities are possible
    a priori.
  - Plan: suppose 2 ≤ pos(1) ≤ k − 1. The values whose prime factors are all large are few and
    each is pinned to a single position; the values with small prime factors fill whole residue
    classes. Count the positions in [2, k − 1] left uncovered by the small-prime classes and show
    the large primes cannot cover all but one of them unless the gap is at an end.
- **A4. Induction through slices.** [preprint: GSK24, Lemma 2.4] + [own argument, unreviewed]
  Strong induction on k. For d ∈ [2, k] the slice D_d(σ) is a WCS of length ⌊k/d⌋ < k, and its
  value 1 is the position of d within T_d. So the induction hypothesis gives: pos(d) is the first
  or the last element of T_d, for every d ≥ 2. (This is Conjecture 5.3's mechanism.) What remains
  for the inductive step is to locate the value 1 itself, using these rigid positions for all
  d ≥ 2 at once, e.g. for the primes d in A3.
- **A5. Lean.** The definition is decidable; check Conjecture 5.2 for small k by `decide` /
  `native_decide` (or a verified enumeration) and formalize Lemmas 2.2–2.4 as the reusable base.
  The Python counts below must be re-done in Lean before any page uses them.

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
