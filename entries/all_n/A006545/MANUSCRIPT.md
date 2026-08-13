# Stable unlabeled unicyclic graphs

Let `R(x)` be the OGF for unlabeled rooted trees.  Pólya's rooted-tree
equation is

```text
R(x) = x*exp(Sum_{j>=1} R(x^j)/j).                  (1)
```

Let `B(x)` count rooted trees in which no vertex has two or more leaf
children.  Replacing the arbitrary multiset of leaf children, with generating
function `1/(1-x)`, by multiplicity zero or one, with generating function
`1+x`, gives

```text
B(x) = x*(1-x^2)*exp(Sum_{j>=1} B(x^j)/j).          (2)
```

For `F(0)=0`, let `D(F)` count unoriented cycles of length at least three
decorated by `F`-objects.  Burnside's lemma gives

```text
D(F) = Sum_{k>=3} (Rot_k(F)+Ref_k(F))/(2*k),
Rot_k(F) = Sum_{d|k} phi(d)*F(x^d)^(k/d),
Ref_(2*m+1)(F) = (2*m+1)*F(x)*F(x^2)^m,
Ref_(2*m)(F) = m*(F(x)^2*F(x^2)^(m-1)+F(x^2)^m).   (3)
```

Every connected unicyclic graph is uniquely an unoriented cycle decorated by
rooted trees, so `D(R)` is the OGF for all unlabeled unicyclic graphs.

McAvaney proved that a cactus is stable if and only if its automorphism group
contains a transposition.  In a unicyclic graph, swapping two vertices and
fixing every other vertex is possible in exactly three ways:

1. two leaf children of one vertex;
2. two bare vertices of a triangle;
3. two opposite bare vertices of a 4-cycle.

The series `D(B)` excludes the first source.  The triangle correction is
`x^2*B(x)`.  For a 4-cycle, the remaining opposite vertices support an
unordered pair of `B`-objects, giving
`x^2*(B(x)^2+B(x^2))/2`.  Therefore

```text
A(x) = D(R)-D(B)+x^2*B(x)+(x^2/2)*(B(x)^2+B(x^2)), (4)
a(n) = [x^n] A(x).
```

Equations (1)--(4) determine every term.  They begin

```text
1,2,3,8,22,62,176,500,1425,4078,11666,33447,95922,
275332,790518,2270963,6525674,18759532,...
```

with offset 3.

## Independent computational checks

The exact series implementation reproduces the standard total-unicyclic
counts through `n=12`:

```text
1,2,5,13,33,89,240,657,1806,5026.
```

Independently, all connected unlabeled `n`-vertex, `n`-edge graphs through
`n=12` were generated with nauty.  One Python checker applies the
neighborhood-invariance criterion recursively; a separate C++ checker counts
`|Aut(G-v)|` and `|Aut(G)_v|` directly at every deletion state.  Both give

```text
1,2,3,8,22,62,176,500,1425,4078.
```

A third elementary pass checks only for a transposition and selects exactly
the same graph6 records at each order.

The exact series implementation also writes an OEIS b-file to any requested
endpoint. The stored `certificates/sample_n3_n100.txt` is a finite audit
sample; the intended submission endpoint is `n=10000`.

## References

- K. L. McAvaney, “Semi-stable and stable cacti,” *J. Austral. Math. Soc.*
  20 (1975), 419–430, doi:10.1017/S1446788700016141.
- K. L. McAvaney, D. D. Grant and D. A. Holton, “Stable and semi-stable
  unicyclic graphs,” *Discrete Math.* 9 (1974), 277–288.
- D. A. Holton and D. D. Grant, “Regular graphs and stability,” *J. Austral.
  Math. Soc.* 20 (1975), 377–384, doi:10.1017/S1446788700020735.
