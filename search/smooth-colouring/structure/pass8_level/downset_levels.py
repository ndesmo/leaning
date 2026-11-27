r"""pass 8: minimal level of (b_i^p) for abstract downsets T in N^k (k = 2, 3).

Abstract version of (b_i^p) (composite_B.md): T subset Z^k finite, |T| = p*m.
Level i holds iff there are homomorphisms F: Z^k -> Z_{p^{i+1}}, g: Z^k -> Z_m with
   (P) x != y in T, g(x) = g(y)  =>  F(x - y) in p^i Z_{p^{i+1}} \ {0}.
Level 0 means F: Z^k -> Z_p, i.e. (F,g) bijective T -> Z_p x Z_m (only "a" if p ∤ m).
Brute force over all g (m^k) and all F (p^{(i+1)k}).  Downsets of N^k of size s are
enumerated exactly (k = 2: partitions; k = 3: plane partitions), so every order ideal is tested.

Usage: python downset_levels.py k smax maxlevel [p1,p2,..] [smin] [minlevel_start: 1 (default) or 0]
Prints, for each (T, p) with level-1 NONE but some level <= maxlevel EXISTS, the minimal level
and whether p | m.  Summary at the end.
"""
import itertools, sys
import numpy as np


def partitions(s, maxpart=None):
    if maxpart is None:
        maxpart = s
    if s == 0:
        yield ()
        return
    for a in range(min(s, maxpart), 0, -1):
        for rest in partitions(s - a, a):
            yield (a,) + rest


def downsets2(s):
    for lam in partitions(s):
        yield [(i, j) for i, a in enumerate(lam) for j in range(a)]


def plane_partitions(s):
    # rows of a plane partition: a sequence of partitions, each contained in the previous
    def rec(rem, prev):
        if rem == 0:
            yield []
            return
        for t in range(rem, 0, -1):
            for lam in partitions(t):
                if prev is not None and (len(lam) > len(prev) or any(lam[q] > prev[q] for q in range(len(lam)))):
                    continue
                for rest in rec(rem - t, lam):
                    yield [lam] + rest
    yield from rec(s, None)


def downsets3(s):
    for pp in plane_partitions(s):
        yield [(i, j, l) for i, lam in enumerate(pp) for j, a in enumerate(lam) for l in range(a)]


def blocks_for(T, g, m):
    fib = {}
    for x in T:
        v = sum(a * b for a, b in zip(g, x)) % m
        fib.setdefault(v, []).append(x)
    return fib


def level_ok(T, p, m, i, k, gcache):
    q = p ** (i + 1)
    Fs = np.array(list(itertools.product(range(q), repeat=k)), dtype=np.int64)
    for g, fib in gcache:
        if any(len(b) != p for b in fib.values()):
            continue
        D = []
        for b in fib.values():
            for x, y in itertools.combinations(b, 2):
                D.append([a - c for a, c in zip(x, y)])
        D = np.array(D, dtype=np.int64)
        V = (Fs @ D.T) % q
        good = np.all((V % (q // p) == 0) & (V != 0), axis=1)
        if good.any():
            return True, (g, tuple(Fs[np.argmax(good)]))
    return False, None


def main():
    k, smax, maxlev = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    plist = [int(a) for a in sys.argv[4].split(',')] if len(sys.argv) > 4 else [2, 3, 5, 7]
    smin = int(sys.argv[5]) if len(sys.argv) > 5 else 2
    global LEV0
    LEV0 = int(sys.argv[6]) if len(sys.argv) > 6 else 1
    gen = downsets2 if k == 2 else downsets3
    stats = {}
    for s in range(smin, smax + 1):
        for p in plist:
            if s % p:
                continue
            m = s // p
            for T in gen(s):
                gcache = [(g, blocks_for(T, g, m)) for g in itertools.product(range(m), repeat=k)]
                res = None
                for i in range(LEV0, maxlev + 1):
                    ok, w = level_ok(T, p, m, i, k, gcache)
                    if ok:
                        res = i
                        break
                key = (p, m % p == 0)
                st = stats.setdefault(key, {})
                st[res] = st.get(res, 0) + 1
                if res is None or res >= max(2, LEV0 + 1) or (LEV0 == 0 and res == 1):
                    print(f"s={s} p={p} m={m} p|m={m % p == 0} minlevel={res} T={T} wit={w if res else None}", flush=True)
    print("SUMMARY (p, p|m): {minlevel: count}  (None = no level <= maxlevel)")
    for key in sorted(stats):
        print(key, dict(sorted(stats[key].items(), key=lambda t: (t[0] is None, t[0] or 0))))


if __name__ == "__main__":
    main()
