"""Second, independent implementation of the kper class (shares no code with kper.rs).
Decides whether there is phi: primes<=n/2 -> Z_N (N=n*p, q=n/p, p || n), extended
multiplicatively, such that for distinct a,b <= n that are (n/2)-smooth:
    phi(a) != phi(b)  and  (phi(a) = phi(b) mod q  =>  phi(a) = phi(b) mod n).
Dropping the primes in (n/2, n] only weakens the constraints, so NONE here implies NONE
for the full class.  Symmetry: units of Z_N preserve the constraint, so phi(2) may be
taken to be a divisor of N.  Usage: python kper_indep.py n p"""
import sys, time
n, p = int(sys.argv[1]), int(sys.argv[2]); N, q = n * p, n // p
assert n % p == 0 and q % p != 0
P = [x for x in range(2, n // 2 + 1) if all(x % d for d in range(2, int(x ** .5) + 1))]
def lpf_big(x):  # largest prime factor of x, or None if x is not P-smooth
    big = None
    for pr in P:
        while x % pr == 0: x //= pr; big = pr
    return big if x == 1 else None
new = {pr: [] for pr in P}   # numbers whose largest prime factor is pr: (x, x//pr)
for x in range(2, n + 1):
    b = lpf_big(x)
    if b: new[b].append((x, x // b))
val = {1: 0}; used = {0}; rep = {0: 0}   # rep[r mod q] = value mod n
nodes = 0
def place(x, v):
    r = v % q
    if v in used or (r in rep and rep[r] != v % n): return False
    used.add(v); val[x] = v; rep.setdefault(r, None)
    if rep[r] is None: rep[r] = v % n; return "new"
    return "old"
def dfs(k):
    global nodes
    if k == len(P): return True
    pr = P[k]
    cands = [d for d in range(1, N + 1) if N % d == 0] if k == 0 else range(N)
    for g in cands:
        g %= N; nodes += 1; done = []; ok = True
        for x, y in new[pr]:
            s = place(x, (g + val[y]) % N)
            if not s: ok = False; break
            done.append((x, s))
        if ok and dfs(k + 1): return True
        for x, s in reversed(done):
            v = val.pop(x); used.discard(v)
            if s == "new": del rep[v % q]
    return False
t = time.time(); r = dfs(0)
print(f"n={n} p={p} N={N} result={'EXISTS' if r else 'NONE'} nodes={nodes} secs={time.time()-t:.1f}")
