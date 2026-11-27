"""Brute-force count of (b_i^p) solutions: all phi(q) in Z_{p^{i+1}} x Z_K on ALL primes q <= n
(no large-prime shortcut), checked directly against the definition in structure/composite_B.md:
phi injective on {1..n} and every fibre over k in Z_K is a coset of p^i Z_{p^{i+1}}. Tiny n only.
usage: python brute_count3.py n p level"""
import sys, itertools
n, p, lv = map(int, sys.argv[1:4]); K = n // p; Q = p ** (lv + 1); PI = p ** lv
pr = [q for q in range(2, n + 1) if all(q % r for r in range(2, q))]
ex = []
for m in range(1, n + 1):
    x, e = m, []
    for q in pr:
        k = 0
        while x % q == 0: x //= q; k += 1
        e.append(k)
    ex.append(e)
cosets = {}  # canonical coset sets
G = [(h, f) for h in range(Q) for f in range(K)]
cnt = 0
for vals in itertools.product(G, repeat=len(pr)):
    V = [(sum(a * v[0] for a, v in zip(e, vals)) % Q, sum(a * v[1] for a, v in zip(e, vals)) % K) for e in ex]
    if len(set(V)) < n: continue
    fib = {}
    for a, b in V: fib.setdefault(b, set()).add(a)
    if len(fib) == K and all(s == {(min(s) + PI * j) % Q for j in range(p)} for s in fib.values()): cnt += 1
print(f"BRUTE3 n={n} p={p} level={lv} count={cnt}")
