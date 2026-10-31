"""Find a representative of every orbit of PGammaL(2,32) on k-subsets, for k = 12..15.

Short orbits: every k-subset with a non-trivial stabilizer is fixed by an element of
prime order, so we enumerate the k-subsets fixed by one element from each conjugacy
class of elements of prime order. Regular orbits: random k-subsets until the number
of regular orbits found equals the number given by the table of marks (P2_32.txt).
"""
import json, random, sys, itertools
import numpy as np
from pgaml232 import group

G = group()
ORDER = len(G)
B = (np.uint64(1) << np.arange(33, dtype=np.uint64))[np.ascontiguousarray(G.T)]

def canon(subset):
    m = np.bitwise_or.reduce(B[list(subset)], axis=0)
    own = np.uint64(sum(1 << i for i in subset))
    return int(m.min()), int((m == own).sum())

def elt_order(g):
    e = tuple(range(33)); x = g; k = 1
    while x != e:
        x = tuple(g[x[i]] for i in range(33)); k += 1
    return k

def cycles(g):
    seen = set(); cyc = []
    for i in range(33):
        if i not in seen:
            c = [i]; seen.add(i); j = g[i]
            while j != i:
                c.append(j); seen.add(j); j = g[j]
            cyc.append(c)
    return cyc

# one element from each conjugacy class of elements of prime order
elts = [tuple(int(x) for x in g) for g in G]
gens = [tuple(int(x) for x in g) for g in G[np.random.default_rng(1).choice(ORDER, 3, replace=False)]]
def inv(p):
    o = [0]*33
    for i, x in enumerate(p): o[x] = i
    return tuple(o)
def conj(p, g):
    gi = inv(g)
    return tuple(g[p[gi[i]]] for i in range(33))
reps = []
seen = set()
for g in elts:
    if g in seen: continue
    o = elt_order(g)
    if o not in (2, 3, 5, 11, 31): continue
    cls = {g}; fr = [g]
    while fr:
        nf = []
        for p in fr:
            for x in gens:
                y = conj(p, x)
                if y not in cls: cls.add(y); nf.append(y)
        fr = nf
    seen |= cls
    reps.append(g)
print("prime-order class representatives:", sorted(elt_order(g) for g in reps), file=sys.stderr)

marks = json.load(open("../P2_32.txt"))
out = {}
for k in range(12, 16):
    expected = dict(zip(marks["ord"], marks["counts"][str(k)]))
    expected = {o: c for o, c in expected.items() if c}
    orbits = {}
    for g in reps:
        cyc = cycles(g)
        for r in range(len(cyc) + 1):
            for comb in itertools.combinations(cyc, r):
                if sum(len(c) for c in comb) != k: continue
                s = [i for c in comb for i in c]
                m, st = canon(s)
                orbits[m] = st
    rng = random.Random(k)
    nreg = expected.get(1, 0)
    reg = sum(1 for st in orbits.values() if st == 1)
    while reg < nreg:
        s = rng.sample(range(33), k)
        m, st = canon(s)
        if m not in orbits:
            orbits[m] = st
            if st == 1: reg += 1
    found = {}
    for st in orbits.values(): found[st] = found.get(st, 0) + 1
    print(k, "orbits", len(orbits), "match" if found == expected else ("MISMATCH", found, expected), file=sys.stderr)
    out[k] = sorted([m, ORDER // st] for m, st in orbits.items())
json.dump(out, open("orbits_P2_32.json", "w"))
