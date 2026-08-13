# A380991(5): a 71-cell construction

## Result

`A380991(5)>=71`.

## Certificate

`certificates/witness_71.txt` lists 71 distinct square-grid cells. The
standard-library verifier checks that their edge-adjacency graph is connected
and normalizes every lattice-line direction to prove that no line contains
more than five cell centers.

## Replay

```bash
python3 scripts/verify_witness.py certificates/witness_71.txt
```

`scripts/greedy_growth.cpp` records the seeded construction search. The
coordinate list is the certificate. This is a lower bound, not an exact term.
