"""Tiny direct check of a witness JSON from cpsat_coset.py against the definition."""
import sys, json
d = json.load(open(sys.argv[1])); n, p, K = d["n"], d["p"], d["K"]; P2 = p * p
phi = {int(q): v for q, v in d["phi"].items()}
def val(m):
    a = b = 0; x = m; q = 2
    while x > 1:
        while x % q == 0: a += phi[q][0]; b += phi[q][1]; x //= q
        q += 1
    return a % P2, b % K
V = [val(m) for m in range(1, n + 1)]
assert len(set(V)) == n, "not injective"
for g in range(K):
    fib = sorted(a for a, b in V if b == g)
    assert len(fib) == p and fib == sorted((fib[0] % p + p * j) for j in range(p)), (g, fib)
print(f"DIRECT OK n={n} p={p} K={K}")
