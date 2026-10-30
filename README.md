# Large Sets of Designs from Lines, Ovoids and Unitals

Supplementary material for the paper of the same title by Yeow Meng Chee.

## Contents

| Path | What it is |
|---|---|
| `groups.txt` | The 187 groups that are 2-homogeneous of degree at most 100, with degree, degree of homogeneity, name and data file |
| `[SGP]2_q.txt`, `L*.txt`, `U*.txt`, `Sz8.txt`, `R3.txt`, `aff/A_d_i.txt` | For each group: its order, the orders of the subgroup classes, and the number of orbits on k-subsets with each stabilizer class, obtained from the table of marks by Möbius inversion |
| `hom2.txt` | Degree of homogeneity and names of the affine groups (GAP primitive groups library) |
| `gap/` | GAP scripts that compute the tables of marks and the orbit data |
| `certs.jsonl` | One certificate for each of the 1365 direct large sets of the paper: N, t, k, v, the group file, and the N classes, each given as a multiset of orbit lengths |
| `verify_final.py` | Checks every certificate (see below) |
| `part*_results.jsonl`, `searchT_results.jsonl`, `cover.json` | Raw search output |
| `base.py`, `engine.py`, `large_sets_table.csv` | The literature baseline and the closure under the known recursive constructions |
| `tableA.py`, `gen_tabA.py` | Produce `tableA.json`, the summary table and the appendix table |
| `count_cf.py` | Counts the direct large sets given in closed form by the theorems on projective lines (214) |
| `thm*.py`, `chain.py`, `four.py`, `lemma.py` | The closed-form theorems and the partition criteria of the paper |
| `families/` | Checks of the infinite families against the known constructions for larger v |

## Verifying the certificates

```
python3 verify_final.py
```

For each certificate, the script loads the orbit data of the stated group and checks that
1. the group is t-homogeneous,
2. there are N classes,
3. each class has total length C(v,k)/N, and
4. the classes together use exactly the orbits of the group on k-subsets, with multiplicity.

Since the group is t-homogeneous, every union of its orbits on k-subsets is a t-design, so each class is a t-design and the classes form an LS[N](t,k,v). An explicit large set is obtained by choosing, for each class, orbits of the stated lengths.

Expected output: `verified 1365 failed 0 []`.

## Reproducing the tables

```
python3 tableA.py      # writes tableA.json and prints the rows of the summary table
python3 gen_tabA.py    # writes note/tab_summary.tex and note/tab_direct.tex
python3 count_cf.py    # closed-form count
```

Requirements: Python 3 with `ortools` (for `part3.py` and `part4.py` only), and GAP 4 with the TomLib and primitive groups packages for the scripts in `gap/`.
