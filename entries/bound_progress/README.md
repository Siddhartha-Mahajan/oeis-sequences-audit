# Bound progress: priority order

This folder contains general inequalities, finite one-sided bounds, certified
intervals, and one unresolved discrepancy. An all-`n` statement belongs here
when it only bounds the sequence rather than determining it. The ranking gives
priority to general theorems, two-sided progress, large improvements, and
results with especially transparent certificates.

1. **A009997 — very high importance.** The elementary all-`n` recurrence
   `a(n+1)>=2^(n-1)*a(n)` is a reusable theorem, not just one computed value;
   it also gives the explicit new frontier bound at `n=8`.
2. **A000410 — high importance.** New mathematical lower- and upper-bound
   methods give the first explicit two-sided interval at `n=10`.
3. **A007847 — high importance.** Exact bounded-normal orbit enumeration and
   support decomposition give a substantial, rigorously reproducible lower
   bound at the first unknown dimension.
4. **A000576 — high importance.** Permanent inequalities turn a known exact
   rectangular prefix into a rigorous two-sided interval for the next square
   case; the method also applies beyond this single value.
5. **A365910 — medium-high importance.** An explicit coloring lowers the
   generic upper bound at `n=10` from `114` to `48`, and the certificate is
   particularly easy to verify.
6. **A343777 — medium-high importance.** A rigorous exhaustive frontier proves
   that the next term exceeds `10^13`, a large exclusion even though it does
   not produce a candidate.
7. **A005312 — medium importance.** An exactly verified matrix improves the
   lower bound at `n=8` from `624` to `2670`.
8. **A306795 — medium importance.** Certified factor and Sturm calculations
   improve the `n=5` lower bound from `112870` to `283695`.
9. **A358784 — medium importance.** An explicit Boolean-matrix semigroup
   raises the `n=4` lower bound from `24846` to `42514`.
10. **A202140 — medium importance.** An explicit generated semigroup raises
    the `n=5` lower bound from `6732481` to `7582856`.
11. **A005281 — modest-medium importance.** An explicit word improves the
    first unknown lower bound from `46` to `58` with a direct checker.
12. **A380991 — modest importance.** Explicit coordinates improve the next
    lower bound from `48` to `71`.
13. **A323134 — unresolved.** The independent counts disagree with OEIS, but
    the equivalence convention is not settled. It should not be submitted as
    a DATA correction until that definition issue is resolved.

The ranking is a submission/research priority, not a claim that one subject
is intrinsically more valuable than another.
