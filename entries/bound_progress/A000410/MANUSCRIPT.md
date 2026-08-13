# New finite bounds for A000410(10)

A000410(n) is the number of unordered sets of `n` distinct nonzero vectors in
`{0,1}^n` whose rational span is singular.  The current exact table stops at
`n=9`.  We prove

```text
20632852027790990462837 <= A000410(10)
                           <= 115875324413944408596657.       (1)
```

## Lower bound

Every rank-nine row set has a unique primitive integral normal up to sign, so
classes belonging to distinct unoriented normals are disjoint.  For each
primitive coefficient type retained by `scripts/evaluate_cutoff_bound.py`, the
Boolean section is enumerated exactly and its rank is checked.  If it contains
`Q` points, the cube-subspace lemma shows that a `d`-dimensional span contains
at most `2^d` Boolean points.  Greedy basis selection therefore supplies at
least `Product_{d=0..8}(Q-2^d)` ordered bases, after which any remaining point
extends a basis to a singular ten-row set.  Summing the disjoint normal classes,
together with the exact A000409 zero-or-repeated-column subclass, yields the
left side of (1).

## Upper bound

Fix a prime `p`.  Divide an integral dependence by the largest common power of
`p`; its reduction is a nonzero normal over `F_p`.  Hence every rationally
singular row set lies in a projective hyperplane over `F_p`.

For a nonzero normal `a`, put

```text
Q(a) = #{x in {0,1}^n : a dot x = 0 mod p}.
```

The zero vector is excluded, so the hyperplane contains at most
`binomial(Q(a)-1,n)` admissible sets.  Thus

```text
A000410(n) <= Sum_[a in P^(n-1)(F_p)] binomial(Q(a)-1,n).      (2)
```

The section size depends only on the coefficient histogram of `a`.  The script
evaluates (2) exactly over all weak compositions of `n`, with multinomial
multiplicity, and divides by `p-1` for scalar multiples.  At `n=10` the values
for `p=2,3,5,7,11,13` are respectively

```text
313211186436066952736703
176507348219639686888276
125651829303147329448277
118121286496007494503870
123845797805944334463926
129589169736979212364148.
```

The raw `p=7` sum overcounts a row set with `k` distinct nonzero columns at
least `(7^(n-k)-1)/6` times.  The number of such row sets is

```text
C_k = S(n+1,k+1) Sum_{j=1..k+1} s(k+1,j) binomial(2^(j-1)-1,n),
```

where `S` and `s` are Stirling numbers of the second and signed first kind.
The classes partition all row sets, which provides an internal check.  At
`n=10`, subtracting the forced excess
`2245962082063085907213` from the raw `p=7` bound gives the right side of
(1).  The correction is replayed by
`scripts/projective_multiplicity_correction.py`.

## Replay

```bash
python3 scripts/evaluate_cutoff_bound.py --n 10 --cutoff 4 --max-support 8 --summary-only
python3 scripts/prime_union_upper.py --n 10 --primes 2 3 5 7 11 13
```

Both computations use exact integer or rational arithmetic.
