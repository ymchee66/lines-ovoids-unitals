"""LOT10 Thm 4.3 consequences for known transitive groups of degree <= VMAX: list of (t, k, v, h)-predicates per prime N."""
import math, sys
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from lot import primes_of, mval
from fastadm import vN
def factor(n):
    f={};d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
def ppow(q):
    f=factor(q)
    if len(f)!=1: return None
    (p,e),=f.items(); return p,e
def groups(VM):
    G=[]  # (name, v, h, t)
    for q in range(2,VM):
        pe=ppow(q)
        if not pe: continue
        p,e=pe
        divs=[f for f in range(1,e+1) if e%f==0]
        if q+1<=VM and q>=3:
            hS=q*(q*q-1)//(2 if q%2 else 1)
            tS=3 if (q%2==0 or q%4==3) else 2
            for f in divs: G.append((f'PSL(2,{q}).{f}',q+1,hS*f,tS))
            if q%2:
                for f in divs: G.append((f'PGL(2,{q}).{f}',q+1,2*hS*f,3))
        if q>=4:
            for f in divs:
                G.append((f'AGL(1,{q}).{f}',q,q*(q-1)*f,3 if (q in (8,32) and f==e) else 2))
                if q%4==3: G.append((f'ASL(1,{q}).{f}',q,q*(q-1)//2*f,2))
        # affine AGL(d,q0) with q=q0^d, d>=2
        for d in range(2,e+1):
            if e%d: continue
            q0=p**(e//d); gl=1
            for i in range(d): gl*=(q0**d-q0**i)
            G.append((f'AGL({d},{q0})',q,q*gl,3 if q0==2 else 2))
        # PSL(n,q), n>=3, on points
        n=3
        while (q**n-1)//(q-1)<=VM:
            v=(q**n-1)//(q-1); h=q**(n*(n-1)//2)
            for i in range(2,n+1): h*=(q**i-1)
            h//=math.gcd(n,q-1)
            G.append((f'PSL({n},{q})',v,h,2)); n+=1
        # PSU(3,q)
        if q**3+1<=VM and q>=3:
            G.append((f'PSU(3,{q})',q**3+1,q**3*(q**3+1)*(q*q-1)//math.gcd(3,q+1),2))
    for m in (1,2):
        q=2**(2*m+1); Q=q*q
        if Q+1<=VM: G.append((f'Sz({q})',Q+1,Q*(Q+1)*(q-1),2))
    return G
def lgC(v,k): return math.lgamma(v+1)-math.lgamma(k+1)-math.lgamma(v-k+1)
def lot43(N,VM,TM):
    out=[]
    for name,v,h,t in groups(VM):
        if t>TM: t=TM
        hf=factor(h); m=float(mval(list(hf)))
        lh=math.log(h)+math.log(m)
        for k in range(t+1,v//2+1):
            if vN(v,k,N) < hf.get(N,0)+1: continue
            if any(vN(v,k,p)<a for p,a in hf.items()): continue
            if lgC(v,k)-lh < math.log(N)+1:
                C=math.comb(v,k)
                from fractions import Fraction
                if Fraction(C,h)/mval(list(hf)) < N: continue
            out.append((t,k,v,name))
    return out
