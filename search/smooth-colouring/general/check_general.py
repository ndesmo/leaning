"""Independent checker (no code shared with gtile.rs) for a gtile EXISTS result.
Usage: python check_general.py n d1,d2,.. "b/b/..,b/b/..,.." "<solution line>" [XMAX]
phi: primes -> G given in the solution line (unlisted primes -> 0), extended
multiplicatively.  Colour of x = the a in A = phi({1..n}) with phi(x)+a in B; this needs
(-A) (+) B = G, which is checked.  Then checks directly that x,2x,..,nx get n distinct
colours for every x <= XMAX."""
import sys, re
n = int(sys.argv[1]); dims = [int(x) for x in sys.argv[2].split(",")]
B = [tuple(int(c) for c in t.split("/")) for t in sys.argv[3].split(",")]
img = {int(p): tuple(int(c) for c in v.split("/")) for p, v in re.findall(r"(\d+):([\d/]+)", sys.argv[4])}
XMAX = int(sys.argv[5]) if len(sys.argv) > 5 else 3000
z = tuple(0 for _ in dims)
add = lambda x, y: tuple((a + b) % d for a, b, d in zip(x, y, dims))
def phi(x):
    s, d = z, 2
    while d * d <= x:
        while x % d == 0: s = add(s, img.get(d, z)); x //= d
        d += 1
    return add(s, img.get(x, z)) if x > 1 else s
A = [phi(k) for k in range(1, n + 1)]
assert len(set(A)) == n
G = 1
for d in dims: G *= d
assert len(B) * n == G
negA = [tuple((-c) % d for c, d in zip(a, dims)) for a in A]
sums = [add(b, na) for na in negA for b in B]
assert len(set(sums)) == G, "(-A)+B not a tiling"
Bs = set(B); col = {}
def colour(g):
    if g not in col:
        cs = [k for k, a in enumerate(A) if add(g, a) in Bs]; assert len(cs) == 1; col[g] = cs[0]
    return col[g]
for x in range(1, XMAX + 1):
    assert len({colour(phi(k * x)) for k in range(1, n + 1)}) == n, f"x={x}"
print(f"OK n={n} G={dims}: rainbow for all x<={XMAX}")
