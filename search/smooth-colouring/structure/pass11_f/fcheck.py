"""Admissible-f / minimal-level test (pass 11).

For a map g on the primes <= n (values mod m = n/p) whose fibres on T_n all have size p, and for
prescribed f-values on generators of M, decide for each level i = 0..L whether there is
F: Z^k -> Z_{p^{i+1}} with F(d) = p^i * b_d (mod p^{i+1}) for every generator d of M
(Prop. 1 of pass8_level.md: this is exactly "f extends at level i").

Generators: for each block {x_0 < ... < x_{p-1}} (sorted by integer), d_j = x_j - x_0.
For p = 2 the admissible f is unique: b_d = 1 for every block difference.
For p > 2 the f-values must be supplied (here: read off a known witness F).

Method: Smith form of D (rows = generators) over Z/p^a with row transform U (own code, no sympy).
Output per level: either an explicit F (checked: F(d) == p^i b_d mod p^{i+1}) or a certificate
c in Z^{#gens} with c.D == 0 (mod p^{i+1}) componentwise and c.b != 0 (mod p), which proves
no level-i F exists (if F existed, 0 == F(c.D) == p^i c.b mod p^{i+1}).

Usage:
  python fcheck.py ck  <exh_n_p.ck> [min_e] [L]   all S-lines with e >= min_e (p = 2 only)
  python fcheck.py w176 <w_N_2_LL.json> [L]        sanity: witness phi -> (F,g), p = 2
  python fcheck.py w162 <w162_hd81_gtile7.txt> [L] sanity: witness, p = 3, f from witness F
"""
import json, sys


def primes_upto(n):
    return [q for q in range(2, n + 1) if all(q % r for r in range(2, int(q ** .5) + 1))]


def expvec(x, P):
    v = []
    for q in P:
        e = 0
        while x % q == 0:
            x //= q; e += 1
        v.append(e)
    assert x == 1
    return v


def blocks_of(n, p, P, g, m):
    cls = {}
    for x in range(1, n + 1):
        v = expvec(x, P)
        cls.setdefault(sum(a * b for a, b in zip(v, g)) % m, []).append(x)
    assert len(cls) == m and all(len(B) == p for B in cls.values()), "fibres not all of size p"
    return [sorted(B) for _, B in sorted(cls.items())]


def solve_mod(D, b, mod, p):
    """Solve D x == b (mod mod), mod = p^a. Returns ('F', x) or ('C', c)."""
    R, K = len(D), len(D[0])
    A = [[a % mod for a in r] for r in D]
    U = [[int(i == j) for j in range(R)] for i in range(R)]
    V = [[int(i == j) for j in range(K)] for i in range(K)]

    def val(a):
        if a % mod == 0:
            return 10 ** 9
        v = 0
        while a % p == 0:
            a //= p; v += 1
        return v
    r = 0
    while r < min(R, K):
        best = None
        for i in range(r, R):
            for j in range(r, K):
                if A[i][j] % mod:
                    vv = val(A[i][j])
                    if best is None or vv < best[0]:
                        best = (vv, i, j)
        if best is None:
            break
        _, i, j = best
        A[r], A[i] = A[i], A[r]; U[r], U[i] = U[i], U[r]
        for row in A:
            row[r], row[j] = row[j], row[r]
        for row in V:
            row[r], row[j] = row[j], row[r]
        s = A[r][r]; vs = val(s); u = s // p ** vs; uinv = pow(u, -1, mod)
        # scale pivot row so pivot = p^vs
        A[r] = [(a * uinv) % mod for a in A[r]]; U[r] = [(a * uinv) % mod for a in U[r]]
        pv = p ** vs
        for i2 in range(R):
            if i2 != r and A[i2][r] % mod:
                t = A[i2][r] // pv  # exact: val(A[i2][r]) >= vs
                assert A[i2][r] == t * pv
                A[i2] = [(a - t * c) % mod for a, c in zip(A[i2], A[r])]
                U[i2] = [(a - t * c) % mod for a, c in zip(U[i2], U[r])]
        for j2 in range(K):
            if j2 != r and A[r][j2] % mod:
                t = A[r][j2] // pv
                assert A[r][j2] == t * pv
                for row in A:
                    row[j2] = (row[j2] - t * row[r]) % mod
                for row in V:
                    row[j2] = (row[j2] - t * row[r]) % mod
        r += 1
    # now U D V == diag(A[i][i]) mod `mod`
    c = [sum(U[i][j] * b[j] for j in range(R)) % mod for i in range(R)]
    y = [0] * K
    for i in range(R):
        s = A[i][i] % mod if i < K else 0
        if s == 0:
            if c[i] % mod:
                return ('C', cert_scale(U[i], c[i], mod, p, mod))
        else:
            if c[i] % s:
                return ('C', cert_scale(U[i], c[i], mod, p, s))
            if i < K:
                y[i] = c[i] // s
    x = [sum(V[i][j] * y[j] for j in range(K)) % mod for i in range(K)]
    return ('F', x)


