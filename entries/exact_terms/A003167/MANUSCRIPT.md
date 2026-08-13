# The seventh term of A003167

## Result

The computation proves

```text
A003167(7) = 155068098.
```

A cuboid with positive integral side lengths `x_1<=...<=x_n` has volume equal
to its surface area exactly when

```text
1/x_1 + ... + 1/x_n = 1/2.
```

Thus it suffices to count the nondecreasing Egyptian-fraction solutions.

## Finite recursion

Suppose the remaining sum is `p/q`, there are `r` denominators left, and the
next denominator is at least `L`. Positivity after choosing `x` requires
`x>q/p`; monotonicity requires `x>=L`; and since every remaining reciprocal is
at most `1/x`, necessity of completing the sum gives `x<=r*q/p`. Therefore

```text
max(L,floor(q/p)+1) <= x <= floor(r*q/p).          (1)
```

After choosing `x`, reduce `(p*x-q)/(q*x)` and recurse. These bounds are both
necessary, cover every solution, and make the search finite.

When only two denominators remain, the identity

```text
(p*x-q)*(p*y-q)=q^2                               (2)
```

turns the terminal recursion into exact divisor enumeration. Deterministic
64-bit Miller--Rabin and Pollard--Rho factor `q`; 128-bit products protect
`q^2` and the complementary divisor from overflow. Every divisor `d<=q` is
tested for integrality and the monotonic lower bound, so every `x<=y` solution
is counted once.

## Disjoint computation certificate

The top-level range is `x_1=3,...,14`. The expensive `x_1=3` branch is refined
without omission or overlap:

```text
x_1 = 4,...,14;
x_1 = 3, x_2 = 8,...,36;
x_1 = 3, x_2 = 7, x_3 = 44,...,210;
x_1 = 3, x_2 = 7, x_3 = 43,
        x_4 = 1807,...,7224, partitioned into consecutive ranges.
```

These ranges follow directly from (1). The aggregation checker proves that
the exceptional `x_4` intervals are consecutive from 1807 through 7224,
validates each fixed prefix/range embedded in the output, and sums 262 branch
counts to 155068098. In total the branches visit 151379115 recursive nodes and
make 151271985 terminal pair calls.

## Independent checks and trust boundary

The same C++ terminal algorithm reproduces the five published counts

```text
2, 10, 108, 2892, 270332
```

for `n=2,...,6`. A separate Python rational recursion, which does not use the
two-denominator factorization, had already reproduced those five terms. The
large `n=7` exactness claim depends on the included C++ enumerator and complete
branch outputs; the small-term replays, mathematical partition proof, and
standard-library aggregation checker audit the implementation from distinct
directions. No floating-point arithmetic or solver is used in a count.

