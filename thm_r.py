"""PSL(2,q) with one odd prime r allowed in stabilisers."""
from math import comb
from thm import primefactors, factorint
def vp(n,r):
    c=0
    while n%r==0: n//=r; c+=1
    return c
def other_ok(q,k,r,p):
    """all odd primes other than r excluded, as in condition (O)"""
    if p!=r and k%p in (0,1): return False
    for l in primefactors(q-1):
        if l>2 and l!=r and k%l in (0,1,2): return False
    for l in primefactors(q+1):
        if l>2 and l!=r and k%l==0: return False
    return True
def psl_r_q3(q,k,r):
    """q = 3 mod 4, PSL(2,q), t=3, k odd; stabilisers of order 1 or r. returns (h, a_r) or None"""
    (p,e),=factorint(q).items()
    if q%4!=3 or k%2==0 or r==p or r==2: return None
    if not other_ok(q,k,r,p): return None
    h=q*(q*q-1)//2
    if (q+1)%r==0:
        if k%r: return None
        if (q+1)%(r*r)==0 and k%(r*r)==0: return None
        f=comb((q+1)//r,k//r); a=r*f//(q+1); assert r*f%(q+1)==0
        return h,a
    if (q-1)%r==0:
        if k%r not in (0,1,2): return None
        if (q-1)%(r*r)==0 and k%(r*r) in (0,1,2): return None
        f=sum(comb(2,e)*comb((q-1)//r,(k-e)//r) for e in range(3) if (k-e)%r==0 and k>=e)
        a=r*f//(q-1); assert r*f%(q-1)==0
        return h,a
    return None
def psl_r_q1(q,k,r):
    """q = 1 mod 4, PSL(2,q), t=2, k odd (k=3 mod 4 if q=1 mod 8), r odd prime dividing (q+1)/2 and k.
    stabilisers 1, 2, r, D_2r. returns (h, {2:n2, r:nr, 2r:nD})"""
    (p,e),=factorint(q).items()
    if q%4!=1 or k%2==0 or r==p or (q+1)%r or k%r: return None
    if q%8==1 and k%4!=3: return None
    if not other_ok(q,k,r,p): return None
    if (q+1)%(r*r)==0 and k%(r*r)==0: return None
    h=q*(q*q-1)//2
    f2=2*comb((q-1)//2,(k-1)//2); fr=comb((q+1)//r,k//r); fD=2*comb((q+1-2*r)//(2*r),(k//r-1)//2)
    ninv=q*(q+1)//2; nCr=q*(q-1)//2; nD=nCr*(q+1)//(2*r)
    gD=fD; gr=fr-(q+1)//(2*r)*fD; g2=f2-(q-1)//2*fD
    out={}
    for m,ns,g in ((2,ninv,g2),(r,nCr,gr),(2*r,nD,gD)):
        num=ns*g*m; assert num%h==0,(q,k,r,m); 
        if num: out[m]=num//h
    return h,out
def pgl_r(q,k,r):
    """PGL(2,q), q odd, t=3, k odd (k=3 mod 4 if q=1 mod 4), r odd prime dividing q+1 and k."""
    (p,e),=factorint(q).items()
    if q%2==0 or k%2==0 or r==p or (q+1)%r or k%r: return None
    if q%4==1 and k%4!=3: return None
    if not other_ok(q,k,r,p): return None
    if (q+1)%(r*r)==0 and k%(r*r)==0: return None
    h=q*(q*q-1)
    f2=2*comb((q-1)//2,(k-1)//2); fr=comb((q+1)//r,k//r); fD=2*comb((q+1-2*r)//(2*r),(k//r-1)//2)
    g2=f2-(q-1)//2*fD; gr=fr-(q+1)//(2*r)*fD
    out={}
    for m,num in ((2,q*(q+1)//2*g2*2),(r,q*(q-1)//2*gr*r),(2*r,q*(q*q-1)//(4*r)*fD*2*r)):
        assert num%h==0,(q,k,r,m)
        if num: out[m]=num//h
    return h,out
def split_r(q,k,r,group):
    """split case: r odd prime dividing q-1, k = 0,1,2 mod r, k odd.
    group 'S': PSL(2,q), q=1 mod 4, t=2.  group 'G': PGL(2,q), q odd, t=3."""
    (p,e),=factorint(q).items()
    if q%2==0 or k%2==0 or r==p or (q-1)%r or k%r not in (0,1,2): return None
    if group=='S' and q%4!=1: return None
    if q%4==1 and k%4!=3: return None
    if not other_ok(q,k,r,p): return None
    if (q-1)%(r*r)==0 and k%(r*r) in (0,1,2): return None
    W=(q-1)//r
    f2=2*comb((q-1)//2,(k-1)//2)
    fr=sum(comb(2,e)*comb(W,(k-e)//r) for e in range(3) if (k-e)%r==0)
    fC=2*comb((q-1)//(2*r),(k-1)//(2*r)) if (k-1)%(2*r)==0 else 0
    M=(q-1-2*r)//(2*r)
    fD=sum(2*comb(M,(k-2*a-r)//(2*r)) for a in (0,1) if k-2*a-r>=0 and (k-2*a-r)%(2*r)==0)
    g2=f2-fC-(q-1)//2*fD; gr=fr-fC-(q-1)//(2*r)*fD
    if group=='S':
        h=q*(q*q-1)//2
        n2=(2*g2,q-1); nr=(r*gr,q-1); n2r=(2*r*fC+(q-1)*fD,q-1)
    else:
        h=q*(q*q-1)
        n2=(g2,q-1); nr=(r*gr,2*(q-1)); n2r=(2*r*fC+(q-1)*fD,2*(q-1))
    out={}
    for m,(a,b) in ((2,n2),(r,nr),(2*r,n2r)):
        assert a%b==0,(q,k,r,m,group)
        if a: out[m]=a//b
    return h,out
