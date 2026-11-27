"""Pass 12 driver: per-n level conjecture.  For each (n, p), p | n, p < n, run dfs3 at levels
0, 1, ..., v_p(n/p)+2 (stop at first FOUND); level i = dfs3 --level i (G = Z_{p^{i+1}} x Z_{n/p});
level 0 = multiplicative colouring into Z_p x Z_{n/p}.  Every FOUND witness is checked by
independent/direct_check3.py.  Usage: python pern.py OUTFILE WORKERS THREADS TIMEOUT n1 n2 ... |
range:a:b"""
import sys, subprocess, os, json, threading
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
IND = os.path.normpath(os.path.join(HERE, '..', '..', 'independent'))
DFS = os.path.join(IND, 'dfs3.exe'); CHK = os.path.join(IND, 'direct_check3.py')
out, workers, threads, to = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
ns = []
for a in sys.argv[5:]:
    if a.startswith('range:'): _, x, y = a.split(':'); ns += list(range(int(x), int(y) + 1))
    else: ns.append(int(a))
def primes_div(n): return [q for q in range(2, n) if n % q == 0 and all(q % r for r in range(2, q))]
def vp(m, p):
    v = 0
    while m % p == 0: m //= p; v += 1
    return v
lock = threading.Lock()
def run1(n, p, lv):
    w = os.path.join(HERE, 'w', f'w_{n}_{p}_L{lv}.json')
    if os.path.exists(w): os.remove(w)
    cmd = [DFS, str(n), str(p), '--level', str(lv), '--threads', str(threads), '--split', '2', '--out', w]
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=to)
        line = [l for l in r.stdout.splitlines() if l.startswith('dfs3 ')]
        line = line[0] if line else 'ERROR ' + r.stderr[-200:]
    except subprocess.TimeoutExpired:
        return 'TIMEOUT', f'timeout {to}s'
    res = 'FOUND' if 'result=FOUND' in line else 'NONE' if 'result=NONE' in line else 'ERR'
    if res == 'FOUND':
        c = subprocess.run([sys.executable, CHK, w], capture_output=True, text=True)
        chk = c.stdout.strip() or ('CHECKFAIL ' + c.stderr[-200:])
        if 'DIRECT3 OK' not in chk: res = 'CHECKFAIL'
        line += ' | ' + chk
    return res, line
def job(np_):
    n, p = np_; v = vp(n // p, p); per = []; minlv = None
    for lv in range(0, v + 3):
        res, line = run1(n, p, lv); per.append(f'L{lv}={res}')
        with lock:
            with open(out, 'a') as f: f.write(f'RUN n={n} p={p} L{lv} {res} :: {line}\n')
        if res == 'FOUND': minlv = lv; break
    s = f'SUMMARY n={n} p={p} v={v} ' + ' '.join(per) + f' min={minlv if minlv is not None else "?"}'
    if minlv is not None and minlv > v: s += ' **EXCEEDS v**'
    with lock:
        with open(out, 'a') as f: f.write(s + '\n')
        print(s, flush=True)
tasks = [(n, p) for n in ns for p in primes_div(n)]
with ThreadPoolExecutor(workers) as ex: list(ex.map(job, tasks))
