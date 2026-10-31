"""Turn the certificates for PGammaL(2,32) into explicit large sets.

Each certificate gives, for every class, the number of orbits of each length.
We hand out the orbit representatives of orbits_P2_32.json accordingly.
"""
import json
from pgaml232 import to_set

orbits = json.load(open("orbits_P2_32.json"))
out = []
for line in open("../certs.jsonl"):
    c = json.loads(line)
    if c["file"] != "P2_32.txt":
        continue
    N, k = c["N"], c["k"]
    pool = {}
    for m, length in orbits[str(k)]:
        pool.setdefault(length, []).append(m)
    classes = list(c["classes"])
    # the certificate lists N-1 classes; the last class takes the remaining orbits
    used = {}
    for cl in classes:
        for L, n in cl.items():
            used[int(L)] = used.get(int(L), 0) + n
    last = {L: len(ms) - used.get(L, 0) for L, ms in pool.items() if len(ms) > used.get(L, 0)}
    if len(classes) == N - 1:
        classes.append({str(L): n for L, n in last.items()})
    assert len(classes) == N
    explicit = []
    for cl in classes:
        reps = []
        for L, n in cl.items():
            for _ in range(n):
                reps.append(to_set(pool[int(L)].pop()))
        explicit.append(sorted(reps))
    assert all(not ms for ms in pool.values())
    out.append({"N": N, "t": 4, "k": k, "v": 33, "group": "PGammaL(2,32)", "classes": explicit})
json.dump(out, open("large_sets_P2_32.json", "w"))
print(len(out), "large sets written")
