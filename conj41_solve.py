import json,sys
from math import lcm
from functools import reduce
from ortools.sat.python import cp_model
from check import load
cases=json.load(open('conj41_cases.json'))
cache={}
def solve(L,h,d,K,TL=20):
    stab={h//l:c for l,c in L.items() if l!=h}
    W=reduce(lcm,stab,1)                     # units: h/W, orbit with stabilizer s has weight W/s
    red={s:(c % s)+min(c//s,K)*s for s,c in stab.items()}
    red={s:c for s,c in red.items() if c}
    tot=sum(c*(W//s) for s,c in red.items())
    assert tot%W==0
    G=tot//W
    if G==0: return True
    m=cp_model.CpModel()
    x={(g,s):m.NewIntVar(0,c,'') for g in range(G) for s,c in red.items()}
    y=[m.NewIntVar(0,d,'') for g in range(G)]
    for s,c in red.items(): m.Add(sum(x[g,s] for g in range(G))==c)
    for g in range(G): m.Add(sum(x[g,s]*(W//s) for s in red)==W*y[g])
    for g in range(G-1): m.Add(y[g]>=y[g+1])
    sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=TL; sv.parameters.num_workers=2
    st=sv.Solve(m)
    if st in (cp_model.OPTIMAL,cp_model.FEASIBLE): return True
    if st==cp_model.INFEASIBLE: return False
    return None
out=[]
for c in cases:
    if c['trivial']: c['status']='trivial'; out.append(c); continue
    if c['file'] not in cache: cache[c['file']]=load(c['file'])
    v,h,res=cache[c['file']]; L=res[c['k']]
    st=None
    for K in (1,2,4):
        r=solve(L,h,c['d'],K)
        if r: st='feasible'; break
        st='infeasible-reduced' if r is False else 'timeout'
    c['status']=st; out.append(c)
    if st!='feasible': print(c['group'],c['v'],c['k'],c['form'],'d',c['d'],'r',c['r'],'m',round(c['m'],2),st,flush=True)
json.dump(out,open('conj41_results.json','w'))
from collections import Counter
print(Counter(c['status'] for c in out))
