"""Direct check of a dfs3 witness JSON against (b_i^p) (structure/composite_B.md): phi on all primes
<= n, extended additively over factorisations; injective on {1..n}; each of the K fibres is a coset
of the order-p subgroup p^i Z_{p^{i+1}}."""
import sys, json
d = json.load(open(sys.argv[1])); n, p, K, lv = d["n"], d["p"], d["K"], d["level"]
Q, PI = p ** (lv + 1), p ** lv
assert d["dims"] == [Q, K]
phi = {int(q): v for q, v in d["phi"].items()}
assert sorted(phi) == [q for q in range(2, n + 1) if all(q % r for r in range(2, q))]
def val(m):
    a = b = 0; x = m; q = 2
    while x > 1:
        while x % q == 0: a += phi[q][0]; b += phi[q][1]; x //= q
        q += 1
    return a % Q, b % K
V = [val(m) for m in range(1, n + 1)]
assert len(set(V)) == n, "not injective"
for g in range(K):
    fib = {a for a, b in V if b == g}
    assert len(fib) == p and fib == {(min(fib) + PI * j) % Q for j in range(p)}, (g, sorted(fib))
print(f"DIRECT3 OK n={n} p={p} level={lv} K={K}")
