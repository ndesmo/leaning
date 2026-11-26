"""Independent checker (shares no code with kper.rs) for a kper solution line
    solution N=.. B=[..] primes p:v p:v ...
Claim: phi (primes -> Z_N, extended multiplicatively; primes not listed -> 0)
yields an n-satisfactory colouring.  Colour of x: the unique a in A=phi({1..n})
with phi(x)+a in B (needs (-A) (+) B = Z_N, checked).  Then directly checks
that x, 2x, ..., nx get n distinct colours for all x <= XMAX.
Usage: python check_tiling_colouring.py n "<solution line>" [XMAX]"""
import sys, re
n = int(sys.argv[1]); line = sys.argv[2]; XMAX = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
N = int(re.search(r"N=(\d+)", line).group(1))
B = [int(t) for t in re.search(r"B=\[([^\]]*)\]", line).group(1).split(",")]
img = {int(a): int(b) for a, b in re.findall(r"(\d+):(\d+)", line.split("primes", 1)[1])}
def phi(x):
    s, d = 0, 2
    while d * d <= x:
        while x % d == 0: s += img.get(d, 0); x //= d
        d += 1
    if x > 1: s += img.get(x, 0)
    return s % N
A = [phi(k) for k in range(1, n + 1)]
assert len(set(A)) == n, "phi not injective on 1..n"
assert len(B) * n == N
sums = sorted((b - a) % N for a in A for b in B)
assert sums == list(range(N)), "(-A)+B is not a tiling of Z_N"
Bs = set(B); col = {}
for g in range(N):
    cs = [k for k, a in enumerate(A) if (g + a) % N in Bs]
    assert len(cs) == 1; col[g] = cs[0]
for x in range(1, XMAX + 1):
    cols = {col[phi(k * x)] for k in range(1, n + 1)}
    assert len(cols) == n, f"block at x={x} not rainbow"
print(f"OK n={n} N={N}: colouring with {n} colours, blocks x..nx rainbow for all x<={XMAX}")
