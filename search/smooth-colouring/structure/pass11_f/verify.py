"""Independent verifier (pass 11), written from the definitions; imports nothing from fcheck/mkcerts.

Definitions used (composite_B.md §0, pass8_level.md §1):
  T_n = exponent vectors of 1..n over primes <= n; g: Z^k -> Z_m (m = n/2) with all fibres on T_n
  of size 2; blocks = fibres. (b_L^2): psi = (F, g): Z^k -> Z_{2^{L+1}} x Z_m injective on T_n with
  each g-fibre mapped onto a coset of 2^L Z_{2^{L+1}}.
Checks per record:
  nof_relation c:  sum_B c_B (v(x_B) - v(y_B)) == 0 over Z and sum c_B odd  => no F at any level
                   (F would give 0 = F(0) = 2^L * sum c_B != 0 mod 2^{L+1}).
  level L, F:      psi injective on T_n, fibre = coset of order-2 subgroup;
                   every lower level i < L impossible: i = 0 by F_2 rank of [D | 1] (own elimination),
                   and the stored mod-2^{i+1} certificate c (c.D == 0 mod 2^{i+1}, sum c odd);
                   colouring of Z+: col(x) = the t in psi(T) with psi(x) - t in {0..2^L-1} x {0}
                   (psi = 0 on primes > n); checks this is a tiling of G and that
                   a, 2a, ..., na get n distinct colours for every a <= A.
Usage: python verify.py certs.json [A]
"""
import json, sys


def factor(x):
    f = {}
    q = 2
    while q * q <= x:
        while x % q == 0:
            f[q] = f.get(q, 0) + 1; x //= q
        q += 1
    if x > 1:
        f[x] = f.get(x, 0) + 1
    return f


def f2_rank(rows):
    rows = [int(''.join(str(a & 1) for a in r), 2) for r in rows]
    basis = []
    for r in rows:
        for b in basis:
            r = min(r, r ^ b)
        if r:
            basis.append(r)
    return len(basis)


def main():
    d = json.load(open(sys.argv[1])); A = int(sys.argv[2]) if len(sys.argv) > 2 else 300
    n, m, P = d['n'], d['m'], d['primes']
    assert 2 * m == n and P == [q for q in range(2, n + 1) if len(factor(q)) == 1 and factor(q).get(q) == 1]
    V = {x: [factor(x).get(q, 0) for q in P] for x in range(1, n + 1)}
    stats = {"nof": 0, "level": {}}
    for rec in d['records']:
        g = rec['g']
        gv = {x: sum(a * b for a, b in zip(V[x], g)) % m for x in V}
        fib = {}
        for x in V:
            fib.setdefault(gv[x], set()).add(x)
        assert len(fib) == m and all(len(s) == 2 for s in fib.values())
        assert sorted(map(frozenset, fib.values()), key=sorted) == sorted((frozenset(pr) for pr in rec['pairs']), key=sorted)
        diffs = [[a - b for a, b in zip(V[y], V[x])] for x, y in rec['pairs']]
        if 'nof_relation' in rec:
            c = rec['nof_relation']
            assert len(c) == len(diffs)
            assert all(sum(ci * dv[j] for ci, dv in zip(c, diffs)) == 0 for j in range(len(P)))
            assert sum(c) % 2 == 1
            stats['nof'] += 1
            continue
        L, F = rec['level'], rec['F']; mod = 2 ** (L + 1)
        psi = {x: (sum(a * b for a, b in zip(V[x], F)) % mod, gv[x]) for x in V}
        assert len(set(psi.values())) == n
        for x, y in rec['pairs']:
            assert (psi[y][0] - psi[x][0]) % mod == 2 ** L
        # lower levels impossible
        if L >= 1:
            assert f2_rank(diffs) < f2_rank([dv + [1] for dv in diffs]), "level 0 would be solvable"
        for i, c in enumerate(rec['lower']):
            mi = 2 ** (i + 1)
            assert all(sum(ci * dv[j] for ci, dv in zip(c, diffs)) % mi == 0 for j in range(len(P)))
            assert sum(c) % 2 == 1
        # tiling of G = Z_mod x Z_m by psi(T) + ({0..2^L-1} x {0})
        img = list(psi.values()); cover = {}
        for t in img:
            for j in range(2 ** L):
                w = ((t[0] + j) % mod, t[1])
                assert w not in cover; cover[w] = t
        assert len(cover) == mod * m
        # colouring check on Z+
        pidx = {q: i for i, q in enumerate(P)}

        def col(x):
            w0 = w1 = 0
            for q, e in factor(x).items():
                if q in pidx:
                    w0 += e * F[pidx[q]]; w1 += e * g[pidx[q]]
            return cover[(w0 % mod, w1 % m)]
        cache = {}
        for a in range(1, A + 1):
            cs = set()
            for j in range(1, n + 1):
                x = a * j
                if x not in cache:
                    cache[x] = col(x)
                cs.add(cache[x])
            assert len(cs) == n, (a, rec['g'])
        stats['level'][L] = stats['level'].get(L, 0) + 1
    print(f"{sys.argv[1]}: n={n}: all {len(d['records'])} records verified; no-f relations: {stats['nof']}; "
          f"level records (lower levels refuted, colouring checked for a<={A}): {stats['level']}")


if __name__ == '__main__':
    main()
