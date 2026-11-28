"""List aperiodic 6-subsets B of Z36 = Z4 x Z9 (0 in B) in the R-analogue with rows along rho:
rho=3: S_B={2,3}, Phi_12 | B, Phi_18 not | B (complements: P-cosets and rows-along-3 shapes);
rho=2: S_B={2,3}, Phi_18 | B, Phi_12 not | B.  Prints k pseudo-random ones as Z4 x Z9 json.
Usage: python pick_B.py rho k seed"""
import sys, itertools, cmath, random, json
rho, k, seed = map(int, sys.argv[1:4])
divs = [d for d in range(2, 37) if 36 % d == 0]
def zs(S): return {d for d in divs if abs(sum(cmath.exp(2j*cmath.pi*s/d) for s in S)) < 1e-7}
want_in = {2, 3, 6, 12} if rho == 3 else {2, 3, 6, 18}
out = []
for rest in itertools.combinations(range(1, 36), 5):
    S = (0,) + rest; Z = zs(S)
    if not ({2, 3} <= Z and not ({4, 9} & Z)): continue
    if rho == 3 and not (12 in Z and 18 not in Z): continue
    if rho == 2 and not (18 in Z and 12 not in Z): continue
    if any(all((s + g) % 36 in S for s in S) for g in range(1, 36)): continue
    out.append(S)
print(len(out), 'candidates', file=sys.stderr)
random.Random(seed).shuffle(out)
for S in out[:k]: print(json.dumps(sorted([s % 4, s % 9] for s in S)))
