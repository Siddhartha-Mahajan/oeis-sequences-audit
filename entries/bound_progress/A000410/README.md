# A000410 reproducibility package

This folder proves the new finite interval

```text
20632852027790990462837 <= A000410(10)
                           <= 115875324413944408596657.
```

The lower bound is a disjoint count of corank-one Boolean hyperplane sections
for finitely many primitive integer normal types.  The upper bound is the best
of exact projective-hyperplane union bounds over the tested primes
`2,3,5,7,11,13`; `p=7` is optimal among them.  An exact correction for row
sets with repeated or zero columns removes their forced multiple counting in
the projective union bound.

See [MANUSCRIPT.md](MANUSCRIPT.md) for the proofs and replay commands.
