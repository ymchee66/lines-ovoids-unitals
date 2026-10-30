"""Two-length theorem for PSL(2,q)/PGL(2,q) on the projective line: predicted orbit data."""
from math import comb
def factorint(n):
    f={};d=2
    while d*d<=n:
        while n%d==0: f[d]=f.get(d,0)+1; n//=d
        d+=1
    if n>1: f[n]=f.get(n,0)+1
    return f
def primefactors(n): return sorted(factorint(n)) if n>1 else []
def pp(q):
    f=factorint(q); (p,e),=f.items(); return p,e
def case(kind,q,k):
    """return (t, h, a) if all k-subset stabilisers have order <=2 by the theorem's conditions, else None.
    kind: 'S' = PSL(2,q), 'G' = PGL(2,q) (q odd)."""
    p,e=pp(q); v=q+1
    if q%2==0:
        if kind!='S': return None
        h=q*(q*q-1); t=3
        if k%4 not in (2,3): return None
        if any(k%l in (0,1,2) for l in primefactors(q-1)): return None
        if any(k%l==0 for l in primefactors(q+1)): return None
        f2=comb(q//2,k//2)            # k odd: (k-1)//2 = k//2 two-cycles plus the fixed point
        a=(q*q-1)*f2*2//h
        return t,h,a
    if k%p in (0,1): return None
    if kind=='S':
        h=q*(q*q-1)//2
        if q%4==1:
            t=2
            if k%2==0: return None
            if q%8==1 and k%4!=3: return None
            f2=2*comb((q-1)//2,(k-1)//2); ninv=q*(q+1)//2
        else:
            t=3
            if k%4==0: return None
            f2=comb((q+1)//2,k//2) if k%2==0 else 0; ninv=q*(q-1)//2
        A=[l for l in primefactors((q-1)//2) if l>2]; B=[l for l in primefactors((q+1)//2) if l>2]
    else:
        h=q*(q*q-1); t=3
        if k%2==0: return None
        if q%4==1 and k%4!=3: return None
        f2=2*comb((q-1)//2,(k-1)//2); ninv=q*(q+1)//2
        A=[l for l in primefactors(q-1) if l>2]; B=[l for l in primefactors(q+1) if l>2]
    if any(k%l in (0,1,2) for l in A): return None
    if any(k%l==0 for l in B): return None
    a=ninv*f2*2//h; assert ninv*f2*2%h==0
    return t,h,a
def ls(t,h,a,v,k,N):
    """direct large set LS[N](t,k,v) from the two-length data?"""
    tot=comb(v,k)
    if tot%N: return False
    s=tot//N
    if (2*s)%h: return False
    sig=2*s//h
    return a>=N*(sig%2)
