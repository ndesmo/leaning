"""Independent CP-SAT solver (shares no code with gtile*.rs).
Question: does a completely multiplicative phi=(h,f): [n] -> Z_{p^2} x Z_K, K=n/p, exist
that is injective on [n] and such that for every g in Z_K the fibre
{h(m): m<=n, f(m)=g} is exactly a coset c_g + pZ_{p^2}?
Usage: python cpsat_coset.py n p [timeout_s] [--nosym] [--out witness.json]
Symmetry (optional, default on): units of Z_{p^2} act on h, units of Z_K act on f; both
preserve injectivity and the coset-fibre property, so WLOG h(2) in {0,1,p} and
f(2) | K (f(2) = gcd representative of its unit orbit)."""
import sys, json, time
from ortools.sat.python import cp_model

args = [a for a in sys.argv[1:] if not a.startswith("--")]
n, p = int(args[0]), int(args[1]); T = float(args[2]) if len(args) > 2 else 3600
nosym = "--nosym" in sys.argv
out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
assert n % p == 0; K = n // p; P2 = p * p
primes = [q for q in range(2, n + 1) if all(q % r for r in range(2, int(q**.5) + 1))]
def fac(m):
    e = {}
    for q in primes:
        while m % q == 0: e[q] = e.get(q, 0) + 1; m //= q
    return e
E = {m: fac(m) for m in range(1, n + 1)}
# --reduce: primes q > n/2 occur only as m=q. Drop them: the remaining n-L values must be
# injective with <= p per fibre and constant residue per fibre; any such partial map extends
# (complete each fibre to its coset / pick any coset for an empty fibre; exactly L free slots
# remain since |G-slots| = pK = n), assigning the large primes to the free slots.
RED = "--reduce" in sys.argv
if RED:
    big = [q for q in primes if 2 * q > n]; primes = [q for q in primes if 2 * q <= n]
    E = {m: e for m, e in E.items() if not (len(e) == 1 and list(e)[0] in big)}
MS = sorted(E)

M = cp_model.CpModel()
h = {q: M.NewIntVar(0, P2 - 1, f"h{q}") for q in primes}
f = {q: M.NewIntVar(0, K - 1, f"f{q}") for q in primes}
H, F, R = {}, {}, {}
for m in MS:
    e = E[m]
    if m == 1:
        H[m] = M.NewConstant(0); F[m] = M.NewConstant(0); R[m] = M.NewConstant(0); continue
    if len(e) == 1 and list(e.values())[0] == 1:
        q = list(e)[0]; H[m] = h[q]; F[m] = f[q]
    else:
        sh = sum(k * h[q] for q, k in e.items()); sf = sum(k * f[q] for q, k in e.items())
        ubh = sum(k * (P2 - 1) for k in e.values()); ubf = sum(k * (K - 1) for k in e.values())
        th = M.NewIntVar(0, ubh // P2, f"th{m}"); tf = M.NewIntVar(0, ubf // K, f"tf{m}")
        H[m] = M.NewIntVar(0, P2 - 1, f"H{m}"); F[m] = M.NewIntVar(0, K - 1, f"F{m}")
        M.Add(H[m] == sh - P2 * th); M.Add(F[m] == sf - K * tf)
    R[m] = M.NewIntVar(0, p - 1, f"R{m}"); s = M.NewIntVar(0, p - 1, f"s{m}")
    M.Add(H[m] == p * s + R[m])          # R = H mod p, s = H div p
# injectivity
M.AddAllDifferent([F[m] * P2 + H[m] for m in MS])
# fibres: exactly p per fibre, constant residue mod p (with injectivity => full coset)
c = [M.NewIntVar(0, p - 1, f"c{g}") for g in range(K)]
M.Add(c[0] == 0)  # 1 is in fibre 0 with h=0
for g in range(K):
    bs = []
    for m in MS:
        b = M.NewBoolVar(f"b{m}_{g}")
        M.Add(F[m] == g).OnlyEnforceIf(b); M.Add(F[m] != g).OnlyEnforceIf(b.Not())
        M.Add(R[m] == c[g]).OnlyEnforceIf(b); bs.append(b)
    M.Add(sum(bs) <= p) if RED else M.Add(sum(bs) == p)
if not nosym:
    M.AddAllowedAssignments([h[2]], [[0], [1], [p]])
    M.AddAllowedAssignments([f[2]], [[d % K] for d in range(1, K + 1) if K % d == 0])
S = cp_model.CpSolver(); S.parameters.max_time_in_seconds = T; import os; S.parameters.num_workers = int(os.environ.get("WORKERS", "22"))
if "--count" in sys.argv:
    class CB(cp_model.CpSolverSolutionCallback):
        def __init__(s): super().__init__(); s.k = 0
        def on_solution_callback(s): s.k += 1
    S.parameters.num_workers = 1; S.parameters.enumerate_all_solutions = True; cb = CB()
    st = S.Solve(M, cb); print(f"COUNT n={n} p={p} status={S.StatusName(st)} count={cb.k}"); sys.exit()
t0 = time.time(); st = S.Solve(M); dt = time.time() - t0
name = S.StatusName(st)
res = {"FEASIBLE": "EXISTS", "OPTIMAL": "EXISTS", "INFEASIBLE": "NONE(proved)"}.get(name, "TIMEOUT/UNKNOWN")
print(f"n={n} p={p} K={K} sym={not nosym} reduce={RED} status={name} -> {res} wall={dt:.1f}s")
if name in ("FEASIBLE", "OPTIMAL"):
    sol = {q: [S.Value(h[q]), S.Value(f[q])] for q in primes}
    if RED:  # fill big primes into free slots
        used = {(S.Value(H[m]), S.Value(F[m])) for m in MS}; free = []
        for g in range(K):
            rs = {S.Value(H[m]) % p for m in MS if S.Value(F[m]) == g}; r = rs.pop() if rs else 0
            free += [(r + p * j, g) for j in range(p) if (r + p * j, g) not in used]
        assert len(free) == len(big); sol.update({q: list(v) for q, v in zip(big, free)})
    line = " ".join(f"{q}:{a}/{b}" for q, (a, b) in sol.items())
    print("SOL", line)
    if out: json.dump({"n": n, "p": p, "K": K, "dims": [P2, K], "phi": sol}, open(out, "w"))
