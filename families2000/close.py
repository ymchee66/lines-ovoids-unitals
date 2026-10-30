"""closure of the literature baseline for one prime N up to VMAX; writes the set of known (t,k,v) with k<=v/2"""
import sys,json,time
P=int(sys.argv[1]); VM=int(sys.argv[2]); TM=int(sys.argv[3])
import os; sys.path.insert(0,os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
import fastadm, engine
engine.adm=fastadm.adm; engine.VMAX=VM; engine.TMAX=TM; engine.PRIMES=[P]
import base
base.adm=fastadm.adm; base.VMAX=VM; base.TMAX=TM; base.PRIMES=[P]
# AGL(1,2^n) semiregular t=2 family for v=2^n beyond 64
from math import comb, gcd
for v in (128,256,512,1024):
    if v<=VM:
        for k in range(3,v-2,2):
            if gcd(k*(k-1),v-1)==1: base.DIRECT.append((comb(v-2,k-2)//(k*(k-1)),2,k,v,"AGL(1,2^n)"))
import lotgen
for (t,k,v,name) in lotgen.lot43(P,VM,TM): base.DIRECT.append((P,t,k,v,'LOT10 Thm 4.3, '+name))
t0=time.time()
L=base.build(False)[P]
known=sorted((t,k,v) for (t,k,v) in L.E if 2*k<=v)
json.dump(dict(P=P,VM=VM,TM=TM,known=known),open(f'known_{P}_{VM}_{TM}_lot.json','w'))
print(P,len(known),round(time.time()-t0,1),flush=True)
