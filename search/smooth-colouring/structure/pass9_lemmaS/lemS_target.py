"""Targeted search for Lemma S violations on T_n (p not dividing m = n/p).

Gamma_p != 0  <=>  dim_Fp {h: Z^k -> F_p linear, constant on blocks} > k - rank_Q M.
So every violation has a NONZERO block-constant h mod p.  This DFS assigns (h(q), g(q)) in
F_p x Z_m jointly to the non-singleton primes q (2q <= n), requiring every g-class to receive
<= p points, all with the same h-value, and h(q_first) = 1 for a chosen prime q_first (every
nonzero h is covered by some choice of q_first after scaling by F_p^*).  Singleton primes
(2q > n) fill holes and take the h-value of their class, so they impose nothing.
Each hit is then tested exactly (lemS.gamma_p_exp).

  python lemS_target.py exh  n p            exhaustive over all q_first
  python lemS_target.py rand n p N seed cap random-restart DFS, node cap per restart
"""
import sys, random, time, json
from lemS import Search, gamma_p_exp, vp


def run(S, p, first, rng, cap, cb):
    m = S.m
    order = S.ns
    cnt = [0] * m
    hv = [None] * m
    cnt[0] = 1
    hv[0] = 0          # the point 0 (the number 1) has h = 0
    g = [0] * S.k
    h = [0] * S.k
    nodes = [0]
    stop = [False]
    fi = order.index(first)

    def rec(t):
        if stop[0] or (cap and nodes[0] > cap):
            return
        nodes[0] += 1
        if t == len(order):
            if cb(g, h):
                stop[0] = True
            return
        i = order[t]
        hs = [1] if t == fi else list(range(p))
        cand = [(a, b) for b in hs for a in range(m)]
        if rng:
            rng.shuffle(cand)
        for a, b in cand:
            g[i], h[i] = a, b
            changed = []
            ok = True
            for x in S.pts_by[i]:
                r = sum(g[j] * x[j] for j in order[:t + 1]) % m
                hx = sum(h[j] * x[j] for j in order[:t + 1]) % p
                if hv[r] is not None and hv[r] != hx:
                    ok = False
                    break
                if cnt[r] >= p:
                    ok = False
                    break
                changed.append((r, hv[r]))
                cnt[r] += 1
                hv[r] = hx
            if ok:
                rec(t + 1)
            for r, old in reversed(changed):
                cnt[r] -= 1
                hv[r] = old
            if stop[0]:
                return
        g[i] = h[i] = 0
    rec(0)
    return nodes[0]


def main():
    mode, n, p = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    S = Search(n, p)
    assert S.m % p != 0
    hits = [0]
    viol = []
    hist = {}
    t0 = time.time()

    def cb(g, h):
        hits[0] += 1
        e, rq = gamma_p_exp(S.blocks_of(g), S.k, p)
        hist[e] = hist.get(e, 0) + 1
        if e > 0:
            viol.append({"g": S.full_g(g), "h_nonsingleton": list(h), "e": e})
            print("VIOLATION e=%d g=%s" % (e, S.full_g(g)), flush=True)
        return mode == 'rand'
    tot = 0
    if mode == 'exh':
        for q in S.ns:
            tot += run(S, p, q, None, None, cb)
    else:
        N, seed, cap = int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])
        rng = random.Random(seed)
        for _ in range(N):
            tot += run(S, p, rng.choice(S.ns), rng, cap, cb)
    print(f"{mode} n={n} p={p} m={S.m} nodes={tot} hits(g,h with h!=0 block-constant)={hits[0]} "
          f"hist={hist} violations={len(viol)} time={time.time()-t0:.1f}s", flush=True)
    if viol:
        json.dump({"n": n, "p": p, "primes": S.P, "samples": [v["g"] for v in viol], "viol": viol},
                  open(f"out/viol_{n}_{p}.json", "w"))


if __name__ == '__main__':
    main()
