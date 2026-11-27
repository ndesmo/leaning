"""Independent check (sympy only) of the downset counterexample to Lemma S / Lemma K.
T in N^5 (size 10), p = 2, m = 5, g = (1,2,4,3,3).  Prints fibres, SNF of M, and the minimal
level by brute force over psi: Z^5 -> Z_{2^{i+1}} x Z_5 (i = 0, 1, 2)."""
import itertools
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
T = [(0,0,0,0,0),(0,0,0,0,1),(0,0,0,1,0),(0,0,0,2,0),(0,0,1,0,0),(0,1,0,0,0),(0,2,0,0,0),(1,0,0,0,0),(1,0,1,0,0),(2,0,0,0,0)]
g = (1,2,4,3,3); m, p = 5, 2
Ts = set(T)
assert all(all(x[i] == 0 or tuple(x[t]-(t == i) for t in range(5)) in Ts for i in range(5)) for x in T), "not a downset"
fib = {}
for x in T:
    fib.setdefault(sum(a*b for a, b in zip(g, x)) % m, []).append(x)
print("fibres:", fib)
assert all(len(v) == p for v in fib.values()) and len(fib) == m
rows = [[a-b for a, b in zip(x, y)] for v in fib.values() for x, y in itertools.combinations(v, 2)]
print("SNF diag:", [smith_normal_form(Matrix(rows), domain=ZZ)[i, i] for i in range(5)])
for i in range(3):
    q = p**(i+1)
    ok = None
    for F in itertools.product(range(q), repeat=5):
        good = True
        for v in fib.values():
            vals = [sum(a*b for a, b in zip(F, x)) % q for x in v]
            if len(set(vals)) != p or any((u - vals[0]) % (q//p) for u in vals):
                good = False
                break
        if good:
            ok = F
            break
    print(f"level {i} (F: Z^5 -> Z_{q}, fibres cosets of order-{p} subgroup, with this g):", "FOUND " + str(ok) if ok else "NONE")
# Does T admit ANY level-0 solution (psi: Z^5 -> Z_10 = Z_2 x Z_5 bijective on T)?
cnt = 0
for F in itertools.product(range(10), repeat=5):
    if len({sum(a*b for a, b in zip(F, x)) % 10 for x in T}) == 10:
        cnt += 1
print("bijective psi: Z^5 -> Z_10 on T (any g):", cnt)
