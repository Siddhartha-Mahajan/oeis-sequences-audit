# Unreported advancements

The approved OEIS entries were checked on 2026-08-14. No result listed below
was present on its live page at that check.

## All-$n$ formulas and recurrences

- **A000530:** add the finite run-composition formula and further terms.
- **A003167:** add the exact finite Egyptian-fraction recursion and
  `a(7)=155068098`.
- **A005787:** add the recurrence, EGF equation, formal product-sum, and terms
  beginning `a(6)=323041664`.
- **A006545:** add the all-$n$ ordinary generating function and further terms.
- **A007234:** correct `a(7),a(8)` from `3642,30753` to `3390,29409`; add the
  conjugacy-type recurrence. The accompanying note also gives the fixed-power
  generalization.

## Exact terms and corrections

- **A001072:** append `a(15)=41142`.
- **A002887:** correct `a(5)` from 50 to 48 and append
  `48,48,122,122,264,264` at `n=5,...,10`.
- **A075099:** append `151,276,556,1066` at `n=7,...,10`; record the separated
  exact value `a(12)=4171` in COMMENTS because `a(11)` remains unknown.
- **A273354:** append `a(3)=11177126654841000000`.
- **A323560:** append `a(19)=36001752`.
- **A337433:** append `a(7)=87`.
- **A363253:** insert `a(6)=a(7)=-1`.
- **A368353, A368354, A368355:** append respectively `-2579770`, `2256911`,
  and `2579770` at `n=6`.

## All-$n$ bounds

- **A009997:** add
  `a(n+1)>=(3^(n-1)+1)*a(n)/2`, hence `a(8)>=78321920095`.

## One-sided bounds and finite progress

- **A005281(7):** `>=58`.
- **A005312(8):** `>=2670`.
- **A007847(10):** `>=5013843621741086`.
- **A202140(5):** `>=7582856`.
- **A306795(5):** `>=283695`.
- **A343777(5):** greater than `10^13`.
- **A358784(4):** `>=42514`.
- **A365910(10):** `<=48`.
- **A380991(5):** `>=71`.

## Definition discussion required

- **A323134:** the independent enumerator disagrees at `n=5,6`; settle the
  intended equivalence and collinearity convention before proposing DATA
  changes.
