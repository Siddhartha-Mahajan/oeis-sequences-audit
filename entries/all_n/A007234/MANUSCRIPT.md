# Maximum squaring-free subsets of symmetric groups

Let `F_n` be the largest cardinality of a subset `X` of the symmetric group
`S_n` such that `sigma in X` implies `sigma^2 not in X`. Equivalently, `F_n`
is the independence number of the functional graph of the squaring map, with
a looped vertex forbidden. The following recurrence uses one state for each
partition of `n`.

## Conjugacy types and square-root fibers

Write a cycle type as `lambda=1^m_1 2^m_2 ... n^m_n` and put

```text
z_lambda = Product_(j=1..n) j^(m_j)*m_j!.
```

The conjugacy class of type `lambda` has cardinality `n!/z_lambda`. Let
`q(mu)` be the cycle type obtained by squaring a permutation of type `mu`: an
odd `j`-cycle remains a `j`-cycle, while an even `2j`-cycle becomes two
`j`-cycles.

For every `mu` with `q(mu)=lambda`, each fixed permutation of type `lambda`
has exactly

```text
r(lambda,mu)=z_lambda/z_mu.                              (1)
```

square roots of type `mu`. The squaring map sends the conjugacy class of `mu`
equivariantly onto the class of `lambda`; the image is nonempty and
conjugacy-invariant, hence is the whole class. All fibers have the same size,
which is the ratio `(n!/z_mu)/(n!/z_lambda)`.

## Reverse-tree recurrence

For a type `lambda` containing an even part, let `E_lambda` and `I_lambda` be
the largest sizes of an independent set in the reverse tree below one
permutation of that type, conditional on excluding and including its root.
Conjugation identifies the rooted reverse functional graphs of any two
permutations having the same type, so these states are type invariants.
Distinct square roots lead to disjoint reverse subtrees because every
permutation has a unique square. Therefore

```text
E_lambda = Sum_{q(mu)=lambda} r(lambda,mu)*max(E_mu,I_mu),
I_lambda = 1 + Sum_{q(mu)=lambda} r(lambda,mu)*E_mu.      (2)
```

These equations are acyclic. If `v(lambda)` is the largest 2-adic valuation
of a cycle length in `lambda`, then every reverse type on the right side has
valuation `v(lambda)+1`: an even target cycle of maximal valuation can only
come from a cycle twice as long. Processing types in descending valuation
determines all nonperiodic states.

For a type whose parts are all odd, the same equations give the weights of
the trees attached to a cycle vertex, except that the unique same-type square
root is omitted. That predecessor lies on the directed squaring cycle rather
than in the attached tree.

## Periodic classes

For an all-odd type `lambda`, put

```text
o_lambda = lcm{j : m_j>0},
L_lambda = ord_(o_lambda)(2),
N_lambda = (n!/z_lambda)/L_lambda.                       (3)
```

Take `L_lambda=1` when `o_lambda=1`. Every permutation in the class has order
`o_lambda`, so its squaring orbit has length `L_lambda`; the class therefore
splits into `N_lambda` directed cycles.

Put `g_lambda=max(0,I_lambda-E_lambda)`. Excluding every cycle root gives the
base weight `L_lambda*E_lambda`. Including a cycle root gains `g_lambda`, and
a cycle of length greater than one has an independent set of
`floor(L_lambda/2)` roots. Hence each component contributes

```text
L_lambda*E_lambda + floor(L_lambda/2)*g_lambda            (4)
```

when `L_lambda>1`. When `L_lambda=1`, the loop forbids its root and the
contribution is `E_lambda`. Summing the component contributions, multiplied
by `N_lambda`, over all all-odd types gives `F_n`. Equations (1)--(4) form an
exact finite recurrence for every `n`.

## Corrected and extended values

The recurrence begins

```text
0, 1, 4, 16, 72, 522, 3390, 29409, 267561, 2820600,
30658050, 377859960, 4866471720, 70224099120,
1052687890800, 17121988170000, ...
```

with offset 1. The values through `n=6` agree with Bouchard and Yeh. Their
reported `3642` and `30753` for `n=7,8` are corrected to `3390` and `29409`.

## General power maps

The proof is not special to squaring. For every fixed `d>=2`, a `j`-cycle in
a permutation's `d`-th power becomes `gcd(j,d)` cycles of length
`j/gcd(j,d)`. The same class-size ratio counts roots, and reverse types are
ordered by the prime-adic valuations for primes dividing `d`. Types whose
parts are coprime to `d` form periodic classes with cycle length
`ord_o(d)`. Thus the identical weighted-tree and weighted-cycle recurrence
computes, for every `n` and fixed `d`, the largest subset `X subset S_n` with
`sigma in X` implying `sigma^d not in X`. A full statement and implementation
are in `POWER_MAP_GENERALIZATION.md` and `scripts/power_map_recurrence.py`.

## Independent verification

The squaring recurrence was checked through `n=50`; this is a verification
horizon, not a limit of the theorem. An optimized C++ program builds the
complete squaring functional graph through `S_11` and applies the exact
leaf/cycle maximum-independent-set algorithm. Two separate Python programs
use, respectively, directed leaf removal and reverse-tree plus weighted-cycle
dynamic programming. All direct calculations agree. A further audit
exhaustively verifies every square-root fiber and formula (1) through `S_7`.
Explicit maximum-set rank lists for `n=7,8,9` provide independently checkable
lower-bound witnesses.

The generic power-map implementation agrees with the squaring recurrence
through `n=12` and with direct functional graphs for exponents `2,3,4,6`
through `S_7`.

The stored `certificates/sample_n1_n50.txt` is a finite audit table. The
recurrence program can write a standard b-file to a requested endpoint; the
stored table ends at the independently verified value `n=50`.

## Reference

- Pierre Bouchard and Yeong-Nan Yeh, “Finding f-free subsets of maximal
  cardinality,” *FPSAC 1992 poster proceedings*, 11–18, ISBN 2-89276-103-4.
