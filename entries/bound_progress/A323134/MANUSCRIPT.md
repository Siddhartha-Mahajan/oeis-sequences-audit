# A323134: possible discrepancy in the knight-polygon counts

## Finding

The geometric enumerator agrees with the OEIS values at `n=2,3,4`, then
gives 3034 at `n=5` and 64877 at `n=6`, instead of 3031 and 64866. It also
gives 1503790 at `n=7`.

The implementation counts simple closed straight-edge knight walks modulo
translation, all eight square symmetries, cyclic starting point, and
reversal. Collinear consecutive knight moves are allowed. An independent
Python recount verifies the first discrepancy: 58840 rooted representatives
and 3034 equivalence classes.

## Replay

```bash
python3 scripts/verify_n5.py
mkdir -p build
c++ -O3 -std=c++20 scripts/count_polygons.cpp -o build/count_polygons
./build/count_polygons 5
```

## Submission status

Do not change DATA from this package alone. First ask the original author or
an editor to confirm the historical equivalence and collinearity convention.
