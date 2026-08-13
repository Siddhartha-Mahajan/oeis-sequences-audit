# A365910(10): a 48-class partition

## Result

`A365910(10)<=48`, improving the entry's generic upper bound 114 at `n=10`.

## Certificate

`certificates/n10_coloring_48.txt` partitions all 210 four-subsets of a
10-element set into 48 classes. Within any class, two blocks intersect in at
most one point. The verifier checks uniqueness, completeness, and every
within-class intersection.

## Replay

```bash
python3 scripts/verify_coloring.py certificates/n10_coloring_48.txt
```

`scripts/dsatur.cpp` is the deterministic-seed construction search. The
partition itself is the certificate. This is an upper bound on a minimum,
not an exact term.
