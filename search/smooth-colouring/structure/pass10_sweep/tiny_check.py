"""Fresh checker written from the definition (no sympy, no code shared with lemS.py/lems.rs/check_indep.py).
T_n = exponent vectors of 1..n over the primes <= n; g given on primes; check every class of Z_m (m=n/p)
has exactly p elements; M = Z-span of x-y over same-class pairs.  Reports rank_Q(M) (exact Fractions),
rank_{F_p}(M), and, if M has full rank, the index [Z^k : M] via Euclidean integer row reduction (HNF).
Gamma_p != 0  <=>  rank_Fp(M) < rank_Q(M).
Usage: python tiny_check.py file.json   (keys n, p, g  or  n, p, samples)"""
import json, sys
from fractions import Fraction
def fac(x, P):
    v = []
    for q in P:
        e = 0
        while x % q == 0: x //= q; e += 1
        v.append(e)
    assert x == 1
    return v
def rank(rows, mod=None):
    A = [[(Fraction(a) if mod is None else a % mod) for a in r] for r in rows]
    r = 0
    for c in range(len(A[0]) if A else 0):
        piv = next((i for i in range(r, len(A)) if A[i][c] != 0), None)
        if piv is None: continue
        A[r], A[piv] = A[piv], A[r]
        inv = (1 / A[r][c]) if mod is None else pow(A[r][c], -1, mod)
        for i in range(len(A)):
            if i != r and A[i][c] != 0:
                f = A[i][c] * inv
                A[i] = [(a - f * b) if mod is None else (a - f * b) % mod for a, b in zip(A[i], A[r])]
        r += 1
    return r
def index_full(rows, k):
    A = [r[:] for r in rows]; d = 1
    for c in range(k):
        while True:
            nz = [i for i in range(c, len(A)) if A[i][c] != 0]
            if not nz: return None
            i0 = min(nz, key=lambda i: abs(A[i][c]))
            A[c], A[i0] = A[i0], A[c]
            done = True
            for i in range(c + 1, len(A)):
                q = A[i][c] // A[c][c]
                if q: A[i] = [a - q * b for a, b in zip(A[i], A[c])]
                if A[i][c] != 0: done = False
            if done: break
        d *= abs(A[c][c])
    return d
def check(n, p, g):
    P = [q for q in range(2, n + 1) if all(q % d for d in range(2, q))]
    m = n // p
    V = {x: fac(x, P) for x in range(1, n + 1)}
    cls = {}
    for x in range(1, n + 1): cls.setdefault(sum(a * b for a, b in zip(g, V[x])) % m, []).append(x)
    assert sorted(cls) == list(range(m)) and all(len(c) == p for c in cls.values())
    rows = [[a - b for a, b in zip(V[x], V[c[0]])] for c in cls.values() for x in c[1:]]
    rq, rp = rank(rows), rank(rows, p)
    idx = index_full(rows, len(P)) if rq == len(P) else None
    return rq, rp, idx, cls
if __name__ == "__main__":
    d = json.load(open(sys.argv[1]))
    gs = [d["g"]] if "g" in d else d["samples"]
    for g in gs:
        rq, rp, idx, cls = check(d["n"], d["p"], g)
        print(f"rank_Q={rq} rank_F{d['p']}={rp} index={idx} Gamma_{d['p']}{'!=0' if rp < rq else '=0'}")
    if "g" in d: print("blocks:", sorted(cls.values()))
