"""Independent checker [pass 13], written from the definitions (shares no code with exp2/grp/t5).
Input: json written by exp2_tn.py (fields n, p, q, dims (of H), r, B (list of H-elements), sols[].phi
with phi[i] = image of the i-th prime <= n in G = Z_dims x Z_r).
For each solution:
  1. A = phi(T_n) computed with sympy.factorint; phi injective on T_n; A (+) B' = G checked by
     computing all |A||B'| sums and requiring them distinct and |A||B'| = |G|  (B' = B x {0}).
  2. Through-G reductions, by enumerating ALL homomorphisms G -> Z_N given by generator images:
     (a)   psi: G -> Z_n bijective on A;
     (c)   u: G -> Z_{e}, e = exponent of H, and w: G -> Z_r with every w-fibre of A of size pq and
           u(fibre) a coset of the order-pq subgroup of Z_e;
     (b^s) for s in {p,q}: u: G -> Z_{e_s} (e_s = s-part of e), w: G -> Z_{n/s}, every w-fibre of A
           of size s, u injective on it with image a coset of the order-s subgroup.
Prints per-solution verdicts and a summary; asserts that they equal the stored T1/T3/T4 flags."""
import sys, json, itertools
from sympy import factorint, primerange

def homs(dims, N):
    """all homs Z_d1 x ... x Z_dk -> Z_N as generator-image tuples"""
    ch = [[x for x in range(N) if (d * x) % N == 0] for d in dims]
    return list(itertools.product(*ch))

def ev(h, g, N): return sum(a * b for a, b in zip(h, g)) % N

def main():
    d = json.load(open(sys.argv[1]))
    n, p, q, r = d['n'], d['p'], d['q'], d['r']
    Hd = list(d['dims']); Gd = Hd + [r]
    primes = list(primerange(2, n + 1))
    order = 1
    for x in Gd: order *= x
    Bp = [tuple(b) + (0,) for b in d['B']]
    e = 1
    for x in Hd: e = e * x // __import__('math').gcd(e, x)
    def spart(x, s):
        y = 1
        while x % (y * s) == 0: y *= s
        return y
    summ = {}
    for si, s in enumerate(d['sols']):
        phi = s['phi']
        A = []
        for m in range(1, n + 1):
            v = [0] * len(Gd)
            for pr, k in factorint(m).items():
                img = phi[primes.index(pr)]
                v = [(a + k * b) % D for a, b, D in zip(v, img, Gd)]
            A.append(tuple(v))
        assert len(set(A)) == n, 'phi not injective'
        sums = {tuple((a + b) % D for a, b, D in zip(x, y, Gd)) for x in A for y in Bp}
        assert len(A) * len(Bp) == order and len(sums) == order, 'not a tiling'
        # (a)
        has_a = any(len({ev(h, x, n) for x in A}) == n for h in homs(Gd, n))
        # (c)
        def coset_ok(vals, N, k):
            sub = {(N // k) * j for j in range(k)}
            v0 = vals[0]
            return len(set(vals)) == k and {(v - v0) % N for v in vals} == sub
        def red(Nu, Nw, k):
            for w in homs(Gd, Nw):
                fib = {}
                for x in A: fib.setdefault(ev(w, x, Nw), []).append(x)
                if any(len(F) != k for F in fib.values()) or len(fib) * k != n: continue
                for u in homs(Gd, Nu):
                    if all(coset_ok([ev(u, x, Nu) for x in F], Nu, k) for F in fib.values()):
                        return True
            return False
        has_c = red(e, r, p * q)
        has_bp = red(spart(e, p), n // p, p)
        has_bq = red(spart(e, q), n // q, q)
        if has_a: assert has_c
        assert (has_c, has_bp, has_bq) == (s['T1'], s['T3'], s['T4']), ('MISMATCH', si, has_c, has_bp, has_bq, s)
        key = (has_a, has_c, has_bp, has_bq)
        summ[key] = summ.get(key, 0) + 1
    print(sys.argv[1], 'all', len(d['sols']), 'tilings verified; (a,c,b^p,b^q) counts:', summ)
main()
