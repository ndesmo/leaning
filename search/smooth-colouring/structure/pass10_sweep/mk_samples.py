"""python mk_samples.py ck/exh_n_p.ck out.json [max]  -> check_indep.py input from S lines (stratified by e)"""
import json, sys, random
from sympy import primerange
f, out = sys.argv[1], sys.argv[2]
mx = int(sys.argv[3]) if len(sys.argv) > 3 else 200
n, p = map(int, f.split('exh_')[1].split('.')[0].split('_'))
by = {}
for l in open(f):
    if l.startswith('S '):
        w = l.split(); by.setdefault(int(w[2]), []).append([int(x) for x in w[3].split(',')])
random.seed(1); S, E = [], []
for e, L in sorted(by.items()):
    for g in random.sample(L, min(len(L), mx // len(by))): S.append(g); E.append(e)
json.dump({"n": n, "p": p, "primes": list(primerange(2, n + 1)), "samples": S, "evals": E}, open(out, 'w'))
