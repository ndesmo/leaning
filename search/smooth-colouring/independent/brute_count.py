"""Brute-force count of all (h,f) on primes <= n satisfying the definition (tiny n only)."""
import sys, itertools
n, p = int(sys.argv[1]), int(sys.argv[2]); K = n // p; P2 = p * p
pr = [q for q in range(2, n + 1) if all(q % r for r in range(2, q))]
ex = []
for m in range(1, n + 1):
    x, e = m, []
    for q in pr:
        k = 0
        while x % q == 0: x //= q; k += 1
        e.append(k)
    ex.append(e)
cnt = 0
for hv in itertools.product(range(P2), repeat=len(pr)):
    H = [sum(a * b for a, b in zip(e, hv)) % P2 for e in ex]
    for fv in itertools.product(range(K), repeat=len(pr)):
        F = [sum(a * b for a, b in zip(e, fv)) % K for e in ex]
        if len(set(zip(H, F))) < n: continue
        fib = {}
        for a, b in zip(H, F): fib.setdefault(b, []).append(a)
        if all(len(v) == p and len({a % p for a in v}) == 1 for v in fib.values()) and len(fib) == K: cnt += 1
print(f"BRUTE n={n} p={p} count={cnt}")
