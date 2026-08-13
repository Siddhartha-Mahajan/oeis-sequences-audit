# A005787 reproducibility package

This folder proves an exact all-`n` recurrence for A005787. It reproduces the
published values, the independently enumerated `a(6)=323041664`, and gives

```text
a(7) = 284820663040,
a(8) = 578706325429760.
```

Quick exact replay:

```bash
python3 scripts/compute_recurrence.py --last-n 20 --output build/recurrence_terms.json
cmp build/recurrence_terms.json certificates/recurrence_terms.json
python3 scripts/verify_recurrence.py
python3 scripts/make_bfile.py --last-n 20 --output build/b005787.txt
```

Independent six-circle enumeration:

```bash
mkdir -p build
c++ -O3 -std=c++17 scripts/count_reachable.cpp -o build/count_reachable
./build/count_reachable > build/count_n1_n6_recomputed.txt
cmp build/count_n1_n6_recomputed.txt certificates/count_n1_n6_exact_intersections.txt
python3 scripts/verify_small_and_arithmetic.py
```

The b-file deliberately stops at `n=20`: subsequent exact integers rapidly
become too large for a long b-file to be useful. The recurrence still
determines every term.
