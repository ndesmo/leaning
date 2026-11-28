"""Shared helpers: finite abelian group Z_{d1} x ... x Z_{dr} with elements as ints (mixed radix)."""
import itertools
from math import gcd
from functools import reduce

def lcm(a, b): return a * b // gcd(a, b)

class Group:
    def __init__(self, dims):
        self.dims = tuple(dims)
        self.els = list(itertools.product(*[range(d) for d in dims]))
        self.N = len(self.els)
        self.idx = {e: i for i, e in enumerate(self.els)}
        N = self.N
        self.add = [[self.idx[tuple((a + b) % d for a, b, d in zip(x, y, dims))] for y in self.els] for x in self.els]
        self.neg = [self.idx[tuple((-a) % d for a, d in zip(x, dims))] for x in self.els]
        self.L = reduce(lcm, dims, 1)
        # all homs H -> Z_L (characters), as value tables
        self.chars = []
        for rs in itertools.product(*[range(d) for d in dims]):
            vals = [sum(xi * ri * (self.L // di) for xi, ri, di in zip(x, rs, dims)) % self.L for x in self.els]
            self.chars.append(vals)
        self.order = []
        for i in range(N):
            k, x = 1, i
            while x != 0:
                x = self.add[x][i]; k += 1
            self.order.append(k)
    def sub(self, a, b): return self.add[a][self.neg[b]]
    def mask(self, S):
        m = 0
        for s in S: m |= 1 << s
        return m
    def periods(self, S):
        """nonzero g with S + g = S"""
        Sset = set(S)
        return [g for g in range(1, self.N) if all(self.add[s][g] in Sset for s in S)]
    def complements(self, B, cap=None):
        """all C with 0 in C and C (+) B = G (exact cover by translates c + B). Assumes 0 in B."""
        N = self.N
        full = (1 << N) - 1
        shm = [self.mask([self.add[c][b] for b in B]) for c in range(N)]
        negB = [self.neg[b] for b in B]
        out = []
        C = [0]
        def rec(cov):
            if cov == full:
                out.append(tuple(sorted(C))); return cap is not None and len(out) >= cap
            g = (~cov & (cov + 1)).bit_length() - 1  # lowest uncovered
            for nb in negB:
                c = self.add[g][nb]
                m = shm[c]
                if m & cov: continue
                C.append(c)
                if rec(cov | m): return True
                C.pop()
            return False
        rec(shm[0])
        return out
