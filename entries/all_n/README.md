# All-n results: priority order

This folder contains exact formulas, recurrences, or generating functions
that determine the relevant sequence in every dimension. The order below is
a judgment of mathematical and OEIS importance, giving extra weight to
corrections of the published record, closure of a genuinely open sequence,
and independently checkable proofs.

1. **A007234 — very high importance.** An exact conjugacy-type recurrence
   corrects two published terms (`a(7)` and `a(8)`), determines every term,
   and resolves the discrepancy by three independent direct
   implementations. This should be submitted first because the current OEIS
   DATA appear wrong.
2. **A005787 — very high importance.** The intersection theorem gives an
   exact recurrence for every `n`, proves the first missing values, and turns
   a short hard sequence into a completely computable one. Its simple
   inclusion--exclusion structure makes it a strong standalone result.
3. **A006545 — high importance.** A structural theorem yields an exact
   all-`n` ordinary generating function and a long extension. It effectively
   closes the enumeration problem, with several independent finite checks.
4. **A000530 — high importance.** A finite binomial-sum formula determines
   every term and is independently audited by exact dynamic programming.
   It is substantial, although it does not correct existing DATA.

The ranking is a submission priority, not a claim that one theorem is
intrinsically more valuable than another.

For A000530, A006545, and A007234, the submission b-file is intended to
contain 10,000 terms. A005787 is the deliberate exception: its integers grow
too quickly for such a file to be useful, so its b-file stops at `n=20`.
These file endpoints are not limits of the all-`n` theorems.
