from math import comb
def chain_ok(h,counts,total,N):
    """counts: {r: n_r} orbits of length h/r with r powers of 2 (r=1 regular). Exact criterion for a partition into N classes of size total/N."""
    if total%N: return False
    s=total//N; m=max(counts).bit_length()-1; unit=h>>m
    if s%unit: return False
    sigma=s//unit; carry=0
    for r in range(m):               # weight 2^r items: orbits of length h/2^(m-r)
        A=counts.get(2**(m-r),0)+carry; beta=(sigma>>r)&1
        if A<N*beta or (A-N*beta)%2: return False
        carry=(A-N*beta)//2
    A=counts.get(1,0)+carry
    return A==N*(sigma>>m)
