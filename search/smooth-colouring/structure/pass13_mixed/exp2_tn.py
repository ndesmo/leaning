"""Exp 2 [pass 13]: periodic tilings of T_n with |B| = pq, pushed into H = G_p x G_q (|H| = p^2 q^2,
n squarefree, n = p*q*r with K = Z_r), searched for a FIXED aperiodic tile B' of H:
    phi: Z^{#primes<=n} -> G = H x Z_r,  phi(T_n) - phi(T_n) avoids (B'-B') x {0}  (packing; with
    |A||B'| = |G| this is A (+) B' = G) and phi injective on T_n.
Each solution is tested for the reductions a proof would produce (all factoring through G):
  T1 (c): a hom chi: H -> Z_L with chi o phi bijective from every K-fibre onto a coset of the
          order-pq subgroup  [(a) through G implies T1];
  T3 (b^p) / T4 (b^q): homs chi_p: H_p -> Z_{L_p}, chi': H_q -> Z_q such that the fibres of
          (chi', pi_K) o phi have size p and chi_p o phi is injective on each with image a coset of
          the order-p subgroup (and symmetrically for q);
  T5 (c via the K-partition, Theorem-3 style, NOT through G): f: M -> Z_pq injective on blocks,
          M = lattice of within-K-fibre differences.
Usage: python exp2_tn.py n p q dims_of_H Bindex|rand seconds [maxsol]
  dims e.g. 4,9 ; B' is chosen among aperiodic tiles of H with complements lacking a common rho."""
import sys, time, itertools, random, json
from grp import Group

def primes_upto(n): return [x for x in range(2, n + 1) if all(x % d for d in range(2, int(x**.5) + 1))]
def expvec(m, P):
    v = []
    for p in P:
        e = 0
        while m % p == 0: m //= p; e += 1
        v.append(e)
    return v

def smith_hom_count(): pass

