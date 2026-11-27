"""pass 8: test "Lemma K" on downsets: with T, p, m, g as in saturation_test.py (all g-fibres of
size p), the induced map gbar: Gamma = Z^k/M -> Z_m is injective on the torsion of Gamma.
(Lemma K implies Lemma S and the bound v_p(elementary divisors) <= v_p(m).)
Usage: python kernel_test.py k smax p1,p2,...   [also tests general block size via p]
"""
import itertools, sys
from downset_levels import downsets2, downsets3, blocks_for
from saturation_test import elem_divisors


def row_basis(D, k):
    # integer row echelon (HNF-like) basis of the lattice spanned by D
    rows = [list(r) for r in D if any(r)]
    basis, col = [], 0
    while rows and col < k:
        nz = [r for r in rows if r[col] != 0]
        z = [r for r in rows if r[col] == 0]
        if not nz:
            col += 1
            continue
        while len(nz) > 1:
            nz.sort(key=lambda r: abs(r[col]))
            piv = nz[0]
            new = [piv]
            for r in nz[1:]:
                q = r[col] // piv[col]
                r2 = [a - q * b for a, b in zip(r, piv)]
                (new if r2[col] != 0 else z).append(r2)
            nz = new
        basis.append(nz[0])
        rows = [r for r in z if any(r)]
        col += 1
    return basis


def main():
    k, smax = int(sys.argv[1]), int(sys.argv[2])
    plist = [int(a) for a in sys.argv[3].split(',')]
    gen = downsets2 if k == 2 else downsets3
    tested = viol = 0
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
                    t = 1
                    for d in ed:
                        t *= d
                    tested += 1
                    if t == 1:
                        continue
                    B = row_basis(D, k)
                    img = set()
                    for c in itertools.product(range(t), repeat=len(B)):
                        y = [sum(ci * b[j] for ci, b in zip(c, B)) for j in range(k)]
                        if all(v % t == 0 for v in y):
                            y = [v // t for v in y]
                            img.add(sum(a * b for a, b in zip(g, y)) % m)
                    if len(img) != t:
                        viol += 1
                        if viol <= 10:
                            print(f"K-VIOLATION s={s} p={p} m={m} T={T} g={g} ed={ed} |g(tors)|={len(img)}", flush=True)
    print(f"tested {tested}; Lemma K violations: {viol}")


if __name__ == "__main__":
    main()
