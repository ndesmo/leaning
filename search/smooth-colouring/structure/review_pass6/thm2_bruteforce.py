"""Referee test of composite_B.md Thm 2 (group-theoretic core), small n.
For every factorisation A (+) B = G with |A| = n squarefree, 0 in A, 0 in B, and the
pi(n)-part of |B| a power p^a of one prime p | n (or 1), check: there is a homomorphism
psi: G -> Z_{p^{a+1}} x Z_{n/p} (cyclic, CRT) injective on A whose fibres over Z_{n/p}
are cosets of the order-p subgroup. (Thm 2 gives psi as a homomorphism of G, since the
proof's psi factors through phi.)  Also check prime-note Thm with a=1 the same way."""
import itertools, sys, random
from math import gcd

def elems(ds):
    return list(itertools.product(*[range(d) for d in ds]))
def add(x,y,ds): return tuple((a+b)%d for a,b,d in zip(x,y,ds))
def sub(x,y,ds): return tuple((a-b)%d for a,b,d in zip(x,y,ds))

def complements(B, ds, G, n):
    """all A containing 0 with A (+) B = G (A as frozenset)."""
    idx={g:i for i,g in enumerate(G)}
    Bl=list(B); res=[]
    covered=[False]*len(G)
    A=[]
    def rec():
        try: i=covered.index(False)
        except ValueError:
            res.append(frozenset(A)); return
        g=G[i]
        for b in Bl:
            a=sub(g,b,ds)
            if a in Aset_block: continue
            cells=[idx[add(a,bb,ds)] for bb in Bl]
            if any(covered[c] for c in cells): continue
            if len(A)>=n: continue
            for c in cells: covered[c]=True
            A.append(a)
            rec()
            A.pop()
            for c in cells: covered[c]=False
    Aset_block=set()
    # force 0 in A: first cell is 0 = a + b with b in B; require a=0 -> cover with a=0 first only
    cells=[idx[add(G[0],bb,ds)] for bb in Bl]
    for c in cells: covered[c]=True
    A.append(G[0]); rec()
    return res

def check(A, ds, n, p, a):
    N1=p**(a+1); N2=n//p; N=N1*N2
    # homs G -> Z_N : x_i with d_i x_i = 0 mod N
    choices=[[x for x in range(N) if (d*x)%N==0] for d in ds]
    Al=list(A)
    for xs in itertools.product(*choices):
        vals=[sum(c*x for c,x in zip(g,xs))%N for g in Al]
        if len(set(vals))!=n: continue
        fib={}
        for v in vals: fib.setdefault(v%N2,[]).append(v%N1)
        ok=True
        for k,f in fib.items():
            if len(f)!=p or len({v%(p**a) for v in f})!=1: ok=False;break
        if ok: return True
    return False

def run(n, ds, maxB=None, seed=1):
    G=elems(ds); order=len(G); m=order//n
    primes=[q for q in range(2,n+1) if n%q==0 and all(q%r for r in range(2,q))]
    mpi=1
    for q in primes:
        while m%(q*mpi)==0 and (m//mpi)%q==0: mpi*=q
    # recompute properly
    mpi=1; mm=m
    for q in primes:
        while mm%q==0: mm//=q; mpi*=q
    qs=[q for q in primes if mpi%q==0]
    if len(qs)>1: print(ds,'mixed, skip'); return
    if qs: p=qs[0]; a=0; t=mpi
    else: p=primes[0]; a=0; t=1
    while t>1: t//=p; a+=1
    others=[g for g in G if any(g)]
    from math import comb
    if maxB and comb(len(others),m-1)>maxB:
        random.seed(seed); Bs=[tuple(random.sample(others,m-1)) for _ in range(maxB)]
    else:
        Bs=list(itertools.combinations(others,m-1))
    nfact=0; bad=0
    for Bt in Bs:
        B=[G[0]]+list(Bt)
        for A in complements(B,ds,G,n):
            nfact+=1
            if not check(A,ds,n,p,a):
                bad+=1; print('COUNTEREXAMPLE',ds,sorted(A),B)
    print(f'n={n} G=Z{ds} m={m} m_pi={mpi} p={p} a={a}: factorisations={nfact} failures={bad}',flush=True)

if __name__=='__main__':
    start=int(sys.argv[1]) if len(sys.argv)>1 else 0
    L=[(6,(12,),None),(6,(2,6),None),(6,(30,),None),(6,(18,),None),(6,(3,6),None),
                    (6,(24,),None),(6,(2,12),None),(6,(2,2,6),None),(6,(36,),3000),(6,(2,18),3000),
                    (6,(48,),3000),(6,(2,24),3000),(6,(4,12),3000),(6,(54,),3000),(6,(3,18),3000),(6,(3,3,6),3000),
                    (10,(20,),None),(10,(2,10),None),(10,(50,),None),(10,(5,10),None),(10,(30,),None),
                    (15,(45,),None),(15,(3,15),None),(15,(75,),3000),(15,(5,15),3000),
                    (6,(60,),2000),(6,(2,30),2000)]
    for n,ds,mx in L[start:]:
        run(n,ds,mx)
