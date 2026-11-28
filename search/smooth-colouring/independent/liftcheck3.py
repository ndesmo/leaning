"""liftcheck3.py witness.json : is a (b_i^p) witness a lift of a lower-level solution?
Definitions (G_i = Z_{p^{i+1}} x Z_K, C_i = p^i Z_{p^{i+1}} x 0; the order-p subgroup).
 * "plain lift": every h(q) lies in p Z_{p^{i+1}}; then phi = j o psi with j(h,f) = (p h, f):
   G_{i-1} -> G_i, and psi is a level-(i-1) solution.  "level-0 lift": every h(q) in p^i Z.
 * Strong test (NOT A LIFT through ANY injective hom G_{i-1} -> G_i): let H = <phi(q)>.  If phi = j o psi
   with j injective then H embeds in G_{i-1}, whose p-part has exponent p^max(i, v_p(K)).  So if H
   contains an element whose order has p-part p^{i+1} > p^max(i, v_p K), phi is not such a lift.
   Checked for H_small (small primes q, 2q <= n; the searched part) and H_all (all primes)."""
import sys, json
from math import gcd
d = json.load(open(sys.argv[1])); n, p, K, lv = d["n"], d["p"], d["K"], d["level"]; Q = p ** (lv + 1)
phi = {int(q): v for q, v in d["phi"].items()}
def vp(x):
    k = 0
    while x % p == 0 and x: x //= p; k += 1
    return k
def ppart_order(h, f):  # p-part exponent of order of (h,f)
    o = (Q // gcd(h, Q)) * (K // gcd(f, K)) // gcd(Q // gcd(h, Q), K // gcd(f, K))
    return vp(o)
bound = max(lv, vp(K))
for name, qs in [("small", [q for q in phi if 2 * q <= n]), ("all", list(phi))]:
    plain = all(phi[q][0] % p == 0 for q in qs); l0 = all(phi[q][0] % (p ** lv) == 0 for q in qs)
    e = max(ppart_order(*phi[q]) for q in qs)
    units = [q for q in qs if phi[q][0] % p]
    strong = e > bound
    print(f"liftcheck3 n={n} p={p} level={lv} K={K} v_p(K)={vp(K)} H_{name}: plain_lift={plain} level0_lift={l0} "
          f"p-exp(H)=p^{e} bound=p^{bound} NOT_A_LIFT_strong={strong} unit-h primes={units[:8]}")
