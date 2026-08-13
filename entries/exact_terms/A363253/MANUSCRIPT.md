# The missing hexagonal and heptagonal cases of A363253

For `s>=3`, write

```text
P_s(k) = ((s-2)k^2-(s-4)k)/2
```

for the `k`-th positive `s`-gonal number. A representation is a sum of
distinct positive `s`-gonal numbers; the singleton representation counts.

## Result

```text
A363253(6) = -1 and A363253(7) = -1.
```

Thus no positive hexagonal number has exactly six representations and no
positive heptagonal number has exactly seven representations.

## Conductor lemma

Suppose the subset sums of `P_s(1),...,P_s(m)` cover every integer in
`[L,U]`, and `P_s(m+1)<=U-L+1`. The intervals `[L,U]` and
`[L+P_s(m+1),U+P_s(m+1)]` overlap, so adjoining `P_s(m+1)` extends the covered
interval. Since `P_s(j+1)<2*P_s(j)` in the ranges used below, the overlap
continues after every later summand. Hence every integer at least `L` is a
sum of distinct positive `s`-gonal numbers.

Exact bitset subset-sum calculations give:

- the subset sums of `P_6(1),...,P_6(11)` cover `[268,678]`; its length 411
  exceeds `P_6(12)=276`;
- the subset sums of `P_7(1),...,P_7(13)` cover `[388,1523]`; its length 1136
  exceeds `P_7(14)=469`.

Therefore every integer at least 268 is a distinct hexagonal subset sum, and
every integer at least 388 is a distinct heptagonal subset sum.

## Late targets have too many representations

For `k>=68` and `d=1,...,6`, set

```text
R_d(k) = P_6(k)-P_6(k-d).
```

At `k=68` the six remainders are
`269,534,795,1052,1305,1554`. They increase with `k`, so each is representable
by distinct positive hexagonal numbers. Also `R_d(k)<P_6(k-d)` throughout
this range. Adjoining `P_6(k-d)` gives six representations of `P_6(k)` whose
largest summands are respectively `P_6(k-1),...,P_6(k-6)`. These are distinct;
together with the singleton, every such target has at least seven
representations.

For `k>=79`, the same argument with `d=1,...,7` uses the heptagonal
remainders `391,777,1158,1534,1905,2271,2632` at `k=79`. Every later target
has at least eight representations.

An exact distinct-subset DP checks the finite prefixes `k<68` and `k<79`.
Counts are capped at seven and eight, respectively, which preserves whether
the true count equals six or seven. No target in either prefix has the desired
exact multiplicity. This proves the result.

## Replay

```bash
python3 scripts/prove_a6_a7.py --output certificates/a6_a7_certificate.replay.json
```

The verifier uses exact integer arithmetic and independently checks the two
covered intervals, every finite-prefix representation count, and all threshold
inequalities used by the conductor argument.
