import json,glob
from math import comb
from collections import Counter,defaultdict
M=json.load(open('members.json'))
byN=defaultdict(list)
for m in M: byN[m['N']].append(m)
def s0(m):
    q=m['q']
    if m['part']=='i' or (m['part']=='iii' and q%60 in (23,47) and 10*m['N']<m['k']<11*m['N']): return comb(q-2,7)//180
    return (q-2)*(q-3)*(q-4)*(q-5)//2520
tab=Counter(); oddq=set(); missing=[]
for N,ms in byN.items():
    fs=glob.glob(f'known_{N}_2000_4_lot.json')
    if not fs: missing.append(N); continue
    want={(m['t'],min(m['k'],m['v']-m['k']),m['v']) for m in ms}
    K=set()
    for x in json.load(open(fs[0]))['known']:
        t=tuple(x)
        if t in want: K.add(t)
    for m in ms:
        known=(m['t'],min(m['k'],m['v']-m['k']),m['v']) in K
        par='even' if (s0(m)//N)%2==0 else 'odd'
        tab[(m['part'],par,known)]+=1
        if par=='odd' and known: oddq.add(m['q'])
for k,v in sorted(tab.items()): print(k,v)
print('missing primes',missing,'q of odd-known:',sorted(oddq))
