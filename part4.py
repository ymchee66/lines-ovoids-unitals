"""Global model: N classes, each non-regular part e_c <= s with e_c = s mod h; regular orbits fill the rest."""
import sys,json
from math import comb
from ortools.sat.python import cp_model
from check import load
def solve(L,h,s,N,TL=300):
    nonreg={l:c for l,c in L.items() if l!=h}; R=L.get(h,0)
    if sum(nonreg.values())==0 and s%h: return 'NO',None
    m=cp_model.CpModel(); ls=sorted(nonreg)
    y=[{l:m.NewIntVar(0,nonreg[l],'') for l in ls} for c in range(N)]
    for l in ls: m.Add(sum(y[c][l] for c in range(N))==nonreg[l])
    tot=sum(l*a for l,a in nonreg.items()); assert tot<=s or True
    zb=tot//h+1
    for c in range(N):
        z=m.NewIntVar(0,zb,'')
        m.Add(sum(l*y[c][l] for l in ls)==s%h+h*z)
        if tot>s and s<2**62: m.Add(sum(l*y[c][l] for l in ls)<=s)
    # symmetry: order classes by count of largest non-regular length
    for c in range(N-1): m.Add(sum(y[c][l]*(i+1) for i,l in enumerate(ls[-3:])) >= sum(y[c+1][l]*(i+1) for i,l in enumerate(ls[-3:])))
    sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=TL; sv.parameters.num_workers=8
    st=sv.Solve(m)
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE):
        gs=[]
        for c in range(N):
            g={l:sv.Value(y[c][l]) for l in ls if sv.Value(y[c][l])}
            e=sum(l*a for l,a in g.items())
            if s>e: g[h]=(s-e)//h
            gs.append(g)
        return 'SAT',gs
    return sv.StatusName(st),None
if __name__=="__main__":
    f=sys.argv[1]; v,h,res=load(f); out=open('part4_results.jsonl','a')
    for line in open('part3_results.jsonl'):
        d=json.loads(line)
        if d['group']!=f[:-4] or d['status']=='SAT' or d['status']=='GCD' or d['status']=='FAIL at class 0': continue
        N,k=d['N'],d['k']; s=comb(v,k)//N
        st,gs=solve(res[k],h,s,N)
        print(f,N,k,st,flush=True)
        print(json.dumps(dict(group=f[:-4],N=N,t=2,k=k,v=v,status=st,classes=[{str(a):b for a,b in g.items()} for g in gs] if gs else None)),file=out,flush=True)
