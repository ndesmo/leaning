# Periodic tilings with |B| prime: the reduction to three finite searches

Status: written 2026-11-26, not yet /reviewed. Each step is labelled. Brute-force sanity check:
`prime_B_bruteforce.py` (output in `prime_B_bruteforce.out`).

## 0. Setting and the precise claim

T = T_195 = {t(m) : 1 ≤ m ≤ 195} ⊂ Z^44, t(m) the exponent vector of m. π = {3, 5, 13}.
A periodic tiling T ⊕ L = Z^44 with a period lattice Λ (L + Λ = L, [Z^44 : Λ] < ∞) gives, with
G = Z^44/Λ and φ the quotient map, a factorisation

    A ⊕ B = G,   A = φ(T),   B = φ(L),   φ injective on T,   |A| = 195,   |G| = 195·|B|.   (*)

Conversely (*) for any homomorphism φ: Z^44 → G (G finite abelian) gives the periodic tiling
L = φ^{-1}(B). (Lemma A of `pass2.md`; the converse direction is immediate.)

Note that |B| depends on the choice of Λ. Take Λ = Per(L), the group of all periods of L. Every
period lattice of L is contained in Per(L), so |B| for Per(L) divides |B| for any Λ. "No periodic
tiling with |B| prime" therefore means: **no periodic tiling has a period lattice of index 195·p
with p prime.** Equivalently, for every periodic tiling, [Z^44 : Per(L)] = 195·m with m = 1 or m
composite. (If some period lattice Λ has index 195·p, then m(Per(L)) divides p, so m(Per(L)) is 1
or p; conversely Λ = Per(L) is itself a period lattice. The value m = 1 is outcome (a) below.)

**Theorem (reduction).** Suppose (*) holds with |B| = p prime. Then one of the following holds:

- (a) there is a homomorphism ψ: Z^44 → Z_195 that is bijective from T onto Z_195 (a multiplicative
  colouring with 195 colours); or
- (b) p ∈ {3, 5, 13}, and there is a homomorphism φ: Z^44 → Z_{p²} × Z_{195/p}, injective on T,
  such that for every k ∈ Z_{195/p} the fibre φ(T) ∩ (Z_{p²} × {k}) is a coset of pZ_{p²} × {k}.

Conversely, each of (a) and (b) gives a periodic tiling: (a) with B = {0}, and (b) with
B = {0, 1, …, p−1} × {0}, since then φ(T) is a union of 195/p cosets of P = pZ_{p²} × {0}, one
over each k, and P ⊕ ({0,…,p−1} × {0}) = Z_{p²} × {0}. So (b) is *exactly* the search space:
nothing is lost and nothing is added.

The cases "H = Z_p × Z_p" and "B a subgroup" are not separate outcomes. Both fall into (a) (§3).
Whether (a) or any of the three (b) searches has a solution is not part of this note. (a) is
excluded by CCP. The three (b) searches (Z9 × Z65, Z25 × Z39, Z169 × Z15) are reported NONE in
the journal, passes 2 and 3 [numerical: single implementation].

## 1. Tools

**D (dilation, finite abelian groups).** Let G be a finite abelian group with A ⊕ B = G, and let
t be an integer with gcd(t, |B|) = 1. Then A ⊕ tB = G, where tB = {tb : b ∈ B}. In particular
|tB| = |B|, so b ↦ tb is injective on B.

- Source: [paper: Tijdeman 1995, Thm 1] for Z, and [paper: Sands / Szabó–Sands] for finite
  abelian groups. Verbatim statements are in §5. The Z^n version is
  [paper: Horak–Kim arXiv:1603.00051v1, Thm 8], quoted verbatim in `pass2.md` §1.
- **Direction.** The dilated set is the one whose size must be coprime to t. Since A ⊕ B = B ⊕ A,
  "gcd(t,|A|) = 1 ⇒ tA ⊕ B = G" and "gcd(t,|B|) = 1 ⇒ A ⊕ tB = G" are the same theorem with the
  roles of the two factors swapped. Below we always dilate **B**, with gcd(t, p) = 1. So A = φ(T)
  and φ never change, and the new factorisation is still of the form (*) with the same φ.
