# An exact recurrence for A005787

Let `F_n` be the set of configurations reachable from the all-white coloring
on `n` circles, represented as Boolean functions on `{0,1}^n`. The allowed
operations on coordinate `i` are

```text
f -> f OR x_i,             f -> f XOR x_i.
```

Put `a(n)=|F_n|` and use the auxiliary initial value `a(0)=1`.

## Last-OR decomposition

For `0<=i<n`, let

```text
E_i = {f : f|_(x_i=0) is in F_(n-1) and f|_(x_i=1) is affine}.
```

Choosing the last OR in a construction shows that `F_n` is contained in the
union of the `E_i`; a construction using no OR is affine and belongs to every
`E_i`. Conversely, every element of `E_i` is constructible. The family
`F_(n-1)` is closed under XOR with a linear form. Given zero-slice `g` and
affine one-slice `h=c XOR l`, first construct `g XOR l`, apply OR on `i`,
restore `l` by coordinate toggles, and toggle coordinate `i` when necessary
to obtain the constant `c`. Thus

```text
F_n = Union_(i=0..n-1) E_i,
|E_i| = 2^n*a(n-1).                                      (1)
```

Restriction to any collection of zero-coordinate faces preserves
reachability, because each operation restricts either to the corresponding
operation in fewer variables or to the identity.

## Multiple intersections

For every `I` contained in `{0,...,n-1}` with `k=|I|>=2`,

```text
| Intersection_(i in I) E_i | = 2^(n+1)*a(n-k).          (2)
```

To prove this, take `f` in the intersection. For each `i in I`, the slice
`f|_(x_i=1)` is affine. These affine slices agree on pairwise overlaps. They
therefore glue to a unique affine function `h` on the whole cube that agrees
with `f` whenever at least one selected coordinate is one. For existence,
first glue two slices; their coefficients are compatible because their
restrictions to the common codimension-two face agree. The resulting global
affine function agrees with every further slice, since the difference on that
slice vanishes on two distinct coordinate hyperplanes. Uniqueness follows
because a nonzero affine function cannot vanish on two distinct coordinate
hyperplanes `x_i=1` and `x_j=1`.

On the remaining face

```text
Z_I={x : x_i=0 for every i in I},
```

put `q=f|_(Z_I)`. The restriction observation gives `q in F_(n-k)`. Hence
`f` determines a unique pair `(h,q)` in `Aff_n X F_(n-k)`.

Conversely, start with such a pair and define `f=h` off `Z_I` and `f=q` on
`Z_I`. We show by induction on `|I|` that `f` lies in every `E_i`. Fix
`i in I`. Its one-slice is affine. Its zero-slice is the analogous patching
problem for `I\{i}` in one fewer variable; the base case `|I\{i}|=1` is
exactly the defining converse for one last OR, and the induction step repeats
the same argument. Thus the zero-slice is reachable and `f in E_i`.
This proves the bijection. Since there are `2^(n+1)` affine functions on `n`
variables, (2) follows.

## Recurrence

Inclusion-exclusion applied to (1), using (2), gives

```text
a(0) = 1,
a(n) = n*2^n*a(n-1)
       + 2^(n+1)*Sum_(k=2..n) (-1)^(k+1)*C(n,k)*a(n-k).  (3)
```

The recurrence determines every term by exact integer arithmetic. It gives

```text
a(6) = 323041664,
a(7) = 284820663040,
a(8) = 578706325429760.
```

## Exponential generating function

Let

```text
A(x)=Sum_(n>=0) a(n)*x^n/n!.
```

Summing (3) coefficientwise gives the formal identity

```text
A(x) = 1 + 2*(1-x-exp(-2*x))*A(2*x).                    (4)
```

Writing `C(x)=2*(1-x-exp(-2*x))`, iteration of (4) yields the explicit formal
product-sum

```text
A(x) = Sum_(m>=0) Product_(j=0..m-1) C(2^j*x)           (5)
     = Sum_(m>=0) 2^m*Product_(j=0..m-1)
         (1-2^j*x-exp(-2^(j+1)*x)).
```

The empty product is one. Formula (5) is well-defined in `Q[[x]]` because
`C(x)` has zero constant term, so its `m`-th summand has valuation at least
`m`; only finitely many summands affect any fixed coefficient.

## Ancillary files

- `scripts/compute_recurrence.py` evaluates (3) with exact integers.
- `scripts/make_bfile.py` writes the deliberately short OEIS b-file through
  `n=20`; the recurrence itself has no such endpoint.
- `certificates/recurrence_terms.json` preserves the values through `a(20)`.
- `scripts/verify_recurrence.py` explicitly constructs the last-OR sets
  through `n=4`, checks every intersection size, checks the independently
  enumerated six-circle intersection table, and compares the recurrence with
  the preserved certificate through `n=20`.
- `scripts/count_reachable.cpp` independently enumerates the six-circle case.
- `certificates/count_n1_n6_exact_intersections.txt` preserves that output.
- `scripts/verify_small_and_arithmetic.py` checks the original finite
  inclusion-exclusion calculation.

All calculations use exact integer arithmetic.
