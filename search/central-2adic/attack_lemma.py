"""Checks for the Attack section of notes/central-2adic.md (run: python -I attack_lemma.py [N]).
L1: coefficients of g_j(u)=2T_{2^j}(u/2) equal (-1)^k (N/(N-k)) C(N-k,k), N=2^j, and
    v2(coef_k) >= j - v2(k) > s2(k) for 1<=k<2^{j-1}, = at k=2^{j-1} (j<=6).
L2: for even n<=N, 1<=j<=4, 1<=t<=2^{j-1} n: v2([u^{2^j n-2t}] g_j^n) >= s2(t)+1.
L3: for q=4,8,16 and even n<=N (exact): the u-formula a_q(n) = sum_m c(n,m) C(m,m/2) (S0);
    S4: v2(c(n,(q-1)n-2t)) >= s2(t)+1 for t>=1; S5 termwise: every t>=1 term has
    valuation > s2((q-1)n/2); and v2(a_q(n)) = s2((q-1)n/2)."""
import sys
from math import comb
N = int(sys.argv[1]) if len(sys.argv) > 1 else 40
def v2(x):
    if x == 0: return 10**9
    x = abs(x); c = 0
    while x % 2 == 0: x //= 2; c += 1
    return c
s2 = lambda x: bin(x).count('1')
def mul(a, b):  # polys in u as lists, index = degree
    r = [0]*(len(a)+len(b)-1)
    for i, x in enumerate(a):
        if x:
            for k, y in enumerate(b): r[i+k] += x*y
    return r
def pw(p, n):
    r = [1]
    for _ in range(n): r = mul(r, p)
    return r
g = {1: [-2, 0, 1]}
for j in range(2, 7):
    sq = mul(g[j-1], g[j-1]); sq[0] -= 2; g[j] = sq
for j in range(1, 7):
    M = 2**j
    for k in range(M//2+1):
        assert g[j][M-2*k] == (-1)**k * M * comb(M-k, k) // (M-k), (j, k)
        if k:
            assert v2(g[j][M-2*k]) >= j - v2(k)
            assert (j - v2(k) > s2(k)) if k < M//2 else (j - v2(k) == s2(k) == 1)
print("L1 ok")
mn = {}
for j in range(1, 5):
    for n in range(2, N+1, 2):
        P = pw(g[j], n); D = 2**j*n
        for t in range(1, D//2+1):
            e = v2(P[D-2*t]) - s2(t)
            assert e >= 1, (j, n, t)
            mn[j] = min(mn.get(j, 99), e)
print("L2 ok, min excess per j:", mn)
for r in (2, 3, 4):
    q = 2**r
    f = [0, 1]
    for j in range(1, r): f = mul(f, g[j])
    for n in range(2, N+1, 2):
        # exact a_q(n) from (1+...+x^{q-1})^n
        p = [1]
        for _ in range(n): p = mul(p, [1]*q)
        a = p[(q-1)*n//2]
        F = pw(f, n)
        assert a == sum(F[m]*comb(m, m//2) for m in range(0, len(F), 2) if F[m])
        Nh = (q-1)*n//2
        assert F[2*Nh] == 1
        for t in range(1, Nh+1):
            c = F[2*Nh-2*t]
            assert v2(c) >= s2(t)+1, ('S4', q, n, t)
            assert v2(c*comb(2*(Nh-t), Nh-t)) > s2(Nh), ('S5', q, n, t)
        assert v2(a) == s2((q-1)*n//2), (q, n)
print("L3 ok")
