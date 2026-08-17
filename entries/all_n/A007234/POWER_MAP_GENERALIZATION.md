# Power-map-free subsets of symmetric groups

The conjugacy-type method for A007234 extends verbatim from squaring to every
fixed exponent `d>=2`.

For a partition type `mu`, let `q_d(mu)` be the type obtained by taking the
`d`-th power: a cycle of length `j` splits into `gcd(j,d)` cycles of length
`j/gcd(j,d)`. For `q_d(mu)=lambda`, every fixed permutation of type `lambda`
has

```text
r_d(lambda,mu)=z_lambda/z_mu
```

`d`-th roots of type `mu`. This follows from equivariance of the power map and
the ratio of conjugacy-class sizes.

Let `P` be the set of prime divisors of `d`, and attach to a type the height

```text
h_d(lambda)=Sum_(p in P) max{v_p(j): m_j(lambda)>0}.
```

If `lambda` has a part not coprime to `d`, then every reverse type `mu` with
`q_d(mu)=lambda` has strictly larger height. Indeed, for a source cycle length
`ell` and target length `j=ell/gcd(ell,d)`,

```text
v_p(j)=max(v_p(ell)-v_p(d),0).
```

Thus the reverse-type graph is acyclic away from types whose parts are all
coprime to `d`, and the same include/exclude tree recurrence applies.

For a periodic type `lambda`, put

```text
o_lambda=lcm{j:m_j(lambda)>0},
L_lambda=ord_(o_lambda)(d),
N_lambda=(n!/z_lambda)/L_lambda.
```

The class splits into `N_lambda` directed `d`-th-power cycles of length
`L_lambda`. The unique same-type predecessor is omitted from the attached
reverse tree. If its attached-tree states are `E_lambda,I_lambda` and
`g_lambda=max(0,I_lambda-E_lambda)`, each cycle contributes

```text
L_lambda*E_lambda + floor(L_lambda/2)*g_lambda
```

when `L_lambda>1`, and `E_lambda` when `L_lambda=1` because the root has a
loop. Summing over periodic types gives the maximum cardinality of a subset
`X` of `S_n` satisfying

```text
sigma in X  ==>  sigma^d not in X.
```

`scripts/power_map_recurrence.py` implements this all-`n`, all-fixed-`d`
recurrence. `scripts/verify_power_generalization.py` checks the `d=2`
specialization against the A007234 recurrence through `n=12` and compares
with direct functional graphs for `d=2,3,4,6` through `S_7`.
