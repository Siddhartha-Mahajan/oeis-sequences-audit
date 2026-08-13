# A343777(5): finite exclusion through 10^13

## Result

`A343777(5)>10^13`. This is a finite search frontier, not an exact new term.

## Method

For every starting index, sums of consecutive positive 5-gonal numbers form
an increasing stream. A priority queue merges all streams in increasing sum
order. Each interval occurs exactly once, so the first value with five
representations would be detected. The computation exhausts the cutoff and
also reproduces the published `a(3)` and `a(4)`.

## Replay

```bash
mkdir -p build
c++ -O3 -std=c++20 scripts/consecutive_polygonal_search.cpp -o build/search
./build/search 5 10000000000000 certificates/n5_recomputed.json
```
