from math import comb,gcd
from functools import reduce
def lemma(L,h,s,N):
    """Residue lemma: g = gcd of all orbit lengths divides s; non-regular total T <= s;
    the lengths l with n_l >= (N-1)(h/gcd(l,h)-1) together with h have gcd g."""
    nonreg={l:c for l,c in L.items() if l!=h}
    if sum(l*c for l,c in nonreg.items())>s: return False
    J=[l for l,c in nonreg.items() if c>=(N-1)*(h//gcd(l,h)-1)]
    return s%reduce(gcd,J,h)==0
