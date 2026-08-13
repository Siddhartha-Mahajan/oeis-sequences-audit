# An all-n formula for A000530

## Result

The exact values extending the published sequence begin

```text
a(9)  = 29995812
a(10) = 368025335
a(11) = 4637331008
a(12) = 59687103424
a(13) = 781671686963
a(14) = 10386703092609
a(15) = 139745901077363.
```

The calculation continues without gaps through

```text
a(50) = 9477445937970947982274905666367581078225599344024301633.
```

The full DP diagnostic record through `n=50` is
`certificates/dp_n1_n50.json`. The stored formula sample through `n=100` ends
with
`a(100)=2686573619815364754279164651828769162775089562608804488153301650705874639028185668593969112596566625475771953480374`.

In addition, `ALL_N_FORMULA.md` proves a finite binomial-sum expression for
every `a(n)` by counting the safe-prefix tree through ordered run compositions.
Its implementation is independent of the state-transition DP and agrees with
all 50 computed values.

## Finite-state proof

For a word `x`, let `c_s(x)` be the number of occurrences of symbol `s` and
`m_s(x)` its longest run of `s`. The relevant predicate is
`c_s(x)+m_s(x)>=2*n`. Call a prefix safe when this fails for both symbols.

The state

```text
(c_0,c_1,m_0,m_1,last,current_run)
```

determines the state after appending either bit and determines whether a
predicate has just become true. Hence equal states have identical future
continuations and their multiplicities may be merged. When a safe state is
extended by zero and the zero predicate first holds, its multiplicity is added
to `a(n)`; an extension triggering either predicate is never propagated.

The procedure is finite. In a safe word, `c_s+m_s<=2*n-1` for each symbol.
If both symbols occur, `m_s>=1`, hence `c_s<=2*n-2` and the length is at most
`4*n-4`; a constant word is shorter still. Propagating until the safe frontier
is empty therefore exhausts all qualifying words rather than imposing a
numerical cutoff.

## Reproducibility and ancillary files

- `scripts/count_dp.py` is the complete integer DP and emits state/transition
  diagnostics with every term.
- `certificates/dp_n1_n50.json` is its preserved output. It reproduces all
  eight previously listed terms before giving the 42 extensions.
- `certificates/sample_n1_n100.txt` is a finite two-column verification table.
- `certificates/formula_n1_n100.json` is the formula output behind that table.
- `scripts/make_bfile.py` writes a standard OEIS b-file to any requested
  endpoint; the intended submission endpoint is `n=10000`.
- `scripts/verify_bruteforce.py` is a structurally independent enumerator of
  literal words. It reproduces the first five terms and checks the convention
  without state merging.
- `ALL_N_FORMULA.md` and `scripts/formula.py` give and implement the all-`n`
  binomial formula.

The all-`n` formula and the finiteness and sufficiency of the DP state are
mathematical. The displayed large integer evaluations are computer-assisted.
No floating-point arithmetic, random search, or external solver is used.
