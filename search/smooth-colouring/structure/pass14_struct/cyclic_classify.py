"""Pass 14 [numerical check of Lemma 3 / Theorem 4 in NOTE.md] on the analogue Z_N, N = p^2 q^2.
Usage: python cyclic_classify.py p q      (p=2 q=3 -> Z36, |B'| = 6; exhaustive over 6-subsets)
Exact tiling criterion used: A (+) B = Z_N  iff |A||B| = N and every d | N, d > 1 has Phi_d | A or Phi_d | B
(Phi_d | A(x) iff A(zeta_d) = 0; evaluated in floating point, tolerance 1e-7)."""
import sys, itertools, cmath
from collections import Counter, defaultdict
p, q = map(int, sys.argv[1:3]); N = p*p*q*q; k = p*q
divs = [d for d in range(2, N+1) if N % d == 0]
Z = [cmath.exp(2j*cmath.pi/d) for d in divs]
def zs(S):
    return frozenset(d for d, z in zip(divs, Z) if abs(sum(z**s for s in S)) < 1e-7)
def periodic(S):
    Ss = set(S); return [g for g in range(1, N) if all((s+g) % N in Ss for s in S)]
subsets = defaultdict(list)            # zero set -> list of sets containing 0
for rest in itertools.combinations(range(1, N), k-1):
    S = (0,)+rest; subsets[zs(S)].append(S)
full = frozenset(divs)
keys = list(subsets)
comp_keys = {K: [K2 for K2 in keys if K | K2 == full] for K in keys}
def pp(K): return tuple(sorted(d for d in K if d in (p, p*p, q, q*q)))
# conventions: order-p period g_p = N/p, order-q period g_q = N/q
gp, gq = N//p, N//q
P_sub = set(range(0, N, N//k))   # order-pq subgroup
def to2(x): return (x % (p*p), x % (q*q))
def is_Cs(C):   # p-periodic, q-projection a coset of q Z_{q^2}, each value hit p times
    Cs = set(C)
    if not all((c+gp) % N in Cs for c in C): return False
    pr = Counter(to2(c)[1] for c in C)
    vals = sorted(pr); return all(v == p for v in pr.values()) and len(vals) == q and len({v % q for v in vals}) == 1
def is_Dt(C):
    Cs = set(C)
    if not all((c+gq) % N in Cs for c in C): return False
    pr = Counter(to2(c)[0] for c in C)
    vals = sorted(pr); return all(v == q for v in pr.values()) and len(vals) == p and len({v % p for v in vals}) == 1
stats = Counter(); bad = []; goodfail = 0
for K in keys:
    if not comp_keys[K]: continue
    comps = [C for K2 in comp_keys[K] for C in subsets[K2]]
    for B in subsets[K]:
        Bper = bool(periodic(B))
        for C in comps:                       # Sands-goodness check for every factorization
            if not Bper and not periodic(C): goodfail += 1
        if Bper: continue
        S = pp(K); dbl = (p*p*q in K, p*q*q in K)
        types = Counter()
        for C in comps:
            hp = (C[0]+gp) % N in C and all((c+gp) % N in C for c in C)
            hq = all((c+gq) % N in C for c in C)
            t = ('P' if hp and hq else 'p' if hp else 'q' if hq else 'aper')
            if t == 'p' and not is_Cs(C): t = 'p-notCs'
            if t == 'q' and not is_Dt(C): t = 'q-notDt'
            types[t] += 1
        stats[(S, dbl, tuple(sorted(types)))] += 1
print(f'N={N} |B|={k}; factorizations with both factors aperiodic: {goodfail}')
print('aperiodic tiles B (containing 0) by (S_B, (Phi_{p^2q}|B, Phi_{pq^2}|B), complement types):')
for key, c in sorted(stats.items()): print(' ', key, c)
