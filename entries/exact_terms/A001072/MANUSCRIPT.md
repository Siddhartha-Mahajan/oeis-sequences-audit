# Minimally 2-edge-connected graphs on 15 vertices

The exact result is `A001072(15)=41142`.

By the Whitney–Robbins ear theorem, every 2-edge-connected graph begins with
a cycle and is obtained by adding open or closed ears. In a minimal
2-edge-connected simple graph every later ear has a new internal vertex: a
one-edge ear could be removed while leaving the preceding graph
2-edge-connected. Every prefix is also minimal; otherwise an edge redundant
in a prefix remains redundant after adding the remaining ears.

The generator starts with cycles and recursively adds every open ear with at
least one new internal vertex and every simple closed ear with at least two.
It retains precisely candidates that are connected and bridgeless but cease
to be so after any edge deletion. Canonical graph6 records from nauty `labelg`
remove isomorphic duplicates.

The counts at orders 3 through 14 are

```text
1,1,3,4,11,23,63,159,459,1331,4083,12750,
```

exactly the published prefix. At order 15 there are 203,421 accepted
pre-canonical candidates and 41,142 canonical records.

An independent verifier avoids the generator's bridge routine. For each edge
`e`, it checks that `G-e` is connected and finds an edge `f` such that
`G-{e,f}` is disconnected. It verifies all records. A separate nauty
`shortg` pass leaves their count and SHA-256 unchanged:

```text
90bae559afbd1a87cdf7703813939a3da6128f17d871f4719407e1a8b0972add.
```
