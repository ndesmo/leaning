# Resumable parallel driver for gtile: one line per B class in out/m3_pass2_<tag>.txt.
# Usage: python pass2.py <tag> <dims> <classfile> <limit> <jobs> <exe>
import sys, subprocess, os, concurrent.futures as cf, threading
tag, dims, cls, limit, jobs, exe = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], int(sys.argv[5]), sys.argv[6]
d = [int(x) for x in dims.split(',')]
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out', f'm3_pass2_{tag}.txt')
done = set()
if os.path.exists(out):
    for l in open(out):
        if 'result=' in l and 'TIMEOUT' not in l: done.add(l.split('B=')[1].split()[0])
        if 'SKIP' in l: done.add(l.split('B=')[1].split()[0])
lock = threading.Lock()
def emit(s):
    with lock:
        with open(out, 'a') as f: f.write(s + '\n')
        print(s, flush=True)
def vec(s): return [int(x) for x in s.split('/')]
def addv(a, b): return [(x + y) % m for x, y, m in zip(a, b, d)]
def run(B):
    els = [vec(t) for t in B.split(',')]
    z, x, y = els
    if (addv(x, x) == y and addv(x, y) == z) or (addv(y, y) == x and addv(x, y) == z):
        emit(f'n=195 dims={d} B={B} result=SKIP-subgroup'); return
    r = subprocess.run([exe, 'n=195', f'dims={dims}', f'B={B}', 'dil=1', f'limit={limit}'], capture_output=True, text=True)
    lines = [l for l in r.stdout.splitlines() if 'result=' in l or 'solution' in l]
    for l in lines: emit(l)
    if any('EXISTS' in l for l in lines):
        with open(os.path.join(os.path.dirname(out), f'HIT_{tag}.txt'), 'a') as f: f.write('\n'.join(lines) + '\n')
todo = [l.strip()[2:] for l in open(cls) if l.strip() and l.strip()[2:] not in done]
print(len(todo), 'to run', flush=True)
with cf.ThreadPoolExecutor(jobs) as ex: list(ex.map(run, todo))
