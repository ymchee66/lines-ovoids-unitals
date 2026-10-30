import json,sys
from math import comb
from collections import defaultdict
sys.path.insert(0,'.')
from base import build, adm, PRIMES, VMAX, TMAX
from check import load
from lemma import lemma
from thm import case, ls
from groups import all_groups
D=json.load(open('tableA.json'))
import base
LOT=[tuple(x) for x in json.load(open('lot_v100.json'))]
base.DIRECT.extend((N,t,k,v,'LOT10 Sec. 4, '+g) for (N,t,k,v,g) in LOT)
L=build(False)
PA={tuple(x[:4]):(x[4],x[5]) for x in D['PA']}
G=all_groups(); byv=defaultdict(list)
for g in G: byv[g[2]].append(g)
cache={}
def short(name):
    name={'U33':'PSU(3,3)','U34':'PSU(3,4)','Sz8':'Sz(8)','L38':'PSL(3,8)','L37':'PSL(3,7)','L43':'PSL(4,3)','L33':'PSL(3,3)','R3':'2G2(3)'}.get(name,name)
    if name.startswith(('S2_','G2_','P2_')):
        q=name[3:]; name={'S':'PSL','G':'PGL','P':'PGammaL'}[name[0]]+f'(2,{q})'
    name=name.replace('3 x Q(16)','3\\times Q_{16}').replace('Q(8)','Q_8').replace('Alt(','A_{').replace('Sym(','S_{')
    import re as _r
    name=_r.sub(r'([AS])_\{(\d+)\)',r'\1_{\2}',name)
    return '\\mathrm{'+(name.replace('PGammaL','P\\Gamma L').replace('AGammaL','A\\Gamma L').replace('PSigmaL','P\\Sigma L')
            .replace('PSz(8)','Sz(8)').replace("'",'.').replace('2G2(3)','{}^2G_2(3)').replace(' ',''))+'}'
def label(key):
    N,t,k,v=key; g,how=PA[key]
    if g and not g.startswith('PSL/P'): return g
    q=v-1
    for kind,nm in (('S',f'PSL(2,{q})'),('G',f'PGL(2,{q})')):
        for kk in (k,v-k):
            c=case(kind,q,kk) if q>2 else None
            if c and c[0]>=t and ls(*c,v,kk,N): return nm
    for (f,name,vv,tm) in sorted(byv[v],key=lambda x:x[0]):
        if t>tm: continue
        if f not in cache: cache[f]=load(f)
        _,h,res=cache[f]
        for kk in (k,v-k):
            if kk in res and lemma(res[kk],h,comb(v,kk)//N,N): return name
    return g
direct=[key for key in PA if not L[key[0]].has(key[1],key[2],key[3])]
rows=defaultdict(lambda: defaultdict(list))   # v -> (t,group) -> [(k,N)]
for key in direct:
    N,t,k,v=key; rows[v][(t,short(label(key)))].append((k,N))
lines=[]
for v in sorted(rows):
    first=True
    for (t,g) in sorted(rows[v]):
        byk=defaultdict(list)
        for k,N in rows[v][(t,g)]: byk[k].append(N)
        ent=", ".join(f"{k}\\,({','.join(map(str,sorted(Ns)))})" for k,Ns in sorted(byk.items()))
        lines.append(f"{v if first else ''} & {t} & ${g}$ & {ent} \\\\")
        first=False
open('note/tab_direct.tex','w').write("\n".join(lines)+"\n")
rows_s=D['rows']
# nonexistence counts
s=[]
for (t,a,kn,di,re,op) in rows_s:
    no=sum(1 for p in PRIMES for (tt,k,v) in L[p].NO if tt==t and 2*k<=v)
    s.append(f"{t} & {a} & {kn} & {no} & {di} & {re} & {op-no} \\\\")
open('note/tab_summary.tex','w').write("\n".join(s)+"\n")
print(len(direct),len(lines)); print("\n".join(s))
