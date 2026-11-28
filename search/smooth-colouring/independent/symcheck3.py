# symcheck3.py n p level [threads] : symcheck.py adapted to dfs3 --level (group U(Z_{p^{i+1}}) x U(Z_K)).
# Original: exact test of dfs2's lex-leader symmetry breaking.
# Runs dfs2_dump.exe --all with and without symmetry, then checks that the symmetric solution set is
# exactly the set of lex-minimal orbit representatives (under U(Z_{p^2}) x U(Z_K), as in dfs2) of the
# no-symmetry solution set.  Solutions are small-prime assignments, element index e = h*K + f.
import subprocess, sys, os
from math import gcd
n, p, lv = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]); th = sys.argv[4] if len(sys.argv) > 4 else "4"
K, p2 = n // p, p ** (lv + 1)
def run(extra):
    o = subprocess.run([os.environ.get("DFS3_EXE", "./dfs3.exe"), str(n), str(p), "--level", str(lv), "--threads", th, "--split", "2", "--all"] + extra,
                       capture_output=True, text=True, timeout=580).stdout
    sols = {tuple(map(int, l.split()[1:])) for l in o.splitlines() if l.startswith("SOL")}
    res = [l for l in o.splitlines() if l.startswith("dfs3")][0]
    return sols, res
S, rs = run([]); N, rn = run(["--nosym"])
gam = [(u, v) for u in range(1, p2) if gcd(u, p2) == 1 for v in (range(K) if K > 1 else [1]) if K == 1 or gcd(v, K) == 1]
act = lambda g, e: ((g[0] * (e // K)) % p2) * K + (g[1] * (e % K)) % K
lexmin = {min(tuple(act(g, e) for e in s) for g in gam) for s in N}
orbit_sizes = sum(len({tuple(act(g, e) for e in s) for g in gam}) for s in S)
closed = all(tuple(act(g, e) for e in s) in N for s in list(N)[:2000] for g in gam)
ok = (S == lexmin) and orbit_sizes == len(N) and S <= N and closed
print(f"symcheck3 level={lv} n={n} p={p} K={K} |Gamma|={len(gam)} sym_sols={len(S)} nosym_sols={len(N)} "
      f"orbits_of_nosym={len(lexmin)} sum_orbit_sizes(sym)={orbit_sizes} nosym_closed={closed} "
      f"{'PASS' if ok else 'FAIL'}")
print("  sym  :", rs); print("  nosym:", rn)
