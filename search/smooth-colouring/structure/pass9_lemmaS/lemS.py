"""pass 9: test Lemma S on T_n directly.

Lemma S: T downset, |T| = p*m, g: Z^k -> Z_m homomorphism with every fibre on T of size p,
M = <x - y : x, y in T, g(x) = g(y)>, Gamma = Z^k / M.  Claim exp(Gamma_p) <= p^{v_p(m)}.

Here T = T_n = exponent vectors of 1..n (k = #primes <= n).  g is given by its values on the
prime basis vectors.  Primes q with 2q > n ("singletons") occur in exactly one point e_q; their
values only fill holes and (Lemma R in pass9_lemmaS.md) do not affect the torsion of Gamma, so
the DFS assigns only non-singleton primes and requires the residue counts to be <= p with total
deficit = #singletons.

Modes:
  python lemS.py exh  n p [maxsol|0] [out.json]    exhaustive DFS over non-singleton prime values
                                         (g(2) restricted to divisors of m: unit symmetry)
  python lemS.py rand n p N seed [out]  N random-restart randomized DFS samples
Torsion: exact rank over Q (Bareiss) vs SNF over Z/p^E (E = 12); rigorous when the number of
pivots mod p^E equals rank_Q (asserted).
"""
import sys, random, json, time


def primes_upto(n):
    s = [True] * (n + 1)
    s[0] = s[1] = False
    for i in range(2, int(n ** .5) + 1):
        if s[i]:
            for j in range(i * i, n + 1, i):
                s[j] = False
    return [i for i in range(n + 1) if s[i]]


def Tn(n):
    P = primes_upto(n)
    T = []
    for x in range(1, n + 1):
        v, y = [], x
        for q in P:
            e = 0
            while y % q == 0:
                y //= q
                e += 1
            v.append(e)
        T.append(v)
    return P, T


