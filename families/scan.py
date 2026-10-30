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
for q in range(7,VM+1):
    if not isq(q): continue
    for k in range(4,13):
        for kind in 'SGA':
            if kind=='A':
                if k>q-2: continue
                c=agl(q,k)
                if not c: continue
                h,a=c; t=2; v=q
            else:
                if q+1>VM or k>q-2 or (kind=='G' and q%2==0): continue
                c=case(kind,q,k)
                if not c: continue
                t,h,a=c; v=q+1
            if not ls(t,h,a,v,k,P): continue
            key=f"{kind}{'e' if q%2==0 else q%4},k{k}"
            r=res.setdefault(key,[0,0]); r[0]+=1
            if v>100 and not L.has(t,min(k,v-k),v): r[1]+=1
            if v<=100: r[0]-=1
json.dump(res,open(f'scan_{P}.json','w'))
