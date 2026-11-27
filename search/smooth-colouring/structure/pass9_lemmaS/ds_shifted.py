"""Lemma S on random SHIFTED downsets: x in T, i < j, x_j > 0  =>  x - e_j + e_i in T
(T_n is shifted with primes in increasing order).  Exhaustive over g as in ds_highdim.py.
Usage: python ds_shifted.py p m k trials seed"""
import sys, random
from lemS import gamma_p_exp, vp
from ds_highdim import all_g

def shifted_downset(size, k, rng):
    T = {tuple([0] * k)}
    def ok(y):
        for j in range(k):
            if y[j] == 0: continue
            z = list(y); z[j] -= 1
            if tuple(z) not in T: return False
            for i in range(j):
                z = list(y); z[j] -= 1; z[i] += 1
                if tuple(z) not in T: return False
        return True
    while len(T) < size:
        cand = set()
        for x in T:
            for i in range(k):
                y = list(x); y[i] += 1; y = tuple(y)
                if y not in T and ok(y): cand.add(y)
        T.add(rng.choice(sorted(cand)))
    return sorted(T)

p, m, k, trials, seed = map(int, sys.argv[1:6])
rng = random.Random(seed)
tested = viol = 0; ex = None
for _ in range(trials):
    T = shifted_downset(p * m, k, rng)
    used = [i for i in range(k) if any(x[i] for x in T)]
    T = [tuple(x[i] for i in used) for x in T]
    for g in all_g(T, len(used), m, p):
        fib = {}
        for x in T:
            fib.setdefault(sum(a * b for a, b in zip(g, x)) % m, []).append(list(x))
        e, _ = gamma_p_exp(list(fib.values()), len(used), p)
        tested += 1
        if e > vp(m, p):
            viol += 1
            if ex is None: ex = (T, g)
print(f"shifted p={p} m={m} k={k} downsets={trials} pairs={tested} violations={viol} example={ex}")
