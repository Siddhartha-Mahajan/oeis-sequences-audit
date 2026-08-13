# Verified OEIS sequence advancements

This repository packages results from a targeted audit of hard, short OEIS
sequences. Each entry is self-contained: a mathematical note, final source,
the certificate or witness, and exact replay commands.

The entry folders are grouped by the strongest kind of result they contain.
A package with both an all-`n` theorem and new exact terms is filed under
`all_n`. The approved OEIS entries were checked on 2026-08-14; see
[LIVE_OEIS_AUDIT.md](LIVE_OEIS_AUDIT.md). None of the results below was present
on its approved OEIS page at that check.

## All-n results

| Entry | Result | Evidence |
|---|---|---|
| [A000530](entries/all_n/A000530/MANUSCRIPT.md) | exact all-`n` formula | run-composition proof and independent exact DP through `n=50` |
| [A005787](entries/all_n/A005787/MANUSCRIPT.md) | all-`n` recurrence; exact `a(6)` through `a(20)` | intersection theorem, independent six-circle enumeration and finite checks |
| [A006545](entries/all_n/A006545/MANUSCRIPT.md) | exact all-`n` OGF | structural transposition theorem and three independent finite checks |
| [A007234](entries/all_n/A007234/MANUSCRIPT.md) | exact all-`n` recurrence; corrected `a(7)=3390`, `a(8)=29409` | conjugacy-type proof, three direct algorithms and explicit witnesses |

## Exact terms and corrections

| Entry | Result | Evidence |
|---|---|---|
| [A000157](entries/exact_terms/A000157/MANUSCRIPT.md) | corrected definition; exact `a(12)` through `a(16)` | two independent exact Burnside computations |
| [A001072](entries/exact_terms/A001072/MANUSCRIPT.md) | `a(15)=41142` | complete ear generation, direct verifier and nauty certificate |
| [A002887](entries/exact_terms/A002887/MANUSCRIPT.md) | corrected `a(5)=48`; exact through `a(10)` | exact profile lower bounds and explicit tree certificates |
| [A003167](entries/exact_terms/A003167/MANUSCRIPT.md) | `a(7)=155068098` | exact 262-branch Egyptian-fraction enumeration |
| [A075099](entries/exact_terms/A075099/MANUSCRIPT.md) | exact `a(7)` through `a(10)`, and `a(12)=4171` | five exact terms and zero-gap MILP records |
| [A273354](entries/exact_terms/A273354/MANUSCRIPT.md) | `a(3)=11177126654841000000` | exact square classification and exhaustive cubic-scaling certificate |
| [A323560](entries/exact_terms/A323560/MANUSCRIPT.md) | `a(19)=36001752` | exact exhaustive enumeration |
| [A337433](entries/exact_terms/A337433/MANUSCRIPT.md) | `a(7)=87` | exact term, MILP record and witness |
| [A363253](entries/exact_terms/A363253/MANUSCRIPT.md) | `a(6)=a(7)=-1` | conductor proof and exact finite-prefix certificates |
| [A368355](entries/exact_terms/A368355/MANUSCRIPT.md) | exact signed extrema at `n=6` | exact terms for A368353-A368355 |

## Bound progress and unresolved discrepancies

| Entry | Result | Evidence |
|---|---|---|
| [A000410](entries/bound_progress/A000410/MANUSCRIPT.md) | `20632852027790990462837 <= a(10) <= 115875324413944408596657` | primitive-normal lower bound and multiplicity-corrected `F_7` hyperplane upper bound |
| [A000576](entries/bound_progress/A000576/MANUSCRIPT.md) | corrected definition; certified interval for `a(12)` | exact `R_{6,12}` prefix and permanent bounds for the remaining rows |
| [A005281](entries/bound_progress/A005281/MANUSCRIPT.md) | `a(7)>=58` | explicit degree-6 word and exhaustive projection check |
| [A005312](entries/bound_progress/A005312/MANUSCRIPT.md) | `a(8)>=2670` | exact-verified matrix witness |
| [A007847](entries/bound_progress/A007847/MANUSCRIPT.md) | `a(10)>=5013843621741086` | exact bounded-normal enumeration, affine-rank checks and support decomposition |
| [A009997](entries/bound_progress/A009997/MANUSCRIPT.md) | all-`n` lower recurrence; `a(8)>=13733158592` | elementary chamber-lifting proof |
| [A202140](entries/bound_progress/A202140/MANUSCRIPT.md) | `a(5)>=7582856` | improved constructive lower bound |
| [A306795](entries/bound_progress/A306795/MANUSCRIPT.md) | `a(5)>=283695` | certified algebraic lower bound |
| [A323134](entries/bound_progress/A323134/MANUSCRIPT.md) | independent counts `3034,64877` at `n=5,6` | convention unresolved; discussion is required before an OEIS correction |
| [A343777](entries/bound_progress/A343777/MANUSCRIPT.md) | `a(5)>10^13` | rigorous finite exclusion |
| [A358784](entries/bound_progress/A358784/MANUSCRIPT.md) | `a(4)>=42514` | improved constructive lower bound |
| [A365910](entries/bound_progress/A365910/MANUSCRIPT.md) | `a(10)<=48` | explicit constructive upper bound |
| [A380991](entries/bound_progress/A380991/MANUSCRIPT.md) | `a(5)>=71` | explicit constructive lower bound |

## What is not packaged

A125620 and A374086 need definition clarification, not a numerical
submission. A269516 produced a useful state reduction but no new bound or
term. A335892 only rechecked published witnesses. A356650, A379177, and
A390607 did not improve the public record.

## Using this repository in OEIS LINKS

Create a release tag before submission. Link each OEIS page directly to the
corresponding tagged entry folder, for example:

```html
Siddhartha Mahajan, <a href="https://github.com/USER/REPO/tree/v1.0.0/entries/exact_terms/A075099">Supporting computation and certificate for A075099</a>.
```

## Trust boundary

The verifier proves only what its note says. Constructive witnesses certify
one-sided bounds. Exhaustive enumerators support exact terms only when the
note also explains the finite search space and symmetry reduction. MILP
records include the optimizer status and zero gap; standalone witness checkers
verify the constructive side but do not independently re-prove the solver's
global bound.
