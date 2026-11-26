"""Test whether the top term dominates 2-adically in the OEIS A402341 formula
a(n) = Sum_{m == n (2)} c(n,m) * C(m, floor(m/2)),  c(n,m) = [u^m] f(u)^n,
f(u) = u(u^2-2)(u^4-4u^2+2)(u^8-8u^6+20u^4-16u^2+2).
For even n, reports the m < 15n whose term has v_2 <= s_2(15n/2) (the top
term m = 15n has v_2 exactly s_2(15n/2)).  Usage: python -I dominant_term.py [N]
"""
import sys
from math import comb

def mul(a, b):
    r = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    r[i + j] += x * y
    return r

def v2(m):
    return (m & -m).bit_length() - 1 if m else 10**9

f = [1]
for g in ([0, 1], [-2, 0, 1], [2, 0, -4, 0, 1], [2, 0, -16, 0, 20, 0, -8, 0, 1]):
    f = mul(f, g)
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
P = [1]
bad = 0
for n in range(1, N + 1):
    P = mul(P, f)
    total = sum(P[m] * comb(m, m // 2) for m in range(len(P)))
    h = 15 * n // 2
    assert total == sum((-1) ** j * comb(n, j) * comb(n - 1 + h - 16 * j, n - 1)
                        for j in range(h // 16 + 1)), n
    if n % 2:
        continue
    s = bin(15 * n // 2).count("1")
    assert v2(total) == s, n
    low = [(m, v2(P[m] * comb(m, m // 2))) for m in range(15 * n)
           if P[m] and v2(P[m] * comb(m, m // 2)) <= s]
    margin = min(v2(P[m] * comb(m, m // 2)) for m in range(15 * n) if P[m]) - s
    bad += bool(low)
    print(n, "s=", s, "min excess over s of terms m < 15n:", margin,
          "competing:", low[:4])
print("even n <=", N, "with a competing term:", bad)
