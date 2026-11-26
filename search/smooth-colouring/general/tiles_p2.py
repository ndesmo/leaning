"""Enumerate p-subsets B (0 in B) of H in {Z_{p^2}, Z_p^2} that tile H, up to translation and Aut(H).
For each class: subgroup?, number of complements C (containing 0), and whether every complement
is a subgroup / coset structure.  Usage: python tiles_p2.py p   (p=3,5 exhaustive)"""
import sys, itertools
p = int(sys.argv[1]); N = p*p
def groups():
    cyc = dict(name=f"Z{N}", el=list(range(N)), add=lambda x,y:(x+y)%N, neg=lambda x:(-x)%N,
               auts=[(lambda u:(lambda x:(u*x)%N))(u) for u in range(1,N) if u%p])
    el2 = [(a,b) for a in range(p) for b in range(p)]
    M = [(a,b,c,d) for a in range(p) for b in range(p) for c in range(p) for d in range(p) if (a*d-b*c)%p]
    nc = dict(name=f"Z{p}^2", el=el2, add=lambda x,y:((x[0]+y[0])%p,(x[1]+y[1])%p), neg=lambda x:((-x[0])%p,(-x[1])%p),
              auts=[(lambda m:(lambda x:((m[0]*x[0]+m[1]*x[1])%p,(m[2]*x[0]+m[3]*x[1])%p)))(m) for m in M])
    return [cyc, nc]
for G in groups():
    el, add, neg = G["el"], G["add"], G["neg"]; z = el[0]
    def diff(S): return {add(a,neg(b)) for a in S for b in S}
    def canon(S):
        best = None
        for u in G["auts"]:
            T = [u(x) for x in S]
            for t in T:
                c = tuple(sorted(add(x,neg(t)) for x in T))
                if best is None or c < best: best = c
        return best
    def comps(B):
        D = diff(B); out = []
        def rec(C, start):
            if len(C) == p: out.append(tuple(C)); return
            for i in range(start, N):
                x = el[i]
                if all(add(x,neg(c)) not in D for c in C): rec(C+[x], i+1)
        rec([z], 1); return out
    def is_sub(S): return all(add(a,b) in set(S) for a in S for b in S)
    seen = {}
    for rest in itertools.combinations(el[1:], p-1):
        B = (z,)+rest; c = canon(B)
        if c in seen: continue
        C = comps(B)
        if C: seen[c] = C
    print(f"{G['name']}: {len(seen)} tiling classes")
    for c, C in seen.items():
        print(f"  B={c} subgroup={is_sub(c)} ncomp(0 in C)={len(C)} all_comps_subgroups={all(is_sub(x) for x in C)} comps={C[:6]}")