def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def rank_Q(rows, k):
    A = [r[:] for r in rows if any(r)]
    rk, prev = 0, 1
    col = 0
    nrow = len(A)
    for col in range(k):
        piv = None
        for i in range(rk, nrow):
            if A[i][col] != 0:
                piv = i
                break
        if piv is None:
            continue
        A[rk], A[piv] = A[piv], A[rk]
        a = A[rk][col]
        for i in range(rk + 1, nrow):
            b = A[i][col]
            Ai = A[i]
            Ar = A[rk]
            A[i] = [(a * Ai[j] - b * Ar[j]) // prev for j in range(k)]
        prev = a
        rk += 1
    return rk


def snf_local(rows, k, p, E=12):
    """valuations of nonzero elementary divisors of the row lattice, over Z/p^E"""
    Q = p ** E
    A = [[x % Q for x in r] for r in rows]
    A = [r for r in A if any(r)]
    vals = []
    cols = list(range(k))
    while A:
        best = None
        for i, r in enumerate(A):
            for j in cols:
                if r[j]:
                    v = vp(r[j], p)
                    if best is None or v < best[0]:
                        best = (v, i, j)
                        if v == 0:
                            break
            if best and best[0] == 0:
                break
        if best is None:
            break
        v, i, j = best
        vals.append(v)
        r = A.pop(i)
        u = r[j] // p ** v
        uinv = pow(u, -1, Q)
        newA = []
        for s in A:
            if s[j]:
                c = (s[j] // p ** v) * uinv % Q  # s[j] divisible by p^v since v minimal
                s = [(s[t] - c * r[t]) % Q for t in range(k)]
            if any(s):
                newA.append(s)
        A = newA
        cols.remove(j)
        # column ops are implicit: column j is now zero in all remaining rows; other
        # columns of r are irrelevant because column operations can clear them (r[j] has
        # minimal valuation among all entries).
    return vals


def gamma_p_exp(blocks, k, p):
    rows = []
    for b in blocks:
        for y in b[1:]:
            rows.append([a - c for a, c in zip(y, b[0])])
    if not rows:
        return 0, 0
    rq = rank_Q(rows, k)
    vals = snf_local(rows, k, p)
    assert len(vals) == rq, (len(vals), rq)
    return max(vals), rq


class Search:
    def __init__(self, n, p):
        self.n, self.p = n, p
        assert n % p == 0
        self.m = n // p
        P, T = Tn(n)
        self.P, self.T, self.k = P, T, len(P)
        self.sing = [i for i, q in enumerate(P) if 2 * q > n]
        self.ns = [i for i, q in enumerate(P) if 2 * q <= n]
        # points grouped by largest non-singleton prime index (singleton points excluded)
        self.pts_by = {i: [] for i in self.ns}
        self.zero_pts = []
        for x in T:
            if any(x[i] for i in self.sing):
                continue
            idx = [i for i in self.ns if x[i]]
            if not idx:
                self.zero_pts.append(x)
            else:
                self.pts_by[max(idx)].append(x)

    def blocks_of(self, gv):
        m = self.m
        fib = {}
        for x in self.T:
            if any(x[i] for i in self.sing):
                continue
            r = sum(gv[i] * x[i] for i in self.ns) % m
            fib.setdefault(r, []).append(x)
        # singleton reduction: only the non-singleton members of each class matter
        return list(fib.values())

    def full_g(self, gv):
        """assign singleton primes to holes (arbitrary order) -> full g on all primes"""
        m, p = self.m, self.p
        cnt = [0] * m
        for x in self.T:
            if any(x[i] for i in self.sing):
                continue
            cnt[sum(gv[i] * x[i] for i in self.ns) % m] += 1
        holes = [r for r in range(m) for _ in range(p - cnt[r])]
        g = list(gv)
        for i, r in zip(self.sing, holes):
            g[i] = r
        return g

    def dfs(self, rng=None, maxsol=None, cb=None, sym=True):
        m, p = self.m, self.p
        cnt = [0] * m
        cnt[0] = len(self.zero_pts)
        gv = [0] * self.k
        nsing = len(self.sing)
        order = self.ns
        divs = [d for d in range(m) if d == 0 or m % d == 0] if sym else list(range(m))
        nodes = [0]
        found = [0]
        # remaining non-singleton points after index t
        remaining = [0] * (len(order) + 1)
        for t in range(len(order) - 1, -1, -1):
            remaining[t] = remaining[t + 1] + len(self.pts_by[order[t]])
        stop = [False]

        def rec(t):
            if stop[0]:
                return
            nodes[0] += 1
            if t == len(order):
                found[0] += 1
                if cb(gv):
                    stop[0] = True
                if maxsol and found[0] >= maxsol:
                    stop[0] = True
                return
            i = order[t]
            cand = divs if (t == 0) else range(m)
            cand = list(cand)
            if rng:
                rng.shuffle(cand)
            pts = self.pts_by[i]
            for a in cand:
                gv[i] = a
                added = []
                ok = True
                for x in pts:
                    r = sum(gv[j] * x[j] for j in order[:t + 1]) % m
                    cnt[r] += 1
                    added.append(r)
                    if cnt[r] > p:
                        ok = False
                        break
                if ok:
                    rec(t + 1)
                for r in added:
                    cnt[r] -= 1
                if stop[0]:
                    return
                if rng and nodes[0] > self.node_cap:
                    return
            gv[i] = 0

        self.node_cap = 10 ** 18
        rec(0)
        return nodes[0], found[0]


def main():
    mode = sys.argv[1]
    n, p = int(sys.argv[2]), int(sys.argv[3])
    S = Search(n, p)
    bound = vp(S.m, p)
    stats = {}
    viol = []
    t0 = time.time()

    dump = []

    def check(gv):
        e, rq = gamma_p_exp(S.blocks_of(gv), S.k, p)
        dump.append((S.full_g(gv), e))
        stats[e] = stats.get(e, 0) + 1
        if e > bound:
            viol.append(S.full_g(gv))
            print("VIOLATION", e, S.full_g(gv), flush=True)
            return True
        return False

    if mode == 'exh':
        maxsol = int(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] != '0' else None
        nodes, found = S.dfs(cb=check, maxsol=maxsol)
        if len(sys.argv) > 5:
            json.dump({"n": n, "p": p, "primes": S.P, "samples": [g for g, _ in dump], "evals": [e for _, e in dump],
                       "hist": {str(a): b for a, b in stats.items()}}, open(sys.argv[5], "w"))
        print(f"n={n} p={p} m={S.m} k={S.k} singletons={len(S.sing)} exhaustive nodes={nodes} "
              f"solutions={found} exp_p-valuation histogram={stats} bound={bound} "
              f"violations={len(viol)} time={time.time()-t0:.1f}s")
    else:
        N, seed = int(sys.argv[4]), int(sys.argv[5])
        out = sys.argv[6] if len(sys.argv) > 6 else None
        rng = random.Random(seed)
        samples = []
        evals = []
        tot = 0
        for it in range(N):
            got = []

            def cb(gv):
                got.append(list(gv))
                return True
            S.node_cap = 200000
            nodes, f = S.dfs(rng=rng, cb=cb, sym=False)
            tot += nodes
            if got:
                g = got[0]
                samples.append(S.full_g(g))
                check(g)
                evals.append(dump[-1][1])
        print(f"n={n} p={p} m={S.m} random restarts={N} samples={len(samples)} nodes={tot} "
              f"histogram={stats} bound={bound} violations={len(viol)} time={time.time()-t0:.1f}s")
        if out:
            json.dump({"n": n, "p": p, "primes": S.P, "samples": samples, "evals": evals, "violations": viol},
                      open(out, "w"))


if __name__ == '__main__':
    main()
