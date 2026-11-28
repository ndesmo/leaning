"""T5 [pass 13]: Theorem-3-style reductions that need NOT factor through G.
For a solution phi (json from exp2_tn.py), with K-fibres as blocks:
  T5c : exists f: M -> Z_p x Z_q (M = Z-span of within-block differences of exponent vectors)
        injective on every block  <=>  (c_{x,y}) for some x,y (Thm 3' in pass13_mixed.md).
  T5bp: for some chi' in Hom(H_q, Z_q) whose fibres with pi_K are blocks of size p:
        f: M' -> Z_p nonzero on all within-block differences  <=> (b_i^p) for some i (or (a)).
  T5bq: symmetric.
Usage: python t5_partition.py file.json"""
import sys, json, itertools
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form

def primes_upto(n): return [x for x in range(2, n + 1) if all(x % d for d in range(2, int(x**.5) + 1))]
def expvec(m, P):
    v = []
    for p in P:
        e = 0
        while m % p == 0: m //= p; e += 1
        v.append(e)
    return v

def zbasis(vecs):
    M = Matrix(vecs).T            # columns generate
    Hm = hermite_normal_form(M)   # column-style HNF, columns = basis
    cols = [list(Hm[:, j]) for j in range(Hm.shape[1]) if any(Hm[:, j])]
    return cols

def coords(basis, v):
    Bm = Matrix(basis).T
    sol = Bm.solve_least_squares(Matrix(v)) if Bm.shape[0] != Bm.shape[1] else Bm.solve(Matrix(v))
    c = [int(x) for x in sol]
    assert list(Bm * Matrix(c)) == list(v), 'not integral'
    return c

def homs_ok(blocks, E, p, sizes_check):
    """enumerate f: M -> Z_p (M spanned by block differences); return list of value-vectors on
    block elements (relative to block base) for f satisfying sizes_check(list of values per block)."""
    diffs = []
    for Bk in blocks:
        b0 = Bk[0]
        for m in Bk[1:]: diffs.append([a - b for a, b in zip(E[m], E[b0])])
    basis = zbasis(diffs)
    C = [coords(basis, d) for d in diffs]
    rk = len(basis); res = []
    for vals in itertools.product(range(p), repeat=rk):
        fv = [sum(c * v for c, v in zip(cc, vals)) % p for cc in C]
        # split per block
        i = 0; per = []; ok = True
        for Bk in blocks:
            vs = [0] + fv[i:i + len(Bk) - 1]; i += len(Bk) - 1
            per.append(vs)
        if sizes_check(per): res.append(per)
    return res

def main():
    d = json.load(open(sys.argv[1])); n, p, q, r = d['n'], d['p'], d['q'], d['r']
    lim = int(sys.argv[2]) if len(sys.argv) > 2 else 10**9
    P = primes_upto(n); T = list(range(1, n + 1)); E = {m: expvec(m, P) for m in T}
    dims = d['dims']
    out = []
    for s in d['sols'][:lim]:
        phi = s['phi']
        val = {}
        for m in T:
            v = [0] * (len(dims) + 1)
            for i, e in enumerate(E[m]):
                v = [(a + e * b) % dd for a, b, dd in zip(v, phi[i], list(dims) + [r])]
            val[m] = v
        fib = {}
        for m in T: fib.setdefault(val[m][-1], []).append(m)
        blocks = list(fib.values())
        F2 = homs_ok(blocks, E, p, lambda per: all(all(vs.count(a) == q for a in range(p)) for vs in per))
        F3 = homs_ok(blocks, E, q, lambda per: all(all(vs.count(a) == p for a in range(q)) for vs in per))
        t5c = any(all(len(set(zip(a, b))) == p * q for a, b in zip(x, y)) for x in F2 for y in F3)
        out.append(t5c)
        print('sol', len(out), 'T1', s['T1'], 'T3', s['T3'], 'T4', s['T4'], 'T5c', t5c, flush=True)
    print('T5c true:', sum(out), 'of', len(out))
main()
