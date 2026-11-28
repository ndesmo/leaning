"""Fresh colouring checker (pass 13), written from the definition only; shares no code with dfs3
or direct_check3.  Input: a witness JSON with fields n, p, level, K and phi = {prime q <= n:
[h, f]} (values in G = Z_{p^(level+1)} x Z_K).

Colouring.  Extend phi to every positive integer completely additively (primes > n get 0; any
value works since no a <= n is divisible by them, so a, 2a, ..., na are unaffected... in fact the
check below does not rely on that: it just colours with the stated rule and tests).  Let
A = {psi(1), ..., psi(n)} and B = {(j, 0) : 0 <= j < p^level}.  The colour of a is the unique
m in [n] with psi(a) - psi(m) in B.  We assert that this m exists and is unique for every a
checked, and that for every a <= LIMIT the n numbers a, 2a, ..., na get n distinct colours."""
import sys, json
d = json.load(open(sys.argv[1])); LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 20000
n, p, lv, K = d["n"], d["p"], d["level"], d["K"]
Q = p ** (lv + 1); W = p ** lv
phi = {int(k): (v[0] % Q, v[1] % K) for k, v in d["phi"].items()}
top = LIMIT * n
# smallest-prime-factor sieve up to n*LIMIT
spf = list(range(top + 1))
i = 2
while i * i <= top:
    if spf[i] == i:
        for j in range(i * i, top + 1, i):
            if spf[j] == j: spf[j] = i
    i += 1
psi = [(0, 0)] * (top + 1)
for m in range(2, top + 1):
    q = spf[m]; h, f = psi[m // q]; a, b = phi.get(q, (0, 0))
    psi[m] = ((h + a) % Q, (f + b) % K)
# lookup table: element of G -> colour (A-component of x = a + b, b in B)
table = {}
for m in range(1, n + 1):
    h, f = psi[m]
    for j in range(W):
        x = ((h + j) % Q, f)
        assert x not in table, ("A+B not direct", m, j)
        table[x] = m
assert len(table) == Q * K, "A+B does not cover G"
for a in range(1, LIMIT + 1):
    cols = {table[psi[k * a]] for k in range(1, n + 1)}
    assert len(cols) == n, ("repeated colour", a)
print(f"COLOURCHECK OK n={n} p={p} level={lv}: all a <= {LIMIT} have a,2a,...,{n}a distinctly coloured")
