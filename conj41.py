"""Test Conjecture 4.1 of Laue, Omidi, Tayfeh-Rezaie on the 187 groups of degree <= 100:
for |G| | C(v,k), N | C/|G| and C/(|G|m) < N <= C/(|G|r) (Thm 4.3 form, r = #primes of |G|;
and Thm 4.4 form with n = lcm of stabilizer orders), decide whether the orbits can be partitioned into N classes of length C/N."""
import json,sys
from math import comb, gcd, lcm, ceil
from fractions import Fraction
from functools import reduce
from check import load
from groups import all_groups
from lot import primes_of, mval
cases=[]
for f,name,v,T in all_groups():
    vv,h,res=load(f)
    for k,L in res.items():
        if not (T<k<=v//2): continue
        C=comb(v,k)
        if C%h: continue
        M=C//h
        ratios={h//l for l in L}; n=reduce(lcm,ratios,1)
        for form,ps in (('4.3',primes_of(h)),('4.4',primes_of(gcd(n,h)))):
            if not ps: continue
            r=len(ps); m=mval(ps)
            for d in range(r, ceil(m)+1):           # class length s = d*h, N = M/d
                if d< r or Fraction(d)>=m: continue
                if M%d: continue
                short={l:c for l,c in L.items() if l!=h}
                Ls=sum(l*c for l,c in short.items())
                cases.append(dict(group=name,file=f,v=v,k=k,h=h,form=form,r=r,m=float(m),d=d,N=M//d,
                                  trivial=Ls<=d*h, Lh=Ls//h))
json.dump(cases,open('conj41_cases.json','w'))
nt=[c for c in cases if not c['trivial']]
print(len(cases),'nontrivial',len(nt), 'max L/h', max([c['Lh'] for c in nt],default=0))
from collections import Counter
print(Counter((c['form']) for c in nt))
