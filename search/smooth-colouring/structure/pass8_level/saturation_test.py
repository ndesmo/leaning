"""pass 8: test "Lemma S" on downsets.

Lemma S (conjectured): T downset in N^k, |T| = p*m, p prime not dividing m, g: Z^k -> Z_m a
homomorphism all of whose fibres on T have exactly p elements.  Let M = lattice spanned by
x - y (x, y in T, g(x) = g(y)).  Then Z^k / M has no p-torsion.

Also records, for p | m, the largest v_p of a nonzero elementary divisor (compare with v_p(m)).
Elementary divisors via gcds of minors (k <= 3).
Usage: python saturation_test.py k smax p1,p2,...
"""
import itertools, sys
from math import gcd
from functools import reduce
from downset_levels import downsets2, downsets3, blocks_for


def det(rows):
    if len(rows) == 1:
        return rows[0][0]
    if len(rows) == 2:
        return rows[0][0] * rows[1][1] - rows[0][1] * rows[1][0]
    a = rows
    return (a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1]) - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
            + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0]))


def elem_divisors(D, k):
    # D: list of integer vectors (rows). returns nonzero elementary divisors d_1 | d_2 | ...
    out, prev = [], 1
    for r in range(1, k + 1):
        g = 0
        for rows in itertools.combinations(D, r):
            for cols in itertools.combinations(range(k), r):
                g = gcd(g, det([[row[c] for c in cols] for row in rows]))
                if g == 1:
                    break
            if g == 1:
                break
        if g == 0:
            break
        out.append(g // prev)
        prev = g
    return out


def vp(x, p):
    v = 0
    while x % p == 0:
        x //= p
        v += 1
    return v


def main():
    k, smax = int(sys.argv[1]), int(sys.argv[2])
    plist = [int(a) for a in sys.argv[3].split(',')]
    gen = downsets2 if k == 2 else downsets3
    viol, tested, worst = 0, 0, {}
    for s in range(2, smax + 1):
        for p in plist:
            if s % p:
                continue
            m = s // p
            for T in gen(s):
                for g in itertools.product(range(m), repeat=k):
                    fib = blocks_for(T, g, m)
                    if len(fib) != m or any(len(b) != p for b in fib.values()):
                        continue
                    D = [tuple(a - c for a, c in zip(x, b[0])) for b in fib.values() for x in b[1:]]
                    ed = elem_divisors(D, k)
                    mv = max([vp(d, p) for d in ed] + [0])
                    tested += 1
                    key = (p, vp(m, p))
                    worst[key] = max(worst.get(key, 0), mv)
                    if m % p and mv > 0:
                        viol += 1
                        if viol <= 10:
                            print(f"S-VIOLATION s={s} p={p} m={m} T={T} g={g} ed={ed}", flush=True)
    print(f"tested (T,g) pairs: {tested}; Lemma S violations (p not | m): {viol}")
    print("max v_p(elementary divisor) by (p, v_p(m)):", dict(sorted(worst.items())))


if __name__ == "__main__":
    main()