import os
RANDOM = os.environ.get('RESTARTS') is not None
RESTARTS = int(os.environ.get('RESTARTS', '0'))
def main():
    n, p, q = map(int, sys.argv[1:4]); dims = tuple(map(int, sys.argv[4].split(',')))
    bsel = sys.argv[5]; tlim = float(sys.argv[6]); maxsol = int(sys.argv[7]) if len(sys.argv) > 7 else 50
    r = n // (p * q); assert p * q * r == n
    H = Group(dims); pq = p * q
    # candidate B': aperiodic tiles whose complements have no common rho
    L = H.L; target = set(range(0, L, L // pq))
    def rhos(C): return {ci for ci, ch in enumerate(H.chars) if {ch[c] for c in C} == target and len({ch[c] for c in C}) == pq}
    cands = []
    if os.environ.get('BPRIME'):
        B = tuple(sorted(H.idx[tuple(b)] for b in json.loads(os.environ['BPRIME'])))
        assert B[0] == 0 and not H.periods(B)
        cands.append((B, H.complements(B, cap=2000)))
    rng = random.Random(int(bsel) if bsel.isdigit() else 0)
    combos = [] if cands else list(itertools.combinations(range(1, H.N), pq - 1)); rng.shuffle(combos)
    for rest in (combos if not cands else []):
        B = (0,) + rest
        if H.periods(B): continue
        comps = H.complements(B)
        if len(comps) < 2: continue
        R = [rhos(C) for C in comps]
        if not set.intersection(*R):
            cands.append((B, comps)); break
    B, comps = cands[0]
    print('H =', dims, 'B\' =', [H.els[b] for b in B], '#complements', len(comps), flush=True)
    # G = H x Z_r, element (h,k) -> h*r + k
    NG = H.N * r
    def gadd(x, y): return H.add[x // r][y // r] * r + (x % r + y % r) % r
    D0 = sorted({H.sub(a, b) for a in B for b in B})          # includes 0
    D0g = [d * r for d in D0]
    addt = [[gadd(x, y) for y in range(NG)] for x in range(NG)]
    forbmask = [sum(1 << addt[x][d] for d in D0g) for x in range(NG)]
    P = primes_upto(n); T = list(range(1, n + 1)); E = {m: expvec(m, P) for m in T}
    big = {m: max(i for i, e in enumerate(E[m]) if e) if m > 1 else -1 for m in T}
    byprime = [[m for m in T if big[m] == i] for i in range(len(P))]
    phi = [None] * len(P)
    def val(m):
        x = 0
        for i, e in enumerate(E[m]):
            for _ in range(e): x = addt[x][phi[i]]
        return x
    sols = []; t0 = time.time(); nodes = [0]; lim = [maxsol]; rngd = random.Random(0)
    def rec(i, forb, pts):
        if time.time() - t0 > tlim or len(sols) >= (lim[0] if RANDOM else maxsol): return
        if i == len(P):
            sols.append((list(phi), dict(pts))); return
        xs = list(range(NG))
        if RANDOM: rngd.shuffle(xs)
        for x in xs:
            nodes[0] += 1
            if i == 0 and x == 0: continue
            phi[i] = x
            f = forb; ok = True; newp = {}
            for m in byprime[i]:
                v = val(m)
                if (f >> v) & 1: ok = False; break
                f |= forbmask[v]; newp[m] = v
            if ok:
                pts.update(newp); rec(i + 1, f, pts)
                for m in newp: del pts[m]
        phi[i] = None
    if RANDOM:
        for rs in range(RESTARTS):
            rngd.seed(rs); before = len(sols); maxsol_save = len(sols) + 1
            t0 = time.time(); lim[0] = before + 1
            rec(0, forbmask[0], {1: 0})
    else:
        rec(0, forbmask[0], {1: 0})
    print(f'solutions found {len(sols)} nodes {nodes[0]} time {time.time()-t0:.1f}s', flush=True)
    # reducibility tests
    rq = []
    Hp_dims = None
    out = []
    for phiv, pts in sols:
        A = [pts[m] for m in T]
        assert len(set(A)) == n
        fib = {}
        for m in T: fib.setdefault(pts[m] % r, []).append(m)
        hval = {m: pts[m] // r for m in T}
        # T1
        t1 = any(all(({(ch[hval[m]] - ch[hval[F[0]]]) % L for m in F} == target) for F in fib.values()) for ch in H.chars)
        # T3/T4: chars of H split by p- and q-parts: char index enumerates residues rs; its order
        def tb(pp, qq):
            # chi_pp: char of p-power order; chi': char with values in qq-torsion (order | qq)
            Lp = 1
            while L % (Lp * pp) == 0: Lp *= pp
            chp = [ch for ch in H.chars if all((v * Lp) % L == 0 for v in ch)]   # values in (L/Lp)Z_L: pp-power order
            chq = [ch for ch in H.chars if all((v * qq) % L == 0 for v in ch)]   # order | qq
            ordp = L // pp
            for c2 in chq:
                fb = {}
                for m in T: fb.setdefault((c2[hval[m]], pts[m] % r), []).append(m)
                if any(len(F) != pp for F in fb.values()): continue
                for c1 in chp:
                    # differences inside each fibre must be nonzero multiples of ordp ... values distinct, coset of <ordp>
                    if all(len({c1[hval[m]] for m in F}) == pp and all((c1[hval[m]] - c1[hval[F[0]]]) % ordp == 0 for m in F) for F in fb.values()):
                        return True
            return False
        t3 = tb(p, q); t4 = tb(q, p)
        out.append((t1, t3, t4, phiv))
    from collections import Counter
    print('test outcomes (T1 c, T3 b^p, T4 b^q):', Counter((a, b, c) for a, b, c, _ in out))
    gm = [o for o in out if not (o[0] or o[1] or o[2])]
    print('genuinely mixed (through G):', len(gm))
    json.dump({'n': n, 'p': p, 'q': q, 'dims': dims, 'r': r, 'B': [H.els[b] for b in B],
               'sols': [{'phi': [[*H.els[x // r], x % r] for x in o[3]], 'T1': o[0], 'T3': o[1], 'T4': o[2]} for o in out]},
              open(f'exp2_n{n}_{"x".join(map(str,dims))}_{bsel}{"_r" if RANDOM else ""}.json', 'w'))

main()
