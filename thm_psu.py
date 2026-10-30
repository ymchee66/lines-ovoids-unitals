from math import comb, gcd
from thm import primefactors, factorint
def v2(n):
    c=0
    while n%2==0: n//=2; c+=1
    return c
def psu(q,k):
    """PSU(3,q), q odd, on q^3+1 points: if hypotheses hold return (h, {2^i: n_i}) orbit counts with stabiliser C_{2^i}."""
    (p,e),=factorint(q).items()
    if q%2==0 or k%2==0: return None
    d=gcd(3,q+1); M=(q+1)//d
    if M & (M-1): return None            # (q+1)/d must be a power of 2
    if k%p in (0,1): return None
    if any(k%l in (0,1,2) for l in primefactors(q-1) if l>2): return None
    if any(k%l==0 for l in primefactors(q*q-q+1)): return None
    if any(k%l==0 for l in primefactors(q+1) if l>2): return None
    h=q**3*(q**3+1)*(q*q-1)//d
    b=v2(M); m=v2((q*q-1)//d)
    W=q**3-q
    def F(i):
        n=2**i; mp=2**max(0,i-b); tot=0
        for j in range(0,q+2):
            if (k-j)%n or j>k: continue
            if i<=b: B=comb(q+1,j)
            else: B=sum(comb(2,ee)*comb((q-1)//mp,(j-ee)//mp) for ee in range(3) if j>=ee and (j-ee)%mp==0)
            tot+=B*comb(W//n,(k-j)//n)
        return tot
    s={i:(q*q*(q*q-q+1) if i<=b else comb(q**3+1,2)) for i in range(1,m+1)}
    c={i:(1 if i<b else (comb(q+1,2) if i==b else 1)) for i in range(1,m)}
    out={}
    for i in range(1,m+1):
        g=F(i)-(c[i]*F(i+1) if i<m else 0)
        num=s[i]*g*2**i
        assert num%h==0,(q,k,i)
        if num: out[2**i]=num//h
    return h,out
