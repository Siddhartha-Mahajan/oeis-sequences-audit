# A ternary chamber-lifting bound for comparative probability orderings

Let `a(n)` be A009997, the number of comparative probability orderings on
subsets of an `n`-element set that arise from generic positive weights, modulo
permutation of the ground set.

## Theorem

For every `n>=1`,

```text
a(n+1) >= ((3^(n-1)+1)/2)*a(n).                      (1)
```

Consequently, from the exact value `a(7)=214580603`,

```text
a(8) >= 365*214580603 = 78321920095.                 (2)
```

## Proof

Fix a chamber counted by `a(n)`. Because a chamber is an open full-dimensional
cone, it contains a representative

```text
0 < w_1 < ... < w_n
```

for which all ternary signed sums of `w_1,...,w_(n-1)` are distinct. Indeed,
one need only avoid the finitely many additional hyperplanes on which two
such sums agree. In particular,

```text
sum_(i=1..n-1) epsilon_i*w_i != 0
```

for every nonzero `epsilon` in `{-1,0,1}^{n-1}`.

Adjoin a new weight `x>w_n`. For each nonzero ternary vector `epsilon` with
positive signed sum, put

```text
delta_epsilon = sum_(i=1..n-1) epsilon_i*w_i > 0
```

and consider the wall

```text
x = w_n + delta_epsilon.                              (3)
```

Writing

```text
P={i: epsilon_i=1},   M={i: epsilon_i=-1},
```

wall (3) is the legitimate subset-sum equality

```text
x + sum_(i in M) w_i = w_n + sum_(i in P) w_i.        (4)
```

The walls are distinct by the choice of the representative, and all lie in
the ray `x>w_n`. Negation pairs the nonzero ternary vectors, so exactly

```text
(3^(n-1)-1)/2
```

of them have positive signed sum. Hence the displayed walls divide the ray
into at least

```text
(3^(n-1)-1)/2 + 1 = (3^(n-1)+1)/2
```

open intervals. Other subset-sum walls can only subdivide these intervals.
Choosing `x` away from every wall in each interval therefore gives at least
that many extension chambers. Adjacent intervals give different orderings
because the comparison in (4) reverses.

It remains to check the quotient by permutations. In every extension, `x` is
the unique largest singleton weight, and the old singleton weights remain in
the strict order `w_1<...<w_n`. Any permutation carrying one extension to
another must therefore fix the new element and every old element in order.
Thus distinct intervals are not identified. Likewise, restricting an
extension to its `n` smallest singleton elements recovers the original
chamber, so extensions of inequivalent base chambers remain inequivalent.
This proves (1), and (2) follows by substitution.

## Iteration

For `m>n>=1`, repeated use of (1) gives the explicit all-dimensions bound

```text
a(m) >= a(n)*Product_(j=n..m-1) (3^(j-1)+1)/2.       (5)
```

The estimate is one-sided and is not asserted to be sharp.
