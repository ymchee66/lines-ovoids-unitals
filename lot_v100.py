import json
from math import comb
from check import load
from groups import all_groups
from lot import lot_ok
PR=[2,3,5,7,11,13,17,19,23,29,31,37,41,43]
out=set()
for f,name,v,T in all_groups():
    vv,h,res=load(f)
    for k,L in res.items():
        if not (T<k<=v-T): continue
        for N in PR:
            if lot_ok(N,v,k,h,L): out.add((N,T,min(k,v-k),v,name))
json.dump(sorted(out),open('lot_v100.json','w'))
print(len(out))
