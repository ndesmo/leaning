"""orbit_reps3.py n p level : prints comma-separated min-index representatives of the orbits of
Gamma = U(Z_{p^{i+1}}) x U(Z_K) on G = Z_{p^{i+1}} x Z_K (element index e = h*K + f), for dfs3 --first.
Soundness (independent of dfs3's lex-leader code): each gamma in Gamma is an automorphism of G with
gamma(F) = F, so phi is a solution iff gamma o phi is; choosing gamma with gamma(phi(q0)) = rep shows
every solution's orbit meets {phi : phi(q0) is a representative}, for the first search variable q0."""
import sys
from math import gcd
n, p, lv = map(int, sys.argv[1:4]); K = n // p; Q = p ** (lv + 1)
U = [u for u in range(1, Q) if gcd(u, Q) == 1]; V = [v for v in range(K) if gcd(v, K) == 1] if K > 1 else [0]
seen, reps = set(), []
for e in range(Q * K):
    if e in seen: continue
    h, f = divmod(e, K)
    orb = {((u * h) % Q) * K + (v * f) % K for u in U for v in V}
    seen |= orb; reps.append(min(orb))
print(",".join(map(str, reps)))
