"""PSL(2,q), q odd, condition (O) for all odd primes: stabilisers are 2-groups. Orbit counts by stabiliser order."""
from math import comb
from thm import primefactors, factorint
def v2(n):
    c=0
    while n%2==0: n//=2; c+=1
    return c
def O_all(q,k):
    (p,e),=factorint(q).items()
    if k%p in (0,1): return False
    if any(k%l in (0,1,2) for l in primefactors(q-1) if l>2): return False
    if any(k%l==0 for l in primefactors(q+1) if l>2): return False
    return True
def C(n,r):
    return comb(n,r) if 0<=r<=n else 0
def psl_2grp(q,k):
    if q%2==0 or not O_all(q,k): return None
    eps=1 if q%4==1 else -1
    h=q*(q*q-1)//2
    a=v2((q-eps)//2)
    ntor=q*(q+eps)//2
    def Fcyc(i):
        n=2**i
        if eps==-1: return C((q+1)//n,k//n) if k%n==0 else 0
        return sum(C(2,e)*C((q-1)//n,(k-e)//n) for e in range(3) if (k-e)%n==0)
    def Fdih(i):           # D of order 2^(i+1), cyclic part 2^i
        n=2**i
        if eps==-1: return C((q+1)//(2*n),k//(2*n)) if k%(2*n)==0 else 0
        m=(q-1-2*n)//(2*n)
        return sum(C(2,y)*C(m,(k-2*x-n*y)//(2*n)) for x in (0,1) for y in (0,1,2) if k-2*x-n*y>=0 and (k-2*x-n*y)%(2*n)==0)
    # classes: ('C',i) i=1..a ; ('D',i) i=1..a  (D,1)=V4
    cls=[('C',i) for i in range(1,a+1)]+[('D',i) for i in range(1,a+1)]
    num={('C',i):ntor for i in range(1,a+1)}
    num[('D',1)]=ntor*(q-eps)//4//3
    for i in range(2,a+1): num[('D',i)]=ntor*(q-eps)//2**(i+1)
    order={('C',i):2**i for i in range(1,a+1)}; order.update({('D',i):2**(i+1) for i in range(1,a+1)})
    F={('C',i):Fcyc(i) for i in range(1,a+1)}; F.update({('D',i):Fdih(i) for i in range(1,a+1)})
    def cont(U,V):          # number of V-class subgroups containing a given U
        tU,i=U; tV,j=V
        if tU=='C' and tV=='C': return 1 if j>i else 0
        if tU=='C' and tV=='D':
            if j<i: return 0
            if j==1: return (q-eps)//4 if i==1 else 0
            inner=(q-eps)//2**(j+1)
            outer=(q-eps)//2 if i==1 else 0
            return inner+outer
        if tU=='D' and tV=='C': return 0
        if tU=='D' and tV=='D':
            if j<=i: return 0
            if i==1: return 3
            return 1
    g={}
    for U in sorted(cls,key=lambda U:-order[U]):
        g[U]=F[U]-sum(cont(U,V)*g[V] for V in cls if order[V]>order[U])
    out={}
    for U in cls:
        x=num[U]*g[U]*order[U]
        assert x%h==0,(q,k,U,x%h)
        if x: out[order[U]]=out.get(order[U],0)+x//h
    return h,out
def fix_count(k,sizes):
    """number of k-subsets that are unions of orbits; sizes = dict size->count"""
    dp={0:1}
    for sz,cnt in sizes.items():
        nd={}
        for s0,w in dp.items():
            for c in range(cnt+1):
                s=s0+c*sz
                if s>k: break
                nd[s]=nd.get(s,0)+w*C(cnt,c)
        dp=nd
    return dp.get(k,0)
def pgl_2grp(q,k):
    if q%2==0 or not O_all(q,k): return None
    e=1 if q%4==1 else -1
    h=q*(q*q-1); b=v2(q-e)
    ninv={1:q*(q+1)//2,-1:q*(q-1)//2}
    nT=q*(q+e)//2
    cls=[('C2',e),('C2',-e)]+[('C',i) for i in range(2,b+1)]+[('VA',0),('VB',0)]+[('D',j) for j in range(2,b+1)]
    num={('C2',e):ninv[e],('C2',-e):ninv[-e],('VA',0):ninv[e]*(q-e)//12,('VB',0):ninv[e]*(q-e)//4}
    for i in range(2,b+1): num[('C',i)]=nT
    for j in range(2,b+1): num[('D',j)]=nT*(q-e)//2**j
    order={('C2',e):2,('C2',-e):2,('VA',0):4,('VB',0):4}
    order.update({('C',i):2**i for i in range(2,b+1)}); order.update({('D',j):2**(j+1) for j in range(2,b+1)})
    v=q+1
    def sizes(U):
        t,i=U
        if t=='C2': return {1:2,2:(q-1)//2} if i==1 else {2:(q+1)//2}
        if t=='C': return {1:2,2**i:(q-1)//2**i} if e==1 else {2**i:(q+1)//2**i}
        if t=='VA': return {2:3,4:(q-5)//4} if e==1 else {4:(q+1)//4}
        if t=='VB': return {2:1,4:(q-1)//4} if e==1 else {2:2,4:(q-3)//4}
        if t=='D':
            n=2**i
            return {2:1,n:1,2*n:(q-1-n)//(2*n)} if e==1 else {n:1,2*n:(q+1-n)//(2*n)}
    F={U:fix_count(k,sizes(U)) for U in cls}
    def cont(U,V):
        tU,i=U; tV,j=V
        if tU=='C2':
            s=i
            if tV=='C': return 1 if s==e else 0
            if tV=='VA': return (q-e)//4 if s==e else 0
            if tV=='VB': return (q-e)//4 if s==e else (q+e)//2
            if tV=='D': return ((q-e)//2**j+(q-e)//2) if s==e else (q+e)//2
            return 0
        if tU=='C':
            if tV=='C': return 1 if j>i else 0
            if tV=='D': return (q-e)//2**j if j>=i else 0
            return 0
        if tU=='VA': return 3 if tV=='D' else 0
        if tU=='VB': return 0
        if tU=='D': return 1 if (tV=='D' and j>i) else 0
    g={}
    for U in sorted(cls,key=lambda U:-order[U]):
        g[U]=F[U]-sum(cont(U,V)*g[V] for V in cls if order[V]>order[U])
    out={}
    for U in cls:
        x=num[U]*g[U]*order[U]
        assert x%h==0,(q,k,U)
        if x: out[order[U]]=out.get(order[U],0)+x//h
    return h,out
def pgl_2grp2(q,k):
    """corrected: dihedral 2-subgroups D_j (j<b) come in two kinds by the type of their outer involutions."""
    if q%2==0 or not O_all(q,k): return None
    e=1 if q%4==1 else -1
    h=q*(q*q-1); b=v2(q-e)
    ninv={1:q*(q+1)//2,-1:q*(q-1)//2}; nT=q*(q+e)//2
    X={}   # class -> dict(order, num, sizes, inside: {class: count of such subgroups inside one X})
    X[('C2',1)]=dict(o=2,n=ninv[1],sz={1:2,2:(q-1)//2})
    X[('C2',-1)]=dict(o=2,n=ninv[-1],sz={2:(q+1)//2})
    for i in range(2,b+1):
        X[('C',i)]=dict(o=2**i,n=nT,sz=({1:2,2**i:(q-1)//2**i} if e==1 else {2**i:(q+1)//2**i}))
    X[('VA',)]=dict(o=4,n=ninv[e]*(q-e)//12,sz=({2:3,4:(q-5)//4} if e==1 else {4:(q+1)//4}))
    X[('VB',)]=dict(o=4,n=ninv[e]*(q-e)//4,sz=({2:1,4:(q-1)//4} if e==1 else {2:2,4:(q-3)//4}))
    def dsz(j,splitouter):      # orbit sizes of a dihedral group of order 2^(j+1); splitouter = number of split outer involutions
        n=2**j; d={}
        if e==1: d[2]=1
        if splitouter: d[n]=d.get(n,0)+splitouter*2//n
        rest=q+1-sum(s*c for s,c in d.items()); d[2*n]=d.get(2*n,0)+rest//(2*n); return d
    for j in range(2,b):
        for sgn in (1,-1):
            X[('D',j,sgn)]=dict(o=2**(j+1),n=nT*(q-e)//2**j//2,sz=dsz(j,2**j if sgn==1 else 0))
    X[('D',b,0)]=dict(o=2**(b+1),n=nT*(q-e)//2**b,sz=dsz(b,2**(b-1)))
    def inside(Xc):
        """counts of each class of proper 2-subgroups inside one subgroup of class Xc"""
        t=Xc[0]; I={}
        if t=='C2': return I
        if t=='C':
            i=Xc[1]; I[('C2',e)]=1
            for l in range(2,i): I[('C',l)]=1
            return I
        if t=='VA': I[('C2',e)]=3; return I
        if t=='VB': I[('C2',e)]=1; I[('C2',-e)]=2; return I
        j,sgn=Xc[1],Xc[2]; n=2**j
        if sgn==0: osp=on=2**(j-1)
        else: osp,on=(n,0) if sgn==1 else (0,n)
        I[('C2',1)]=I.get(('C2',1),0)+osp; I[('C2',-1)]=I.get(('C2',-1),0)+on
        I[('C2',e)]+=1
        for l in range(2,j+1): I[('C',l)]=1
        # Klein four-groups {1,z,s,sz}: s and sz have the same type
        pairs_sp, pairs_ns = osp//2, on//2
        A_from = pairs_sp if e==1 else pairs_ns     # pairs of type e give VA
        B_from = pairs_ns if e==1 else pairs_sp
        I[('VA',)]=A_from; I[('VB',)]=B_from
        for l in range(2,j):
            if sgn==0: I[('D',l,1)]=I[('D',l,-1)]=2**(j-l)//2
            else: I[('D',l,sgn)]=2**(j-l)
        return I
    F={c:fix_count(k,X[c]['sz']) for c in X}
    cont={}
    for Xc in X:
        for Y,cnt in inside(Xc).items():
            cont[(Y,Xc)]=X[Xc]['n']*cnt//X[Y]['n']
            assert X[Xc]['n']*cnt % X[Y]['n']==0,(q,Y,Xc)
    g={}
    for U in sorted(X,key=lambda U:-X[U]['o']):
        g[U]=F[U]-sum(cont.get((U,V),0)*g[V] for V in X if X[V]['o']>X[U]['o'])
    out={}
    for U in X:
        x=X[U]['n']*g[U]*X[U]['o']
        assert x%h==0,(q,k,U)
        if x: out[X[U]['o']]=out.get(X[U]['o'],0)+x//h
    return h,out
