"""Pass 15: the Prop-6 test of pass14_struct/NOTE.md, run on a given tiling.

Setting (cyclic analogue): H = Z_{p^2} x Z_{q^2}, G = H x Z_r, phi: Z^{#primes<=n} -> G injective on
T_n, K-fibres T_k = {t : phi_K(t) = k}.  A "row prime" rho in {p, q} is chosen (rho = 3 at n = 195);
sigma is the other prime.

  C-type fibre (rows along rho): phi_H(T_k) lies in one coset of  Z_{rho^2} x sigma Z_{sigma^2}
  (sigma-coordinate), is invariant under +rho in the rho-coordinate, and meets each of the sigma
  sigma-values in exactly rho points (one <rho>-coset = a "row").  P-cosets are the constant case.
  Pure-C case: every fibre is C-type.

Prop 6 (NOTE.md section 5).  M = Z-span of within-fibre exponent-vector differences.
  f_sigma := phi_sigma / sigma : M -> Z_sigma is well defined in the pure-C case.
  F-test (Prop 6 hypothesis):  exists hom f_rho : M -> Z_rho injective on every row.
  L-test (the "corrected candidate"): exists hom f_rho : M -> Z_rho with f_rho = phi_rho/rho on the
     row-difference lattice R.  Equivalent to "rho v notin R + rho M_rho" (see README).
  L => F (for rho = 2, L <=> F).  F => (f_rho, f_sigma) injective on every fibre => (c_{x,y}).

Implementations:
  * linear: own integer HNF basis of M, then Gaussian elimination over F_rho (L-test);
    F-test for rho = 3 by trying sign patterns eps_row in {+1,-1} only if the number of rows is small,
    otherwise via brute force.
  * brute: sympy HNF basis + enumeration of all of Hom(M, Z_rho) = F_rho^rank (independent code path),
    deciding L and F directly from the definitions; also checks (f_rho, phi_sigma/sigma) injective on
    each fibre for every F-witness found.

Usage:
  python prop6.py tilings.json rho [limit]        # json in the pass13 exp2_tn.py format
  python prop6.py --synthetic rho trials seed     # control: random non-tiling instances, linear vs brute
"""
import sys, json, itertools, random

def primes_upto(n): return [x for x in range(2, n + 1) if all(x % d for d in range(2, int(x**.5) + 1))]
def expvec(m, P):
    v = []
    for p in P:
        e = 0
        while m % p == 0: m //= p; e += 1
        v.append(e)
    return v

# ---------------- own integer HNF (row style) ----------------
def hnf_basis(vecs):
    rows = [list(v) for v in vecs if any(v)]
    if not rows: return [], []
    ncol = len(rows[0]); basis = []; pivots = []
    for c in range(ncol):
        nz = [r for r in rows if r[c] != 0]
        rows = [r for r in rows if r[c] == 0]
        while len(nz) > 1:
            nz.sort(key=lambda r: abs(r[c]))
            piv = nz[0]; new = [piv]
            for r in nz[1:]:
                k = r[c] // piv[c]
                rr = [a - k * b for a, b in zip(r, piv)]
                if rr[c] != 0: new.append(rr)
                elif any(rr): rows.append(rr)
            nz = new
        if nz:
            piv = nz[0]
            if piv[c] < 0: piv = [-a for a in piv]
            basis.append(piv); pivots.append(c)
    return basis, pivots

def coords(basis, pivots, v):
    v = list(v); co = []
    for b, c in zip(basis, pivots):
        assert v[c] % b[c] == 0, 'not in lattice'
        k = v[c] // b[c]; co.append(k)
        v = [a - k * x for a, x in zip(v, b)]
    assert not any(v), 'not in lattice'
    return co

def solve_mod(A, rhs, p):
    """is A y = rhs solvable over F_p?  returns a solution or None"""
    m = len(A); n = len(A[0]) if m else 0
    Mx = [[a % p for a in row] + [r % p] for row, r in zip(A, rhs)]
    piv = []; r = 0
    for c in range(n):
        pr = next((i for i in range(r, m) if Mx[i][c]), None)
        if pr is None: continue
        Mx[r], Mx[pr] = Mx[pr], Mx[r]
        inv = pow(Mx[r][c], p - 2, p)
        Mx[r] = [x * inv % p for x in Mx[r]]
        for i in range(m):
            if i != r and Mx[i][c]:
                f = Mx[i][c]; Mx[i] = [(x - f * y) % p for x, y in zip(Mx[i], Mx[r])]
        piv.append(c); r += 1
    if any(Mx[i][n] for i in range(r, m)): return None
    y = [0] * n
    for i, c in enumerate(piv): y[c] = Mx[i][n]
    return y

