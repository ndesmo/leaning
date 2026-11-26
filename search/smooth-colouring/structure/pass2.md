# Structural pass 2: the dilation reduction made precise, and the three-prime gap

Notation: T = T_195 = {t(m) : 1 <= m <= 195}, with t(m) = (v_r(m))_r in Z^44 (44 primes up to 195).
pi = {3, 5, 13}. Sources were downloaded and read locally: Wang–Wang arXiv:2609.15081 (HTML v1)
and Horak–Kim arXiv:1603.00051v1 (PDF). The Greenfeld–Tao and Bhattacharya quotes are from the arXiv
API abstracts.

## 1. Cited statements (verbatim)

**[paper: Horak–Kim, arXiv:1603.00051v1, Thm 8]** The setting: for a tiling T of Z^n by translates
of V with translation set L, T_T is the linear map on Laurent polynomials with T_T(x^a) = 1 if a is
in L and 0 otherwise, and Q_V = sum over a in (-V) of x^a. Verbatim:
> "Theorem 8. Let T be a tiling of Z^n by translates of V, and let a be an integer relatively prime
> to |V|. Then, for any polynomial P ∈ Z[x1^{±1}, ..., xn^{±1}], we have
> T(P Q_V(x1^a, ..., xn^a)) = P(1, ..., 1)."

Taking P = x^m gives |(m - aV) ∩ L| = 1 for every m, that is, **aV ⊕ L = Z^n**. Their proof
(Lemmas 9 and 10) is the Frobenius argument: Q_V(x^p) ≡ Q_V^p mod p, plus a counting step. It needs
only V finite and p ∤ |V|.

**[paper: Horak–Kim, Thm 6]** "Let V ⊂ Z^n, and T be a tiling of Z^n by translates of V. If |V| = q
is prime, then q(v − w) is a period of T for any v, w ∈ V."

**[paper: Wang–Wang 2609.15081, §4.3]** "The dilation theorem of Horak and Kim [7, Theorem 8], or
its measurable version [9, Theorem 1.2(i)], gives (4.4) S_k f = 1 if (k,pq)=1." The measurable
version, [9] = Grebík–Greenfeld–Rozhoň–Tao, IMRN 2023, was not read by me.

**[paper: Greenfeld–Tao, Annals 200 (2024), arXiv:2211.15847, abstract]** "The periodic tiling
conjecture asserts that any finite subset of a lattice Z^d which tiles that lattice by
translations, in fact tiles periodically. In this work we disprove this conjecture for
sufficiently large d".

**[paper: Bhattacharya, arXiv:1602.05738, abstract]** "We prove that any finite set F⊂Z^2 that
tiles Z^2 by translations also admits a periodic tiling."

Consequence: **no theorem known to me makes a tiling of Z^44 by T_195 periodic.** Periodicity is
known for d = 2 (Bhattacharya) and for tiles of prime size (Szegedy; Horak–Kim Thm 6). It is false
in general for large d (Greenfeld–Tao). Wang–Wang prove it ad hoc for T_205 only (Lemma 4.4).

## 2. Lemma A (finite / periodic reduction) [own argument, unreviewed; it agrees with the first step of the Wang–Wang Lemma 4.5 proof]

**Lemma A.** The following are equivalent:
1. T_195 admits a *periodic* tiling of Z^44.
2. T_195 ⊕ L = Z^44 for some L, with L + Λ = L for a lattice Λ of finite index.
3. There are a finite abelian group H whose order is divisible only by 3, 5 and 13, with
   |H| = 195·m, and a homomorphism ψ: Z^44 → H that is injective on T, such that ψ(T) ⊕ B = H for
   some B ⊆ H.

Moreover m > 1 in (3). Each of (1)–(3) implies that 195 is satisfactory.

