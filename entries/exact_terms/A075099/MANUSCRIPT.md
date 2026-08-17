# Five exact values of A075099

## Result

The computations prove

```text
A075099(7)  = 151
A075099(8)  = 276
A075099(9)  = 556
A075099(10) = 1066
A075099(12) = 4171.
```

The first replaces the conjectural value 156. The even values satisfy
Mallows's conjectured identity `a(2*n)=a(n)+2^(2*n)` at `n=4,5,6`; the ninth
term is new odd-index data. The value at `n=12` is separated by the unresolved
`n=11` term and satisfies `a(12)=a(6)+2^12`. The model reproduces the known
values at `n=2,...,6`.

## General concatenation bounds

For all positive `m,n`,

```text
a(m+n) <= a(m)+a(n)+2^(m+n).                          (1)
```

Generate all words of lengths `m` and `n` using optimal programs, taking the
union of their intermediate sets. Every word of length `m+n` is then the
product of its length-`m` prefix and length-`n` suffix, so one final
multiplication per target completes the construction. When `m=n`, the same
length-`m` program serves both factors, giving the sharper specialization

```text
a(2*m) <= a(m)+2^(2*m).                                (2)
```

The constructions at `m=4,5,6` attain the right-hand side of (2).

## Method

Every length-`n` target word costs one final multiplication. A shorter word
costs one multiplication exactly when it is selected as a reusable
intermediate. Binary variables choose the intermediates. For every selected
word and every required target, split-witness variables require at least one
cut whose two factors are generators or selected shorter words. These witness
variables may be continuous in `[0,1]`: if no cut is usable then every witness
is forced to zero, while a usable cut can be assigned one. Thus this relaxation
does not change the feasible binary intermediate families.

The objective is `2^n` plus the number of selected intermediates. For
`n=7,8,9,10,12`, HiGHS finds respectively 23, 20, 44, 42, and 75
intermediates. Adding the final targets gives 151, 276, 556, 1066, and 4171.
Every exact run has matching primal and dual objectives, solver status
optimal, and zero MIP gap. The archived programs are checked independently of
the optimizer.

At `n=11`, a 900-second run found 90 intermediates, hence a construction with
total cost 2138, but stopped with solver-reported lower bound 2118. The
construction record is included because it proves the one-sided bound
`a(11)<=2138`; the incomplete optimization is not used as an exactness claim.

## Files and replay

- `certificates/n7_milp.json` through `certificates/n10_milp.json`, and
  `certificates/n12_milp.json`: optimal records and all selected intermediate
  words.
- `certificates/n11_time_limited.json`: non-optimal run retained to distinguish
  the construction bound from the completed runs.
- `scripts/verify_construction.py`: standard-library construction checker.
- `scripts/solve_milp.py`: complete NumPy/SciPy MILP model.

Quick constructive check:

```bash
for f in certificates/n{7,8,9,10,12}_milp.json; do
  python3 scripts/verify_construction.py "$f"
done
```

Full optimization replay, after installing the root requirements:

```bash
python3 scripts/solve_milp.py 10 --output certificates/n10_recomputed.json
```

The quick checker certifies each construction. Global optimality is the
integer optimizer's zero-gap conclusion for the fully included model.
