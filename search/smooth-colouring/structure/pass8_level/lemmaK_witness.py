"""pass 8: test Lemma K on actual [n] witnesses (dfs3 JSON files, gtile 'solution' lines).
For a witness psi = (h, g) on primes <= n: blocks = g-fibres of [n] (checked to have size p),
M = lattice of block differences in Z^{pi(n)}.  Computes the Smith form of M (with column
transform V), the torsion Gamma_tors = (+) Z_{d_r}, and tests whether gbar: Gamma -> Z_K is
injective on Gamma_tors (|image| = |Gamma_tors|).  Also reports v_p(|Gamma_tors|), max v_p(d_r),
v_p(K) and the 'true level' log_p|h(Z^k)| - 1 of the witness.
Usage: python lemmaK_witness.py FILE...   (FILE = *.json from dfs3, or a text file with a
       'solution' line from gtile6/7 together with its 'n=.. p=..' header line)
"""
import json, re, sys
from math import gcd
from sympy import Matrix, primerange
from sympy.matrices.normalforms import smith_normal_form


def expvec(x, primes):
    v = []
    for q in primes:
        e = 0
        while x % q == 0:
            x //= q
            e += 1
        v.append(e)
    return v


def snf_with_V(D):
    """Return (diag, V) with U*D*V = diag form; only V (unimodular, k x k) is tracked."""
    A = [row[:] for row in D]
    nr, k = len(A), len(A[0])
    V = [[int(i == j) for j in range(k)] for i in range(k)]

    def colop(j1, j2, c):  # col j1 += c*col j2
        for r in range(nr):
            A[r][j1] += c * A[r][j2]
        for r in range(k):
            V[r][j1] += c * V[r][j2]

    def colswap(a, b):
        for r in range(nr):
            A[r][a], A[r][b] = A[r][b], A[r][a]
        for r in range(k):
            V[r][a], V[r][b] = V[r][b], V[r][a]

    diag = []
    t = 0
    while t < min(nr, k):
        # find nonzero pivot of minimal abs value in submatrix
        best = None
        for r in range(t, nr):
            for c in range(t, k):
                if A[r][c] and (best is None or abs(A[r][c]) < abs(A[best[0]][best[1]])):
                    best = (r, c)
        if best is None:
            break
        r, c = best
        A[t], A[r] = A[r], A[t]
        colswap(t, c)
        done = False
        while not done:
            done = True
            for c in range(t + 1, k):
                if A[t][c]:
                    q = A[t][c] // A[t][t]
                    colop(c, t, -q)
                    if A[t][c]:
                        colswap(t, c); done = False
            for r in range(t + 1, nr):
                if A[r][t]:
                    q = A[r][t] // A[t][t]
                    A[r] = [a - q * b for a, b in zip(A[r], A[t])]
                    if A[r][t]:
                        A[t], A[r] = A[r], A[t]; done = False
            if done:
                # divisibility condition
                for r in range(t + 1, nr):
                    for c in range(t + 1, k):
                        if A[r][c] % A[t][t]:
                            A[t] = [a + b for a, b in zip(A[t], A[r])]
                            done = False
                            break
                    if not done:
                        break
        diag.append(abs(A[t][t]))
        t += 1
    return diag, V


def vp(x, p):
    v = 0
    while x and x % p == 0:
        x //= p; v += 1
    return v


def load(fn):
    if fn.endswith('.json'):
        w = json.load(open(fn))
        n, p, H, K = w['n'], w['p'], w['dims'][0], w['dims'][1]
        phi = {int(q): tuple(v) for q, v in w['phi'].items()}
        return n, p, H, K, phi
    txt = open(fn).read()
    hdr = re.search(r"n=(\d+) p=(\d+) H=\[(\d+)\]", txt)
    n, p, H = map(int, hdr.groups())
    sol = re.search(r"^solution (.*)$", txt, re.M).group(1)
    phi = {int(q): (int(a), int(b)) for q, a, b in re.findall(r"(\d+):(\d+)/(\d+)", sol)}
    return n, p, H, n // p, phi


def main():
    for fn in sys.argv[1:]:
        n, p, H, K, phi = load(fn)
        primes = list(primerange(2, n + 1))
        vecs = {x: expvec(x, primes) for x in range(1, n + 1)}
        gv = {x: sum(e * phi[q][1] for e, q in zip(vecs[x], primes)) % K for x in vecs}
        hv = {x: sum(e * phi[q][0] for e, q in zip(vecs[x], primes)) % H for x in vecs}
        blocks = {}
        for x in vecs:
            blocks.setdefault(gv[x], []).append(x)
        assert len(blocks) == K and all(len(b) == p for b in blocks.values()), "fibres not of size p"
        D = [[a - c for a, c in zip(vecs[x], vecs[b[0]])] for b in blocks.values() for x in b[1:]]
        diag, V = snf_with_V(D)
        # cross-check diag with sympy
        sd = smith_normal_form(Matrix(D))
        sdiag = sorted(abs(sd[i, i]) for i in range(min(sd.shape)) if sd[i, i] != 0)
        assert sorted(d for d in diag if d) == sdiag, (diag, sdiag)
        # M*V = row space of diag(d), so the torsion generator for d_j is row j of V^{-1}
        Vinv = Matrix(V).inv()
        assert all(Vinv[i, j] == int(Vinv[i, j]) for i in range(Vinv.rows) for j in range(Vinv.cols))
        tors = [(d, [int(Vinv[j, r]) for r in range(len(primes))]) for j, d in enumerate(diag) if d > 1]
        for d, y in tors:  # sanity: d*y in M  <=>  d*y*V has entries divisible by diag
            yV = [sum(d * y[r] * V[r][c] for r in range(len(primes))) for c in range(len(primes))]
            assert all((yV[c] % diag[c] == 0) if c < len(diag) and diag[c] else yV[c] == 0 for c in range(len(primes)))
        order = 1
        for d, _ in tors:
            order *= d
        gimg = K
        for d, y in tors:
            gimg = gcd(gimg, sum(e * phi[q][1] for e, q in zip(y, primes)) % K)
        imgsize = K // gimg if tors else 1
        rank = sum(1 for d in diag if d)
        hgen = H
        for q in primes:
            hgen = gcd(hgen, phi[q][0])
        hsize = H // hgen
        truelev = vp(hsize, p) - 1
        print(f"{fn.split('/')[-1]}: n={n} p={p} K={K} rank(M)={rank}/{len(primes)} |Gamma_tors|={order} "
              f"elemdiv>1={[d for d, _ in tors]} vp(K)={vp(K, p)} max vp(d)={max([vp(d, p) for d, _ in tors] + [0])} "
              f"|gbar(tors)|={imgsize} LemmaK={'OK' if imgsize == order else 'FAIL'} truelevel={truelev}", flush=True)


if __name__ == "__main__":
    main()
