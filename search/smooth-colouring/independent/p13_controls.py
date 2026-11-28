"""p13_controls.py MODE p level n1 n2 [timeout] [threads] : pass-13 positive controls for dfs3 (copy dfs3_p13a.exe).
MODE sym   : plain dfs3 find mode (lex-leader symmetry).
MODE genu  : dfs3 --nosym --first U, U = all elements (h,f) with h a unit mod p, for the first search
             variable.  A sound restriction (searches a subset of solutions), used to force a witness that
             is NOT a plain lift.  Every FOUND witness goes through direct_check3.py and liftcheck3.py."""
import subprocess, sys, os
mode, p, lv, n1, n2 = sys.argv[1], *map(int, sys.argv[2:6]); to = int(sys.argv[6]) if len(sys.argv) > 6 else 60
th = sys.argv[7] if len(sys.argv) > 7 else "4"; exe = "./dfs3_p13a.exe"; os.makedirs("out/p13/w", exist_ok=True)
for n in range(n1, n2 + 1, p):
    K = n // p; Q = p ** (lv + 1); f = f"out/p13/w/w_{n}_{p}_L{lv}_{mode}.json"
    if os.path.exists(f): os.remove(f)
    extra = [] if mode == "sym" else ["--nosym", "--first", ",".join(str(h * K + g) for h in range(Q) if h % p for g in range(K))]
    try:
        o = subprocess.run([exe, str(n), str(p), "--level", str(lv), "--threads", th, "--split", "2", "--out", f] + extra,
                           capture_output=True, text=True, timeout=to).stdout
        r = ([l for l in o.splitlines() if l.startswith("dfs3")] or ["NO-OUTPUT (crash?)"])[0]
    except subprocess.TimeoutExpired:
        r = f"TIMEOUT{to}s"
    print(f"{mode} {n} {p} L{lv}: {r}", flush=True)
    if "FOUND" in r:
        for c in ["direct_check3.py", "liftcheck3.py"]:
            print("   " + subprocess.run([sys.executable, c, f], capture_output=True, text=True).stdout.strip().replace("\n", "\n   "), flush=True)
