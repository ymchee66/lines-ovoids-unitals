import csv,glob,json
from math import comb
from check import load
from thm import case, ls, factorint
from lemma import lemma
R=list(csv.DictReader(open('large_sets_table.csv')))
cache={f[:-4]:load(f) for f in glob.glob('[SGP]2_*.txt')}
def tm(g,q): return 3 if (g[0]!='S' or q%2==0 or q%4==3) else 2
T=set();Lm=set()
for r in R:
    if r['status']!='open': continue
    N,t,k,v=(int(r[x]) for x in 'Ntkv'); q=v-1
    if len(factorint(q))!=1: continue
    for kind in 'SG':
        for kk in (k,v-k):
            c=case(kind,q,kk)
            if c and c[0]>=t and ls(*c,v,kk,N): T.add((N,t,k,v))
    if (N,t,k,v) in T: continue
    for g,(vv,h,res) in cache.items():
        if vv!=v or t>tm(g,q): continue
        for kk in (k,v-k):
            if kk in res and lemma(res[kk],h,comb(v,kk)//N,N): Lm.add((N,t,k,v))
print('theorem',len(T),'lemma extra',len(Lm))
json.dump(dict(theorem=sorted(T),lemma=sorted(Lm)),open('cover.json','w'))
