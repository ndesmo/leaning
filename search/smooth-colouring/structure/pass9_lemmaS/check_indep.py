"""Independent checker (shares no code with lemS.py).

Input: JSON {"n":..., "p":..., "primes":[...], "samples":[[g(q) for q in primes], ...]}.
For each g: Z^k -> Z_{n/p} (given on the prime basis) it
  1. factors every x in 1..n with sympy.factorint,
  2. checks every residue class of Z_{n/p} receives exactly p of the numbers 1..n,
  3. builds M from ALL pairs x, y in a common class (no singleton reduction),
  4. computes the Smith normal form with sympy over ZZ and reports v_p of the largest
     p-power dividing a nonzero invariant factor (log_p exp(Gamma_p)).
Usage: python check_indep.py file.json [max_samples]
"""
import json, sys, itertools
from sympy import factorint, Matrix, ZZ, primerange
from sympy.matrices.normalforms import smith_normal_form

d = json.load(open(sys.argv[1]))
n, p = d["n"], d["p"]
lim = int(sys.argv[2]) if len(sys.argv) > 2 else 10 ** 9
primes = list(primerange(2, n + 1))
assert primes == d["primes"]
m = n // p
vec = {}
for x in range(1, n + 1):
    f = factorint(x)
    vec[x] = [f.get(q, 0) for q in primes]
bad = 0
hist = {}
ev = d.get("evals")
for idx, g in enumerate(d["samples"][:lim]):
    cls = {}
    for x in range(1, n + 1):
        cls.setdefault(sum(a * b for a, b in zip(g, vec[x])) % m, []).append(x)
    assert len(cls) == m and all(len(c) == p for c in cls.values()), "fibre sizes wrong"
    rows = []
    for c in cls.values():
        for x, y in itertools.combinations(c, 2):
            rows.append([a - b for a, b in zip(vec[x], vec[y])])
    S = smith_normal_form(Matrix(rows), domain=ZZ)
    diag = [abs(S[i, i]) for i in range(min(S.shape)) if S[i, i] != 0]
    e = 0
    for dd in diag:
        v = 0
        while dd % p == 0:
            dd //= p
            v += 1
        e = max(e, v)
    hist[e] = hist.get(e, 0) + 1
    if ev is not None and ev[idx] != e:
        bad += 1
        print("DISAGREE sample", idx, ev[idx], e)
print(f"n={n} p={p} checked={sum(hist.values())} log_p exp(Gamma_p) histogram={hist} "
      f"per-sample disagreements with lemS.py={bad if ev is not None else 'n/a'}")
