# Brute-force least N admitting a valid n-set mod N (Fonollosa arXiv:2607.08366).
# Valid: the all-ones multiplicity vector is the only k>=0, sum k = n, with sum k_i a_i = sum a_i mod N.
# WLOG 0 in A (translating A by t shifts both sides by n*t).
import itertools, sys
from math import comb

def vectors(n):
    out = []
    for c in itertools.combinations_with_replacement(range(n), n):
        k = [0]*n
        for i in c: k[i] += 1
        if any(x != 1 for x in k): out.append(k)
    return out

def valid(A, N, V):
    p = sum(A) % N
    return all(sum(k[i]*A[i] for i in range(len(A))) % N != p for k in V)

def least_valid(n, Nmax):
    V = vectors(n)
    for N in range(n, Nmax+1):
        for rest in itertools.combinations(range(1, N), n-1):
            A = (0,) + rest
            if valid(A, N, V): return N, A
    return None

def conj(n): return 2**n - 2**(n.bit_length()-1)

nmax = int(sys.argv[1]) if len(sys.argv) > 1 else 5
for n in range(2, nmax+1):
    N, A = least_valid(n, conj(n))
    print(f"n={n}: least valid N={N} (conjectured {conj(n)}), first set found {A}")
# Super-increasing set {2^k-1}: least valid modulus, n <= 9
for n in range(2, 10):
    V = vectors(n); A = [2**k-1 for k in range(n)]
    L = next(N for N in range(n, 2**n+1) if valid([a % N for a in A], N, V) and len({a % N for a in A}) == n)
    print(f"super-increasing n={n}: least valid N={L}, formula {conj(n)}")
