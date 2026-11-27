"""Checks for notes/weakly-consecutive.md, section A7 (issue #68).

1. Enumerates every weakly consecutive sequence (WCS) of length k <= KMAX by backtracking with
   the test gcd(sigma(i), |i - j|) | sigma(j) (equivalent to Def. 1.1 of GSK24), and checks the
   general form of the slice lemma A7.1 on each: if d = sigma(1) >= 2 and k/d >= 2 then
   sigma(k - d + 1) = d*e with e | k/d, e >= 2, and gcd(sigma(k - d + 1), sigma(k)) | d - 1;
   plus the mirror statement for d' = sigma(k).
2. Lists the k <= LIST with exactly two distinct prime factors and says which are covered by
   Theorem A7.2 (k = r * s^b, r, s distinct primes, b >= 1, s does not divide r - 1).

Run: python -I tools/wc_slice_check.py
"""
from math import gcd

KMAX = 20
LIST = 100


def wcs(k):
    out, seq, used = [], [], [False] * (k + 1)

    def rec():
        i = len(seq) + 1
        if i > k:
            out.append(tuple(seq))
            return
        for v in range(1, k + 1):
            if used[v]:
                continue
            ok = True
            for j0, w in enumerate(seq):
                dist = i - (j0 + 1)
                if w % gcd(v, dist) or v % gcd(w, dist):
                    ok = False
                    break
            if ok:
                used[v] = True
                seq.append(v)
                rec()
                seq.pop()
                used[v] = False

    rec()
    return out


def slice_ok(s, k):
    d = s[0]
    if d < 2 or k // d < 2:
        return True
    assert k % d == 0  # A6.1 corollary
    x = s[k - d]  # position k - d + 1
    if x % d:
        return False
    e = x // d
    return e >= 2 and (k // d) % e == 0 and (d - 1) % gcd(x, s[-1]) == 0


def factor(n):
    f, p = {}, 2
    while p * p <= n:
        while n % p == 0:
            f[p] = f.get(p, 0) + 1
            n //= p
        p += 1
    if n > 1:
        f[n] = f.get(n, 0) + 1
    return f


def covered(k):
    f = factor(k)
    if len(f) != 2:
        return None
    (p, a), (q, b) = f.items()
    # r = the prime with exponent 1, s = the other prime; need s not dividing r - 1
    return (a == 1 and (p - 1) % q != 0) or (b == 1 and (q - 1) % p != 0)


if __name__ == "__main__":
    for k in range(1, KMAX + 1):
        L = wcs(k)
        bad = [s for s in L if not slice_ok(s, k) or not slice_ok(s[::-1], k)]
        interior = [s for s in L if s[0] != 1 and s[-1] != 1]
        print(f"k={k:2d} N={len(L):2d} slice-lemma failures={len(bad)} interior-1={len(interior)}")
    cov = [k for k in range(2, LIST + 1) if covered(k)]
    unc = [k for k in range(2, LIST + 1) if covered(k) is False]
    print("two prime factors, covered by A7.2:", cov)
    print("two prime factors, not covered:", unc)
