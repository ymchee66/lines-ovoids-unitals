import numpy as np, re, json, sys
from itertools import combinations
from math import comb
from scipy.sparse import coo_matrix
from scipy.sparse.csgraph import connected_components
txt=open('mat.txt').read().replace('\n',' ')
groups={}
for m in re.finditer(r'(M\w+) (\d+)\s+(\[.*?\]\s*\])\s*(?=M|$)',txt):
    groups[m[1]]=(int(m[2]),json.loads(m[3].replace(' ','')))
def masks(n,k):
    # all k-subsets as uint32 via combinations (n<=24)
    idx=np.array(list(combinations(range(n),k)),dtype=np.uint32)
    return np.sort((np.uint32(1)<<idx).sum(axis=1,dtype=np.uint64).astype(np.uint64))
def orbit_lengths(name,k):
    h,gens=groups[name]; n=len(gens[0])
    M=masks(n,k); N=len(M); rows=[];cols=[]
    for g in gens:
        img=np.zeros(N,dtype=np.uint64)
        for i in range(n):
            img|=((M>>np.uint64(i))&np.uint64(1))<<np.uint64(g[i]-1)
        j=np.searchsorted(M,img); rows.append(np.arange(N)); cols.append(j)
    A=coo_matrix((np.ones(N*len(gens),dtype=np.int8),(np.concatenate(rows),np.concatenate(cols))),shape=(N,N))
    nc,lab=connected_components(A,directed=True,connection='weak')
    sizes=np.bincount(lab); L={}
    for s in sizes: L[int(s)]=L.get(int(s),0)+1
    assert sum(a*b for a,b in L.items())==comb(n,k)
    return h,L
if __name__=="__main__":
    out={}
    for name in sys.argv[1:]:
        h,gens=groups[name]; n=len(gens[0]); out[name]={'v':n,'order':h,'counts':{}}
        for k in range(2,n//2+1):
            _,L=orbit_lengths(name,k); out[name]['counts'][k]=L; print(name,k,sorted(L.items()),flush=True)
    json.dump(out,open('mathieu_orbits.json','w'))
