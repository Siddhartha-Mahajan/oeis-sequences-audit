# A chamber-lifting lower bound for comparative probability orderings

Let `a(n)` be A009997, the number of comparative probability orderings on the
subsets of an `n`-element set that arise from generic positive weights, modulo
permutation symmetry.  Then, for every `n>=1`,

```text
a(n+1) >= 2^(n-1)*a(n).
```

## Proof

Choose a chamber counted by `a(n)` and a generic representative

```text
0 < w_1 < ... < w_n.
```

Adjoin a new weight `x>w_n`.  For each nonempty subset `S` of
`{1,...,n-1}`, consider the wall

```text
x = w_n + Sum_{i in S} w_i.
```

It records equality of the new singleton `{x}` with the old subset
`{w_n} union S`.  Because the original representative is generic, its subset
sums are all distinct.  The displayed `2^(n-1)-1` wall positions are therefore
distinct and all lie in the open ray `x>w_n`.

These walls divide that ray into at least `2^(n-1)` open intervals.  Away from
the finitely many subset-sum walls, choosing `x` in any interval gives a
generic ordering on `n+1` elements.  Two intervals separated by one of the
displayed walls give different orderings, since the comparison of `{x}` with
the corresponding old subset reverses.  Moreover, the restriction of every
extension to the first `n` elements is the original ordering.  Thus extensions
of distinct base orderings are distinct, and each base ordering has at least
`2^(n-1)` extensions.  This proves the recurrence.

Using the exact published value `a(7)=214580603` gives

```text
a(8) >= 2^6*a(7)
     = 64*214580603
     = 13733158592.
```

The same recurrence can be iterated to give explicit lower bounds in every
higher dimension.  It is not asserted to be sharp.
