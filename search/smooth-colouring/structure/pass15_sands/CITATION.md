# Citation check: "Sands 1957" (good groups / Hajós property) in pass14_struct/NOTE.md

Scope: NOTE.md §1 (line ~65, marked [unverified citation]), used in §3 Theorem 4 steps (i).4,
(ii).6, (iii) last bullet, and §Open item 2 (non-cyclic H). About 30 minutes of web search.
**I could not reach the primary papers.** Sands 1957/1962 and de Bruijn 1953 sit behind the
Springer/KNAW paywalls, and I could not get the Szabó (2004) or Szabó–Sands (2009) books. All the
statements below come from secondary sources that quote the classification, plus the abstract of
Sands' 1958 PhD thesis.

## Sources actually read (verbatim quotes)

S1. C. De Felice, "Finite maximal codes and factorizations of cyclic groups", arXiv:2202.09675
(2022), §6.1. https://arxiv.org/abs/2202.09675
> "We recall that a subset S of G is periodic if there exists g in G \ 0 such that g + S = S. A
> factorization (T, R) of G is periodic if at least one factor is periodic."
> "A group is good (or it has the Hajós property) if any of its factorization is periodic,
> otherwise it is bad. [...] In a sequence of different papers, good cyclic groups were
> characterized [41]. They are Z/p^nqZ, Z/p^2q^2Z, Z/p^2qrZ, Z/pqrsZ and their subgroups, where
> p, q, r, s are different primes."
[41] = S. Szabó, Topics in Factorization of Abelian Groups, Birkhäuser, 2004.

S2. J. C. Lagarias, S. Szabó, "Universal spectra and Tijdeman's conjecture on factorization of
cyclic groups", arXiv:math/0008132 (2000), §2. https://arxiv.org/abs/math/0008132
> "Tijdeman showed that this conjecture holds for any m for which Z/mZ is a "good" group in the
> sense of Hajós [5] and de Bruijn [1]. The complete list of cyclic "good" groups are known to be
> those of order p^n (n ≥ 1), pq, pqr, p^nq (n > 1), p^2q^2, p^2qr and pqrs, where p, q, r and s
> are distinct primes, c.f. [18] for references."
[18] = R. Tijdeman, "Decomposition of the integers as a direct sum of two subsets", Number Theory
Seminar Paris 1992–93, CUP 1995, 261–276. (Szabó is a co-author of S2 and of the 2009 book.)

S3. T. Banakh et al., "Kaleidoscopical configurations in G-spaces", arXiv:1001.0903v3 (2011),
Theorem 4.1. https://arxiv.org/abs/1001.0903
> "Theorem 4.1 (Hajós-Sands). A finite Abelian group G has the Hajós property if and only if G is
> isomorphic to a subgroup of a group that has one of the following types:
> (p^n, q), (p^2, q^2), (p^2, q, r), (p, q, r, s), (p, p), (p, 3, 3), (3^2, 3), (p^3, 2, 2),
> (p^2, 2, 2, 2), (p, 2^2, 2), (p, 2, 2, 2, 2), (p, q, 2, 2), (2^n, 2), (2^2, 2^2), where
> p < q < r < s are distinct primes and n ∈ N."
It cites this to [8] = A. D. Sands, "On the factorisation of finite Abelian groups II", Acta
Math. Acad. Sci. Hungar. 13 (1962), 153–169. (The superscripts were recovered with
`pdftotext -layout` and may lose detail in the 2-group entries. Those entries do not matter here.)

S4. S. Fan, T. Zhang, "Periodicity of tiles in finite abelian groups", arXiv:2408.12901v2 (2025),
§1. https://arxiv.org/abs/2408.12901
> "Following [41, Page 5], we say that a finite abelian group G has the Hajós property if, for
> every tiling pair (A, T) of G, either A or T is periodic. In the literature, such groups are
> sometimes referred to as good groups"
> "The classification was completed by Sands [36], who provided the following complete list of
> finite abelian groups with the Hajós property: Z_{p^n q}, Z_{p^2q^2}, Z_{p^2qr}, Z_{pqrs}, [...]
> Z_p × Z_3^2, Z_9 × Z_3, Z_{2^n} × Z_2, Z_4^2, Z_p^2, where p, q, r, s are distinct primes [...]
> All these groups and all subgroups of them have the Hajós property."
[36] = Sands, Acta Math. Acad. Sci. Hungar. 13 (1962) 153–159[sic]; [41] = Szabó–Sands 2009 book.
(The 2-group entries came out garbled in extraction. Read this way, the list matches S3.)

S5. A. D. Sands, PhD thesis "The factorisation of finite abelian groups", Glasgow 1958, abstract.
https://theses.gla.ac.uk/72566 . The abstract defines "good" as "one factor in any factorisation
must have a non-trivial subgroup as a factor". It also says "In this thesis the problem is solved
completely for finite abelian groups" and "all the groups not shown to be bad by this theorem or
one of the theorems of de Bruijn are shown to be good." It names no specific orders.

S6. MathWorld, "Hajós Group", https://mathworld.wolfram.com/HajosGroup.html . It says "Sands
(1962) completed the classification of finite Hajós groups" and lists the cyclic orders as
p^a, p^a q, p^2qr, p^2q^2, pqr, pqrs. It also lists de Bruijn, Indag. Math. 15 (1953) 258–264.

