# A definition correction and bounds for A000576(12)

Write `R_{k,n}` for the number of reduced `k X n` Latin rectangles: the first
row and first column are in natural order.  The data in A000576 are
`R_{n-2,n}`.  They are not the normalized counts under the standard convention
in the linked literature, where only the first row is fixed.  Indeed,
`R_{2,4}=3`, the displayed term, whereas there are nine normalized `2 X 4`
rectangles.

After `k` rows of a normalized Latin rectangle have been chosen, legal
placements for the next row are perfect matchings in an `(n-k)`-regular
bipartite graph with two parts of size `n`.  If `d=n-k`, Schrijver's theorem and
the Bregman--Minc theorem give

```text
((d-1)^(d-1)/d^(d-2))^n <= per(G) <= (d!)^(n/d).
```

Multiplying integer roundings of these bounds over successive row extensions
is valid because every partial rectangle has an extension graph of the stated
degree.  For `n=12`, begin with the published exact value

```text
R_{6,12}=16790769154925929673725062021120.
```

The exact integer extension bounds for degrees `6,5,4,3` are respectively

```text
38632..518400, 5445..97731, 534..13824, 32..1296.
```

Converting between normalized and reduced rectangles and using the known
divisor `floor(12/2)!=720` yields

```text
167650325863480269832990259815752180695040
    <= R_{10,12} <=
42335447246821837670204841011691110328906547200.
```

More generally, the same multiplication gives explicit bounds for every
`R_{n-2,n}` and can begin at any exactly enumerated fixed-height prefix.

Stones and Wanless also imply, on specializing their results to `k=n-2`, that
`floor(n/2)!` divides A000576(n), and that A000576(n) is congruent to 0 modulo
`n` for composite `n` and to 1 modulo `n` for prime `n`.
