"""Independent checker for the YES lines of the scan output.

Usage:  python check_colourings.py out/scan_*.txt

Each YES line reads
    n YES dims=d1,d2,... primes=p:t1,t2,...;p:...  nodes=.. secs=..
and claims: the homomorphism phi from the positive integers under
multiplication to G = Z_d1 x Z_d2 x ... defined by the listed images of the
primes p <= n/2 can be completed (choosing images of the primes in (n/2, n])
to a bijection {1..n} -> G.

This script shares no code with the search.  It
  1. checks |G| = n,
  2. computes phi(x) for all x <= n having only listed prime factors, by trial
     division, and checks these values are pairwise distinct,
  3. gives the primes in (n/2, n] the unused group elements (in sorted order)
     and checks phi is then a bijection {1..n} -> G,
  4. checks, straight from the definition of an n-satisfactory colouring, that
     a, 2a, ..., na get pairwise different colours for every a <= ABOUND, where
     primes > n are sent to 0.
It prints the completed prime images to stdout if --dump is given.
"""
import sys
from itertools import product
from math import prod

ABOUND = 3000


def factorise(x):
    f = {}
    d = 2
    while d * d <= x:
        while x % d == 0:
            f[d] = f.get(d, 0) + 1
            x //= d
        d += 1
    if x > 1:
        f[x] = f.get(x, 0) + 1
    return f


def check_line(line, dump=False):
    parts = line.split()
    n = int(parts[0])
    dims = primes_field = None
    for tok in parts[2:]:
        if tok.startswith("dims="):
            dims = tuple(int(v) for v in tok[5:].split(","))
        elif tok.startswith("primes="):
            primes_field = tok[7:]
    assert prod(dims) == n, "group order"
    img = {}
    if primes_field:
        for item in primes_field.split(";"):
            p, t = item.split(":")
            t = tuple(int(v) for v in t.split(","))
            assert len(t) == len(dims) and all(0 <= a < d for a, d in zip(t, dims))
            img[int(p)] = t
    zero = tuple(0 for _ in dims)

    def phi(x):
        acc = list(zero)
        for p, e in factorise(x).items():
            if p > n:
                continue  # primes > n go to 0
            t = img[p]
            for i, d in enumerate(dims):
                acc[i] = (acc[i] + e * t[i]) % d
        return tuple(acc)

    # step 2
    smooth = [x for x in range(1, n + 1) if all(p in img for p in factorise(x))]
    vals = {}
    for x in smooth:
        v = phi(x)
        assert v not in vals, f"n={n}: phi({x}) = phi({vals.get(v)})"
        vals[v] = x
    # step 3
    rest = [x for x in range(1, n + 1) if x not in set(smooth)]
    for x in rest:
        f = factorise(x)
        assert list(f.items()) == [(x, 1)] and 2 * x > n, f"n={n}: unexpected unlisted {x}"
    free = sorted(set(product(*[range(d) for d in dims])) - set(vals))
    assert len(free) == len(rest)
    for x, v in zip(rest, free):
        img[x] = v
    image = {phi(x) for x in range(1, n + 1)}
    assert len(image) == n, f"n={n}: not a bijection"
    # step 4
    for a in range(1, ABOUND + 1):
        cols = {phi(a * i) for i in range(1, n + 1)}
        assert len(cols) == n, f"n={n}: a={a} fails"
    if dump:
        print(n, "dims=" + ",".join(map(str, dims)),
              " ".join(f"{p}:{','.join(map(str, img[p]))}" for p in sorted(img)))
    return n


def main():
    dump = "--dump" in sys.argv
    files = [a for a in sys.argv[1:] if not a.startswith("--")]
    yes, no = [], []
    for fn in files:
        with open(fn) as fh:
            for line in fh:
                parts = line.split()
                if len(parts) < 2:
                    continue
                if parts[1] == "YES":
                    yes.append(check_line(line, dump))
                elif parts[1] == "NO":
                    no.append(int(parts[0]))
    yes.sort()
    no.sort()
    print(f"verified {len(yes)} multiplicative colourings (bijection + definition check for a <= {ABOUND})")
    print("n with verified colouring: min", min(yes) if yes else None, "max", max(yes) if yes else None)
    missing = [x for x in range(1, (max(yes + no) if yes + no else 0) + 1) if x not in set(yes) and x not in set(no)]
    print("n reported NO by the search (not verified by this script):", no)
    print("n missing from the files:", missing)


if __name__ == "__main__":
    main()
