# An exact recurrence for A005787

Let `F_n` be the set of configurations reachable from the all-white coloring
on `n` circles, represented as Boolean functions on `{0,1}^n`. The allowed
operations on coordinate `i` are

```text
f -> f OR x_i,             f -> f XOR x_i.
```

Put `a(n)=|F_n|` and use the auxiliary initial value `a(0)=1`.

## Last-OR decomposition

For `0 <= i < n`, let

```text
E_i = {f : f|_(x_i=0) is in F_(n-1) and f|_(x_i=1) is affine}.
```

Choosing the last OR in a construction shows that `F_n` is the union of the
`E_i`. Conversely, every element of `E_i` is constructible. The set
`F_(n-1)` is closed under XOR with a linear form. Given zero-slice `g` and
affine one-slice `h=c XOR l`, construct `g XOR l`, apply OR on `i`, restore
the linear form by coordinate toggles, and toggle coordinate `i` when needed
to obtain the constant `c`. Consequently,

```text
|E_i| = 2^n a(n-1).                                      (1)
```

Every all-zero coordinate restriction of a reachable function is reachable,
as follows by restricting a construction operation by operation.

## Multiple intersections

For every `I` contained in `{0,...,n-1}` with `k=|I|>=2`, one has

```text
| intersection_(i in I) E_i | = 2^(n+1) a(n-k).          (2)
```

Indeed, for `f` in the intersection, each restriction to `x_i=1`, `i in I`,
is affine. These affine functions agree on their pairwise overlaps and glue
to a unique affine function `h` on `{0,1}^n`, agreeing with `f` whenever at
least one selected coordinate is one. On the remaining face

```text
Z_I = {x : x_i=0 for every i in I},
```

the restriction `q=f|_(Z_I)` belongs to `F_(n-k)`. This maps `f` to a unique
pair `(h,q)` in `Aff_n X F_(n-k)`.

Conversely, define `f=h` off `Z_I` and `f=q` on `Z_I`. Induction on `k`
using the last-OR decomposition shows that `f` belongs to every selected
`E_i`. Thus the map is a bijection. There are `2^(n+1)` affine functions on
`n` variables, proving (2).

## Recurrence and generating-function identity

Inclusion--exclusion applied to `F_n=union_i E_i`, using (1) and (2), gives

```text
a(0) = 1,
a(n) = n*2^n*a(n-1)
       + 2^(n+1)*Sum_(k=2..n) (-1)^(k+1)*C(n,k)*a(n-k).  (3)
```

As a formal exponential-generating-function identity, if
`A(x)=Sum_(n>=0) a(n)x^n/n!`, then

```text
A(x) = 1 + 2*(1-x-exp(-2*x))*A(2*x).                    (4)
```

The recurrence reproduces the published values and the independent
six-circle enumeration, and gives

```text
a(6) = 323041664,
a(7) = 284820663040,
a(8) = 578706325429760.
```

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
  inclusion--exclusion calculation.

All calculations use exact integer arithmetic.
