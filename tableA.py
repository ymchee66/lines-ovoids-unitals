"""Existence table layers: literature (L) and literature + direct results of the projective-lines paper (A)."""
import sys,json,re
sys.path.insert(0,'.')
import base
from base import build, adm, PRIMES, VMAX, TMAX
def names_for_part(d,default):
    return d.get('group') or default
PA={}   # (N,t,k,v) -> (group, how)
def put(key,group,how):
    N,t,k,v=key
    if N not in PRIMES: return
    k=min(k,v-k); key=(N,t,k,v)
    if key not in PA: PA[key]=(group,how)
c=json.load(open('cover.json'))
for x in c['theorem']: put(tuple(x),'PSL/PGL(2,q)','theorem')
for x in c['lemma']: put(tuple(x),'PSL/PGL/PGammaL(2,q)','lemma')
from groups import all_groups
TM={}
for _f,_n,_v,_T in all_groups():
    TM[_n]=_T; TM[_f]=_T; TM[_f.replace('.txt','')]=_T; TM['aff/'+_f]=_T
for _k in ['L38','L37','Sz8','U33','U34','R3','L33','L43']: TM.setdefault(_k,2)
def tmax(d):
    """degree of homogeneity of the group of a search record: a partition into unions of orbits of a
    T-homogeneous group gives T-designs, whatever t the search was run for"""
    T=TM.get(d.get('group')) or TM.get(d.get('file',''))
    assert T is not None, d.get('group')
    T=max(T,d['t'])
    assert adm(d['N'],T,d['k'],d['v']) or d['N'] not in PRIMES
    return T
UPG=[]
for f in ['part5_results.jsonl','part6_results.jsonl','part7_results.jsonl','searchT_results.jsonl']:
    try:
        for l in open(f):
            d=json.loads(l)
            if d['status']=='SAT':
                T=tmax(d)
                if T>d['t']: UPG.append((d['N'],d['t'],T,d['k'],d['v'],d.get('group')))
                put((d['N'],T,d['k'],d['v']),d.get('group'),'lemma' if d.get('lemma') or d.get('how')=='lemma' else 'ip')
    except FileNotFoundError: pass
for l in open('part8_results.jsonl'):
    d=json.loads(l)
    if d['status']=='SAT': put((d['N'],d['t'],d['k'],d['v']),'PGammaL(2,32)','lemma' if d['lemma'] else 'ip')
PA={k:v for k,v in PA.items() if not (k[1]<4 and any((k[0],tt,k[2],k[3]) in PA for tt in range(k[1]+1,5)))}
import os
LOTFILE=os.environ.get('LOTFILE','lot_v100.json')
LOT=[tuple(x) for x in json.load(open(LOTFILE))]
base.DIRECT.extend((N,t,k,v,'LOT10 Sec. 4, '+g) for (N,t,k,v,g) in LOT)
L=build(False)
DIRECT0=list(base.DIRECT)
base.DIRECT.extend((N,t,k,v,'PL') for (N,t,k,v) in PA)
A=build(False)
base.DIRECT[:]=DIRECT0
rows=[]
for t in range(2,TMAX+1):
    adm_=known=direct=rec=0
    for p in PRIMES:
        for v in range(t+2,VMAX+1):
            for k in range(t+1,v//2+1):
                if not(adm(p,t,k,v) and v-k>=t): continue
                adm_+=1
                if L[p].has(t,k,v): known+=1
                elif A[p].has(t,k,v):
                    if (p,t,k,v) in PA: direct+=1
                    else: rec+=1
    rows.append((t,adm_,known,direct,rec,adm_-known-direct-rec))
for r in rows: print(r)
print('upgraded records',len(UPG),'distinct',len({(u[0],u[2],u[3],u[4]) for u in UPG}))
json.dump(dict(rows=rows,PA=[list(k)+list(v) for k,v in PA.items()]),open('tableA.json','w'))
