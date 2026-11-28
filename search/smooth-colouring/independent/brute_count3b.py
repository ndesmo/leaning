"""brute_count3b.py n p level : exact count of (b_i^p) solutions phi: primes<=n -> Z_{p^{i+1}} x Z_K
over ALL primes (no large-prime shortcut, no symmetry), written from the definition in
structure/composite_B.md only.  Same object as brute_count3.py, but with prefix pruning so that
level 4 (p=3) and level 3 (p=5) tiny cases are feasible.  Primes are assigned in increasing order; after
prime q, every m<=n with largest prime factor <= q has a known value.  Pruning uses only NECESSARY
conditions of the definition: (1) injectivity among known values; (2) two known values in the same
fibre f must have h-difference in p^i Z (a fibre is one coset of p^i Z_{p^{i+1}}).  Every leaf is then
re-checked against the full definition (injective on {1..n}, all K fibres are cosets).
usage: python brute_count3b.py n p level [q0]   (q0: count only solutions with h(q0) a unit mod p)"""
import sys
n, p, lv = map(int, sys.argv[1:4]); UQ = int(sys.argv[4]) if len(sys.argv) > 4 else None  # optional: only phi with h(UQ) a unit mod p
K = n // p; Q = p ** (lv + 1); PI = p ** lv
pr = [q for q in range(2, n + 1) if all(q % r for r in range(2, q))]
def fac(m):
    e = {}; x = m
    for q in pr:
        while x % q == 0: x //= q; e[q] = e.get(q, 0) + 1
    return e
F = {m: fac(m) for m in range(1, n + 1)}
# group m by largest prime index
newm = {i: [m for m in range(2, n + 1) if max(F[m]) == q] for i, q in enumerate(pr)}
phi = {}
cnt = 0
def val(m):
    a = b = 0
    for q, k in F[m].items(): a += k * phi[q][0]; b += k * phi[q][1]
    return a % Q, b % K
def full_check():
    V = [val(m) for m in range(1, n + 1)]
    if len(set(V)) < n: return False
    fib = {}
    for a, b in V: fib.setdefault(b, set()).add(a)
    return len(fib) == K and all(s == {(min(s) + PI * j) % Q for j in range(p)} for s in fib.values())
def rec(i, known, used):
    global cnt
    if i == len(pr):
        if full_check(): cnt += 1
        return
    q = pr[i]
    for h in range(Q):
        if q == UQ and h % p == 0: continue
        for f in range(K):
            phi[q] = (h, f); ok = True; add = []
            for m in newm[i]:
                v = val(m)
                if v in used or any(v[1] == w[1] and (v[0] - w[0]) % PI for w in known + add): ok = False; break
                add.append(v); used.add(v)
            if ok: rec(i + 1, known + add, used)
            for v in add: used.discard(v)
    del phi[q]
v1 = (0, 0)
rec(0, [v1], {v1})
print(f"BRUTE3B n={n} p={p} level={lv}" + (f" unit_h_at={UQ}" if UQ else "") + f" count={cnt}")