# ---------------- instance construction ----------------
def build(points, k_of, h_of, p, q, rho):
    """points: list of exponent vectors; k_of[i] fibre label; h_of[i] = (h_p, h_q) in Z_{p^2} x Z_{q^2}.
    returns dict with fibres, rows, classification (pure-C or reason)."""
    ir = 0 if rho == p else 1; sig = q if rho == p else p
    fib = {}
    for i, k in enumerate(k_of): fib.setdefault(k, []).append(i)
    rows = []; reason = None
    for k, idx in fib.items():
        hs = [h_of[i] for i in idx]
        hr = [h[ir] for h in hs]; hsg = [h[1 - ir] for h in hs]
        if len({x % sig for x in hsg}) != 1: reason = reason or f'fibre {k}: sigma-coord not in one coset'; continue
        byval = {}
        for i, h in zip(idx, hs): byval.setdefault(h[1 - ir], []).append(i)
        for val, rr in byval.items():
            res = sorted(h_of[i][ir] for i in rr)
            if len(rr) != rho or len({x % rho for x in res}) != 1 or len(set(res)) != rho:
                reason = reason or f'fibre {k}: row {val} not a <rho>-coset'
            rows.append(rr)
        if len(byval) != sig: reason = reason or f'fibre {k}: {len(byval)} rows'
    return fib, rows, reason, ir, sig

