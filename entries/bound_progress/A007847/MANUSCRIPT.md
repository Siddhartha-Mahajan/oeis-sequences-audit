# A bounded-normal lower bound for A007847(10)

Let `H(n)` be the number of affine hyperplanes spanned by vertices of the
unit `n`-cube.  The exact published values of `H(n)` stop at `n=9`.  The
calculation packaged here proves

```text
H(10) >= 5013843621741086.
```

This is a lower bound only.

## Canonical normal types

Every spanned hyperplane has an equation

```text
c_1 x_1 + ... + c_n x_n = b
```

with a primitive integer normal `c`.  Coordinate permutations, coordinate
complementations, and reversal of the normal identify a canonical type with

```text
0 <= c_1 <= ... <= c_n,  gcd(c_1,...,c_n)=1,
0 <= b <= (c_1+...+c_n)/2.
```

For each such type with `c_n <= 12`, the program lists the cube vertices on
the indicated level and retains the type exactly when those vertices have
affine rank `n-1`.  If the positive coefficients have multiplicities
`m_1,...,m_r`, its orbit contains

```text
n!/(m_0! m_1! ... m_r!) * 2^(n-m_0-delta)
```

hyperplanes, where `m_0` is the number of zero coefficients and `delta=1`
for the central level `2*b=sum(c_i)`, otherwise `delta=0`.  Thus every retained
orbit consists of distinct hyperplanes, and distinct canonical types have
disjoint orbits.

The rank calculation is performed modulo `1000000007`.  A reported rank of
`n-1` modulo a prime certifies rank at least `n-1` over the rationals; all
points already lie in one hyperplane, so their rational affine rank is exactly
`n-1`.  A false positive is therefore impossible.

## Support decomposition

Let `F(n)` count spanned hyperplanes whose primitive normal has full support.
Every hyperplane has a unique support, so

```text
H(n) = Sum_{k=1..n} binomial(n,k) F(k).
```

Binomial inversion applied to the exact published `H(1),...,H(9)` shows that
the number of dimension-10 hyperplanes with nonfull support is

```text
Sum_{k=1..9} binomial(10,k) F(k) = 4483041603010078.
```

The bounded enumeration certifies a further `530802018731008` full-support
dimension-10 hyperplanes.  These sets are disjoint, giving

```text
H(10) >= 4483041603010078 + 530802018731008
      = 5013843621741086.
```

## Independent checks

At coefficient bound 12, the same enumerator exactly reproduces the complete
published dimension-7 result `H(7)=71343208` and its 623 symmetry classes.
The support-combination script recomputes the binomial inversion from the
published terms and invokes the C++ enumerator afresh.  No randomized search,
floating-point arithmetic, or solver result is used.

## Files

- `scripts/bounded_normals.cpp`: canonical enumeration, exact orbit sizes,
  and modular affine-rank certificates.
- `scripts/combine_known_supports.py`: support inversion and final addition.

The source enumerates only types whose largest primitive absolute normal
coefficient is at most 12.  It does not exclude other types, hence it supports
the displayed lower bound but not equality.
