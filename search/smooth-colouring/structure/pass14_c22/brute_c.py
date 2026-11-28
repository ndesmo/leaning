"""brute_c.py -- naive independent count of (c_{x,y}) solutions (pass 14 count control).

Written straight from the definition in structure/pass13_mixed.md §2; shares no code with c22.rs.
Counts homomorphisms psi: Z^{pi(n)} -> G = Z_{p^x} x Z_{q^y} x Z_r (one value per prime <= n,
INCLUDING the large primes, enumerated explicitly) such that
  - every value of G is hit by at most `cap` elements of T = {1..n} (cap = 1: psi injective on T),
  - for every k, the multiset {(psi_p(a), psi_q(a)) : psi_r(a) = k} is `cap` copies of a coset of
    P = p^{x-1}Z_{p^x} x q^{y-1}Z_{q^y}   (checked at the leaf by explicit set comparison).
Pruning (all necessary conditions read off the definition): the multiplicity cap, the fibre size
n/r, and pairwise: two elements of T in the same Z_r-fibre have (p,q)-parts differing by an element
of P (they lie in one coset).  The pairwise test is done against every earlier element of the fibre.
Usage: python brute_c.py n p x q y r [cap]
"""
import sys
from itertools import product
from collections import Counter
from sympy import factorint, primerange

n, p, x, q, y, r = map(int, sys.argv[1:7])
cap = int(sys.argv[7]) if len(sys.argv) > 7 else 1
MP, MQ = p ** x, q ** y
PP = [(i * (p ** (x - 1)) % MP) for i in range(p)] if x >= 1 else [0]
PQ = [(j * (q ** (y - 1)) % MQ) for j in range(q)] if y >= 1 else [0]
PSUB = set(product(PP, PQ))
FIB = n // r
primes = list(primerange(2, n + 1))
fac = {a: factorint(a) for a in range(1, n + 1)}
# numbers grouped by largest prime factor
by_last = {l: [a for a in range(2, n + 1) if max(fac[a]) == l] for l in primes}
G = list(product(range(MP), range(MQ), range(r)))

psi = {}
val = {1: (0, 0, 0)}
mult = Counter({(0, 0, 0): 1})
fcnt = Counter({0: 1})
count = 0


def value(a):
    s0 = s1 = s2 = 0
    for l, e in fac[a].items():
        g = psi[l]
        s0 += e * g[0]; s1 += e * g[1]; s2 += e * g[2]
    return (s0 % MP, s1 % MQ, s2 % r)


def leaf_ok():
    for k in range(r):
        vals = Counter((v[0], v[1]) for v in val.values() if v[2] == k)
        if any(c != cap for c in vals.values()):
            return False
        d = list(vals)
        if len(d) != len(PSUB):
            return False
        u = d[0]
        if {((w[0] - u[0]) % MP, (w[1] - u[1]) % MQ) for w in d} != PSUB:
            return False
    return True


def rec(i):
    global count
    if i == len(primes):
        if len(val) == n and leaf_ok():
            count += 1
        return
    l = primes[i]
    for g in G:
        psi[l] = g
        added = []
        ok = True
        for a in by_last[l]:
            v = value(a)
            if mult[v] >= cap or fcnt[v[2]] >= FIB:
                ok = False
                break
            if any(w[2] == v[2] and ((v[0] - w[0]) % MP, (v[1] - w[1]) % MQ) not in PSUB for w in val.values()):
                ok = False
                break
            mult[v] += 1; fcnt[v[2]] += 1; val[a] = v; added.append(a)
        if ok:
            rec(i + 1)
        for a in added:
            v = val.pop(a); mult[v] -= 1; fcnt[v[2]] -= 1
    del psi[l]


rec(0)
print(f"BRUTE n={n} p={p} x={x} q={q} y={y} r={r} cap={cap} count={count}")