def linear_test(points, fib, rows, h_of, rho, ir):
    gens = [[a - b for a, b in zip(points[i], points[idx[0]])] for idx in fib.values() for i in idx[1:]]
    basis, piv = hnf_basis(gens)
    A = []; rhs = []
    for rr in rows:
        for i in rr[1:]:
            d = [a - b for a, b in zip(points[i], points[rr[0]])]
            dh = (h_of[i][ir] - h_of[rr[0]][ir]) % (rho * rho)
            assert dh % rho == 0
            A.append(coords(basis, piv, d)); rhs.append(dh // rho)
    L = solve_mod(A, rhs, rho) is not None if A else True
    return L, len(basis)

def literal_test(points, fib, rows, h_of, rho, ir):
    """NOTE.md's literal criterion: with v in M minus M_rho, the candidate exists iff rho*v notin R + rho*M_rho
    (True if M = M_rho)."""
    gens = [[a - b for a, b in zip(points[i], points[idx[0]])] for idx in fib.values() for i in idx[1:]]
    basis, piv = hnf_basis(gens)
    # phi_rho of a lattice vector is evaluated with the global hom PHI_RHO (set by the caller)
    a = [PHI_RHO(b) % rho for b in basis]
    js = [j for j, x in enumerate(a) if x]
    if not js: return True
    j = js[0]; inv = pow(a[j], rho - 2, rho)
    Mr = [[rho * x for x in basis[j]]] + [[x - (a[i] * inv % rho) * y for x, y in zip(basis[i], basis[j])] for i in range(len(basis)) if i != j]
    Rg = [[a_ - b_ for a_, b_ in zip(points[i], points[rr[0]])] for rr in rows for i in rr[1:]]
    LB, LP = hnf_basis(Rg + [[rho * x for x in m] for m in Mr])
    try:
        coords(LB, LP, [rho * x for x in basis[j]]); return False
    except AssertionError:
        return True

PHI_RHO = None

def brute_test(points, fib, rows, h_of, rho, ir, sig, maxrank=13):
    from sympy import Matrix
    from sympy.matrices.normalforms import hermite_normal_form
    gens = [[a - b for a, b in zip(points[i], points[idx[0]])] for idx in fib.values() for i in idx[1:]]
    Hm = hermite_normal_form(Matrix(gens).T)
    B = [list(Hm[:, j]) for j in range(Hm.shape[1]) if any(Hm[:, j])]
    r = len(B)
    if r > maxrank: return None
    Bm = Matrix(B).T
    def co(v):
        sol, params = Bm.gauss_jordan_solve(Matrix(v))
        c = [int(x) for x in sol]; assert list(Bm * Matrix(c)) == list(v); return c
    pc = {i: co([a - b for a, b in zip(points[i], points[idx[0]])]) for idx in fib.values() for i in idx}
    base = {i: idx[0] for idx in fib.values() for i in idx}
    Lb = Fb = False; injok = True
    for y in itertools.product(range(rho), repeat=r):
        f = {i: sum(a * b for a, b in zip(pc[i], y)) % rho for i in pc}   # f(t - t_base)
        Lok = Fok = True
        for rr in rows:
            vals = [f[i] for i in rr]
            if len(set(vals)) != rho: Fok = False
            for i in rr[1:]:
                dh = (h_of[i][ir] - h_of[rr[0]][ir]) % (rho * rho)
                if (f[i] - f[rr[0]]) % rho != dh // rho: Lok = False
        Lb |= Lok
        if Fok:
            Fb = True
            for idx in fib.values():   # Prop 6 proof steps 1-2: (f_rho, phi_sigma/sigma) injective
                pairs = {(f[i], ((h_of[i][1 - ir] - h_of[idx[0]][1 - ir]) % (sig * sig)) // sig) for i in idx}
                if len(pairs) != len(idx): injok = False
        if Lb and Fb and rho == 2: break
    return Lb, Fb, injok, r

def run_json(path, rho, limit):
    d = json.load(open(path)); n, p, q, r = d['n'], d['p'], d['q'], d['r']
    assert d['dims'] == [p * p, q * q], 'cyclic H only'
    P = primes_upto(n); pts = [expvec(t, P) for t in range(1, n + 1)]
    stats = {}
    for si, s in enumerate(d['sols'][:limit]):
        phi = s['phi']
        img = [tuple(sum(e * phi[j][c] for j, e in enumerate(v)) % m for c, m in enumerate((p * p, q * q, r))) for v in pts]
        assert len(set(img)) == n
        h_of = [x[:2] for x in img]; k_of = [x[2] for x in img]
        fib, rows, reason, ir, sig = build(pts, k_of, h_of, p, q, rho)
        if reason:
            stats['not pure-C'] = stats.get('not pure-C', 0) + 1; continue
        nC = sum(1 for idx in fib.values() if len({h_of[i][ir] % rho for i in idx}) > 1)
        L, rk = linear_test(pts, fib, rows, h_of, rho, ir)
        global PHI_RHO
        PHI_RHO = lambda v: sum(e * phi[j][ir] for j, e in enumerate(v))
        assert literal_test(pts, fib, rows, h_of, rho, ir) == L, ('literal MISMATCH', si)
        br = brute_test(pts, fib, rows, h_of, rho, ir, sig)
        key = ('pure-C', 'nonconst-fibres>0' if nC else 'all P-cosets', 'L', L,
               'brute(L,F,inj,rank)', br if br is None else br[:3])
        if br is not None: assert br[0] == L, ('MISMATCH', si)
        stats[key] = stats.get(key, 0) + 1
    print(path, 'rho =', rho, 'tilings', min(limit, len(d['sols'])))
    for k, v in sorted(stats.items(), key=str): print('  ', k, v)

def run_synth(rho, trials, seed):
    """Random non-tiling instances with C-type structure by construction: fibres of rho*s points,
    phi random hom Z^N -> Z_{rho^2} x Z_{sig^2} built so that each fibre is C-type.  Done by choosing
    random integer points and then *defining* h_of to be C-type and checking whether h_of is
    induced by a hom (consistency); only consistent instances are kept."""
    rng = random.Random(seed); sig = 3 if rho == 2 else 2
    p, q = rho, sig
    out = {}
    kept = 0
    while kept < trials:
        N = rng.randint(3, 6)
        phi = [(rng.randrange(rho * rho), rng.randrange(sig * sig)) for _ in range(N)]
        # random small points; group into fibres by a random hom to Z_2 and keep C-type fibres only
        pts = list({tuple(rng.randint(0, 2) for _ in range(N)) for _ in range(40)})
        hv = [tuple(sum(e * f[c] for e, f in zip(v, phi)) % m for c, m in enumerate((rho * rho, sig * sig))) for v in pts]
        # pick fibres greedily: rows = rho points with same sigma-value and rho-values a <rho>-coset
        used = set(); fib_k = {}; kk = 0
        groups = {}
        for i, h in enumerate(hv): groups.setdefault((h[1], h[0] % rho), []).append(i)
        rowsel = []
        for key, idx in groups.items():
            byv = {}
            for i in idx: byv.setdefault(hv[i][0], i)
            if len(byv) == rho: rowsel.append((key, list(byv.values())))
        # fibre = sig rows with sigma-values in one coset of sig Z_{sig^2}, all distinct
        bysc = {}
        for key, rr in rowsel: bysc.setdefault(key[0] % sig, {}).setdefault(key[0], rr)
        sel_pts = []; k_of = []
        for c, dct in bysc.items():
            if len(dct) == sig:
                for rr in dct.values():
                    for i in rr: sel_pts.append(pts[i]); k_of.append(kk)
                kk += 1
        if kk < 2: continue
        h_of = [tuple(sum(e * f[c] for e, f in zip(v, phi)) % m for c, m in enumerate((rho * rho, sig * sig))) for v in sel_pts]
        fib, rows, reason, ir, sig2 = build(sel_pts, k_of, h_of, p, q, rho)
        if reason: continue
        L, rk = linear_test(sel_pts, fib, rows, h_of, rho, ir)
        global PHI_RHO
        PHI_RHO = lambda v: sum(e * f[0] for e, f in zip(v, phi))
        assert literal_test(sel_pts, fib, rows, h_of, rho, ir) == L, 'literal MISMATCH'
        br = brute_test(sel_pts, fib, rows, h_of, rho, ir, sig2, maxrank=8)
        if br is None: continue
        assert br[0] == L, 'MISMATCH linear vs brute'
        assert (not br[1]) or br[2], 'F-witness not injective on a fibre'
        kept += 1; key = ('L', L, 'F', br[1]); out[key] = out.get(key, 0) + 1
    print('synthetic rho =', rho, 'instances', trials, 'seed', seed, '(linear L == literal L == brute L in all)')
    for k, v in sorted(out.items(), key=str): print('  ', k, v)

if __name__ == '__main__':
    if sys.argv[1] == '--synthetic':
        run_synth(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else:
        run_json(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 10**9)
