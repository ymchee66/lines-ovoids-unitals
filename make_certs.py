"""Explicit certificate (orbit partition) for every direct large set in tableA.json; writes certs.jsonl."""
import json,sys,os
from math import comb
sys.path.insert(0,'.')
from base import build
from check import load
from groups import all_groups
import part3, part4
L=build(False)
D=json.load(open('tableA.json'))
PA={tuple(x[:4]):(x[4],x[5]) for x in D['PA']}
direct=sorted(k for k in PA if not L[k[0]].has(k[1],k[2],k[3]))
G=all_groups(); byv={}
for f,n,v,T in G: byv.setdefault(v,[]).append((f,n,T))
# existing verified certificates
have={}
for fn in ['part5_results.jsonl','part6_results.jsonl','part7_results.jsonl','searchT_results.jsonl','part8_results.jsonl']:
    for l in open(fn):
        d=json.loads(l)
        if d['status']=='SAT' and d.get('classes'): have.setdefault((d['N'],d['k'],d['v']),[]).append(d)
done=set()
if os.path.exists('certs.jsonl'):
    for l in open('certs.jsonl'): d=json.loads(l); done.add((d['N'],d['t'],d['k'],d['v']))
out=open('certs.jsonl','a'); cache={}
names={f:n for f,n,v,T in G}
def fileof(d):
    if d.get('file'): return d['file']
    g=d['group']
    for f,n,v,T in G:
        if g in (n,f[:-4],f.split('/')[-1][:-4]): return f
    return 'P2_32.txt'
for key in direct:
    if key in done: continue
    N,t,k,v=key; rec=None
    for d in have.get((N,k,v),[])+have.get((N,v-k,v),[]):
        f=fileof(d); T=[x for x in byv[v] if x[0]==f][0][2]
        if T>=t: rec=(f,d['k'],d['classes'],'ip' if not d.get('lemma') else 'lemma'); break
    if rec is None:
        for f,n,T in sorted(byv[v],key=lambda x:x[0]):
            if T<t: continue
            if f not in cache: cache[f]=load(f)
            vv,h,res=cache[f]
            kk=k if k in res else v-k
            if kk not in res: continue
            s=comb(v,kk)//N
            st,gs=part3.solve(res[kk],h,s,N,TL=10)
            if st!='SAT' and st.startswith('FAIL at class') and st!='FAIL at class 0': st,gs=part4.solve(res[kk],h,s,N,TL=60)
            if st=='SAT':
                rec=(f,kk,[{str(a):b for a,b in g.items()} for g in gs],'solved'); break
    print(json.dumps(dict(N=N,t=t,k=k,v=v,file=rec[0] if rec else None,group=names.get(rec[0]) if rec else None,kk=rec[1] if rec else None,classes=rec[2] if rec else None)),file=out,flush=True)
