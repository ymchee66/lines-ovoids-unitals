import json,sys
from math import comb
from fractions import Fraction
def load(f):
    d=json.loads(open(f).read()); h=d['order']; v=d['v']
    res={}
    for k,o in d['counts'].items():
        o=[Fraction(str(x).replace(' ','')) for x in o]; k=int(k)
        assert all(x>=0 and x.denominator==1 for x in o),(f,k)
        L={}
        for x,u in zip(o,d['ord']):
            if x: L[h//u]=L.get(h//u,0)+int(x)
        assert sum(a*b for a,b in L.items())==comb(v,k)
        res[k]=L
    return v,h,res
if __name__=="__main__":
    v,h,res=load(sys.argv[1])
    for k,L in res.items(): print(k,sum(L.values()),sorted(L.items())[:6])
