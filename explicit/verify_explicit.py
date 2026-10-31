"""Verify the explicit large sets of 4-designs in large_sets_P2_32.json.

For each LS[N](4,k,33), the file gives N classes of k-subsets of the 33 points of
PG(1,32), and each class is the union of the orbits of the listed k-subsets under
PGammaL(2,32). The script checks that
  1. PGammaL(2,32) is transitive on 4-subsets, so every union of orbits is a 4-design,
  2. the listed k-subsets lie in pairwise distinct orbits,
  3. every class has total orbit length C(33,k)/N, and
  4. the orbit lengths add up to C(33,k), so the classes partition all k-subsets.
"""
import json, itertools
from math import comb
import numpy as np
from pgaml232 import group

G = group()
B = (np.uint64(1) << np.arange(33, dtype=np.uint64))[np.ascontiguousarray(G.T)]

def canon(subset):
    m = np.bitwise_or.reduce(B[list(subset)], axis=0)
    own = np.uint64(sum(1 << i for i in subset))
    return int(m.min()), len(G) // int((m == own).sum())

reps4 = {canon(s)[0] for s in itertools.combinations(range(33), 4)}
assert len(reps4) == 1, "not 4-homogeneous"
ok = 0
for ls in json.load(open("large_sets_P2_32.json")):
    N, k = ls["N"], ls["k"]
    s = comb(33, k) // N
    seen = set(); total = 0
    for cl in ls["classes"]:
        L = 0
        for B_ in cl:
            assert len(B_) == k
            m, length = canon(B_)
            assert m not in seen, "orbit repeated"
            seen.add(m); L += length
        assert L == s, (N, k, L, s)
        total += L
    assert len(ls["classes"]) == N and total == comb(33, k)
    ok += 1
    print(f"LS[{N}](4,{k},33) verified: {len(seen)} orbits in {N} classes")
print("verified", ok)
