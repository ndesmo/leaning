r"""Pass 10: torsion of the 'partial-additivity group'
   A_R = < s_u (u in Z_m), s_0 = 0 | s_{a+b} = s_a + s_b for {a,b} in R >
for EVERY set R of unordered pairs {a,b}, a,b in Z_m minus {0}.
Mode 'foreign': primes dividing |Tor(A_R)| that do NOT divide m.
Mode 'pm': for q | m, max over R of v_q(exp Tor A_R), vs v_q(m).
(Lemma P of pass10_shifted.md: Gamma ~= A_R (+) free part.)  Also checks cex1 of pass 9 (expect Z_10).
Usage: python small_m.py mmax [foreign|pm]"""
import sys, itertools
from sympy import Matrix, factorint
from sympy.matrices.normalforms import smith_normal_form

def torsion(m, R):
    rows = []
    for a, b in R:
        r = [0] * (m - 1); c = (a + b) % m
        if c: r[c - 1] += 1
        r[a - 1] -= 1; r[b - 1] -= 1
        rows.append(r)
    if not rows: return []
    S = smith_normal_form(Matrix(rows))
    return [abs(S[i, i]) for i in range(min(S.shape)) if abs(S[i, i]) > 1]

def main():
    mmax, mode = int(sys.argv[1]), (sys.argv[2] if len(sys.argv) > 2 else "foreign")
    print("cex1 (m=5, R={(3,3),(1,1),(2,2),(1,4)}) torsion:", torsion(5, [(3,3),(1,1),(2,2),(1,4)]))
    for m in range(2, mmax + 1):
        pairs = [(a, b) for a in range(1, m) for b in range(a, m)]
        bad = {}; best = {q: 0 for q in factorint(m)}
        for r in range(len(pairs) + 1):
            for R in itertools.combinations(pairs, r):
                for d in torsion(m, R):
                    f = factorint(d)
                    for q in f:
                        if m % q: bad.setdefault(q, R)
                        else: best[q] = max(best[q], f[q])
        if mode == "foreign":
            print(f"m={m}: subsets={2**len(pairs)} foreign primes: {sorted(bad)} examples:",
                  {q: bad[q] for q in sorted(bad)[:3]}, flush=True)
        else:
            print(f"m={m}: max v_q(exp Tor) over all R: {best}; v_q(m): {dict(factorint(m))}", flush=True)

if __name__ == "__main__":
    main()