- Self-contained proof [own argument, standard; it is the classical Frobenius argument]. It is
  enough to treat t = q prime, q ∤ |B|; then iterate over the prime factors of t, using |qB| = |B|
  at each step. In Z[G] we have A(x)B(x) = G(x) := Σ_{g∈G} x^g, and B(x)G(x) = |B|·G(x). Mod q,
  B(x)^q ≡ B(x^q), where B(x^q) = Σ_{b∈B} x^{qb} counts coincidences with multiplicity. Hence
      A(x)B(x^q) ≡ A(x)B(x)^q = B(x)^{q−1}G(x) = |B|^{q−1}G(x)   (mod q).
  - Every coefficient c_g of A(x)B(x^q) is a nonnegative integer with c_g ≡ |B|^{q−1} ≢ 0
    (mod q), so c_g ≥ 1.
  - Σ_g c_g = |A|·|B| = |G|, so c_g = 1 for all g.
  - So every g is a + qb in exactly one way, counting b ∈ B with multiplicity. That gives
    injectivity of b ↦ qb on B and A ⊕ qB = G. ∎

**Δ (direct sums by differences)** [elementary]. For X, Y ⊆ G, the map X × Y → G, (x, y) ↦ x + y,
is injective iff (X − X) ∩ (Y − Y) = {0}. If in addition |X||Y| = |G|, then X ⊕ Y = G.

**Q (quotient by a subgroup factor)** [elementary]. If A ⊕ S = G with S a subgroup of G, then
the quotient map G → G/S is a bijection from A onto G/S. If moreover |A| = 195, then G/S is an
abelian group of order 195 = 3·5·13, hence cyclic. So ψ = (G → G/S) ∘ φ is as in (a).

**Lemma 1** (order-p difference ⇒ (a)) [own argument, unreviewed; checked by brute force for
p = 3, 5]. In (*) with |B| = p prime, suppose some d ∈ B − B, d ≠ 0, has order p in G. Then
A ⊕ ⟨d⟩ = G, and (a) holds.

*Proof.* Write d = b₁ − b₂. For k = 1, …, p−1 we have gcd(k, p) = 1, so A ⊕ kB = G by D, and
kd = kb₁ − kb₂ ∈ kB − kB. Moreover kd ≠ 0, because d has order p and p ∤ k. Since A ⊕ kB = G,
Δ gives (A − A) ∩ (kB − kB) = {0}, so kd ∉ A − A. Since d has order p, ⟨d⟩ = {0, d, …, (p−1)d}, so
(A − A) ∩ (⟨d⟩ − ⟨d⟩) = (A − A) ∩ ⟨d⟩ = {0}. Also |A|·|⟨d⟩| = 195p = |G|, so A ⊕ ⟨d⟩ = G by Δ,
and Q gives (a). ∎

In particular: **if B is a subgroup, then (a) holds**, by Q directly. A subgroup of prime order p
is cyclic of order p, so any nonzero difference has order p.

## 2. Step 1: p ∉ {3, 5, 13}  [own argument, unreviewed]

