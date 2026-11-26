"""N5 check (notes/central-2adic.md): for even n <= N and 1 <= t <= n,
t + v2(C(n,t)) + s2(3n/2 - t) > s2(3n/2).  Usage: python -I carry_q4.py [N]"""
import sys
from math import comb

def v2(x):
    return (x & -x).bit_length() - 1

def s2(x):
    return bin(x).count("1")

N = int(sys.argv[1]) if len(sys.argv) > 1 else 2000
bad = [(n, t) for n in range(2, N + 1, 2) for t in range(1, n + 1)
       if not t + v2(comb(n, t)) + s2(3 * n // 2 - t) > s2(3 * n // 2)]
print("violations:", len(bad), bad[:10])
