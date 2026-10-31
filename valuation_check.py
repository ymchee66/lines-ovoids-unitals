"""Lemma 3.5 (the valuation lemma) (valuation condition) for PSL(3,3), PSL(3,7), PSL(3,8) and PSL(4,3): counts the admissible LS[N](2,k,v), N<=43 prime, that it excludes."""
import sys,json
from math import comb
from check import load
sys.path.insert(0,'.')
from engine import adm
PR=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]
def vp(n,p):
    c=0
    while n%p==0: n//=p; c+=1
    return c
def primes(n):
    out=[];d=2
    while d*d<=n:
        if n%d==0:
            out.append(d)
            while n%d==0: n//=d
        d+=1
    if n>1: out.append(n)
    return out
for f,name in [('L33.txt','PSL(3,3)'),('L37.txt','PSL(3,7)'),('L38.txt','PSL(3,8)'),('L43.txt','PSL(4,3)')]:
    v,h,res=load(f)
    tot=excl=0; exp=[]; minc=[]
    for k in sorted(res):
        if k<3 or 2*k>v: continue
        L=res[k]
        for N in PR:
            if not adm(N,2,k,v): continue
            tot+=1
            s=comb(v,k)//N
            ok=True
            for l in primes(h):
                w=vp(s,l)
                c=sum(n for ln,n in L.items() if vp(ln,l)<=w)
                if c<N: ok=False; break
            if not ok: excl+=1
            else: exp.append((N,k))
    print(name,v,h,'admissible t=2 prime N<=43:',tot,'excluded by valuation lemma:',excl,'remaining:',len(exp),exp[:40])
