# Proof reduction for A002887

## 1. Cutting numbers

For a tree `T` of order `N`, delete a vertex `v` and let the resulting
component sizes be `s_1,...,s_d`.  Since paths in a tree are unique,

```text
c_T(v) = Sum_{i<j} s_i*s_j
       = ((N-1)^2 - Sum_i s_i^2)/2.                 (1)
```

Harary and Ostrand proved that the cutting center of a tree is a path.

## 2. Profiles of a center path

Suppose the center path has vertices `v_1,...,v_k`.  Delete its `k-1` path
edges.  Let `b_i` be the order of the rooted component containing `v_i`, and
let the branches incident with `v_i` but not lying on the center path have
orders forming a partition of `b_i-1`.  Write `q_i` for the sum of the squares
of those branch orders.  Put

```text
L_i = b_1 + ... + b_(i-1),
R_i = b_(i+1) + ... + b_k.
```

By (1), all center vertices have equal cutting number if and only if there is
an integer `K` such that

```text
L_i^2 + R_i^2 + q_i = K                         (2)
```

for every `i`.  Their common cutting number is

```text
C = ((N-1)^2-K)/2.                              (3)
```

Thus every possible tree gives a positive composition `(b_1,...,b_k)` and an
exact partition-square-sum witness satisfying (2).

## 3. Exact rooted-subtree feasibility

For fixed `N` and proposed center value `C`, call a positive integer `s`
*safe* if some rooted tree of order `s`, attached by its root to an outside
component of order `N-s`, has every vertex's cutting number strictly below
`C`.

Size 1 is safe.  Inductively, suppose the root has child-subtree orders
`t_1,...,t_d`, all already safe, with sum `s-1` and square sum `q`.  Formula
(1) at the root becomes

```text
(N-s)(s-1) + ((s-1)^2-q)/2.                    (4)
```

Therefore `s` is safe exactly when a partition of `s-1` into safe smaller
sizes makes (4) strictly less than `C`.  This is both necessary and sufficient:
necessity follows by deleting the root of any safe tree; sufficiency follows
by attaching witnessing safe rooted trees of the indicated sizes to a new
root.  Consequently the unbounded integer-partition DP in `profile_search.py`
computes the exact safe sizes and exact attainable square sums, not a
relaxation.

For each composition, the program intersects the shifted square-sum spectra in
(2), computes `C` from (3), and applies the exact safe-subtree recursion to all
off-path branches.  Hence:

- every tree with a k-vertex cutting center appears in the search;
- every accepted profile yields an explicit tree whose off-path vertices are
  strictly below the center value.

Searching orders increasingly therefore proves the lower bound when the first
accepted profile is reached.  `build_profile_tree.py` realizes that profile,
and `verify_certificate.py` checks the resulting edge list without using the
profile argument.

## 4. Results

The first accepted orders are

```text
k       1   2   3   4   5   6    7    8    9    10
min N   3   4   7  10  48  48  122  122  264   264
```

The first four agree with direct unlabeled-tree enumeration and the published
prefix.  The fifth corrects the unproved value 50 in the OEIS record.