Here |G| = 195p with p ∤ 195, so G = G_p × G_{p'} with |G_p| = p. Let t = 195. Then
gcd(t, |B|) = gcd(195, p) = 1, so A ⊕ tB = G by D, and |tB| = p. Also tG = G_p, since
multiplication by 195 kills G_{p'} (order 195) and is an automorphism of G_p. So tB ⊆ G_p with
|tB| = p = |G_p|, that is, tB = G_p is a subgroup, and Q (applied to A ⊕ G_p = G) gives (a).

This covers p = 2 and every prime p ≥ 7 other than 13.

## 3. Step 2: p ∈ {3, 5, 13}  [own argument, unreviewed]

**Hypothesis used here: 195 = 3·5·13 is squarefree.** Hence p ∥ 195, so p² ∥ |G| and 195/p is
coprime to p. (For a non-squarefree n in place of 195 this step, and 2a, would need changing.)

Now |G| = 195p = p²·(195/p), and 195/p is squarefree and coprime to p. So G = H × K, with H the
p-Sylow subgroup, |H| = p², so H ≅ Z_{p²} or Z_p × Z_p, and K of order 195/p, cyclic because it is
abelian of squarefree order, so K ≅ Z_{195/p}.

**2a. Push B into H.** Let t = |K| = 195/p. Then gcd(t, |B|) = gcd(195/p, p) = 1, because 195 is
squarefree. By D, A ⊕ B' = G with B' := tB and |B'| = p. Multiplication by t kills K and is an
automorphism of H, so B' ⊆ H. Translating, we may assume 0 ∈ B'. This is legitimate, since
A ⊕ (B' − b₀) = G − b₀ = G. The set A and the map φ are unchanged.

**2b. Fibres are complements in H** [elementary]. For g ∈ G put C_g := (A ∩ (H + g)) − g ⊆ H.
Every element of H + g is a + b with a ∈ A and b ∈ B', uniquely, and since B' ⊆ H, a ∈ H + g.
Hence C_g ⊕ B' = H for every coset H + g, and |C_g| = p²/p = p. Identifying G/H with K, the C_g
are, **up to translation** (by g), the fibres A ∩ (H + g) of A over K. Being a coset of a subgroup
of H is invariant under translation, so it does not matter which representative g is used.

**2c. Case B' − B' contains an element of order p.** Then (a), by Lemma 1 applied to A ⊕ B' = G.
This case includes:
- **H ≅ Z_p × Z_p, always.** Every nonzero element of H has order p, and B' − B' ≠ {0} since
  |B'| = p ≥ 2. So no search is needed for Z_p², for any p. The Z3² searches of pass 2 and the
  Z5² searches of pass 3 were redundant.
- **H ≅ Z_{p²} and B' − B' meets pZ_{p²} \ {0}.** This includes B' = pZ_{p²}, the only subgroup
  of order p.

**2d. Case H ≅ Z_{p²}, and every nonzero element of B' − B' is a unit.** Then the p elements of
B' are pairwise incongruent mod p, so B' is a complete residue system mod p. Fix a fibre
C = C_g, so C ⊕ B' = H. Fix d ∈ B' − B', d ≠ 0, a unit. For any unit u ∈ Z_{p²}, let k = u·d^{−1}
mod p², a unit, so gcd(k, p) = 1. Then C ⊕ kB' = H by D, applied in the group H (where
|B'| = p), and u = kd ∈ kB' − kB'. So u ∉ C − C by Δ. Hence C − C ⊆ pZ_{p²}: C lies in one coset
of pZ_{p²}, and since |C| = p, C *is* that coset. As this holds for every fibre, we are in (b),
with φ composed with an isomorphism G ≅ Z_{p²} × Z_{195/p}.

This proves the Theorem. ∎

## 4. What was not needed, and comparison with the journal

- **Rédei's theorem is not needed.** Lemma 1 (dilation plus Δ) settles Z_p × Z_p outright, and
  2d settles Z_{p²}. Both use only D, which is proved above in five lines. Rédei's theorem
  (verbatim in §5) does give the stronger true fact that every complement of a non-subgroup B' in
  an order-p² group is a subgroup coset. The reduction does not use that fact.
- The brute force (`prime_B_bruteforce.py`, p = 3, 5, both groups, all B ∋ 0 and all complements
  C ∋ 0) finds no counterexample to Lemma 1, 2d or D. Counts: Z9 has 10 tileable B (9 complete
  residue systems and the subgroup); Z25 has 626 (5⁴ residue systems and the subgroup). In Z3² all
  28 sets B ∋ 0 of size 3 are tileable, and in Z5² 3426 of 10626 are. Every complement of a
  non-subgroup B is a subgroup, as Rédei predicts. For p = 13 the argument above is general in p.
- **Journal checks.**
  - Pass 2: "Tijdeman, with roles swapped: gcd(t,|B|)=1 ⇒ A ⊕ tB = G, t = 65". This is correct,
    and it is the direction used here.
  - Pass 3: "dilating by t = |K|". Also correct.
  - Pass 3, Z_p²: "Every fibre complements the line spanned by a difference in B − B, which
    reduces to the multiplicative case". This is correct but stated too briefly. The clean form is
    Lemma 1: A itself complements ⟨d⟩, by dilation. No Rédei and no fibre-by-fibre argument is
    needed.
  - Pass 3: "by Rédei's theorem … every complement of a non-subgroup B is a coset of an order-p
    subgroup". The statement is true, but it is not needed. For Z_{p²}, 2d proves it directly.
- **What the reduction rests on:**
  - (i) D, proved here, and also in the literature (§5).
  - (ii) CCP's result that no multiplicative colouring exists for 195, to exclude (a). See §5 for
    exactly what CCP state.
  - (iii) The three (b) searches. These are numerical, single implementation, and the NONE
    results lack a second checker.
  - The reduction itself has no known gap. It has not been independently reviewed.
- **Scope.** This excludes only the periodic tilings whose period group has index 195p. Composite
  |B| (9, 15, 25, …) and non-periodic tilings are untouched. As the journal says, this does not
  settle whether 195 is satisfactory.

## 5. Cited statements (verbatim)

**[paper: CCP arXiv:1902.00446, PDF text extracted with pdftotext]**
- Thm 1.6(4): "n admits a partial G-isomorphism for some abelian group (G, ⊕) of order n, i.e.,
  there is a bijection h : [n] → G such that whenever a, b ∈ [n], if ab ∈ [n], then
  h(ab) = h(a) ⊕ h(b)."
- Def 4.12: "Given an abelian group (G, +) of order n, we say that an abelian group structure on
  [n], ([n], ⊕), is a G-satisfactory group if and only if ([n], ⊕) ≅ (G, +) and a ⊕ b = ab
  whenever a, b, ab ∈ [n]."
- Thm 5.1: "Theorem 5.1 (Forcade-Pollington [FP90]). There are positive integers n for which no
  multiplicative colorings exist. The smallest such n is n = 195."
- §5.1: "they employed an exhaustive search algorithm that identified 195 as the least value of n
  for which there are no G-satisfactory groups."

Outcome (a) is a partial Z_195-isomorphism: h(m) = ψ(t(m)). Conversely, a partial isomorphism
extends to ψ by setting ψ(e_r) = h(r) for primes r. So (a) is excluded by [FP90] as reported by
CCP. That result is computational. FP90 itself was not read. The project's own multiplicative
search agrees.

**[paper: Horak–Kim arXiv:1603.00051v1, Thm 8]**: verbatim in `pass2.md` §1. It is the Z^n
version of D.

**Dilation theorem D, from secondary sources** (the originals, Tijdeman 1995, Sands 2000 and
Szabó–Sands 2009, were not read). Quotes were copied from pdftotext extractions:
- Zhao–Yuan, arXiv:2002.11872v1, Prop. 2.1, citing Szabó–Sands, *Factoring Groups into Subsets*,
  Thm 7.12: "If G = A · B is a factorization of the finite abelian group G (written
  multiplicatively) and k is an integer relatively prime to |A|, then G = Ak · B is a
  factorization of the abelian group G, where Ak = {ak : a ∈ A}."
- W. Zhou, arXiv:2412.18132v5, Prop. 1: "Let G be an additive finite Abelian group, and (A, B) a
  tiling pair in G. If q ∈ N is co-prime to |A|, then (qA, B) is still a tiling pair in G." The
  paper attributes the cyclic case to Tijdeman [Thm 1] and the general case to Sands, Bull. LMS 32
  (2000), Prop. 3.
- Coven–Meyerowitz, arXiv:math/9802122v1, Lemma 2.2, which is the Z version.
- In D, the set being dilated is the one whose size is coprime to t. We use D with the roles of A
  and B swapped, dilating B with gcd(t, p) = 1.
- Do **not** cite Łaba–Londner §2.3 or Tao's blog Cor. 5 for D: they need t coprime to |G|.

**Rédei** (not used): Kiss–Malikiosis–Somlai–Vizer, arXiv:1807.02844v3, Thm 2.1: "Let G = A1 + A2
+ · · · + An be a factorization of an abelian group G, where each Ai contains 0 and is of prime
cardinality. Then at least one of the sets Ai is a subgroup of G."

## Revision (pass 7)

Referee fixes from the pass-6 read (journal, pass 6, item 2), applied 2026-11-27:
- §0: the equivalent form now reads "m = 1 or m composite", with a one-line reason why Per(L)
  gives the right quantifier (m = 1 is outcome (a)).
- §3: squarefreeness of 195 is stated explicitly as the hypothesis behind p² ∥ |G|.
- 2b: the C_g are the fibres of A over K *up to translation*; noted that being a coset is
  translation-invariant.
- Lemma 1: added why kd ≠ 0 (d has order p, p ∤ k), which Δ needs.
No mathematical content changed; the note is still not formally /reviewed.
