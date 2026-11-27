# Pass 10: Conjecture S′ (Lemma S for shifted downsets): presentation, special cases, evidence

Status: written 2026-11-27 (explorer pass 10, structural strategy). Not /reviewed. Notation as in
`pass8_level.md` and `pass9_lemmaS.md`: T is a finite downset of N^k with 0 ∈ T, |T| = p·m, and
every coordinate is used (e_i ∈ T for all i; unused coordinates only add free Z summands).
g: Z^k → Z_m is a homomorphism whose fibres on T all have size p. The blocks are the fibres.
M = ⟨x − y : x, y in one block⟩ and Γ = Z^k/M. Write g_i = g(e_i).
Scripts and outputs are in `pass10_shifted/`, and commands are run from there.

## 0. Verdict

- **S′ is not proved**, neither for shifted downsets, nor for T_n, nor for T_195. The gap is
  stated exactly in §4.
- What is new:
  1. **Lemma P** [own argument, unreviewed]. Γ has a presentation that depends only on the set
     R ⊂ Z_m × Z_m of "additive pairs" of (T, g). So S′ becomes a statement about partial
     additivity on Z_m. Pass 9 had only one direction of this (Lemma E's partial additivity).
     Lemma P says those relations are a *complete* presentation of Γ.
  2. **A genuine special case** [Lemma P + numerical: exhaustive over all R, sympy SNF]. Lemma S
     holds for **every** downset (shifted or not) when m ∈ {2, 3, 4}, for every p. When m = 5 or
     m = 6 it holds for every p ∉ {2, 3}. None of these covers n = 195, where m ∈ {65, 39, 15}.
  3. **Lemma C** [own argument, unreviewed], a sufficient "cyclic-chain" criterion. On the pass-9
     T_195 samples it certifies Γ_p = 0 in only 0/400 cases for p = 3, 206/600 for p = 5 and
     815/1000 for p = 13. So it cannot be the route to S′ for T_195.
  4. **Exhaustive test over all shifted downsets** of size p·m (all g) in the ranges below, with
     0 violations [numerical: new implementation, `enum_shifted.py`]. This replaces the pass-9
     *random* shifted samples by complete enumeration at small sizes.
- No counterexample to S′ was found.

## 1. Lemma P (presentation of Γ by additive pairs) [own argument, unreviewed]

Let R = R(T, g) = { {g(x), g_i} : x ∈ T, x + e_i ∈ T } (unordered pairs in Z_m). Define

  A_R = ⟨ s_u (u ∈ Z_m) | s_0 = 0,  s_{a+b} = s_a + s_b for every {a, b} ∈ R ⟩.

**Claim.** Γ ≅ A_R. Under this isomorphism e_i ↦ s_{g_i}, the class of x ∈ T maps to s_{g(x)},
and ḡ: Γ → Z_m corresponds to s_u ↦ u.

*Proof.*
1. α: Z^k → A_R, e_i ↦ s_{g_i}. Let x ∈ T. Since T is a downset, there is a path
   0 = x_0, x_1, …, x_r = x in T with x_{t+1} = x_t + e_{i_t}. By induction on t,
   α(x_t) = s_{g(x_t)}: the step uses the relation for the pair {g(x_t), g_{i_t}} ∈ R, which gives
   s_{g(x_t) + g_{i_t}} = s_{g(x_t)} + s_{g_{i_t}}. So α(x) = s_{g(x)}. If x and y lie in one
   block, then g(x) = g(y), so α(x) = α(y). Hence M ⊂ ker α, and α induces ᾱ: Γ → A_R.
2. β: A_R → Γ, s_u ↦ [x] for any x ∈ T with g(x) = u.
   - Such an x exists because |T| = pm and every fibre has size p, so g(T) = Z_m.
   - [x] does not depend on the choice, because the fibre is one block.
   - β(s_0) = [0] = 0.
   - Each relation holds in Γ. Take {a, b} ∈ R with witness x, x + e_i ∈ T, g(x) = a and
     g_i = b. Then β(s_{a+b}) = [x + e_i] = [x] + [e_i] = β(s_a) + β(s_b), using e_i ∈ T.
3. β∘ᾱ(e_i) = β(s_{g_i}) = [e_i], and ᾱ∘β(s_u) = α(x) = s_{g(x)} = s_u. Both maps are the identity
   on generators. ∎

Consequences:
- Γ, and hence Γ_p, depends on (T, g) only through R.
- **S′ (case p ∤ m) is equivalent to the following.** Every function φ: Z_m → F_p with φ(0) = 0
  and φ(a + b) = φ(a) + φ(b) for all {a, b} ∈ R is the reduction mod p of some φ̃: Z_m → Z with
  the same property. Here φ = h∘(block), as in Lemma E.
- *Check.* For cex1 of pass 9, R ⊇ {{3,3}, {1,1}, {2,2}, {1,4}}, and these four relations already
  give A ≅ Z_10 (`small_m.py` prints `torsion: [10]`). This agrees with pass 9's SNF of M.

## 2. Special case: small m [Lemma P + numerical]

`python small_m.py 6 foreign` and `python small_m.py 6 pm` enumerate **every** set R of unordered
pairs in Z_m ∖ {0}. That is 2, 8, 64, 1024 and 32768 sets for m = 2…6. Each run computes the
Smith form of the relation matrix (sympy). Outputs are in `out/small_m.txt` and
`out/small_m_pm.txt`.

| m | primes q ∤ m dividing \|Tor A_R\| for some R | max_R v_q(exp Tor A_R) for q \| m | v_q(m) |
|---|---|---|---|
| 2 | none | 1 | 1 |
| 3 | none | 1 | 1 |
| 4 | none | 2 | 2 |
| 5 | **2, 3** (e.g. R = {{1,1}, {2,3}, {4,4}}: 2-torsion) | 1 | 1 |
| 6 | none | **2 (q = 2), 2 (q = 3)** | 1, 1 |

Since every R(T, g) is one of the enumerated sets, Lemma P gives the following.

**Corollary [Lemma P + numerical].** Lemma S, exp(Γ_p) ≤ p^{v_p(m)}, holds for every downset T and
every g with p-element fibres, in these cases:
- m ∈ {2, 3, 4}, any p;
- m = 5 or m = 6, any p ∉ {2, 3}.

The m = 5 entries are not counterexamples to S′ for shifted sets: an R with foreign torsion need
not come from a shifted (T, g). cex1 shows that one does come from a non-shifted downset. For
n = 195 this corollary says nothing, since m ∈ {15, 39, 65}.

## 3. Lemma C (cyclic-chain criterion) [own argument, unreviewed]

**Claim.** Suppose there is a unit b ∈ Z_m^× such that {tb, b} ∈ R for t = 1, …, m − 2. Then
A_R ≅ Z or A_R ≅ Z_m. In particular Γ has no p-torsion for p ∤ m.

*Proof.*
1. By induction on t, s_{(t+1)b} = s_{tb} + s_b gives s_{tb} = t·s_b for 0 ≤ t ≤ m − 1. Since b is
   a unit, every u ∈ Z_m equals t_u·b for a unique t_u ∈ {0, …, m − 1}. So A_R is cyclic,
   generated by s_b, and s_u = t_u s_b.
2. Every relation {a, c} ∈ R then reads (t_{a+c} − t_a − t_c)·s_b = 0. The coefficient lies in
   {0, −m}, because t_a + t_c < 2m and it is ≡ t_{a+c} mod m.
3. So A_R is Z/dZ with d ∈ {0, m}. ∎

[numerical: `python chain_crit.py p` on the pass-9 T_195 samples; output `out/chain_crit.txt`]

| p | samples where Lemma C applies |
|---|---|
| 3 | 0/400 |
| 5 | 206/600 |
| 13 | 815/1000 |

All of these samples have Γ_p = 0 anyway (pass 9). So Lemma C is far from sufficient. A proof of
S′ must use relations that wrap around Z_m with mixed steps, not a single chain.

## 4. Exhaustive shifted-downset test [numerical: `enum_shifted.py`, new implementation]

`enum_shifted.py` is written from the definitions and shares no code with pass 8 or 9.
- It enumerates **all** shifted downsets of size p·m, as order ideals of the multiset poset (lower
  covers x − e_j and x − e_j + e_{j−1}).
- It enumerates **all** g ∈ Z_m^k with every fibre of size p, with g_1 restricted to divisors of
  m (unit scaling preserves the fibres).
- It tests Γ_p = 0 via rank_{F_p}(M) = rank_Q(M), using exact Fraction arithmetic for rank_Q.
- Only p ∤ m is tested.

Self-tests (`python selftest.py`):
- The detector flags cex1: rank_F2 = 4 < rank_Q = 5.
- The enumeration counts (1, 1, 2, 3, 5, 8, 13 for sizes 1–7) match a brute force by single-point
  extension with a direct shiftedness check.

Results (`out/exh_shifted.txt`, `out/exh_shifted_b.txt`):

| p | m | \|T\| | shifted downsets | pairs (T, g) | violations |
|---|---|---|---|---|---|
| 2 | 3 | 6 | 8 | 33 | 0 |
| 3 | 2 | 6 | 8 | 23 | 0 |
| 2 | 5 | 10 | 50 | 10 116 | 0 |
| 5 | 2 | 10 | 50 | 431 | 0 |
| 3 | 4 | 12 | 119 | 97 221 | 0 |
| 7 | 2 | 14 | 279 | 7 074 | 0 |

- Outputs are in `out/exh_shifted_small.txt` (first four rows) and `out/exh_shifted.txt`.
- (p, m) = (2, 7), (5, 3) and (3, 5) were started and killed unfinished at the time limit; the g
  enumeration prunes weakly. (11, 2) did not finish within 200 s.
- These sizes overlap the pass-9 random shifted runs (2, 5) and (3, 4), and the pass-9 T_n
  exhaustive sweep (n ≤ 42). So this is a second, independent implementation and complete
  enumeration at small size, not new territory.
- Note from §2: every row with m ∈ {2, 3, 4} is already implied by the small-m corollary, which
  holds for all downsets. The only row with content beyond §2 is (p, m) = (2, 5). There arbitrary
  R can carry 2-torsion, and cex1 realizes such an R with a non-shifted downset. So that row is
  evidence that **shiftedness excludes cex1-type R at |T| = 10** (for every g, exhaustively).

## 5. The gap, exactly

- S′ for p ∤ m is the lifting statement of §1. It asks that every R-additive φ: Z_m → F_p lift
  to an R-additive φ̃: Z_m → Z, where R = R(T, g) comes from a shifted downset with p-to-1 g.
- What the counterexamples show:
  - Torsion arises from "halving" or "p-sectioning" relations: an s_a that occurs only in
    relations like s_{2a} = 2s_a (cex1: e4 occurs only through 2e4 ∼ e1).
  - Shiftedness adds the pairs {g_j, g_i} for all j < i whenever 2e_i ∈ T, and more generally
    {g(x − e_i + e_j), …}.
- I could not show that these extra pairs pin down every such s_a modulo p.
- The natural induction is on R, adding relations in some order with the torsion tracked by SNF.
  It needs an invariant that survives intermediate stages. The intermediate R's are arbitrary,
  and §2 shows that arbitrary R can carry foreign torsion (m = 5). So the invariant must use the
  shifted structure of the *final* R. I did not find one.
- For T_195 specifically: Lemma C fails on most p = 3 samples, so no single-chain argument works.

## 6. Reproduction

```
cd search/smooth-colouring/structure/pass10_shifted
python selftest.py
python small_m.py 6 foreign      # ~2 min
python small_m.py 6 pm
python chain_crit.py 3; python chain_crit.py 5; python chain_crit.py 13
python enum_shifted.py p m       # (p, m) as in §4
```
