"""Pass 10: EXHAUSTIVE test of conjecture S' on all shifted downsets of a given size.
Written from the definitions; shares no code with pass 8/9.
Shifted downset: finite T in N^k, 0 in T, closed under x -> x - e_j and x -> x - e_j + e_i (i<j).
Points are stored as nonincreasing tuples of coordinate indices (multisets), 0-based.
For every T of size p*m (all coordinates used) and EVERY homomorphism g: Z^k -> Z_m whose fibres
on T all have size p (g_0 restricted to divisors of m: unit scaling preserves the fibres),
test Gamma_p = 0 via  rank_Fp(M) == rank_Q(M)  (Gamma = Z^k/M; Gamma_p = 0 iff these ranks agree).
Only p not dividing m is tested (then S' says Gamma_p = 0).
Usage: python enum_shifted.py p m [maxT]"""
import sys, time
from fractions import Fraction

def lower_covers(x):
    out = set()
    for t in range(len(x)):
        out.add(x[:t] + x[t+1:])                      # x - e_{x[t]}
        if x[t] > 0:
            y = list(x); y[t] -= 1
            out.add(tuple(sorted(y, reverse=True)))   # x - e_j + e_{j-1}
    return out

def upper_covers(x, kmax):
    out = set()
    for j in range(kmax + 1):                          # add e_j
        out.add(tuple(sorted(x + (j,), reverse=True)))
    for t in range(len(x)):                            # shift up one step
        y = list(x); y[t] += 1
        out.add(tuple(sorted(y, reverse=True)))
    return out

def shifted_downsets(N):
    level = {frozenset([()])}
    for size in range(1, N):
        nxt = set()
        for T in level:
            kmax = max((max(x) for x in T if x), default=-1) + 1
            cand = set()
            for x in T:
                for y in upper_covers(x, kmax):
                    if y not in T and lower_covers(y) <= T:
                        cand.add(y)
            for y in cand:
                nxt.add(T | {y})
        level = nxt
    return level

def vec(x, k):
    v = [0] * k
    for i in x: v[i] += 1
    return v

def rank_mod(rows, p):
    rows = [[a % p for a in r] for r in rows]; r = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        inv = pow(rows[r][c], p - 2, p)
        rows[r] = [a * inv % p for a in rows[r]]
        for i in range(len(rows)):
            if i != r and rows[i][c]:
                f = rows[i][c]; rows[i] = [(a - f * b) % p for a, b in zip(rows[i], rows[r])]
        r += 1
    return r

def rank_Q(rows):
    rows = [[Fraction(a) for a in r] for r in rows]; r = 0
    ncol = len(rows[0]) if rows else 0
    for c in range(ncol):
        piv = next((i for i in range(r, len(rows)) if rows[i][c] != 0), None)
        if piv is None: continue
        rows[r], rows[piv] = rows[piv], rows[r]
        for i in range(r + 1, len(rows)):
            if rows[i][c] != 0:
                f = rows[i][c] / rows[r][c]; rows[i] = [a - f * b for a, b in zip(rows[i], rows[r])]
        r += 1
    return r

def all_g(V, k, m, p):
    """all g in Z_m^k with every fibre on V of size exactly p"""
    by_last = [[] for _ in range(k)]; base = 0
    for v in V:
        nz = [i for i in range(k) if v[i]]
        if nz: by_last[nz[-1]].append(v)
        else: base += 1
    g = [0] * k; cnt = [0] * m; cnt[0] = base
    if base > p: return
    divs = [d for d in range(m) if d == 0 or m % d == 0]
    def rec(i):
        if i == k:
            yield list(g); return
        for a in (divs if i == 0 else range(m)):
            g[i] = a; added = []; ok = True
            for v in by_last[i]:
                s = sum(gi * vi for gi, vi in zip(g, v)) % m
                cnt[s] += 1; added.append(s)
                if cnt[s] > p: ok = False; break
            if ok: yield from rec(i + 1)
            for s in added: cnt[s] -= 1
    yield from rec(0)

def main():
    p, m = int(sys.argv[1]), int(sys.argv[2]); assert m % p != 0
    t0 = time.time(); Ts = shifted_downsets(p * m)
    nT = pairs = viol = 0
    for T in sorted(Ts, key=lambda s: sorted(s)):
        k = max((max(x) for x in T if x), default=-1) + 1
        V = [vec(x, k) for x in T]; nT += 1
        for g in all_g(V, k, m, p):
            fib = {}
            for v in V: fib.setdefault(sum(a * b for a, b in zip(g, v)) % m, []).append(v)
            rows = [[a - b for a, b in zip(y, B[0])] for B in fib.values() for y in B[1:]]
            pairs += 1
            if rank_mod(rows, p) != rank_Q(rows):
                viol += 1
                if viol <= 3: print("VIOLATION", sorted(T), g, flush=True)
    print(f"p={p} m={m} |T|={p*m} shifted_downsets={nT} pairs(T,g)={pairs} violations={viol} time={time.time()-t0:.1f}s")

if __name__ == "__main__":
    main()
