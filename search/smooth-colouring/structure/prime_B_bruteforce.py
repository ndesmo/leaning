"""Brute-force check of the order-p^2 lemmas in prime_B_reduction.md, p = 3, 5.
For H = Z_{p^2} and H = Z_p x Z_p, enumerate all B, C of size p containing 0 with
B (+) C = H (iff (B-B) n (C-C) = {0}, given |B||C| = |H|), and check:
 L1 (any H): if d in B-B has order p, then C (+) <d> = H for every complement C of B.
 L2 (Z_{p^2}): if B-B has no nonzero multiple of p, every complement C of B is pZ_{p^2}.
 L3: dilation: B (+) C = H  =>  kB (+) C = H for gcd(k,p)=1.
Also prints the classification of B (up to translation) having a complement."""
import itertools, sys
import numpy as np

def run(p, cyclic):
    if cyclic:
        els = [(x,) for x in range(p*p)]
        add = lambda a, b: ((a[0]+b[0]) % (p*p),)
        neg = lambda a: ((-a[0]) % (p*p),)
        mul = lambda k, a: ((k*a[0]) % (p*p),)
    else:
        els = [(x, y) for x in range(p) for y in range(p)]
        add = lambda a, b: ((a[0]+b[0]) % p, (a[1]+b[1]) % p)
        neg = lambda a: ((-a[0]) % p, (-a[1]) % p)
        mul = lambda k, a: ((k*a[0]) % p, (k*a[1]) % p)
    idx = {e: i for i, e in enumerate(els)}
    zero = els[0]
    sets = [(zero,) + c for c in itertools.combinations(els[1:], p-1)]
    def dmask(S):
        m = 0
        for a in S:
            for b in S:
                m |= 1 << idx[add(a, neg(b))]
        return m
    masks = np.array([dmask(S) for S in sets], dtype=np.int64)
    def order(d):
        k, x = 1, d
        while x != zero:
            x = add(x, d); k += 1
        return k
    def cyc(d):
        S, x = {zero}, d
        while x != zero:
            S.add(x); x = add(x, d)
        return S
    nB_with, fails = 0, 0
    classes = {}
    for i, B in enumerate(sets):
        comp = np.nonzero((masks & masks[i]) == 1)[0]
        if len(comp) == 0:
            continue
        nB_with += 1
        Cs = [sets[j] for j in comp]
        diffs = {add(a, neg(b)) for a in B for b in B} - {zero}
        # L1
        for d in diffs:
            if order(d) == p:
                D = cyc(d)
                for C in Cs:
                    if len({add(c, x) for c in C for x in D}) != p*p:
                        fails += 1; print("L1 FAIL", B, C, d)
        # L2
        if cyclic and all(d[0] % p != 0 for d in diffs):
            P = {(p*j,) for j in range(p)}
            for C in Cs:
                if set(C) != P:
                    fails += 1; print("L2 FAIL", B, C)
        # L3
        for k in range(1, p*p):
            if k % p == 0: continue
            kB = [mul(k, b) for b in B]
            for C in Cs:
                if len({add(x, c) for x in kB for c in C}) != p*p:
                    fails += 1; print("L3 FAIL", B, C, k)
        sub = len(cyc_closure(B, add, zero)) == p
        key = ("subgroup" if sub else "non-subgroup",
               "every complement C (with 0) is a subgroup" if all(len(cyc_closure(C, add, zero)) == p for C in Cs) else "some C not a subgroup")
        classes[key] = classes.get(key, 0) + 1
    print(f"p={p} H={'Z_%d' % (p*p) if cyclic else 'Z_%d^2' % p}: {len(sets)} sets B with 0; "
          f"{nB_with} have a complement; failures={fails}; classes={classes}")
    return fails

def cyc_closure(S, add, zero):
    G = set(S) | {zero}
    while True:
        new = {add(a, b) for a in G for b in G} | G
        if new == G: return G
        G = new

f = 0
for p in (3, 5):
    for cyc_ in (True, False):
        f += run(p, cyc_)
print("TOTAL FAILURES", f)
