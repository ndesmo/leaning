"""Independent checker for a pure-type counterexample certificate.

Certificate: N and weights w_p (p prime <= 195).  chi(p) = exp(2 pi i w_p / N), extended
completely multiplicatively to [195].  Since chi^N = 1, the sums S_k = sum_{m<=195} chi(m)^k
depend only on k mod N.  We check, in exact arithmetic (polynomial reduction modulo the
cyclotomic polynomial Phi_N, so a sum of N-th roots of unity is 0 iff the reduced polynomial is 0):
  * S_k = 0 for every k in [1, N] with gcd(k, 195) = 1  (this is every k coprime to 195, mod N);
  * which of A_3 = S_3, A_5 = S_5, A_13 = S_13 are nonzero.
Also prints the float values as a sanity cross-check.  Written from the definitions only.

usage: python puretype_check.py cert.json
"""
import sys, json, cmath
from math import gcd
from sympy import cyclotomic_poly, Poly, symbols, factorint

X = symbols("x")
cert = json.load(open(sys.argv[1]))
N = cert["N"]
w = {int(p): int(v) % N for p, v in cert["w"].items()}

def phi(m):
    s = 0
    for p, e in factorint(m).items():
        s += e * w[p]
    return s % N

ph = [phi(m) for m in range(1, 196)]
assert len(w) == 44 and all(p in w for p in range(2, 196) if len(factorint(p)) == 1 and factorint(p).get(p) == 1)
Phi = Poly(cyclotomic_poly(N, X), X)

def S_exact_zero(k):
    coeff = [0] * N
    for t in ph:
        coeff[(k * t) % N] += 1
    P = Poly(list(reversed(coeff)), X)
    r = P.rem(Phi)
    return r.is_zero

def S_float(k):
    return sum(cmath.exp(2j * cmath.pi * k * t / N) for t in ph)

bad = [k for k in range(1, N + 1) if gcd(k, 195) == 1 and not S_exact_zero(k)]
print("N =", N)
print("k coprime to 195 with S_k != 0:", bad)
print("max |S_k| (float) over coprime k:", max(abs(S_float(k)) for k in range(1, N + 1) if gcd(k, 195) == 1))
for p in (3, 5, 13):
    print(f"A_{p}: exact zero = {S_exact_zero(p)}, float = {S_float(p):.6f}")
nz = [p for p in (3, 5, 13) if not S_exact_zero(p)]
print("VALID (all coprime moments vanish):", not bad)
print("nonzero A_p for p in", nz, "->", "MIXED" if len(nz) >= 2 else "pure")
