"""Partition orbits into N classes of equal size s: give N-1 classes a non-regular part = r mod h, last class gets the rest; fill with regular orbits."""
import sys,json
from math import comb, gcd
from functools import reduce
from ortools.sat.python import cp_model
from check import load
def solve(L,h,s,N,TL=60):
    nonreg={l:c for l,c in L.items() if l!=h}; R=L.get(h,0)
    r=s%h; avail=dict(nonreg); groups=[]
    g=reduce(gcd,list(L)); 
    if s%g: return 'GCD',None
    for c in range(N-1):
        m=cp_model.CpModel(); ls=sorted(avail)
        y={l:m.NewIntVar(0,avail[l],'') for l in ls}; z=m.NewIntVar(0,10**6,'')
        m.Add(sum(l*y[l] for l in ls)==r+h*z)
        m.Minimize(z)
        sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=TL; sv.parameters.num_workers=8
        st=sv.Solve(m)
        if st not in (cp_model.OPTIMAL,cp_model.FEASIBLE): return 'FAIL at class %d'%c,None
        grp={l:sv.Value(y[l]) for l in ls if sv.Value(y[l])}
        for l,a in grp.items(): avail[l]-=a
        groups.append(grp)
    groups.append({l:a for l,a in avail.items() if a})
    need=[]
    for grp in groups:
        e=sum(l*a for l,a in grp.items())
        if e>s or (s-e)%h: return 'BAD',None
        need.append((s-e)//h)
    assert sum(need)==R
    for grp,n in zip(groups,need):
        if n: grp[h]=n
    return 'SAT',groups
if __name__=="__main__":
    import csv
    Rw=list(csv.DictReader(open('large_sets_table.csv')))
    out=open('part3_results.jsonl','a')
    for f in sys.argv[1:]:
        v,h,res=load(f)
        T=sorted((int(r['N']),int(r['k'])) for r in Rw if int(r['v'])==v and int(r['t'])==2 and r['status']=='open')
        for N,k in T:
            L=res[k]; s=comb(v,k)//N
            st,groups=solve(L,h,s,N)
            print(f,N,k,st,flush=True)
            print(json.dumps(dict(group=f[:-4],N=N,t=2,k=k,v=v,status=st,classes={i:{str(a):b for a,b in g.items()} for i,g in enumerate(groups)} if groups else None)),file=out,flush=True)
