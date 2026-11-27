"""Check for notes/weakly-consecutive.md, A7.4 (issue #68): k = 4r, r an odd prime.

Backtracking search (same pairwise test as wc_slice_check.py: gcd(sigma(i), |i - j|) | sigma(j),
equivalent to Def. 1.1 of GSK24) for a WCS of length k = 4r with sigma(1) = 2**alpha
(alpha = 1, 2) and sigma(k) = r. By A6.2 and reversal these are the only end pairs an interior 1
can have for k = 4r, so "no solution" means no WCS of length 4r has an interior 1.
Expected: no solution for every r (A7.4 proves this for r >= 5; r = 3 is k = 12, Lean k <= 16).

Run: python -I search/weakly-consecutive/wc_4r_check.py [r ...]   (default r = 3, 5, 7; r = 11 did
not finish in 5 minutes with this plain backtracking)
"""
from math import gcd
import sys
import time

RS = [int(a) for a in sys.argv[1:]] or [3, 5, 7]


def search(k, first, last):
    seq = [0] * (k + 1)
    used = [False] * (k + 1)
    seq[1], seq[k] = first, last
    used[first] = used[last] = True
    placed = [1, k]

    def ok(i, v):
        for j in placed:
            w, dist = seq[j], abs(i - j)
            if w % gcd(v, dist) or v % gcd(w, dist):
                return False
        return True

    if first % gcd(last, k - 1) or last % gcd(first, k - 1):
        return None

    def rec(i):
        if i == k:
            return list(seq[1:])
        for v in range(1, k + 1):
            if not used[v] and ok(i, v):
                used[v] = True
                seq[i] = v
                placed.append(i)
                res = rec(i + 1)
                if res:
                    return res
                placed.pop()
                used[v] = False
        return None

    return rec(2)


if __name__ == "__main__":
    for r in RS:
        k = 4 * r
        for alpha in (1, 2):
            t = time.time()
            res = search(k, 2 ** alpha, r)
            print(f"k={k} (r={r}) sigma(1)={2**alpha} sigma(k)={r}: "
                  f"{'FOUND ' + str(res) if res else 'no WCS'} ({time.time() - t:.1f}s)", flush=True)
