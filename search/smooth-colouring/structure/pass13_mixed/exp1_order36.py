"""Exp 1 [pass 13]: in every abelian group H of order p^2 q^2 (default p,q = 2,3, |H| = 36),
enumerate all tiles B (0 in B, |B| = pq) and their complements C (0 in C, C (+) B = H, |C| = pq).
For APERIODIC B report:
  - whether every complement is periodic (Hajos/Sands-type behaviour);
  - the period orders occurring among complements;
  - 'uniform rho': a hom rho: H -> Z_L (L = exp H) that maps EVERY complement C bijectively onto
    the order-pq subgroup (L/pq)Z_L  (this is what a Thm-2-style argument would produce);
  - whether each complement individually has such a rho;
  - whether some pair of complements has no common rho.
Usage: python exp1_order36.py [p q]"""
import sys, itertools
from grp import Group

p, q = (int(sys.argv[1]), int(sys.argv[2])) if len(sys.argv) > 2 else (2, 3)
pq = p * q
gtypes = [(p*p, q*q), (p, p, q*q), (p*p, q, q), (p, p, q, q)]

def good_rhos(G, C):
    """indices of chars rho with rho(C) = (L/pq) Z_L bijectively"""
    L = G.L
    if L % pq: return set()
    target = set(range(0, L, L // pq))
    res = set()
    for ci, ch in enumerate(G.chars):
        v = {ch[c] for c in C}
        if len(v) == pq and v == target: res.add(ci)
    return res

for dims in gtypes:
    G = Group(dims)
    ntiles = naper = 0
    stats = dict(allCper=0, someCaper=0, uniform=0, eachHas=0, eachLacks=0, pairNoCommon=0)
    perorders = {}
    examples = []
    for rest in itertools.combinations(range(1, G.N), pq - 1):
        B = (0,) + rest
        comps = G.complements(B)
        if not comps: continue
        ntiles += 1
        if G.periods(B): continue
        naper += 1
        pers = []
        for C in comps:
            po = sorted({G.order[g] for g in G.periods(C)})
            pers.append(tuple(po))
        key = tuple(sorted(set(pers)))
        perorders[key] = perorders.get(key, 0) + 1
        if all(pers): stats['allCper'] += 1
        else: stats['someCaper'] += 1
        R = [good_rhos(G, C) for C in comps]
        if all(R): stats['eachHas'] += 1
        else: stats['eachLacks'] += 1
        inter = set.intersection(*R) if R else set()
        if inter: stats['uniform'] += 1
        else:
            nc = any(not (R[i] & R[j]) for i in range(len(R)) for j in range(i + 1, len(R)))
            if nc:
                stats['pairNoCommon'] += 1
                if len(examples) < 3:
                    examples.append((B, comps[:6], pers[:6]))
    print(f'H=Z{dims}: tiles={ntiles} aperiodic={naper} {stats}')
    print('   complement period-order patterns (per aperiodic B): ', perorders)
    for B, cs, ps in examples:
        print('   example B=', [G.els[b] for b in B])
        for C, pp in zip(cs, ps): print('      C=', [G.els[c] for c in C], 'period orders', pp)
    sys.stdout.flush()
