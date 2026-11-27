"""firstcheck3.py n p level : test of dfs3 --nosym --first REPS (pass 8). Checks that the --first solution set
equals {s in nosym set : s[0] in REPS} and that its Gamma-closure is the whole nosym solution set."""
import subprocess, sys
from math import gcd
n, p, lv = map(int, sys.argv[1:4]); K, Q = n // p, p ** (lv + 1)
reps = subprocess.run([sys.executable, "orbit_reps3.py", str(n), str(p), str(lv)], capture_output=True, text=True).stdout.strip()
def run(extra):
    o = subprocess.run(["./dfs3.exe", str(n), str(p), "--level", str(lv), "--threads", "8", "--split", "2", "--all", "--nosym"] + extra,
                       capture_output=True, text=True, timeout=580).stdout
    return {tuple(map(int, l.split()[1:])) for l in o.splitlines() if l.startswith("SOL")}, [l for l in o.splitlines() if l.startswith("dfs3")][0]
N, rn = run([]); R, rr = run(["--first", reps]); rs = set(map(int, reps.split(",")))
gam = [(u, v) for u in range(1, Q) if gcd(u, Q) == 1 for v in (range(K) if K > 1 else [1]) if K == 1 or gcd(v, K) == 1]
act = lambda g, e: ((g[0] * (e // K)) % Q) * K + (g[1] * (e % K)) % K
clos = {tuple(act(g, e) for e in s) for s in R for g in gam}
ok = R == {s for s in N if s[0] in rs} and clos == N
print(f"firstcheck3 level={lv} n={n} p={p} nosym={len(N)} first={len(R)} closure={len(clos)} {'PASS' if ok else 'FAIL'}")
