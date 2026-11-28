"""check_colouring.py -- independent checker for a (c_{x,y}) witness (pass 14).

Shares no code with c22.rs.  Input: a witness file written by `c22 ... --wit FILE`:
  line 1: n p x q y r cap      line 2: tokens "prime=a,b,c" giving psi(prime) in Z_{p^x} x Z_{q^y} x Z_r.
Checks, from the definitions:
 (1) the (c_{x,y}) property: psi injective on {1..n}, and each Z_r-fibre of psi({1..n}) is a coset of
     P = p^{x-1}Z x q^{y-1}Z (explicit set comparison);
 (2) the tiling A (+) B = G with A = psi({1..n}), B = {(i, j, 0) : 0 <= i < p^{x-1}, 0 <= j < q^{y-1}}
     (all |A||B| sums distinct and |A||B| = |G|);
 (3) the colouring itself: psi extended to every prime <= X (primes > n get pseudo-random values),
     colour(m) = the unique a in {1..n} with psi(m) + psi(a) in B (checked unique), and for every
     a <= X/n the colours of a, 2a, ..., na are pairwise distinct.  X = 5000 by default.
Also reports whether the witness is "genuine" (labels with nonzero p- and q-parts), informational.
Usage: python check_colouring.py WITFILE [X]
"""
import sys, random
from sympy import factorint, primerange

lines = open(sys.argv[1]).read().split("\n")
n, p, x, q, y, r, cap = map(int, lines[0].split())
assert cap == 1, "colouring check only for genuine (cap=1) witnesses"
X = int(sys.argv[2]) if len(sys.argv) > 2 else 5000
MP, MQ = p ** x, q ** y
LP, LQ = p ** (x - 1), q ** (y - 1)
psi = {}
for tok in lines[1].split():
    l, v = tok.split("=")
    psi[int(l)] = tuple(int(t) for t in v.split(","))
assert set(psi) == set(primerange(2, n + 1)), "witness must give every prime <= n"
rng = random.Random(12345)
for l in primerange(n + 1, X + 1):
    psi[l] = (rng.randrange(MP), rng.randrange(MQ), rng.randrange(r))


def ev(m):
    s = [0, 0, 0]
    for l, e in factorint(m).items():
        for i in range(3):
            s[i] += e * psi[l][i]
    return (s[0] % MP, s[1] % MQ, s[2] % r)


A = {a: ev(a) for a in range(1, n + 1)}
# (1)
assert len(set(A.values())) == n, "not injective on T"
Psub = {(i * LP % MP, j * LQ % MQ) for i in range(p) for j in range(q)}
labels = []
for k in range(r):
    fibre = [(v[0], v[1]) for v in A.values() if v[2] == k]
    u = fibre[0]
    assert {((w[0] - u[0]) % MP, (w[1] - u[1]) % MQ) for w in fibre} == Psub and len(fibre) == p * q, f"fibre {k} not a coset"
    labels.append((u[0] % LP, u[1] % LQ))
print("(1) c-property OK")
# (2)
B = [(i, j, 0) for i in range(LP) for j in range(LQ)]
sums = {((a[0] + b[0]) % MP, (a[1] + b[1]) % MQ, (a[2] + b[2]) % r) for a in A.values() for b in B}
assert len(sums) == n * len(B) == MP * MQ * r, "not a tiling"
print("(2) tiling A+B=G OK, |B| =", len(B))
# (3)
Bset = set(B)
inv = {}
for a, v in A.items():
    inv.setdefault(v, a)
colour = {}
for m in range(1, X + 1):
    g = ev(m)
    cands = [a for a, v in A.items() if ((g[0] + v[0]) % MP, (g[1] + v[1]) % MQ, (g[2] + v[2]) % r) in Bset]
    assert len(cands) == 1, f"colour of {m} not unique: {cands}"
    colour[m] = cands[0]
for a in range(1, X // n + 1):
    cs = [colour[a * i] for i in range(1, n + 1)]
    assert len(set(cs)) == n, f"a={a}: colours of a..na not distinct"
print(f"(3) colouring OK: colours of a,2a,...,{n}a distinct for all a <= {X // n} (all x <= {X} coloured)")
gp = any(l[0] != 0 for l in labels) or x < 2
gq = any(l[1] != 0 for l in labels) or y < 2
print("genuine (nonzero label parts):", gp and gq, "labels:", labels)
print("CHECK PASSED")