## Verdicts

1. **Z225 = Z_{3²5²} is good.** This is the p²q² case. **Secondary source only.** S1, S2, S3, S4
   and S6 agree. The classification is attributed to Sands 1962 (II), Acta Math. Acad. Sci.
   Hungar. 13, 153–169 (S3, S4, S6), and through S1 to Szabó 2004. I did not find which paper
   first proves the p²q² case, and I did not see the 1957 paper (vol. 8, 65–86; bibliography
   entry confirmed in S1 as "Acta Math. Acad. Sc. Hungaricae, 8:65–86, 1957").

2. **Z75 = Z_{3·5²} is good.** This is the p^n q case with p=5, n=2, q=3. **Secondary source
   only.** S1–S4 and S6 agree. It is usually credited to de Bruijn (Indag. Math. 15 (1953)
   258–264), and S5 confirms that "theorems of de Bruijn" settle part of the list. The NOTE's
   parenthetical "(de Bruijn)" is consistent with this, but I did not see de Bruijn's paper.

3. **The non-cyclic groups are not good.** **Secondary source only (S3, S4).** The classification
   is an "iff" (S3: "if and only if G is isomorphic to a subgroup of ..."). I checked each group
   against the S3 list:
   - Z3²×Z25. Its 3-rank is 2 and it has an element of order 25. The only listed types with 3-rank
     2 are (p,3,3) with p prime, (3²,3) and (3,3). None contains Z25. **Not good.**
   - Z9×Z5². Its 5-rank is 2. The only listed types with odd p-rank ≥ 2 are (p,p) (a p-group),
     (p,3,3) and (3²,3). None has 5-rank 2 together with a 3-part. **Not good.**
   - Z3²×Z5². This needs 3-rank 2 and 5-rank 2 at the same time. No listed type has this.
     **Not good.**
   So the NOTE's claim "These are not good groups" agrees with the published classification. Being
   bad only means that *some* factorization has both factors aperiodic. That does not by itself
   give aperiodic complements of the specific shape the NOTE needs. The NOTE's further remark,
   "aperiodic complements exist in the analogues", is its own claim and is not covered by this
   citation.

4. **Does the NOTE use "good" in the source's sense?** **Yes, apart from the attribution.**
   - Definition. The NOTE says "every factorization has a periodic factor". S1 says "at least one
     factor is periodic", S4 says "either A or T is periodic", S6 says "at least one of the subsets
     A, B is periodic", and Sands (S5) says "has a non-trivial subgroup as a factor". For finite
     G these are equivalent: A+g=A with g≠0 holds iff A = ⟨g⟩ ⊕ A'. Periodicity is unchanged by
     translation, so normalisation (0 ∈ A∩B) makes no difference. Only *one* factor is guaranteed
     to be periodic, not both.
   - Uses. (i).4 gives a factorization of Z225 with both factors aperiodic, which contradicts
     goodness. (iii) says B' is aperiodic, so A_k is periodic. (ii).6 says B̄' is aperiodic in Z75,
     so Ā_k'' is periodic. Each of these uses only "at least one factor is periodic". In (ii).6 the
     step from "periodic, 5 points" to "coset of the order-5 subgroup" is elementary: the period
     generates a subgroup of order dividing 5, and Z75 has a unique order-5 subgroup. It is not
     part of the citation. In (ii) the NOTE identifies H/⟨g3⟩ ≅ Z3×Z25 with Z75. That is correct,
     since gcd(3,25)=1.
   - The NOTE's "iff N divides one of p^n q, p²q², p²qr, pqrs" matches S1 word for word ("...and
     their subgroups"). The pqr and p^n cases are divisors of these, so they are covered.
   - **Mismatch to fix: attribution.** The NOTE cites "Acta Math. Acad. Sci. Hungar. 8 (1957)" for
     the classification. The secondary sources credit the completed classification to
     **Sands 1962, "On the factorisation of finite abelian groups II", Acta Math. Acad. Sci.
     Hungar. 13, 153–169** (S3, S4, S6). Suggested wording: "Sands (Acta Math. Hungar. 8 (1957);
     13 (1962)); see Szabó, Topics in Factorization of Abelian Groups (2004) and Szabó–Sands,
     Factoring Groups into Subsets (2009), as quoted in Lagarias–Szabó arXiv:math/0008132 and
     De Felice arXiv:2202.09675". Mark it [cited, secondary] until the 1962 paper or one of the
     books has been read.
   - Side note on the task brief. The brief's list "Z_{p^a q}, Z_{p²q²}, Z_{pqr}, Z_{p²qr},
     Z_{pqrs}" is correct and agrees with S2 and S6. Z_{pqr} is redundant, since pqr | p²qr.

## Still missing for "verified from source"
I have not read Sands 1962 (doi:10.1007/BF02033634), Sands 1957 (vol. 8), de Bruijn 1953, or the
relevant theorem in Szabó–Sands 2009 (§ on good groups). The repo-internal alternative in NOTE
Open item 3 (CM Lemma 2.4 / Sands 1977, already quoted verbatim, or direct enumeration in Z225)
would remove the dependence altogether.
