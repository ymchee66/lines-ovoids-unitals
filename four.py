from ortools.sat.python import cp_model
def four_ok(h,r,n2,nr,nD,total,N,TL=10):
    """orbits: n2 of length h/2, nr of h/r, nD of h/(2r), rest regular. Exact criterion (assuming non-regular total <= s)."""
    if total%N: return False
    s=total//N; u=h//(2*r)
    if s%u: return False
    sig=s//u
    T=n2*h//2+nr*h//r+nD*u
    if T>s: return None          # criterion assumes T <= s
    inv2=(r+1)//2
    n2=min(n2,N); nr=min(nr,N*r)
    m=cp_model.CpModel(); M=[m.NewIntVar(0,N,'') for j in range(2*r)]
    m.Add(sum(M)==N)
    cap=min(nD,2*r*N)
    z=m.NewIntVar(0,cap//(2*r)+1,'')
    m.Add(sum(j*M[j] for j in range(2*r))==nD%(2*r)+2*r*z)
    m.Add(sum(j*M[j] for j in range(2*r))<=cap)
    m.Add(sum(M[j] for j in range(2*r) if (sig-j)%2)<=n2)
    m.Add(sum(((sig-j)*inv2)%r*M[j] for j in range(2*r))<=nr)
    sv=cp_model.CpSolver(); sv.parameters.max_time_in_seconds=TL
    return sv.Solve(m) in (cp_model.OPTIMAL,cp_model.FEASIBLE)
