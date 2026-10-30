"""LOT10 Conjecture 4.2: G=PSL(2,q) if q=3 mod 4, PGL(2,q) otherwise (q odd). If |G| divides C(q+1,k) then LS[C/|G|](3,k,q+1) exists.
With N=C/|G| each design has exactly |G| blocks: the short orbits must be grouped into sets of total length |G|."""
import sys
from math import comb
from fractions import Fraction
from ortools.sat.python import cp_model
from check import load
def patterns(ds, target=Fraction(1), start=0):
    # multisets of denominators d (orbit length h/d) with sum 1/d = 1, d>1
    if target==0: yield []; return
    for i in range(start,len(ds)):
        f=Fraction(1,ds[i])
        if f<=target:
            for rest in patterns(ds,target-f,i): yield [ds[i]]+rest
def check(f):
    v,h,res=load(f); q=v-1; out=[]
    for k in range(4,v//2+1):
        if comb(v,k)%h: continue
        L=res[k]; short={h//l:c for l,c in L.items() if l!=h}
        if not short: out.append((k,'OK-semiregular')); continue
        ds=sorted(short)
        P=list(patterns(ds))
        m=cp_model.CpModel(); x=[m.NewIntVar(0,10**12,'') for _ in P]
        for d in ds: m.Add(sum(p.count(d)*x[i] for i,p in enumerate(P))==short[d])
        s=cp_model.CpSolver(); s.parameters.max_time_in_seconds=60; st=s.Solve(m)
        out.append((k,s.StatusName(st),len(P)))
    return out
for f in sys.argv[1:]:
    print(f,check(f),flush=True)
