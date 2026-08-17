# A368353–A368355 at n=6: exact Hankel determinant extrema

## Results

For 6 X 6 Hankel matrices formed from a permutation of `0,...,10`, exhaustive
enumeration gives

```text
A368353(6) = -2579770
A368354(6) =  2256911
A368355(6) =  2579770
```

The minimum is attained by `[4,6,1,5,9,10,0,8,2,3,7]`; the maximum by
`[3,6,8,2,10,0,1,7,9,4,5]`.

## Method and replay

Fraction-free Bareiss elimination computes every determinant exactly.
Reversal conjugates the Hankel matrix by the reversal permutation matrix, so
one representative from each reversal pair suffices: `11!/2=19958400`
cases.

```bash
mkdir -p build
c++ -O3 -std=c++20 -pthread scripts/exhaustive_hankel6.cpp -o build/exhaustive_hankel6
./build/exhaustive_hankel6 4
```
