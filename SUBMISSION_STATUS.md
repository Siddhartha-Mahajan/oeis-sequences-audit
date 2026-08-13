# Unreported advancements

The approved OEIS entries were checked on 2026-08-14. No result listed below
was present on its live page. A175554 was removed from this repository because
its `a(5)` verification was approved on 2026-08-10.

## All-n results

- A000530: add the all-`n` formula; generate and verify the intended
  10,000-term b-file before submission.
- A005787: add the exact recurrence and terms beginning
  `a(6)=323041664`, `a(7)=284820663040`, and
  `a(8)=578706325429760`; use the short b-file through `n=20`.
- A006545: add the all-`n` OGF; generate and verify the intended 10,000-term
  b-file before submission.
- A007234: correct `a(7),a(8)` from `3642,30753` to `3390,29409`, add the
  exact conjugacy-type recurrence, and prepare the submission b-file at the
  largest practical range up to 10,000 terms.

## Exact terms and corrections

- A000157: correct the underdefined NAME and upload exact ancillary values
  `a(12)` through `a(16)`.
- A001072: append `a(15)=41142`.
- A002887: correct `a(5)` from 50 to 48 and append
  `a(5),...,a(10)=48,48,122,122,264,264`.
- A003167: append `a(7)=155068098`.
- A075099: append `a(7),...,a(10)=151,276,556,1066`; put the separated
  exact value `a(12)=4171` in COMMENTS because `a(11)` is unknown.
- A273354: append `a(3)=11177126654841000000`.
- A323560: append `a(19)=36001752`.
- A337433: append `a(7)=87`.
- A363253: insert `a(6)=a(7)=-1`.
- A368353, A368354, A368355: append respectively `-2579770`, `2256911`,
  and `2579770` at `n=6`.

## One-sided bounds and finite progress

- A000410(10):
  `20632852027790990462837 <= a(10) <= 115875324413944408596657`.
- A000576(12):
  `167650325863480269832990259815752180695040 <= a(12) <= 42335447246821837670204841011691110328906547200`.
- A005281(7) `>=58`.
- A005312(8) `>=2670`.
- A007847(10) `>=5013843621741086`.
- A009997: add `a(n+1)>=2^(n-1)*a(n)` for `n>=1`, hence
  `a(8)>=13733158592`.
- A202140(5) `>=7582856`.
- A306795(5) `>=283695`.
- A343777(5) is greater than `10^13`.
- A358784(4) `>=42514`.
- A365910(10) `<=48`.
- A380991(5) `>=71`.

## Not ready for DATA

- A323134: the independent enumerator disagrees at `n=5,6`; ask for the
  intended equivalence convention before proposing a correction.
