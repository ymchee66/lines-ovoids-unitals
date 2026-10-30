import sys,json
import os; sys.path.insert(0,os.path.join(os.path.dirname(os.path.abspath(__file__)),'..'))
from math import comb
from thm import factorint, case, ls
def isq(q): return len(factorint(q))==1
M=[]
for q in range(17,2000):
    if not isq(q): continue
    fams=[]
    if q%60 in (23,47):
        fams.append((10,comb(q-2,7)//180,(q-1)*(q-3)*(q-5)*(q-7)//1920,'S'))
    if q%12==5 and q%5!=1 and q%7 not in (0,1,6):
        fams.append((7,(q-2)*(q-3)*(q-4)*(q-5)//2520,(q-3)*(q-5)//24,'G'))
    if q%2==0:
        m=q.bit_length()-1
        if m>=5 and m%2 and m%3: fams.append((7,(q-2)*(q-3)*(q-4)*(q-5)//2520,(q-2)*(q-4)//24,'S'))
    for n,s0,a,kind in fams:
        c=case(kind,q,n); assert c and c[2]==a and 2*comb(q+1,n)//c[1]==s0,(q,n)
        for N in factorint(s0):
            if N<5 or not((s0//N)%2==0 or N<=a): continue
            assert ls(c[0],c[1],c[2],q+1,n,N)
            M.append(dict(N=N,t=3,k=n,v=q+1,q=q,part='i' if n==10 else 'ii'))
            V=N*(q+2)
            if V<=2000:
                for k in range(n*N+1,(n+1)*N): M.append(dict(N=N,t=4,k=k,v=V,q=q,part='iii'))
json.dump(M,open('members.json','w'))
Ps=sorted({m['N'] for m in M})
open('primes.txt','w').write('\n'.join(map(str,Ps))+'\n')
print(len(M),len([m for m in M if m['t']==3]),len(Ps))
