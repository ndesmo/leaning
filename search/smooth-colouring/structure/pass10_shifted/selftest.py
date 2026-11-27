"""Self-tests for enum_shifted.py: (1) the detector flags cex1 of pass 9 (a non-shifted downset);
(2) shifted-downset counts agree with a brute force over subsets of a box, sizes <= 7."""
import itertools
from enum_shifted import rank_mod, rank_Q, shifted_downsets
T = [(0,0,0,0,0),(0,0,0,0,1),(0,0,0,1,0),(0,0,0,2,0),(0,0,1,0,0),(0,1,0,0,0),(0,2,0,0,0),
     (1,0,0,0,0),(1,0,1,0,0),(2,0,0,0,0)]
g = (1,2,4,3,3); fib = {}
for v in T: fib.setdefault(sum(a*b for a,b in zip(g,v)) % 5, []).append(v)
assert all(len(b) == 2 for b in fib.values())
rows = [[a-b for a,b in zip(y,B[0])] for B in fib.values() for y in B[1:]]
print("cex1: rank_F2 =", rank_mod(rows,2), " rank_Q =", rank_Q(rows), "(differ => flagged)")
def is_shifted(S):
    for x in S:
        for j in range(len(x)):
            if x[j]:
                y = list(x); y[j] -= 1
                if tuple(y) not in S: return False
                for i in range(j):
                    z = list(y); z[i] += 1
                    if tuple(z) not in S: return False
    return True
for N in range(1, 8):
    k = N - 1
    box = [x for x in itertools.product(range(N), repeat=k) if sum(x) < N] if k else [()]
    cnt = 0
    # brute force: shifted downsets of size N in N^k using all k coords (e_{k-1} in T)
    # enumerate by closure: every shifted downset is the closure of its elements; brute subsets too big,
    # so instead grow by BFS over ALL subsets reachable by adding one element (no covering logic used).
    level = {frozenset([tuple([0]*k)])}
    for s in range(1, N):
        nxt = set()
        for S in level:
            for x in box:
                if x not in S:
                    S2 = S | {x}
                    if is_shifted(S2): nxt.add(S2)
        level = nxt
    def uses_all(S): return all(any(x[i] for x in S) for i in range(k))
    def canon(S):  # drop unused trailing coords; shifted => used coords are an initial segment
        return frozenset(S)
    brute = sum(1 for S in level if uses_all(S))
    # enum_shifted counts all shifted downsets of size N (any number of used coords);
    # brute with padding to k coords: count those using exactly j coords, sum over j
    tot = 0
    for j in range(0, k + 1):
        tot += sum(1 for S in level if all(any(x[i] for x in S) for i in range(j)) and not any(x[i] for x in S for i in range(j, k)))
    print(N, "enum:", len(shifted_downsets(N)), "brute:", tot)
