"""Lemma S on random THRESHOLD downsets T = {x in N^k : w.x <= 1} (w random positive), the
class containing every T_n (w_q = log q / log n).  Same exhaustive-g test as ds_highdim.py.
Usage: python ds_threshold.py p m k trials seed"""
import sys, random, time, itertools
from lemS import gamma_p_exp, vp
from ds_highdim import all_g

def thr_downset(size, k, rng):
    while True:
        w = [rng.uniform(0.05, 1.0) for _ in range(k)]
        T = []
        def rec(i, x, s):
            if i == k:
                T.append(tuple(x)); return
            a = 0
            while s + a * w[i] <= 1 + 1e-12:
                rec(i + 1, x + [a], s + a * w[i]); a += 1
                if len(T) > size: return
        rec(0, [], 0.0)
        if len(T) == size and all(any(x[i] for x in T) for i in range(k)):
            return sorted(T), w

p, m, k, trials, seed = map(int, sys.argv[1:6])
rng = random.Random(seed)
tested = viol = 0; hist = {}; t0 = time.time()
for _ in range(trials):
    T, w = thr_downset(p * m, k, rng)
    for g in all_g(T, k, m, p):
        fib = {}
        for x in T:
            fib.setdefault(sum(a * b for a, b in zip(g, x)) % m, []).append(list(x))
        e, rq = gamma_p_exp(list(fib.values()), k, p)
        tested += 1; hist[e] = hist.get(e, 0) + 1
        if e > vp(m, p):
            viol += 1
            if viol <= 3: print("VIOLATION", e, "w=", [round(a, 4) for a in w], T, g, flush=True)
print(f"threshold p={p} m={m} k={k} downsets={trials} pairs={tested} hist={hist} bound={vp(m,p)} violations={viol} time={time.time()-t0:.1f}s")