*Proof.*
- (1) ⇔ (2) is the definition.
- (3) ⇒ colouring. Write ψ(x) = s + b uniquely, with s in ψ(T) and b in B, and colour x by s;
  this uses 195 colours. Suppose t(am) and t(am') get the same colour, with m ≠ m' ≤ 195. Then
  ψ(t(m)) − ψ(t(m')) = b − b' for some b, b' in B. Directness forces ψ(t(m)) = ψ(t(m')), and
  injectivity forces m = m', a contradiction.
- (3) ⇒ (2). Take L = ψ^{-1}(B), which is ker ψ-periodic.
- (2) ⇒ (3), step 1. Let G = Z^44/Λ and φ the quotient map. Then φ(T) ⊕ φ(L) = G: uniqueness
  lifts because L + Λ = L. In particular φ is injective on T and |G| = 195·|φ(L)|.
- Step 2. Split G = G_π × G_π' (Hall decomposition) and let e, e' be the exponents of the two
  factors. By CRT choose k > 0 with k ≡ 1 (mod e) and k ≡ 0 (mod e'). Then gcd(k, 195) = 1,
  because e is a π-number and k ≡ 1 mod e. Multiplication by k is the identity on G_π and zero on
  G_π', so kG = G_π.
- Step 3. Horak–Kim Thm 8 gives kT ⊕ L = Z^44, and reducing mod Λ as in step 1 gives
  kφ(T) ⊕ φ(L) = G. So ψ := kφ is injective on T, and ψ(T) ⊆ G_π =: H.
- Step 4. A direct sum with a summand inside a subgroup H restricts to each coset H + g:
  ψ(T) ⊕ (φ(L) ∩ (H + g)) = H + g. Translating gives a tiling of H.
- m > 1. If m = 1, ψ is a bijection T → H, a homomorphism, with |H| = 195. That is a group
  logarithm of length 195, which does not exist. Sources: Forcade–Pollington, Blackburn–McKee as
  cited by Wang–Wang, and CCP. Every abelian group of order 195 is cyclic. ∎

So the sketch in journal item 3 is correct, and slightly stronger: the period group may be
replaced by a π-group. The remaining gap is entirely **(non-periodic tiling) ⇒ (periodic tiling)**.
A finite search over π-groups H can only ever prove existence.

A self-contained replacement for Thm 8 in a finite group G [own, standard]. Let A ⊕ B = G and let
p ∤ |A| be prime. In Z[G], A(x)^p ≡ A(x^p) (mod p), so A(x^p)B(x) ≡ A^{p−1}·G = |A|^{p−1}·G
(mod p). Every coefficient is then a nonnegative integer ≢ 0 (mod p), and the coefficients sum to
|A||B| = |G|. Hence every coefficient is 1, which gives pA ⊕ B = G. Iterating over the prime
factors of k gives the result for k.

## 3. Wang–Wang §4.3 for 195: what survives and what fails

Setup: the invariant measure, f = ω(0), S_k F = Σ_{a∈T} F(ω+ka) and A_k(z) = Σ z(a)^k. A spectral
character z is the same as a completely multiplicative χ: [195] → 𝕋.

Survives for 195 [own check of each step, unreviewed]:
- (i) S_k f = 1 for all k coprime to 195. This is the measurable dilation theorem, not checked.
- (ii) A_k(z) = 0 for all k coprime to 195, σ_f̃-a.e.
- (iii) (I−R_3)(I−R_5)(I−R_13)ν = 0. The Fourier multiplier of the operator is
  1_{gcd(k,195)=1}, so this follows exactly as in WW.
- (iv) The Frobenius congruences 3 | S_3 f, 5 | S_5 f and 13 | S_13 f, since
  S_p f ≡ S_1^p f = 195^{p−1} ≡ 0 (mod p).

**The precise obstruction.** WW's key consequence is A_p(z)A_q(z) = 0. That gives the constant
S_pS_q f = pq, and then the rectangle factorization f = gh of (4.5), on which Lemma 4.4 rests. For
195 this fails at two independent points:
- **O1 (counting; it fails even for genuine polygon unions).** WW's dichotomy comes from
  pP + qQ = pq having only the solutions (q,0) and (0,p). The equation 3a + 5b + 13c = 195 has
  **109** nonnegative solutions; only three are pure: (65,0,0), (0,39,0) and (0,0,15).
  - For a mixed union, two or three of A_3, A_5, A_13 can be nonzero. No pairwise product is
    forced to vanish, so no S_pS_q f is forced to be constant.
- **O2 (Lam–Leung).** The table on each μ_195-coset is a function on Z_3×Z_5×Z_13 with zero third
  mixed difference, so it equals X(i,j) + Y(i,l) + Z(j,l). A nonnegative table need not be a
  nonnegative sum of polygons.
  - Example: (ω+ω²)(ζ_5+…+ζ_5^4) + (ζ_13+…+ζ_13^12), with 8 + 12 = 20 points.
  - So even "a union of polygons" is not available. WW's nonnegativity step (choose i_0 minimising
    a column) is genuinely two-dimensional.

Whether O1 and O2 are *realised by characters of T_195* is open. Multiplicativity is a strong
constraint: in WW, Lemma 4.3 extracts z_r^{492} = 1 for r = 2, 3, 5 from it, using a
computer-checked finite lemma (Lemma 4.2). Coven–Meyerowitz and Łaba–Londner concern tiles of Z
(cyclic groups) and do not apply directly in Z^44; I did not fetch them.

## 4. Most promising next step (a finite computation)

**Pure-type question.** Is every completely multiplicative χ: [195] → 𝕋 with
Σ_{m≤195} χ(m)^k = 0 for all gcd(k,195) = 1 of pure type? Pure type means at most one of A_3, A_5,
A_13 is nonzero.
- The question depends only on the coincidence pattern Γ_z = {x : z(x) ∈ μ_195} together with
  the induced map Γ_z → Z_195. This is a finite, if large, combinatorial search, in the style of
  WW Lemma 4.2. Large primes r > 97 occur once in [195], and each must sit in a coset table with
  mass at least 3. This forces strong coincidences.
- If **yes**: all S_pS_q f = 195, and one should attempt a three-factor box version of (4.5) and a
  pi-analogue of Lemma 4.4. For a pure 13-gon spectrum, z^13 takes at most 15 values on T, which
  is the analogue of WW's |E| ≤ 5 trick.
- If **no**: an explicit mixed χ (weights w_r in Z_195 or Z_585) is a concrete certificate that
  the spectral route of §4.3 cannot work for 195, and the next attack should be non-spectral.
- A cheap first test: search for weights w ∈ Z_N^44 (N = 195, 585) whose count vector on Z_N has
  vanishing coprime moments and is of mixed type.
