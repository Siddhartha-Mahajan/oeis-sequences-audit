# Exact determination of A273354(3)

Let `r_2^+(N)` and `r_3^+(N)` denote the numbers of unordered pairs of
positive integers representing `N` as a sum of two squares and two cubes,
respectively.

## Theorem

```text
A273354(3) = 11177126654841000000.
```

## Upper bound

Put

```text
N0 = 11177126654841000000 = 3343221000^2.
```

Direct integer arithmetic gives exactly the three cube identities

```text
N0 = 279300^3  + 2234400^3
   = 790020^3  + 2202480^3
   = 1256850^3 + 2094750^3.
```

An exhaustive scan of `1 <= x <= floor((N0/2)^(1/3))` finds no other pair.
The factorization is

```text
N0 = 2^6 * 3^6 * 5^6 * 7^6 * 19^4.
```

Every prime congruent to 3 modulo 4 has even exponent, and

```text
P(N0)=Product_(p == 1 mod 4)(v_p(N0)+1)=7.
```

Since `N0` is a square, the positive-square-pair formula proved in sprint 01
gives `r_2^+(N0)=(7-1)/2=3`. Explicitly,

```text
N0 = 936101880^2  + 3209492160^2
   = 1176813792^2 + 3129254856^2
   = 2005932600^2 + 2674576800^2.
```

Thus `a(3) <= N0`.

## Finite minimality reduction

Suppose `M<N0` has at least three positive-cube representations

```text
M=x_1^3+y_1^3=x_2^3+y_2^3=x_3^3+y_3^3.
```

Let `g=gcd(x_1,y_1,x_2,y_2,x_3,y_3)`. Then

```text
M=g^3 m,
```

where `m` is a primitive three-cube value in the sense of A003825. Conversely,
every positive cubic multiple of a primitive three-cube value has at least
three cube representations. Hence every possible `M<N0` occurs among

```text
{m*g^3 : m is in A003825, g>=1, m*g^3<N0}.
```

The downloaded A003825 b-file contains 34,204 increasing primitive values and
ends at `24146313058579372203303>N0`; 6,177 entries are below `N0`. Their
cubic multiples below `N0` give 110,969 distinct candidates.

Each candidate was factored with deterministic 64-bit Miller--Rabin and
Pollard rho. For a factorization of `M`, the exact formula

```text
r_2^+(M) = (P(M)-[M is a square]+[M/2 is a square])/2
```

was applied when all `3 mod 4` prime exponents were even, and zero otherwise.
None of the 110,969 candidates has `r_2^+(M)=3`. Therefore no smaller `M`
can satisfy both multiplicity conditions.

## Reproducibility and trust boundary

Run

```bash
build/analyze_primitive_scalings ../../sources/A003825_bfile.txt \
  11177126654841000000 results/below_candidate.json
python3 scripts/verify_minimality_certificate.py
```

The independent Python verifier regenerates all 110,969 candidates, proves
each recorded factor prime by deterministic Miller--Rabin, reconstructs every
factorization, recalculates every square-pair count, directly scans all cube
pairs of `N0`, and checks the summary.

The finite minimality argument depends on the completeness of the external
A003825 primitive b-file through `N0`. As a strong independent consistency
check, cubic multiples of that primitive list reproduce, without omissions or
extras, all 100,000 entries in the independently supplied A018787 b-file,
whose endpoint is `8295223270128128000`. The arithmetic filtering and the
candidate construction are independently replayable within this sprint.
