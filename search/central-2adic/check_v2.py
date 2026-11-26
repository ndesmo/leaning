"""Numerical check of the OEIS A402341 2-adic conjecture and analogues.

a_q(n) = coefficient of x^floor((q-1)n/2) in (1 + x + ... + x^(q-1))^n.
Conjecture (A402341, q = 16): for even n, v_2(a_16(n)) = s_2(15n/2).

Method: P_n = P_{n-1} * (1 - x^q) / (1 - x), i.e. subtract the q-shift and take
prefix sums, all mod 2^K and truncated at degree floor((q-1)N/2) (coefficients
of degree <= c of P_n depend only on those of degree <= c of P_{n-1}).
v_2 is read off the residue; a residue of 0 mod 2^K is reported as ">= K".
Cross-checks: exact alternating-sum formula (OEIS A273975 / A402341) at
sampled n, and the A402341 b-file (n <= 829) if its path is given.

Usage: python -I check_v2.py [N] [q ...] [--bfile PATH]
"""
import sys
from itertools import accumulate
from math import comb

K = 48
MASK = (1 << K) - 1


def s2(m):
    return bin(m).count("1")


def v2(m, cap=None):
    if m == 0:
        return cap
    return (m & -m).bit_length() - 1


def exact(q, n):
    """Exact a_q(n) by Sum_j (-1)^j C(n,j) C(n-1+h-qj, n-1), h = floor((q-1)n/2)."""
    if n == 0:
        return 1
    h = (q - 1) * n // 2
    return sum((-1) ** j * comb(n, j) * comb(n - 1 + h - q * j, n - 1)
               for j in range(h // q + 1))


def residues(q, N):
    """Return list r[n] = a_q(n) mod 2^K for n = 0..N."""
    cmax = (q - 1) * N // 2
    P = [1] + [0] * cmax
    out = [1]
    for n in range(1, N + 1):
        top = min((q - 1) * n, cmax)
        # Q = P*(1 - x^q) on degrees 0..top, then prefix sums
        Q = P[:top + 1]
        for i in range(top, q - 1, -1):
            Q[i] -= Q[i - q]
        P = [x & MASK for x in accumulate(Q)] + [0] * (cmax - top)
        out.append(P[(q - 1) * n // 2])
    return out


def main(argv):
    bfile = None
    if "--bfile" in argv:
        i = argv.index("--bfile")
        bfile = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    N = int(argv[0]) if argv else 2000
    qs = [int(a) for a in argv[1:]] or [16, 4, 8]
    for q in qs:
        r = residues(q, N)
        # cross-check against exact formula at sampled n
        sample = sorted(set(list(range(0, min(N, 200) + 1)) +
                            list(range(0, N + 1, max(1, N // 20))) + [N]))
        bad = [n for n in sample if exact(q, n) & MASK != r[n]]
        print(f"q={q} N={N}: exact-formula cross-check at {len(sample)} n: "
              f"{'OK' if not bad else 'MISMATCH ' + str(bad[:10])}")
        if q == 16 and bfile:
            nb = 0
            with open(bfile) as f:
                for line in f:
                    parts = line.split()
                    if len(parts) == 2 and not line.startswith("#"):
                        n, a = int(parts[0]), int(parts[1])
                        if n <= N:
                            assert a & MASK == r[n], n
                            nb += 1
            print(f"  b-file cross-check: {nb} terms agree mod 2^{K}")
        even_fail, sat = [], []
        dist = {}
        for n in range(0, N + 1):
            c = (q - 1) * n // 2
            v = v2(r[n])
            if v is None:
                sat.append(n)
                continue
            d = v - s2(c)
            if n % 2 == 0:
                if d != 0:
                    even_fail.append((n, v, s2(c)))
            else:
                dist[d] = dist.get(d, 0) + 1
        print(f"  even n <= {N}: v_2 = s_2((q-1)n/2) fails at "
              f"{len(even_fail)} n; first: {even_fail[:8]}")
        print(f"  residue 0 mod 2^{K} (undetermined) at: {sat[:8]}")
        print(f"  odd n: distribution of v_2 - s_2(floor((q-1)n/2)): "
              f"{dict(sorted(dist.items()))}")
        odd_small = [(n, v2(r[n]) - s2((q - 1) * n // 2)) for n in range(1, 64, 2)]
        print(f"  odd n < 64, (n, diff): {odd_small}")


if __name__ == "__main__":
    main(sys.argv[1:])
