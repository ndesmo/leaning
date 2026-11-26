"""Brute-force checks for composite_B.md.

Main check (Lemma C, the only non-elementary step of Theorem 2): for every factorisation
C (+) B = H of a finite abelian p-group H with |C| = p, and every nontrivial character chi with
B^(chi) != 0, chi is injective on C and chi(C) is a coset of mu_p.
  - exhaustive (all C containing 0, all complements B containing 0): |H| in {9, 25, 27}
  - sampled (random C of size p that tile, up to `cap` complements each): |H| in {81, 125}
Also checks Lemma P (B + p(c - c') = B) on the same pairs, and counts aperiodic B.
Usage: python composite_bruteforce.py [samples]      (about 1-3 minutes)
"""
import itertools, random, sys, cmath

def group(dims):
    els = list(itertools.product(*[range(d) for d in dims]))
    add = lambda x, y: tuple((a + b) % d for a, b, d in zip(x, y, dims))
    neg = lambda x: tuple((-a) % d for a, d in zip(x, dims))
    mul = lambda k, x: tuple((k * a) % d for a, d in zip(x, dims))
    return els, add, neg, mul

def complements(dims, C, cap=None):
    """All B with C (+) B = H and 0 in B (0 in C assumed); exact cover by translates b + C."""
    els, add, neg, mul = group(dims)
    idx = {e: i for i, e in enumerate(els)}
    N = len(els); z = tuple(0 for _ in dims)
    Cn = [neg(c) for c in C]
    out, cov, B = [], [False] * N, [z]
    def place(b):
        cells = [idx[add(b, c)] for c in C]
        if any(cov[i] for i in cells): return None
        for i in cells: cov[i] = True
        return cells
    place(z)
    def rec():
        if cap and len(out) >= cap: return
        try: i = cov.index(False)
        except ValueError: out.append(list(B)); return
        for cn in Cn:
            b = add(els[i], cn); cells = place(b)
            if cells is None: continue
            B.append(b); rec(); B.pop()
            for j in cells: cov[j] = False
    rec()
    return out

def check_pair(dims, p, C, B, add, neg, mul, els, stats):
    L = 1
    for d in dims: L = max(L, d)          # exponent of H (all dims are powers of p)
    z = tuple(0 for _ in dims)
    Bs = set(B)
    per = lambda h: all(add(b, h) in Bs for b in B)
    for c in C:                            # Lemma P
        for c2 in C:
            assert per(mul(p, add(c, neg(c2)))), ("LemmaP", dims, C, B)
    if not any(per(h) for h in els if h != z): stats['aperiodic'] += 1
    for y in els:                          # Lemma C
        if y == z: continue
        r = lambda x: sum(yk * xk * (L // dk) for yk, xk, dk in zip(y, x, dims)) % L
        val = sum(cmath.exp(2j * cmath.pi * r(b) / L) for b in B)
        if abs(val) < 1e-7: continue
        stats['chars'] += 1
        rs = sorted(r(c) for c in C)
        r0 = rs[0] % (L // p)
        assert rs == sorted(r0 + k * (L // p) for k in range(p)), ("LemmaC", dims, y, C, B)
    stats['pairs'] += 1

def run(dims, p, exhaustive, samples=0, cap=20):
    els, add, neg, mul = group(dims)
    z = tuple(0 for _ in dims)
    stats = {'pairs': 0, 'aperiodic': 0, 'chars': 0, 'tilingC': 0}
    if exhaustive:
        for rest in itertools.combinations([e for e in els if e != z], p - 1):
            C = [z] + list(rest)
            Bs = complements(dims, C)
            if Bs: stats['tilingC'] += 1
            for B in Bs: check_pair(dims, p, C, B, add, neg, mul, els, stats)
    else:
        random.seed(1); tries = 0
        Hp = [e for e in els if mul(p, e) == z and e != z]
        while stats['tilingC'] < samples and tries < 100000:
            tries += 1
            if random.random() < 0.3:
                C = [z] + random.sample([e for e in els if e != z], p - 1)
            else:   # bias towards sets whose differences are p-torsion plus a random p-multiple
                C = [z] + [add(random.choice(Hp), mul(p * random.randrange(2), random.choice(els)))
                           for _ in range(p - 1)]
            if len(set(C)) != p: continue
            Bs = complements(dims, C, cap=cap)
            if not Bs: continue
            stats['tilingC'] += 1
            for B in Bs: check_pair(dims, p, C, B, add, neg, mul, els, stats)
    print("H =", dims, "exhaustive" if exhaustive else "sampled", stats, "-> no counterexample")
    sys.stdout.flush()

if __name__ == "__main__":
    S = int(sys.argv[1]) if len(sys.argv) > 1 else 40
    for dims in [(9,), (3, 3), (25,), (5, 5), (27,), (9, 3), (3, 3, 3)]:
        run(dims, 3 if dims[0] % 3 == 0 else 5, True)
    for dims, p in [((81,), 3), ((27, 3), 3), ((9, 9), 3), ((9, 3, 3), 3), ((3, 3, 3, 3), 3),
                    ((125,), 5), ((25, 5), 5), ((5, 5, 5), 5)]:
        run(dims, p, False, samples=S)
