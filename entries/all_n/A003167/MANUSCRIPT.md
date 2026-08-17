# An exact recursion and the seventh term of A003167

## Result

The computation proves

```text
A003167(7) = 155068098.
```

More generally, the Egyptian-fraction formulation gives an exact finite
recursion for every dimension.

## Cuboids and Egyptian fractions

A cuboid with positive integral side lengths `x_1<=...<=x_n` has volume equal
to its total facet area exactly when

```text
1/x_1 + ... + 1/x_n = 1/2.                              (1)
```

Thus `A003167(n)` counts the nondecreasing positive-integer solutions of (1).

Suppose the remaining sum is `p/q`, there are `r` denominators left, and the
next denominator is at least `L`. For `r>=2`, positivity after choosing `x`
requires `x>q/p`, monotonicity requires `x>=L`, and the fact that every
remaining reciprocal is at most `1/x` gives `x<=r*q/p`. Hence

```text
max(L,floor(q/p)+1) <= x <= floor(r*q/p).               (2)
```

After choosing `x`, reduce `(p*x-q)/(q*x)` and recurse with lower bound `x`.
The interval (2) is finite at every node and contains every possible next
denominator, so this is an exact all-`n` recursion. A formal statement is in
`ALL_N_RECURRENCE.md`.

When only two denominators remain, the identity

```text
(p*x-q)*(p*y-q)=q^2                                     (3)
```

turns the terminal recursion into exact divisor enumeration. Deterministic
64-bit Miller--Rabin and Pollard--Rho factor `q`; 128-bit products protect
`q^2` and the complementary divisor from overflow. Every divisor `d<=q` is
tested for integrality and the monotonic lower bound, so every `x<=y` solution
is counted once.

## Disjoint computation certificate for n=7

The top-level range is `x_1=3,...,14`. The expensive `x_1=3` branch is refined
without omission or overlap:

```text
x_1 = 4,...,14;
x_1 = 3, x_2 = 8,...,36;
x_1 = 3, x_2 = 7, x_3 = 44,...,210;
x_1 = 3, x_2 = 7, x_3 = 43,
        x_4 = 1807,...,7224, partitioned into consecutive ranges.
```

These ranges follow directly from (2). The aggregation checker proves that
the exceptional `x_4` intervals are consecutive from 1807 through 7224,
validates each fixed prefix and range embedded in the output, and sums 262
branch counts to 155068098. In total the branches visit 151379115 recursive
nodes and make 151271985 terminal pair calls.

## Independent checks

The same C++ terminal algorithm reproduces the five published counts

```text
2, 10, 108, 2892, 270332
```

for `n=2,...,6`. A separate Python rational recursion, which does not use the
two-denominator factorization, also reproduces those values. The large `n=7`
claim is certified by the included enumerator, the complete disjoint branch
outputs, and the standard-library aggregation checker. No floating-point
arithmetic or solver is used.
