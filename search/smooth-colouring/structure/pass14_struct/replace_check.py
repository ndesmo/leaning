"""Pass 14 [numerical check of Lemma 2 (replacement) and Prop 5 case (iii)] on Z_N, N = p^2 q^2 (default Z36).
For every aperiodic tile B (0 in B) with S_B = {p, q^2}: all complements are g_p-periodic (g_p = N/p);
check that B mod <g_p> has an order-q period in Z_N/<g_p>, build the lifted periodic B'' (Lemma 2) and
verify directly that every complement C of B satisfies C (+) B'' = Z_N.  Also, for S_B = {p,q} with
Phi_{pq^2} | B, Phi_{p^2 q} not | B, check that B mod <g_p> has NO order-q period (so no replacement)."""
import sys, itertools, cmath
p, q = (map(int, sys.argv[1:3]) if len(sys.argv) > 2 else (2, 3)); N = p*p*q*q; k = p*q
divs = [d for d in range(2, N+1) if N % d == 0]
def zs(S): return frozenset(d for d in divs if abs(sum(cmath.exp(2j*cmath.pi*s/d) for s in S)) < 1e-7)
def tiles(A, B): return len({(a+b) % N for a in A for b in B}) == N
def per(S): return [g for g in range(1, N) if {(s+g) % N for s in S} == set(S)]
gp = N//p; M = N//p                      # Z_N/<g_p> = Z_M via x -> x mod M
by = {}
for rest in itertools.combinations(range(1, N), k-1):
    S = (0,)+rest; by.setdefault(zs(S), []).append(S)
full = frozenset(divs); ok = bad = noq = 0; tested = 0
for K, Bs in by.items():
    comps = [C for K2, L in by.items() if K | K2 == full for C in L]
    if not comps: continue
    spp = {d for d in K if d in (p, p*p, q, q*q)}
    for B in Bs:
        if per(B): continue
        if not (spp == {p, q*q} or (spp == {p, q} and p*q*q in K and p*p*q not in K)): continue
        Bbar = sorted({b % M for b in B}); assert len(Bbar) == k
        qper = [h for h in range(1, M) if (h*q) % M == 0 and {(b+h) % M for b in Bbar} == set(Bbar)]
        if spp == {p, q*q}:
            tested += 1
            if not qper: bad += 1; continue
            h = qper[0]; hl = next(x for x in range(N) if x % M == h and (x*q) % N == 0)   # lift of order q
            B0 = []; covered = set()
            for b in Bbar:                       # choose orbit reps of <h> in Bbar, lift them
                if b in covered: continue
                orb = [(b + i*h) % M for i in range(q)]; covered |= set(orb); B0.append(b)
            B2 = sorted({(b0 + i*hl) % N for b0 in B0 for i in range(q)})
            assert len(B2) == k and per(B2) and sorted({x % M for x in B2}) == Bbar
            ok += all(tiles(C, B2) for C in comps)
        elif spp == {p, q} and p*q*q in K and p*p*q not in K:
            noq += (not qper)
print(f'Z{N}: S_B={{p,q^2}} aperiodic tiles tested {tested}, replacement worked for all complements: {ok}, no order-q period: {bad}')
print(f'S_B={{p,q}}, Phi_pq2 | B, Phi_p2q not | B: B mod <g_p> has no order-q period in {noq} cases (expected: all)')
