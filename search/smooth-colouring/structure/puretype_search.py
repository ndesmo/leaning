"""Pure-type question search (pass 3).

Find weights w_p in Z_N (p prime <= 195, N a {3,5,13}-number) such that the multiset
phi(m) = sum_p v_p(m) w_p mod N, m = 1..195, is a nonnegative union of polygons
(cosets of the order-p subgroups of Z_N, p in {3,5,13}) with polygon counts
(a, b, c) chosen so that at least two of A_3, A_5, A_13 are forced nonzero.

For N = 195 = 3*5*13: x -> 3x kills the Z_3 part and is bijective on the rest, so a 5- or
13-polygon stays a polygon (sum 0) and each 3-polygon collapses to 3 copies of one point of
3Z_N ~ mu_65.  Hence A_3 = 3 * sum_{3-polygons} zeta^{3x}, a sum of a points of mu_65; it is
nonzero whenever a is not of the form 5i+13j.  Similarly for A_5 (b not of form 3i+13j) and
A_13 (c not of form 3i+5j).  The solution is re-verified independently by puretype_check.py.

usage: python puretype_search.py [a b c] [seed]
"""
import sys, json
from ortools.sat.python import cp_model

N = 195
M = 195
primes = [p for p in range(2, M + 1) if all(p % q for q in range(2, int(p ** .5) + 1))]
def vp(m, p):
    e = 0
    while m % p == 0:
        m //= p; e += 1
    return e

def solve(a, b, c, seed=0, tlimit=300):
    md = cp_model.CpModel()
    w = {p: md.NewIntVar(0, N - 1, f"w{p}") for p in primes}
    y = {}
    phi = {}
    for m in range(1, M + 1):
        vs = {p: vp(m, p) for p in primes if m % p == 0}
        ph = md.NewIntVar(0, N - 1, f"phi{m}")
        if m == 1:
            md.Add(ph == 0)
        else:
            s = sum(e * w[p] for p, e in vs.items())
            tot = sum(vs.values())
            q = md.NewIntVar(0, tot, f"q{m}")
            md.Add(ph == s - N * q)
        phi[m] = ph
        row = [md.NewBoolVar(f"y{m}_{x}") for x in range(N)]
        md.AddExactlyOne(row)
        md.Add(ph == sum(x * row[x] for x in range(N)))
        y[m] = row
    # polygons
    polys = []
    for p in (3, 5, 13):
        step = N // p
        for r in range(step):
            polys.append((p, r, md.NewIntVar(0, M, f"P{p}_{r}")))
    for x in range(N):
        cov = [v for (p, r, v) in polys if x % (N // p) == r]
        md.Add(sum(y[m][x] for m in range(1, M + 1)) == sum(cov))
    md.Add(sum(v for (p, r, v) in polys if p == 3) == a)
    md.Add(sum(v for (p, r, v) in polys if p == 5) == b)
    md.Add(sum(v for (p, r, v) in polys if p == 13) == c)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = tlimit
    sv.parameters.num_workers = 16
    sv.parameters.random_seed = seed
    st = sv.Solve(md)
    print("status", sv.StatusName(st), "time", sv.WallTime())
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {p: sv.Value(w[p]) for p in primes}
    return None

if __name__ == "__main__":
    a, b, c = (int(t) for t in sys.argv[1:4]) if len(sys.argv) >= 4 else (1, 2, 14)
    seed = int(sys.argv[4]) if len(sys.argv) >= 5 else 0
    assert 3 * a + 5 * b + 13 * c == M
    sol = solve(a, b, c, seed)
    if sol:
        out = f"cert_N{N}_{a}_{b}_{c}.json"
        json.dump({"N": N, "a": a, "b": b, "c": c, "w": {str(p): v for p, v in sol.items()}},
                  open(out, "w"), indent=0)
        print("wrote", out, sol)
