import sys,json
P=int(sys.argv[1]); VM=int(sys.argv[2])
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import engine; engine.VMAX=VM; engine.TMAX=4; engine.PRIMES=[P]
import base
base.VMAX=VM; base.TMAX=4; base.PRIMES=[P]
from thm import case, ls, factorint
def isq(q): return q>2 and len(factorint(q))==1
ours=[]
PA=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','tableA.json')))['PA']
for x in PA:
    if x[0]==P: ours.append((P,x[1],x[2],x[3],'PA'))
for q in range(4,VM):
    if not isq(q): continue
    for kind in 'SG':
        if kind=='G' and q%2==0: continue
        for k in range(4,(q+1)//2+1):
            c=case(kind,q,k)
            if c and ls(c[0],c[1],c[2],q+1,k,P): ours.append((P,c[0],k,q+1,'thm'))
L=base.build(False)[P]
D0=list(base.DIRECT); base.DIRECT.extend(ours); A=base.build(False)[P]; base.DIRECT[:]=D0
new4=sorted((t,k,v) for (t,k,v) in A.E if t>=3 and 2*k<=v and (t,k,v) not in L.E)
json.dump(dict(P=P,new4=new4,why={str(x):A.E[x] for x in new4}),open(f'new4_{P}.json','w'))
print(P,len(new4),new4[:15])
