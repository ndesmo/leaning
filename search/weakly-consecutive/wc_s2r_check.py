"""A7.5 helper: for k = s^2 r (r, s distinct primes, s | r - 1) list the exceptional
pairs with r | s^2 - s + 1, and test whether the 'divisor of k + 1' step used for k = 63
applies: some m | k + 1 with m * s^2 > k and a position j in [1, k] with m | j and
j = 1 - s (mod s^2).  [numerical, Python, not Lean]"""
import sys
from math import isqrt


def is_prime(n):
    return n >= 2 and all(n % p for p in range(2, isqrt(n) + 1))


def k1_step(s, r):
    k = s * s * r
    hits = []
    for m in range(2, k + 1):
        if (k + 1) % m == 0 and m * s * s > k:
            for j in range(m, k + 1, m):
                if (j - (1 - s)) % (s * s) == 0:
                    hits.append((m, j))
                    break
    return hits


bound = int(sys.argv[1]) if len(sys.argv) > 1 else 60
covered, exc = [], []
for s in range(2, bound):
    if not is_prime(s):
        continue
    for r in range(s + 1, max(s * s, 1000 // (s * s) + 1)):
        if is_prime(r) and (r - 1) % s == 0:
            k = s * s * r
            if (s * s - s + 1) % r:
                if k <= 1000:
                    covered.append(k)
            else:
                exc.append((k, s, r, k1_step(s, r)[:1]))
print("k = s^2 r <= 1000 covered by A7.5 (main part):", sorted(covered))
print("exceptions (k, s, r, first k+1 hit):")
for e in exc:
    print(" ", e)
