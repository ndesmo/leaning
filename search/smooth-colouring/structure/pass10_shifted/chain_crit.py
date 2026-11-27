"""Pass 10: how often does the cyclic-chain criterion (Lemma C of pass10_shifted.md) certify
Gamma_p = 0 on the pass-9 T_195 samples?  Criterion: some unit b of Z_m with {tb, b} in R for
t = 1..m-2, where R = {{g(x), g(q)} : x, x+e_q in T_n}.  Usage: python chain_crit.py p"""
import json, sys
from math import gcd
p = sys.argv[1]
d = json.load(open(f"../pass9_lemmaS/out/rand195_p{p}.json"))
n = int(d["n"]); P = d["primes"]; m = n // int(p)
def vec(j):
    v = []
    for q in P:
        e = 0
        while j % q == 0: j //= q; e += 1
        v.append(e)
    return v
V = [vec(j) for j in range(1, n + 1)]
ok = 0
for g in d["samples"]:
    gv = [sum(a * b for a, b in zip(g, v)) % m for v in V]
    R = set()
    for j in range(1, n + 1):
        for qi, q in enumerate(P):
            if j * q <= n:
                a, b = gv[j - 1], g[qi]; R.add((min(a, b), max(a, b)))
    hit = any(all((min(t*b % m, b), max(t*b % m, b)) in R for t in range(1, m - 1))
              for b in range(1, m) if gcd(b, m) == 1)
    ok += hit
print(f"p={p} m={m} samples={len(d['samples'])} chain-criterion holds in {ok}")
