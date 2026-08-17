# OEIS sequence advancements: formulas, exact terms, and certificates

This repository collects exact formulas, recurrences, corrected terms,
certified finite computations, and one-sided bounds for difficult short
sequences in the On-Line Encyclopedia of Integer Sequences. Each entry folder
contains a mathematical note, source code, and the certificate or witness
needed to replay the stated result.

The combined paper is available as
[All-$n$ Formulae and Certified Advances for Difficult OEIS Sequences](manuscript/oeis_sequence_advancements.pdf).
It emphasizes results that determine a sequence in every dimension and gives
selected exact and computational results in appendices.

Repository: <https://github.com/Siddhartha-Mahajan/oeis-sequences-audit>

## All-$n$ results

| Entry | Main result | Independent evidence |
|---|---|---|
| [A007234](entries/all_n/A007234/MANUSCRIPT.md) | exact conjugacy-type recurrence; corrected `a(7)=3390`, `a(8)=29409`; extension to every fixed power map `sigma -> sigma^d` | three direct functional-graph algorithms, exhaustive root-fiber audit through `S_7`, explicit maximum sets |
| [A005787](entries/all_n/A005787/MANUSCRIPT.md) | exact recurrence, functional equation, and formal product-sum for reachable circle colorings | complete small intersections and independent six-circle enumeration |
| [A006545](entries/all_n/A006545/MANUSCRIPT.md) | exact ordinary generating function for stable unlabeled unicyclic graphs | structural transposition classification and three independent graph checks |
| [A000530](entries/all_n/A000530/MANUSCRIPT.md) | finite binomial-sum formula | independent exact state DP through `n=50` and literal brute force |
| [A003167](entries/all_n/A003167/MANUSCRIPT.md) | exact finite Egyptian-fraction recursion; `a(7)=155068098` | 262 disjoint branch certificates and independent rational recursion |

## All-$n$ bounds

A general theorem in
[A009997](entries/all_n_bounds/A009997/MANUSCRIPT.md) gives

```text
a(n+1) >= ((3^(n-1)+1)/2)*a(n),
```

hence `a(8)>=78321920095`.

## Exact terms and corrections

| Entry | Result | Certificate |
|---|---|---|
| [A001072](entries/exact_terms/A001072/MANUSCRIPT.md) | `a(15)=41142` | complete ear generation, direct verifier, and nauty hash |
| [A002887](entries/exact_terms/A002887/MANUSCRIPT.md) | corrected `a(5)=48`; exact values through `a(10)` | exhaustive cutting-center profiles and explicit trees |
| [A075099](entries/exact_terms/A075099/MANUSCRIPT.md) | `a(7),...,a(10)=151,276,556,1066`; separated exact value `a(12)=4171` | exact MILP with matching global bounds; independent program checks |
| [A273354](entries/exact_terms/A273354/MANUSCRIPT.md) | `a(3)=11177126654841000000` | exact representations and exhaustive minimality certificate |
| [A323560](entries/exact_terms/A323560/MANUSCRIPT.md) | `a(19)=36001752` | exact exhaustive enumeration |
| [A337433](entries/exact_terms/A337433/MANUSCRIPT.md) | `a(7)=87` | exact zero-gap MILP and independently verified labeling |
| [A363253](entries/exact_terms/A363253/MANUSCRIPT.md) | `a(6)=a(7)=-1` | conductor proof and finite-prefix certificates |
| [A368355](entries/exact_terms/A368355/MANUSCRIPT.md) | exact signed extrema at `n=6` for A368353–A368355 | exhaustive enumeration |

## One-sided bounds and finite progress

| Entry | Result |
|---|---|
| [A005281](entries/bound_progress/A005281/MANUSCRIPT.md) | `a(7)>=58` |
| [A005312](entries/bound_progress/A005312/MANUSCRIPT.md) | `a(8)>=2670` |
| [A007847](entries/bound_progress/A007847/MANUSCRIPT.md) | `a(10)>=5013843621741086` |
| [A202140](entries/bound_progress/A202140/MANUSCRIPT.md) | `a(5)>=7582856` |
| [A306795](entries/bound_progress/A306795/MANUSCRIPT.md) | `a(5)>=283695` |
| [A323134](entries/bound_progress/A323134/MANUSCRIPT.md) | independent counts `3034,64877` at `n=5,6`; convention remains unresolved |
| [A343777](entries/bound_progress/A343777/MANUSCRIPT.md) | `a(5)>10^13` |
| [A358784](entries/bound_progress/A358784/MANUSCRIPT.md) | `a(4)>=42514` |
| [A365910](entries/bound_progress/A365910/MANUSCRIPT.md) | `a(10)<=48` |
| [A380991](entries/bound_progress/A380991/MANUSCRIPT.md) | `a(5)>=71` |

## Replaying the results

Run commands from the relevant entry directory. Most quick checkers use only
the Python standard library. Optional packages for the MILP and symbolic
certificates are listed in `requirements.txt`.

```bash
python3 -m pip install -r requirements.txt
```

C++ programs use C++20. Entry notes distinguish quick certificate checks from
long exhaustive regenerations. To verify every packaged file after extraction:

```bash
sha256sum -c MANIFEST.sha256
```

The live OEIS comparison used when assembling the package is recorded in
[LIVE_OEIS_AUDIT.md](LIVE_OEIS_AUDIT.md).
