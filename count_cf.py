import json,sys
from math import comb
sys.path.insert(0,'.')
from base import build
from thm import case, ls, factorint
from thm_r import psl_r_q3, psl_r_q1, pgl_r, split_r
from thm_2grp import psl_2grp, pgl_2grp2
from chain import chain_ok
from four import four_ok
L=build(False)
def lp(h,r,a,total,N):
    if total%N: return False
    s=total//N
    if (r*s)%h: return False
    sig=r*s//h
    return a>=N*(sig%r)
def decided(N,t,k,v):
    q=v-1
    if q<4 or len(factorint(q))!=1: return False
    for kk in (k,v-k):
        tot=comb(v,kk)
        for kind in 'SG':
            if kind=='G' and q%2==0: continue
            c=case(kind,q,kk)
            if c and c[0]>=t and ls(*c,v,kk,N): return True
        tS=3 if (q%4==3 or q%2==0) else 2
        for r in factorint(q*q-1):
            if r==2: continue
            if t<=3:
                x=psl_r_q3(q,kk,r)
                if x and lp(x[0],r,x[1],tot,N): return True
            for f,tt in ((lambda: psl_r_q1(q,kk,r),2),(lambda: pgl_r(q,kk,r),3),(lambda: split_r(q,kk,r,'S'),2),(lambda: split_r(q,kk,r,'G'),3)):
                if t>tt: continue
                try: x=f()
                except AssertionError: x=None
                if x:
                    h,o=x
                    if four_ok(h,r,o.get(2,0),o.get(r,0),o.get(2*r,0),tot,N): return True
        for f,tt in ((lambda: psl_2grp(q,kk),tS),(lambda: pgl_2grp2(q,kk),3)):
            if t>tt: continue
            try: x=f()
            except Exception: x=None
            if x:
                h,o=x
                if o and chain_ok(h,o,tot,N): return True
    return False
PA=[tuple(x[:4]) for x in json.load(open('tableA.json'))['PA']]
dr=[k for k in PA if not L[k[0]].has(k[1],k[2],k[3])]
print('direct',len(dr),'given in closed form',sum(decided(*k) for k in dr))
