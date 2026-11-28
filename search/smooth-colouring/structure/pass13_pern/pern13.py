"""Pass 13 driver (pern.py of pass 12, adapted): explicit (n, p) list, one fixed level per call.
Runs independent/dfs3_pern.exe (a copy of dfs3.exe) with --log logs/L{lv}_{n}_{p}.log, so a
TIMEOUT run can be resumed with --resume on that log.  FOUND witnesses are checked with
independent/direct_check3.py and with the fresh colour_check.py (a <= 20000).
Usage: python pern13.py OUTFILE WORKERS THREADS TIMEOUT LEVEL n:p n:p ..."""
import sys, subprocess, os, threading
from concurrent.futures import ThreadPoolExecutor
HERE = os.path.dirname(os.path.abspath(__file__))
IND = os.path.normpath(os.path.join(HERE, '..', '..', 'independent'))
DFS = os.path.join(IND, 'dfs3_pern.exe'); CHK = os.path.join(IND, 'direct_check3.py')
CC = os.path.join(HERE, 'colour_check.py')
out, workers, threads, to, lv = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
pairs = [tuple(map(int, a.split(':'))) for a in sys.argv[6:]]
os.makedirs(os.path.join(HERE, 'logs'), exist_ok=True); os.makedirs(os.path.join(HERE, 'w'), exist_ok=True)
lock = threading.Lock()
def job(np_):
    n, p = np_
    w = os.path.join(HERE, 'w', f'w_{n}_{p}_L{lv}.json'); log = os.path.join(HERE, 'logs', f'L{lv}_{n}_{p}.log')
    if os.path.exists(w): os.remove(w)
    cmd = [DFS, str(n), str(p), '--level', str(lv), '--threads', str(threads), '--split', '2', '--out', w, '--log', log]
    if os.path.exists(log): cmd += ['--resume', log]   # dfs3 appends to --log, so same file
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=to)
        line = [l for l in r.stdout.splitlines() if l.startswith('dfs3 ')]
        line = line[0] if line else 'ERROR ' + r.stderr[-200:]
        res = 'FOUND' if 'result=FOUND' in line else 'NONE' if 'result=NONE' in line else 'ERR'
    except subprocess.TimeoutExpired:
        done = sum(1 for l in open(log) if l.startswith('task ') and 'stopped=false' in l) if os.path.exists(log) else 0
        res, line = 'TIMEOUT', f'timeout {to}s, task-done lines in log={done} (log {os.path.basename(log)})'
    if res == 'FOUND':
        for chk, tag in ((CHK, 'DIRECT3 OK'), (CC, 'COLOURCHECK OK')):
            c = subprocess.run([sys.executable, chk, w], capture_output=True, text=True)
            s = c.stdout.strip() or ('CHECKFAIL ' + c.stderr[-200:])
            if tag not in s: res = 'CHECKFAIL'
            line += ' | ' + s
    with lock:
        with open(out, 'a') as f: f.write(f'RUN n={n} p={p} L{lv} {res} :: {line}\n')
        print(f'RUN n={n} p={p} L{lv} {res}', flush=True)
with ThreadPoolExecutor(workers) as ex: list(ex.map(job, pairs))
