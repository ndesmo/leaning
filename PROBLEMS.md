# Problems: scouted candidates

Open problems this project could work on, found by `/scout`. Each candidate has a GitHub issue
labelled `problem`. **Approval is the `approved` label on that issue, and only the owner adds it.**
The author loop works only on approved issues, takes them by priority, and re-checks that a problem is
still open before starting it.

How this list was made:
- **Scouted 2026-11-25** by five agents covering:
  - recent arXiv papers;
  - Google DeepMind's `formal-conjectures` repository;
  - the `teorth/erdosproblems` mirror (Apache-2.0);
  - MathOverflow (through the official Stack Exchange API);
  - the Open Problem Garden;
  - the OEIS.
- **One site not used:** erdosproblems.com bars AI agents. One scout read its forum before that
  restriction was known, and nothing from those pages is used here.
- **"Open" means** that the searches recorded below, run on 2026-11-25, found no solution. It is not
  a guarantee.

Scores are 0–2:
- **Open:** strength of the evidence that the problem is still open.
- **Lean:** 2 if Mathlib can state the problem directly.
- **Tract.:** 2 if a concrete first target is likely to be finished.
- **Value:** how much the answer matters. Crowding and minor results lower it.

## Ranked shortlist

| Id | Problem | Area | Open | Lean | Tract. | Value | Status |
|---|---|---|---|---|---|---|---|
| P1 | Weakly consecutive sequences start or end with 1 | combinatorics | 2 | 2 | 2 | 1 | taken (#21) |
| P2 | 2-adic valuation of central coefficients of (1+x+…+x¹⁵)ⁿ (OEIS A402341) | number theory | 1 | 2 | 2 | 1 | taken (#22) |
| P3 | Minimum modulus for valid residue sets (Fonollosa) | additive combinatorics | 2 | 2 | 2 | 1 | candidate (#23) |
| P4 | Periodicity of 3-sumfree sequences S₁,d−1,2d−1 | combinatorial number theory | 1 | 2 | 2 | 1 | candidate (#24) |
| P5 | Order reciprocity of prime pairs, case (3,3) | number theory | 1 | 2 | 1 | 1 | candidate (#25) |
| P6 | Centered maximal function: Var(Mf) bound, small discrete cases | real analysis | 2 | 1 | 1 | 2 | candidate (#26) |
| P7 | Intersecting families of triangulations (Kalai), 10-gon | combinatorics | 1 | 1 | 1 | 2 | candidate (#27) |
| P8 | Catch-Up game draws for N ≡ 0, 3 mod 4 | combinatorial games | 2 | 1 | 1 | 1 | candidate (#28) |
| P9 | Max queens each attacking exactly 3 (OEIS A051756) | combinatorics | 1 | 1 | 1 | 1 | candidate (#29) |
| P10 | Helly numbers of composite grids | discrete geometry | 2 | 1 | 1 | 1 | candidate (#30) |
| P11 | Colouring ℤ⁺ with n colours, multiples distinct, n = 195 | combinatorics | 2 | 1 | 0 | 2 | candidate (#31) |
| P12 | Erdős #677: equal lcms of disjoint intervals | number theory | 1 | 2 | 1 | 0 | candidate (#37), crowded |
| P13 | Erdős #287: gaps in Egyptian fractions of 1 | number theory | 1 | 2 | 1 | 0 | candidate (#38), crowded |
| P14 | WOWII graph conjectures 61, 133, 199 | graph theory | 1 | 2 | 1 | 0 | candidate (#39), crowded |

The leading candidates (P1–P4) are elementary, already well suited to Lean, and quiet: no citing
work or competing claims were found. Their limitation is modest value; a result would be a solid
contribution, not a headline. P6 and P7 matter more but are harder, and P7 has an active research
group.

## Candidates

### P1. Weakly consecutive sequences start or end with 1
- **Source:** Garrison, Seiler, Knowles, "Weakly Consecutive Sequences", arXiv:2401.09497 (17 Jan
  2024). https://arxiv.org/abs/2401.09497
- **Definition (verbatim, Def. 1.1):** "Let σ:[k]→[k] be a permutation … We say σ is weakly
  consecutive if, for all i,j∈[k] and integers m, if m∣σ(i) and m∣(i−j), then m∣σ(j)."
- **Statement (verbatim):** "Conjecture 5.2. Any WCS either begins or ends with the term 1 (in other
  words, σ(1)=1 or σ(k)=1). Surprisingly, we have not been able to prove this conjecture by working
  straight from the definition."
- **Open evidence:** Semantic Scholar lists no citing papers. An arXiv search for "weakly
  consecutive" returns only this paper, and a web search found nothing later (2026-11-25).
- **Known:** Conjecture 5.1 (generation from 4 seeds by 3 rules) was checked by computer up to
  k = 500. Conjecture 5.2 follows from 5.1.
- **First target:** prove 5.2 from the definition, starting from where multiples of the largest
  primes ≤ k can sit, and check it in Lean for small k by `decide`.
- **Risks:** a short arXiv-only paper, so the difficulty is unknown. It might follow quickly from a
  lemma in the paper.
- **Status:** taken (#21), slug `weakly-consecutive`. Openness re-checked 2026-11-25; notes in
  [notes/weakly-consecutive.md](notes/weakly-consecutive.md).

### P2. 2-adic valuation of central coefficients (OEIS A402341)
- **Source:** https://oeis.org/A402341 (entry created 2026-11-17).
- **Statement (verbatim):** "Conjecture: for even n, the 2-adic valuation of a(n) equals
  A000120(15*n/2). Verified for n <= 1500." Here a(n) is the central coefficient of
  (1+x+…+x¹⁵)ⁿ.
- **Open evidence:** the entry has had no revision since creation, and a web search found no proof
  (2026-11-25). The scout re-checked it for even n ≤ 160.
- **Known:** the entry proves that a(n) is odd if and only if n = (16^k − 1)/15.
- **First target:** use 1+…+x¹⁵ = (1+x)(1+x²)(1+x⁴)(1+x⁸) and Kummer/Lucas-type carry arguments.
  Start with a lower bound, or one residue class of n.
- **Risks:** very new, so someone may prove it soon. It could fail beyond n = 1500.
- **Status:** taken (#22), slug `central-2adic`. Openness re-checked 2026-11-26; notes in
  [notes/central-2adic.md](notes/central-2adic.md).

### P3. Minimum modulus for valid residue sets (Fonollosa)
- **Source:** arXiv:2607.08366 (v2, 14 Jul 2026). The statement is already in Lean in
  `formal-conjectures`: `Arxiv/2607.08366/MinModulus.lean`.
- **Statement (verbatim):** "Conjecture 1 (Fonollosa, 2026). For every n ≥ 2 and every
  N < 2^n − 2^⌊log₂ n⌋, no set of n residues mod N is valid."
- **Open evidence:** tagged open in the repository, last touched 2026-10-29, with no PRs or issues.
  No later work was found (2026-11-25).
- **Known:** CP-SAT certifies it for n ≤ 7, and a search finds no counterexample for n ≤ 13. An
  exponential lower bound "appears to be open" (paper §7).
- **First target:** certify n = 8, every N < 252, or prove any general lower bound.
- **Risks:** the author may extend the computations. n = 8 may be heavy for Lean's kernel.

### P4. Periodicity of the 3-sumfree sequences S₁,d−1,2d−1
- **Source:** van Berkel, Bosma, "On t-sumfree sequences", arXiv:2609.16843 (v1 15 Sep 2026).
- **Statement (verbatim):** "Conjecture 4. For every d≥3 the 3-sumfree sequence S_{1,d−1,2d−1} is
  ultimately periodic, and, with the exception of d=3 or d=5, the preperiod length is d+3 and the
  period length is d modulo 8d−1."
- **Open evidence:** Semantic Scholar lists no citations. Related 2025–26 papers treat other
  families (2026-11-25).
- **Known:** the authors say "our proof methods apply here and we are convinced the following result
  is correct, we have not written down a full proof". Theorem 19 proves a similar family by block
  induction.
- **First target:** write out the block-induction proof modelled on Theorem 19, after reading the
  residue pattern mod 8d−1 from data.
- **Risks:** the authors may post the proof first. The result is modest.

### P5. Order reciprocity of prime pairs, case (3,3)
- **Source:** Costello, Korpal, arXiv:2608.03268 (4 Aug 2026); IACR ePrint 2025/150.
- **Statement (verbatim):** "(3) Are there any fixed values of (k,k′) with min(k,k′)>2 for which
  there are no pairs of primes with (k,k′)-order reciprocity?"
- **Open evidence:** no follow-up was found by web search (2026-11-25).
- **Known:** (2,2) is impossible. An exhaustive search covers primes up to the 200 millionth.
- **First target:** classify (3,3), where p ∣ Φ₃(q) and q ∣ Φ₃(p), with elementary mutual-divisibility
  arguments.
- **Risks:** the answer may simply be "pairs exist". Whether elementary methods work is untested.

### P6. Centered maximal function variation, small discrete cases
- **Source:** Hagelstein, Kosz, Stempak, arXiv:2407.06734 (v3).
- **Statement (verbatim):** "Conjecture Δ. Suppose f∈BV(ℝ). Then
  Var(Mf) ≤ Var(f) − ½||f(∞)|−|f(−∞)||." The weaker Var(Mf) ≤ Var(f) is also open.
- **Open evidence:** the only citing work, arXiv:2610.18544 (Oct 2026), gives partial results for
  characteristic functions. No full proof was found (2026-11-25).
- **Known:**
  - The conjecture holds for alternating piecewise-constant f.
  - The continuous and discrete versions are equivalent, and it reduces to nonnegative simple
    functions.
  - It holds with a constant C (Kurka), and with C = 1 for indicator functions.
- **First target:** the discrete version for 3-valued functions or small support. Run an exhaustive
  counterexample search, then try a proof for 3-step functions.
- **Risks:** long-standing, with active specialists. A general proof is unlikely.

### P7. Intersecting families of triangulations (Kalai), 10-gon
- **Source:** MathOverflow 114646 (Kalai). https://mathoverflow.net/q/114646
- **Statement (verbatim):** "Let 𝒯ₙ be the family of all triangulations on an n-gon … Let
  𝒮 ⊂ 𝒯ₙ be a subfamily of triangulations with the property that every two triangulations of 𝒮
  have a common diagonal. Problem: Show that |𝒮| ≤ |𝒯ₙ₋₁|."
- **Open evidence:** no accepted answer. Leader–Tan (arXiv 2610.39116, Oct 2026) prove only special
  cases.
- **Known:** proved for small polygons and checked by computer up to about 9 vertices
  (arXiv 1710.02518).
- **First target:** compute the largest intersecting family for the 10-gon (1430 triangulations,
  bound 429).
- **Risks:** clique-search certificates are hard to check. Leader and Tan are active right now.

### P8. Catch-Up game draws
- **Source:** `formal-conjectures`, `Paper/CatchUpConjecture.lean`.
- **Statement (verbatim):** "If T_N is even (equivalently N ≡ 0 (mod 4) or N ≡ 3 (mod 4)), then under
  optimal play the game Catch-Up({1, …, N}) ends in a draw."
- **Open evidence:** tagged open, with no PRs or issues. The literature has only computer checks for
  N ≤ 20.
- **First target:** settle N = 23, 24 by memoized search, and Lean-check the smallest new case.
- **Risks:** the state space grows like 2^N. The repo's `value` is noncomputable, so a computable
  mirror is needed.

### P9. Max queens each attacking exactly 3 (OEIS A051756)
- **Source:** https://oeis.org/A051756.
- **Statement (verbatim):** "Conjecture: a(n) = 2[(6n-2)/5] for n >= 2; verified up to n = 100."
  The upper bound is stated, without a linked proof.
- **Open evidence:** no proof found. The related exactly-one case was settled in arXiv 2608.27432
  (Aug 2026).
- **First target:** a periodic construction achieving the bound for all n, plus a written proof of
  the upper bound.
- **Risks:** the same group may do k = 3 next.

### P10. Helly numbers of composite grids
- **Source:** Dillon, arXiv:2411.10549 (Adv. Geom. 2025), Problem 1.
- **Statement (verbatim):** "Evaluate h((ℤ∖ℙ)²) and h(ℤ²∖ℙ²)."
- **Open evidence:** no citing work on these sets (2026-11-25).
- **Known:** h ≤ 18 for both.
- **First target:** a computer search for large empty convex polygons, which gives lower bounds with
  checkable certificates.
- **Risks:** a lower bound alone is minor.

### P11. Colouring ℤ⁺ so that a, 2a, …, na get distinct colours, n = 195
- **Source:** MathOverflow 26358; Caicedo–Chartier–Pach, EJC 28 (2021) P1.34.
- **Statement (verbatim title):** "Can we color Z^+ with n colors such that a, 2a, ..., na all have
  different colors for all a?"
- **Open evidence:** "the first open instance … is when n=195". Nothing newer was found.
- **First target:** a SAT search for a periodic, non-multiplicative colouring at n = 195.
- **Risks:** the search may be infeasible.

### P12–P14. Crowded candidates
Other people, including AI-assisted groups, are actively working on these. A further unreviewed
attempt would add little.
- **P12, Erdős #677** (statement from `formal-conjectures` 677.lean): the k = 3 case may already be
  covered by T. H. Chan, arXiv:2408.01306. Not yet checked.
- **P13, Erdős #287:** a public AI-generated Lean attempt exists.
- **P14, WOWII 61, 133, 199:** other groups are sweeping the WOWII conjectures.

## Rejected
- **Solved:**
  - hypercontractivity on ℤₙ (arXiv:2605.30867);
  - 3-subsumfree Conjectures 5 and 6 (arXiv:2606.17447, 2609.16843);
  - OEIS A226898 (proved, Nov 2026);
  - MO 93656 (Chan–Kontorovich–Pak);
  - Norine's path version (2026 preprints).
- **Crowded or a resolution already claimed:**
  - Erdős #458, #307 and #850;
  - Erdős #686 and #506 (active resolution attempts);
  - Dean k = 5;
  - WOWII 72, 84, 96 and 372;
  - TxGraffiti 3;
  - the unfair 0-1 polynomial conjecture.
- **No tractable target:**
  - Euler's 8n+3 conjecture;
  - OEIS A061220;
  - Alzer–Berg Conjecture 23 (Lean fit 0);
  - MathOverflow 512119 (computation only).
