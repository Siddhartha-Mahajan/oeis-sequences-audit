# A202140(5): improved two-generator Boolean-semigroup bound

## Result

`A202140(5)>=7582856`, improving the published lower bound 6732481.

## Witness

With matrix rows separated by `/`, the two generators are

```text
00001/10000/01000/00100/00010
00100/10000/01001/00010/00001
```

Exact breadth-first closure under right Boolean-matrix multiplication has
7582856 elements. The program first reproduces the published witness and
then checks every one- and two-bit perturbation, including the displayed
improvement.

## Replay

```bash
mkdir -p build
c++ -O3 -std=c++20 scripts/verify_and_neighbors.cpp -o build/verify_and_neighbors
./build/verify_and_neighbors
```

The result is a constructive lower bound, not an exact value for `a(5)`.
