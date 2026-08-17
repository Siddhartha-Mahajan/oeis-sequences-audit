# Exact finite recursion for A003167

For coprime integers `p>=0`, `q>=1`, an integer `r>=0`, and a lower bound
`L>=1`, let

```text
C(r,p,q,L)
```

be the number of nondecreasing `r`-tuples

```text
L <= x_1 <= ... <= x_r
```

satisfying

```text
1/x_1 + ... + 1/x_r = p/q.
```

Use the terminal conventions

```text
C(0,0,1,L)=1,
C(0,p,q,L)=0 for p>0.
```

For `r=1`, the value is one exactly when `p>0`, `p` divides `q`, and
`q/p>=L`; otherwise it is zero.

For `r>=2` and `p>0`, every possible first denominator satisfies

```text
max(L,floor(q/p)+1) <= x <= floor(r*q/p).              (1)
```

The lower bound makes the residual sum positive. The upper bound follows
because all `r` reciprocals are at most `1/x`. Therefore

```text
C(r,p,q,L) = Sum_x C(r-1,p_x,q_x,x),                   (2)
```

where `(p_x,q_x)` is the reduced form of

```text
(p*x-q)/(q*x).
```

The interval in (1) is finite, so (2), together with the terminal cases, is an
exact finite recursion.

For the sequence,

```text
A003167(n)=C(n,1,2,1).                                  (3)
```

Indeed, an integral `n`-cuboid with nondecreasing side lengths has volume
equal to its total facet area exactly when the reciprocals of its side lengths
sum to `1/2`.

## Two-denominator acceleration

When `r=2`,

```text
(p*x-q)*(p*y-q)=q^2.                                    (4)
```

Thus the terminal count can be obtained by enumerating divisors `d|q^2` and
testing

```text
x=(d+q)/p,
y=(q^2/d+q)/p,
L<=x<=y.
```

This is an acceleration of the all-`n` recursion, not an additional
assumption. The C++ implementation uses deterministic integer factorization
for this terminal step and exact rational reduction everywhere else.
