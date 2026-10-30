"""Verify certs.jsonl: for each direct large set, the classes partition the orbits of the stated group on k-subsets
into N classes of equal total length C(v,k)/N, and the group is t-homogeneous."""
import json
from math import comb
from check import load
from groups import all_groups
T={f:tm for f,n,v,tm in all_groups()}
cache={}; ok=0; bad=[]
for l in open('certs.jsonl'):
    d=json.loads(l); N,t,k,v=d['N'],d['t'],d['k'],d['v']; f=d['file']
    if f is None or d['classes'] is None: bad.append((N,t,k,v,'none')); continue
    if f not in cache: cache[f]=load(f)
    vv,h,res=cache[f]; kk=d['kk']; assert vv==v and kk in (k,v-k)
    s=comb(v,kk)//N; tot={}
    good=comb(v,kk)%N==0 and len(d['classes'])==N and T[f]>=t
    for c in d['classes']:
        if sum(int(a)*b for a,b in c.items())!=s: good=False
        for a,b in c.items(): tot[int(a)]=tot.get(int(a),0)+b
    good=good and tot==res[kk]
    if good: ok+=1
    else: bad.append((N,t,k,v,f))
print('verified',ok,'failed',len(bad),bad[:10])
