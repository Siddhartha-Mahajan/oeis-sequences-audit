# A symmetric order-eight anti-Hadamard witness

## Result

For A005312, the following symmetric nonsingular `0,1` matrix has sum of
inverse squared singular values equal to 2670:

```text
10011100
00110010
01011011
11101001
10111000
10000011
01100110
00110101
```

Consequently `A005312(8)>=2670`. No upper bound or exactness claim is made.

## Verification

For a nonsingular matrix `A`, the objective is
`sum sigma_i(A)^(-2)=||A^(-1)||_F^2`. The verifier performs Gauss--Jordan
inversion over Python's exact rational numbers, checks symmetry and the `0,1`
entries, and sums the squares of all inverse entries. It returns the integer
2670 exactly.

## Ancillary files

- `certificates/n8_witness_2670.txt` contains the heuristic score and the
  matrix verbatim.
- `scripts/verify_matrix.py` is the exact checker.
- `scripts/search_n8.cpp` is the stochastic search actually used to find the
  witness. It rejects singular matrices by an exact Bareiss determinant before
  using floating-point inverse scores for search guidance. Floating point is
  not part of the final certification.
