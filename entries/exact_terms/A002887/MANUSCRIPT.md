# Exact cutting-center orders for center paths of sizes five through ten

For a tree `T` of order `N`, delete a vertex `v` and let the component orders
be `s_1,...,s_d`. Its cutting number is

```text
c_T(v)=Sum_{i<j}s_i*s_j=((N-1)^2-Sum_i s_i^2)/2.    (1)
```

Harary and Ostrand proved that a tree's cutting center is a path. Suppose its
vertices are `v_1,...,v_k`. Removing the path edges produces rooted components
of orders `b_1,...,b_k`; let `q_i` be the sum of squared orders of off-path
branches at `v_i`, and put `L_i=b_1+...+b_(i-1)` and
`R_i=b_(i+1)+...+b_k`. All path vertices have equal cutting number exactly
when

```text
L_i^2+R_i^2+q_i=K                                    (2)
```

for a common integer `K`.

The profile search enumerates every positive composition and every exact
attainable partition square sum in (2). Rooted-subtree feasibility is
recursive: a size is admitted only if some partition into admitted child
sizes makes the root and every descendant have cutting number strictly below
the proposed center value. This is necessary and sufficient, not a
relaxation.

Searching orders increasingly gives

```text
k       1   2   3   4   5   6    7    8    9    10
min N   3   4   7  10  48  48  122  122  264   264.
```

Each accepted profile is realized as an explicit tree. The independent
checker deletes every vertex, recomputes every component size and cutting
number, and confirms that the maximizers are exactly the intended path.
