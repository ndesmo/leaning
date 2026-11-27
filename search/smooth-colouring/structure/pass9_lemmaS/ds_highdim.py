"""Lemma S on random downsets of N^k for k up to 8 (pass 8 only did k = 2, 3).

For each random downset T of size p*m and EVERY homomorphism g: Z^k -> Z_m with all fibres on
T of size p (exhaustive DFS over (g(e_1),...,g(e_k)) in Z_m^k), compute log_p exp(Gamma_p)
and compare with v_p(m).  Also records rank deficiency (Gamma infinite).
Usage: python ds_highdim.py p m k trials seed
"""
import sys, random, time
from lemS import gamma_p_exp, vp


def random_downset(size, k, rng):
    T = {tuple([0] * k)}
    while len(T) < size:
        # addable: y not in T with all y - e_i (y_i > 0) in T
        cand = set()
        for x in T:
            for i in range(k):
                y = list(x)
                y[i] += 1
                y = tuple(y)
                if y in T:
                    continue
                if all(y[j] == 0 or tuple(y[t] - (t == j) for t in range(k)) in T for j in range(k)):
                    cand.add(y)
        T.add(rng.choice(sorted(cand)))
    return sorted(T)


def all_g(T, k, m, p):
    # DFS over coordinates; a point is decided once all its nonzero coordinates are assigned
    order = list(range(k))
    last = {}
    for x in T:
        nz = [i for i in order if x[i]]
        last.setdefault(max(nz) if nz else -1, []).append(x)
    cnt = [0] * m
    for x in last.get(-1, []):
        cnt[0] += 1
    g = [0] * k
    out = []

    def rec(i):
        if i == k:
            out.append(list(g))
            return
        for a in range(m):
            g[i] = a
            add = []
            ok = True
            for x in last.get(i, []):
                r = sum(g[j] * x[j] for j in range(i + 1)) % m
                cnt[r] += 1
                add.append(r)
                if cnt[r] > p:
                    ok = False
                    break
            if ok:
                rec(i + 1)
            for r in add:
                cnt[r] -= 1
    if cnt[0] <= p:
        rec(0)
    return out


def main():
    p, m, k, trials, seed = map(int, sys.argv[1:6])
    rng = random.Random(seed)
    tested = viol = 0
    hist = {}
    t0 = time.time()
    for _ in range(trials):
        T = random_downset(p * m, k, rng)
        used = [i for i in range(k) if any(x[i] for x in T)]
        T = [tuple(x[i] for i in used) for x in T]
        kk = len(used)
        for g in all_g(T, kk, m, p):
            fib = {}
            for x in T:
                fib.setdefault(sum(a * b for a, b in zip(g, x)) % m, []).append(list(x))
            e, rq = gamma_p_exp(list(fib.values()), kk, p)
            tested += 1
            hist[e] = hist.get(e, 0) + 1
            if e > vp(m, p):
                viol += 1
                print("VIOLATION", e, T, g, flush=True)
    print(f"p={p} m={m} k<={k} downsets={trials} pairs(T,g)={tested} hist={hist} bound={vp(m,p)} "
          f"violations={viol} time={time.time()-t0:.1f}s")


if __name__ == '__main__':
    main()
