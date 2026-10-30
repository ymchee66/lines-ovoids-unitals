import sys,json
P=int(sys.argv[1]); VM=int(sys.argv[2])
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import engine; engine.VMAX=VM; engine.TMAX=3; engine.PRIMES=[P]
import base; base.VMAX=VM; base.TMAX=3; base.PRIMES=[P]
from thm import case, ls, factorint
from thm_aff import agl
from math import comb
def isq(q): return q>2 and len(factorint(q))==1
L=base.build(False)[P]
res={}
def rec(name,t,k,v):
    r=res.setdefault(name,[0,0,[]]); r[0]+=1
    if not L.has(t,min(k,v-k),v): r[1]+=1; r[2].append(v)
for q in range(4,VM):
    if not isq(q): continue
    if q%120 in (53,77) and q+1<=VM:
        if ((q-2)*(q-3)//30)%P==0 and P<=(q-3)//2: rec('k5',2,5,q+1)
    if q%4==3 and q%5 in (2,3) and (q%3==2 or q%3==0) and q+1<=VM:
        s0=(q-2)*(q-3)//60
        if s0%P==0 and ((s0//P)%2==0 or P<=(q-3)//4): rec('pgl5',3,5,q+1)
    if q%4==1 and q+1<=VM:
        c=case('G',q,7)
        if c and ls(c[0],c[1],c[2],q+1,7,P): rec('pgl7',3,7,q+1)
    if q%12==5 and q%5!=1:
        s0=(q-2)*(q-3)*(q-4)*(q-5)//360
        if s0%P==0 and ((s0//P)%2==0 or P<=(q-3)*(q-5)//24): rec('agl6',2,6,q)
print(P,{k:(v[0],v[1],v[2][:8]) for k,v in res.items()})
