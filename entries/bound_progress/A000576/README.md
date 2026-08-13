# A000576 audit and frontier bound

A000576 is the number `R_{n-2,n}` of **reduced** `(n-2) X n` Latin
rectangles.  The current OEIS name says "normalized", but under the convention
used in all three linked papers that would give a different sequence.

This folder proves

```text
167650325863480269832990259815752180695040
    <= A000576(12) <=
42335447246821837670204841011691110328906547200.
```

The exact starting value `R_{6,12}` is from Stones, Lin, Liu and Wang (2016).
The remaining four row extensions are bounded by Schrijver's permanent lower
bound and the Bregman--Minc upper bound.  Both endpoints are rounded to
multiples of `6!`, a divisor supplied by the Stones--Wanless theorem.

Replay with:

```bash
python3 scripts/permanent_bounds.py 12 --from-known --details
```
