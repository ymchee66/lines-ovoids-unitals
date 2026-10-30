from math import comb
from thm import primefactors
def ree(q,k):
    if k%2==0 or k%3!=2: return None
    if any(k%l in (0,1,2) for l in primefactors(q-1) if l>2): return None
    if any(k%l==0 for l in primefactors(q+1) if l>2): return None
    if any(k%l==0 for l in primefactors(q*q-q+1)): return None
    f2=sum(comb(q+1,j)*comb((q**3-q)//2,(k-j)//2) for j in range(1,min(q+1,k)+1,2))
    h=q**3*(q**3+1)*(q-1); assert (2*f2)%(q*(q*q-1))==0
    return h,2*f2//(q*(q*q-1))
