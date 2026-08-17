# Stable unlabeled unicyclic graphs

Let `R(x)` be the ordinary generating function for unlabeled rooted trees.
Pólya's rooted-tree equation is

```text
R(x) = x*exp(Sum_(j>=1) R(x^j)/j).                       (1)
```

Let `B(x)` count rooted trees in which no vertex has two or more leaf
children. In the rooted-tree multiset construction, the arbitrary multiset of
leaf children has generating function `1/(1-x)`. Replacing it by multiplicity
zero or one, with generating function `1+x`, multiplies the rooted-tree
operator by `(1+x)(1-x)=1-x^2`. Thus

```text
B(x) = x*(1-x^2)*exp(Sum_(j>=1) B(x^j)/j).               (2)
```

For `F(0)=0`, let `D(F)` count unoriented cycles of length at least three
decorated by `F`-objects. Burnside's lemma for the dihedral group gives

```text
D(F) = Sum_(k>=3) (Rot_k(F)+Ref_k(F))/(2*k),
Rot_k(F) = Sum_(d|k) phi(d)*F(x^d)^(k/d),
Ref_(2*m+1)(F) = (2*m+1)*F(x)*F(x^2)^m,
Ref_(2*m)(F) = m*(F(x)^2*F(x^2)^(m-1)+F(x^2)^m).        (3)
```

Every connected unicyclic graph is uniquely an unoriented cycle decorated by
rooted trees, so `D(R)` is the OGF for all unlabeled unicyclic graphs.

## Classification of transpositions

McAvaney, Grant and Holton proved that a unicyclic graph is stable if and only
if its automorphism group contains a transposition. A transposition swaps two
vertices `u,v` and fixes every other vertex, so `u` and `v` are twins:

```text
N(u)\{v}=N(v)\{u}.
```

In a connected unicyclic graph, twin pairs occur in exactly three forms.

1. If `u,v` are nonadjacent and have one common neighbor, they are two leaf
   children of that neighbor. Any additional neighbor would have to be common
   and would create a second cycle.
2. If `u,v` are adjacent, connectedness forces a common neighbor. Unicyclicity
   permits exactly one, so `u,v` are the two bare vertices of a triangle.
3. If nonadjacent twins have two common neighbors, those four vertices form
   the unique cycle, a 4-cycle, and `u,v` are opposite bare vertices.

Three or more common neighbors, or extra incident edges in the last two
cases, would create more than one cycle. Conversely, each displayed
configuration visibly gives a transposition. This proves the classification.

## Generating function

The series `D(B)` counts unicyclic graphs with no pair of sibling leaves, so
`D(R)-D(B)` counts those stable by the first mechanism. Among the remaining
`B`-decorated cycles, triangle transpositions contribute

```text
x^2*B(x),
```

because two cycle vertices are bare and the third carries an arbitrary
`B`-object. For a 4-cycle, the transposed opposite vertices are bare and the
other opposite pair carries an unordered pair of `B`-objects, giving

```text
x^2*(B(x)^2+B(x^2))/2.
```

The triangle and 4-cycle families are disjoint and contain no repeated-leaf
transposition. Therefore the OGF is

```text
A(x) = D(R)-D(B)+x^2*B(x)
       +(x^2/2)*(B(x)^2+B(x^2)),                         (4)
a(n) = [x^n] A(x).
```

Equations (1)--(4) determine every term. They begin

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
`n=12` were generated with nauty. One Python checker applies the classical
stability criterion recursively; a separate C++ checker counts
`|Aut(G-v)|` and `|Aut(G)_v|` directly at every deletion state. Both give

```text
1,2,3,8,22,62,176,500,1425,4078.
```

A third elementary pass checks only for a transposition and selects exactly
the same graph6 records at each order.

The exact series implementation writes an OEIS b-file to any requested
endpoint. The stored `certificates/sample_n3_n100.txt` is a finite audit
sample and supplies a compact b-file through `n=100`.

## References

- K. L. McAvaney, “Semi-stable and stable cacti,” *J. Austral. Math. Soc.*
  20 (1975), 419–430, doi:10.1017/S1446788700016141.
- K. L. McAvaney, D. D. Grant and D. A. Holton, “Stable and semi-stable
  unicyclic graphs,” *Discrete Math.* 9 (1974), 277–288.
- D. A. Holton and D. D. Grant, “Regular graphs and stability,” *J. Austral.
  Math. Soc.* 20 (1975), 377–384, doi:10.1017/S1446788700020735.
