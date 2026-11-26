# Pass 3: the Pure-type question has answer NO (explicit mixed character)

Question (pass2.md §4): is every completely multiplicative χ: [195] → 𝕋 with
S_k := Σ_{m≤195} χ(m)^k = 0 for all k coprime to 195 of pure type, i.e. is at most one of
A_3 = S_3, A_5 = S_5, A_13 = S_13 nonzero?

**Answer: no.** [computer-verified certificate, exact arithmetic] The file
`cert_N195_1_2_14.json` gives χ(p) = e(w_p/195). For it, S_k = 0 for every k coprime to 195. It
also has **A_3 = 3, A_5 = 10 and A_13 = 182, so all three are nonzero.**

## Reduction to a single vanishing sum (N a {3,5,13}-number) [own, standard]
If χ takes values in μ_N with N = 3^a 5^b 13^c, then the residues k mod N that contain an integer
coprime to 195 are exactly the units of Z_N. So S_k for these k are the Galois conjugates of S_1,
and the condition is just S_1 = 0. The checker tests all 96 units anyway.

## The certificate, by hand
Write Z_195 = Z_3 × Z_5 × Z_13 (CRT). The weights are:
- The Z_13-component ψ(m) = φ(m) mod 13 of φ(m) = Σ v_p(m) w_p carries almost everything:
  - w_2 ≡ 0.
  - All primes ≤ 67, together with 73, 79, 83, 89, 97, 103, 127, 131, 137, 139 and 167–193,
    have weights in 15Z_195 (pure Z_13).
- Ten points are moved off the Z_13-axis, into Z_3 × Z_5 × {0}:
  - 113 ↦ (1,0,0) and 101 ↦ (2,0,0). With m = 1 at 0, this makes one 3-gon.
  - 157, 163 ↦ (0,1,0); 107, 109 ↦ (0,2,0); 149, 151 ↦ (0,3,0); 71 and 142 = 2·71 ↦ (0,4,0).
    With two more points at 0, this makes two 5-gons.
- The resulting distribution is 14 points on each of the 13 points of {0}×{0}×Z_13, which is
  14 thirteen-gons (182 points). On top of that come one 3-gon and two 5-gons:
  3·1 + 5·2 + 13·14 = 195.
- So S_1 = 0. Under x ↦ 3x the 3-gon collapses to 3 copies of one point, and the 5- and 13-gons
  stay polygons, so A_3 = 3. In the same way A_5 = 5·2 = 10 and A_13 = 13·14 = 182.

The mechanism is general. The primes in (97,195] occur once each, and those in (65,97] occur as
r and 2r. They can be placed almost freely, so any small excess of a pure configuration can be
redistributed into polygons of the other primes. Multiplicativity is no obstruction here.

## Non-root-of-unity characters [own argument, unreviewed]
For a mixed example, roots of unity are WLOG. Let Γ = ⟨χ(p)⟩ ≅ μ_M × Z^r, with free generators
u_1..u_r, and write χ(m) = ζ^{f(m)} u^{n(m)}.
- For each residue ρ of k mod M, the Laurent polynomial Q_ρ(x) = Σ_m ζ^{ρ f(m)} x^{n(m)} vanishes
  on {u^k : k ≡ ρ, gcd(k,195) = 1}. That set is an arithmetic progression of powers of u. Its
  Zariski closure is the whole torus, since the u_i are multiplicatively independent.
- So Q_ρ ≡ 0, and every fibre class {m : n(m) = n} has a vanishing root-of-unity sum.
- Now specialise u to a root of unity of large prime order L coprime to M, along a linear map
  Z^r → Z_L that is injective on the finitely many n(m). This preserves the vanishing.
- It also preserves each A_p ≠ 0, because the cyclotomic fields are linearly disjoint.
- For the converse question ("yes"), general χ would matter. But the answer is no, so this is moot.

## What this does and does not show
- It shows the step "condition (ii) plus multiplicativity ⇒ A_pA_q = 0", which is WW §4.3's key
  consequence, **fails for 195**, even at N = 195 and even with all three A_p nonzero. Mechanism O1
  of pass2.md is realised by an actual character of T_195.
- It does **not** show that 195 is or is not satisfactory.
- It does not rule out that σ_f̃-a.e. characters satisfy extra constraints beyond (ii), for example
  from (iii), from the Frobenius congruences (iv), or from positivity of the measure, that exclude
  this χ. Only per-character condition (ii) was tested. A rescue of the spectral route would need
  such an extra input.

## Reproduction
- `python puretype_check.py cert_N195_1_2_14.json` takes a few seconds. It uses sympy: each
  polynomial Σ x^{kφ(m)} is reduced mod Φ_195, plus a float cross-check (max |S_k| ≈ 5e-12).
- `python puretype_search.py 1 2 14` uses OR-tools CP-SAT with 16 workers and takes about 280 s.
  It searches w ∈ Z_195^44 with the φ-multiset equal to a union of a 3-gons, b 5-gons and c 13-gons.
- An attempt at (a,b,c) = (2,17,8) timed out at 300 s (UNKNOWN). It was not pursued, since one
  mixed example suffices.
