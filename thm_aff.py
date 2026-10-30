from math import comb
from thm import primefactors, factorint
def agl(q,k):
    """AGL(1,q) on q points, t=2: return (h,a) if all stabilisers have order <=2."""
    (p,e),=factorint(q).items(); h=q*(q-1)
    if q%2==1:
        if k%p==0: return None
        if q%4==1 and k%4 not in (2,3): return None
        if any(k%l in (0,1) for l in primefactors(q-1) if l>2): return None
        a=2*comb((q-1)//2,k//2)//(q-1); assert 2*comb((q-1)//2,k//2)%(q-1)==0
    else:
        if k%4==0: return None
        if any(k%l in (0,1) for l in primefactors(q-1)): return None
        a=0 if k%2 else 2*comb(q//2,k//2)//q
    return h,a
