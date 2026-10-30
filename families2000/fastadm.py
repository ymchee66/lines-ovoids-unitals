def vN(a,b,p):
    """exponent of prime p in C(a,b) via Kummer: number of carries adding b and a-b in base p"""
    if b<0 or b>a: return None
    c=0; carry=0; x=b; y=a-b
    while x or y or carry:
        s=x%p+y%p+carry
        carry=1 if s>=p else 0
        c+=carry; x//=p; y//=p
    return c
def adm(p,t,k,v):
    if not (0<=t<=k<=v): return False
    for i in range(t+1):
        if vN(v-i,k-i,p)<1: return False
    return True
