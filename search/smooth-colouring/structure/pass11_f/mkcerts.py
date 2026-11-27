"""Producer of certificates (pass 11). For every violator g in a ck file (p = 2):
  * exact integer left kernel of D (rows = block differences) by integer row reduction with a
    unimodular transform; if some kernel basis vector has odd coordinate sum, that vector c is an
    exact certificate that NO admissible f exists (c.D = 0 over Z, sum c odd, so f(0) = 1);
    otherwise f exists (sum-parity vanishes on the kernel lattice) -- independent of Prop. 1.
  * minimal level from fcheck.py (mod 2^{i+1} Smith form), with explicit F at the minimal level and
    mod-2^{i+1} certificates for every lower level.
Usage: python mkcerts.py <exh_n_2.ck> <min_e> <out.json>
"""
import json, sys
from fcheck import primes_upto, blocks_of, gens, min_level, expvec


def int_left_kernel(D):
    R, K = len(D), len(D[0])
    A = [r[:] for r in D]
    U = [[int(i == j) for j in range(R)] for i in range(R)]
    r = 0
    for c in range(K):
        while True:
            nz = [i for i in range(r, R) if A[i][c] != 0]
            if not nz:
                break
            i0 = min(nz, key=lambda i: abs(A[i][c]))
            A[r], A[i0] = A[i0], A[r]; U[r], U[i0] = U[i0], U[r]
            done = True
            for i in range(r + 1, R):
                if A[i][c]:
                    q = A[i][c] // A[r][c]
                    A[i] = [a - q * b for a, b in zip(A[i], A[r])]
                    U[i] = [a - q * b for a, b in zip(U[i], U[r])]
                    if A[i][c]:
                        done = False
            if done:
                break
        if any(A[i][c] for i in range(r, R)):
            r += 1
    ker = [U[i] for i in range(R) if not any(A[i])]
    for c in ker:
        assert all(sum(c[i] * D[i][j] for i in range(R)) == 0 for j in range(K))
    assert len(ker) == R - r
    return ker


def main():
    f, mine, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    n, p = map(int, f.replace('\\', '/').split('exh_')[1].split('.')[0].split('_'))
    assert p == 2
    m = n // 2; P = primes_upto(n); res = []; hist = {}
    for l in open(f):
        if not l.startswith('S '):
            continue
        w = l.split(); e = int(w[2])
        if e < mine:
            continue
        g = [int(x) for x in w[3].split(',')]
        B = blocks_of(n, p, P, g, m)
        D, b = gens(B, P, p)
        ker = int_left_kernel(D)
        odd = next((c for c in ker if sum(c) % 2), None)
        lev, lv = min_level(D, b, p, 6)
        assert (odd is None) == (lev is not None), "exact kernel test disagrees with fcheck"
        rec = {"g": g, "e": e, "pairs": [[Bk[0], Bk[1]] for Bk in B]}
        if odd is not None:
            rec["nof_relation"] = odd
        else:
            rec["level"] = lev
            x = lv[lev][1]  # F on prime basis mod 2^{lev+1}
            rec["F"] = x
            rec["lower"] = [lv[i][1] for i in range(lev)]
        res.append(rec)
        hist[(e, lev)] = hist.get((e, lev), 0) + 1
    print(f"n={n} m={m}: {len(res)} violators; (e, level|None): {sorted(hist.items(), key=str)}")
    json.dump({"n": n, "p": 2, "m": m, "primes": P, "records": res}, open(out, 'w'))


if __name__ == '__main__':
    main()