def cert_scale(Urow, ci, mod, p, s):
    # row Urow kills D up to s*e_r*V^{-1}; scale by mod/s (s a power of p dividing mod)
    t = mod // s
    return [(t * a) % mod for a in Urow]


def gens(blocks, P, p, fvals=None):
    D, b = [], []
    for B in blocks:
        vs = [expvec(x, P) for x in B]
        for j in range(1, p):
            D.append([a - c for a, c in zip(vs[j], vs[0])])
            b.append(1 if fvals is None else fvals[(B[0], B[j])])
    return D, b


def min_level(D, b, p, L):
    """returns (level or None, per-level list of ('F',x)/('C',c)) with independent re-check."""
    res = []
    for i in range(L + 1):
        mod = p ** (i + 1)
        kind, w = solve_mod(D, [(p ** i * bb) % mod for bb in b], mod, p)
        if kind == 'F':
            for d, bb in zip(D, b):
                assert sum(a * c for a, c in zip(d, w)) % mod == (p ** i * bb) % mod
        else:
            for col in range(len(D[0])):
                assert sum(w[r] * D[r][col] for r in range(len(D))) % mod == 0
            assert (sum(a * c for a, c in zip(w, b)) * p ** i) % mod != 0
        res.append((kind, w))
    lev = next((i for i, (k_, _) in enumerate(res) if k_ == 'F'), None)
    # monotonicity sanity
    if lev is not None:
        assert all(k_ == 'F' for k_, _ in res[lev:])
    return lev, res


def main():
    mode = sys.argv[1]
    if mode == 'ck':
        f = sys.argv[2]; mine = int(sys.argv[3]) if len(sys.argv) > 3 else 1
        L = int(sys.argv[4]) if len(sys.argv) > 4 else 5
        n, p = map(int, f.replace('\\', '/').split('exh_')[1].split('.')[0].split('_'))
        assert p == 2
        m = n // p; P = primes_upto(n)
        hist = {}; out = []
        for l in open(f):
            if not l.startswith('S '):
                continue
            w = l.split(); e = int(w[2])
            if e < mine:
                continue
            g = [int(x) for x in w[3].split(',')]
            B = blocks_of(n, p, P, g, m)
            D, b = gens(B, P, p)
            lev, res = min_level(D, b, p, L)
            hist[(e, lev)] = hist.get((e, lev), 0) + 1
            out.append({"g": g, "e": e, "level": lev,
                        "certs": [{"level": i, "kind": k_, "vec": v} for i, (k_, v) in enumerate(res)]})
        print(f"n={n} p={p} m={m} bound v_p(m)={vp(m, p)} checked={len(out)}  (e, minimal level or None=no f up to L={L}):")
        for k_, v in sorted(hist.items(), key=str):
            print("  ", k_, v)
        if len(sys.argv) > 5:
            json.dump({"n": n, "p": p, "primes": P, "L": L, "results": out}, open(sys.argv[5], 'w'))
    elif mode == 'w176':
        d = json.load(open(sys.argv[2])); L = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        n, p, K = d['n'], d['p'], d['K']; P = primes_upto(n)
        g = [d['phi'][str(q)][1] for q in P]; Fw = [d['phi'][str(q)][0] for q in P]
        B = blocks_of(n, p, P, g, K)
        D, b = gens(B, P, p)
        lev, res = min_level(D, b, p, L)
        print(f"witness {sys.argv[2]}: n={n} p={p} stated level {d['level']}; computed minimal level for its partition = {lev}")
        print("   per level:", [k_ for k_, _ in res])
    elif mode == 'w162':
        L = int(sys.argv[3]) if len(sys.argv) > 3 else 5
        txt = open(sys.argv[2]).read().split('solution')[1].split('\n')[0].split()
        phi = {int(t.split(':')[0]): tuple(map(int, t.split(':')[1].split('/'))) for t in txt}
        n, p, lv = 162, 3, 3; m = n // p; P = primes_upto(n)
        Fw = [phi[q][0] for q in P]; g = [phi[q][1] for q in P]
        B = blocks_of(n, p, P, g, m)
        # f from witness: F(d) = p^lv * f(d) mod p^(lv+1)
        fv = {}
        for Bk in B:
            for j in range(1, p):
                dd = [a - c for a, c in zip(expvec(Bk[j], P), expvec(Bk[0], P))]
                Fd = sum(a * c for a, c in zip(dd, Fw)) % p ** (lv + 1)
                assert Fd % p ** lv == 0 and Fd != 0
                fv[(Bk[0], Bk[j])] = Fd // p ** lv
        D, b = gens(B, P, p, fv)
        lev, res = min_level(D, b, p, L)
        print(f"witness n=162 p=3 (level 3): computed minimal level for (partition, witness f) = {lev}")
        print("   per level:", [k_ for k_, _ in res])


def vp(m, p):
    v = 0
    while m % p == 0:
        m //= p; v += 1
    return v


if __name__ == '__main__':
    main()
