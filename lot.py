"""Large sets that follow from Laue, Omidi and Tayfeh-Rezaie, Ars Combin. 97 (2010), Section 4:
Thm 4.3 (|G| divides C(v,k), N | C/|G|, N <= C/(|G| m)), Thm 4.4 (same with the primes of gcd(n,|G|), n = lcm of stabilizer orders),
Thm 4.1 (orbit sizes |G| and |G|/m only) and Thm 4.2 (sizes |G|, |G|/m, |G|/n, one orbit |G|/(mn)), where |G| divides C(v,k)."""
from fractions import Fraction
from math import comb, gcd, lcm
from functools import reduce
def primes_of(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0: n//=d
        d+=1
    if n>1: out.append(n)
    return out
def mval(ps):
    ps=sorted(ps); m=Fraction(0)
    for i in range(len(ps)):
        x=Fraction(1)
        for p in ps[i:]: x*=Fraction(p,p-1)
        m+=x
    return m
def lot_sizes(v,k,h,L=None):
    """set of N (all divisors are allowed; returns a predicate) for which LOT Section 4 gives an LS[N](t,k,v) of G-invariant designs.
    L: dict orbit length -> count, if known."""
    C=comb(v,k)
    if C%h: return None
    M=C//h
    bound=Fraction(C,h)/mval(primes_of(h))
    allN=False
    if L:
        ratios=sorted({h//l for l in L})
        n=reduce(lcm,ratios,1)
        g=gcd(n,h)
        b44=Fraction(C,h)/mval(primes_of(g)) if g>1 else Fraction(C,h)
        bound=max(bound,b44)
        nontriv=[r for r in ratios if r>1]
        if len(nontriv)<=1: allN=True                      # Thm 4.1
        elif len(nontriv)==3:
            a,b,c=nontriv
            if a!=b and a*b==c and L.get(h//c,0)==1: allN=True   # Thm 4.2
    return M,bound,allN
def lot_ok(N,v,k,h,L=None):
    r=lot_sizes(v,k,h,L)
    if r is None: return False
    M,bound,allN=r
    return M%N==0 and (allN or N<=bound)
