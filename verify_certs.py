"""Check every SAT certificate used in tableA: N classes, each of total length C(v,k)/N, using exactly the orbits of the group."""
import json,sys
from math import comb
from check import load
from groups import all_groups
G=all_groups(); byname={}
for f,n,v,T in G:
    byname[n]=f; byname[f[:-4]]=f; byname[f.split('/')[-1][:-4]]=f; byname[f]=f
byname['L38']='L38.txt'; byname['L37']='L37.txt'
cache={}; ok=bad=0; badl=[]
for fn in ['part5_results.jsonl','part6_results.jsonl','part7_results.jsonl','searchT_results.jsonl','part8_results.jsonl']:
    for l in open(fn):
        d=json.loads(l)
        if d['status']!='SAT': continue
        f=d.get('file') or byname.get(d['group']) or ('P2_32.txt' if fn=='part8_results.jsonl' else None)
        if f not in cache: cache[f]=load(f)
        v,h,res=cache[f]; N,k=d['N'],d['k']
        assert v==d['v'],(f,d['v'])
        kk=k if k in res else v-k
        L=res[kk]; s=comb(v,kk)//N
        cl=d['classes']
        if cl is None: badl.append((fn,'noclasses',d['group'],N,d['t'],k,v)); bad+=1; continue
        tot={}
        good=len(cl)==N and comb(v,kk)%N==0
        for c in cl:
            if sum(int(a)*b for a,b in c.items())!=s: good=False
            for a,b in c.items(): tot[int(a)]=tot.get(int(a),0)+b
        if tot!=L: good=False
        if good: ok+=1
        else: bad+=1; badl.append((fn,d['group'],N,d['t'],k,v))
print('ok',ok,'bad',bad); from collections import Counter; print(Counter((b[0],b[1]=="noclasses") for b in badl)); print([b for b in badl if b[1]!="noclasses"][:20])
