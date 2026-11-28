"""Diagnostic: in pure-C tilings (row prime rho), list the t whose phi_rho residue mod rho differs
from the majority residue of its fibre (the 'shifted' points).  Usage: python diag_shift.py file.json rho"""
import sys, json
from collections import Counter
from prop6 import primes_upto, expvec, build
d = json.load(open(sys.argv[1])); rho = int(sys.argv[2]); n, p, q, r = d['n'], d['p'], d['q'], d['r']
P = primes_upto(n); pts = [expvec(t, P) for t in range(1, n + 1)]
cnt = Counter()
for s in d['sols']:
    phi = s['phi']
    img = [tuple(sum(e * phi[j][c] for j, e in enumerate(v)) % m for c, m in enumerate((p*p, q*q, r))) for v in pts]
    h = [x[:2] for x in img]; k = [x[2] for x in img]
    fib, rows, reason, ir, sig = build(pts, k, h, p, q, rho)
    if reason: continue
    shifted = []
    for idx in fib.values():
        res = Counter(h[i][ir] % rho for i in idx)
        if len(res) > 1:
            maj = res.most_common(1)[0][0]
            shifted += [i + 1 for i in idx if h[i][ir] % rho != maj]
    if shifted: cnt[tuple(sorted(shifted))] += 1
for k_, v in cnt.most_common(): print(v, 'tilings, shifted t =', k_)
