"""Lemma S on random downsets, split by whether T is midpoint-convex
(x, y in T, x + y in 2Z^k  =>  (x + y)/2 in T; every threshold downset, hence every T_n, is).
Usage: python ds_convex.py p m k trials seed"""
import sys, random, itertools
from lemS import gamma_p_exp, vp
from ds_highdim import random_downset, all_g

def midconvex(T):
    S = set(T)
    for x, y in itertools.combinations(T, 2):
        if all((a + b) % 2 == 0 for a, b in zip(x, y)) and tuple((a + b) // 2 for a, b in zip(x, y)) not in S:
            return False
    return True

p, m, k, trials, seed = map(int, sys.argv[1:6])
rng = random.Random(seed)
res = {True: [0, 0, 0], False: [0, 0, 0]}  # downsets, pairs, violations
ex = None
for _ in range(trials):
    T = random_downset(p * m, k, rng)
    used = [i for i in range(k) if any(x[i] for x in T)]
    T = [tuple(x[i] for i in used) for x in T]
    c = midconvex(T)
    res[c][0] += 1
    for g in all_g(T, len(used), m, p):
        fib = {}
        for x in T:
            fib.setdefault(sum(a * b for a, b in zip(g, x)) % m, []).append(list(x))
        e, _ = gamma_p_exp(list(fib.values()), len(used), p)
        res[c][1] += 1
        if e > vp(m, p):
            res[c][2] += 1
            if c and ex is None: ex = (T, g)
print(f"p={p} m={m} k={k}: midpoint-convex [downsets,pairs,viol]={res[True]}  non-convex={res[False]}  example(convex viol)={ex}")
