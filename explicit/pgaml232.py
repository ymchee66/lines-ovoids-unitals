"""PGammaL(2,32) acting on the 33 points of PG(1,32).

Points 0..31 are the elements of GF(32) = GF(2)[x]/(x^5+x^2+1), written as integers
(bit i is the coefficient of x^i), and point 32 is infinity.
"""
import numpy as np

POLY = 0b100101

def gmul(a, b):
    r = 0
    while b:
        if b & 1:
            r ^= a
        b >>= 1
        a <<= 1
        if a & 32:
            a ^= POLY
    return r

def ginv(a):
    for b in range(1, 32):
        if gmul(a, b) == 1:
            return b

INF = 32
GENERATORS = {
    "x+1": [x ^ 1 for x in range(32)] + [INF],
    "wx": [gmul(2, x) for x in range(32)] + [INF],
    "1/x": [INF] + [ginv(x) for x in range(1, 32)] + [0],
    "x^2": [gmul(x, x) for x in range(32)] + [INF],
}

def group():
    """All 163680 elements, as an array of shape (163680, 33)."""
    gens = [tuple(g) for g in GENERATORS.values()]
    e = tuple(range(33))
    seen = {e}
    frontier = [e]
    while frontier:
        new = []
        for h in frontier:
            for g in gens:
                y = tuple(g[h[i]] for i in range(33))
                if y not in seen:
                    seen.add(y)
                    new.append(y)
        frontier = new
    return np.array(sorted(seen), dtype=np.uint8)

def masks(G, subset):
    """Bitmasks of the images of a subset under all elements of G."""
    imgs = G[:, list(subset)].astype(np.uint64)
    return (np.uint64(1) << imgs).sum(axis=1)

def canon(G, subset):
    """(least image bitmask, stabilizer order) of a subset."""
    m = masks(G, subset)
    own = sum(1 << i for i in subset)
    return int(m.min()), int((m == np.uint64(own)).sum())

def to_set(mask):
    return [i for i in range(33) if mask >> i & 1]
