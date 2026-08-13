# A007234

This folder proves an exact all-`n` recurrence for the maximum size of an
`(x -> x^2)`-free subset of `S_n`.  It corrects the last two published values
and extends the sequence:

```text
a(7)=3390, a(8)=29409, a(9)=267561, a(10)=2820600,
a(11)=30658050, a(12)=377859960, ...
```

The former values `3642` and `30753` at `n=7,8` disagree with the exact
recurrence and with three direct functional-graph implementations.

Quick exact replay:

```bash
python3 scripts/verify_recurrence.py --through 50
```

The stored values through `n=50` are a verification sample, not the claimed
limit of the recurrence. The exact recurrence determines every term. The
submission b-file target is 10,000 terms.

Direct permutation replay through `n=9`:

```bash
mkdir -p build
c++ -O3 -std=c++17 scripts/compute_a007234.cpp -o build/compute_a007234
for n in 1 2 3 4 5 6 7 8 9; do build/compute_a007234 "$n"; done
python3 scripts/component_dp.py 9
python3 scripts/verify_witness.py 8 certificates/n8_selected_ranks.txt 29409
```

See [`MANUSCRIPT.md`](MANUSCRIPT.md) for the proof and
[`OEIS_EDITS.md`](OEIS_EDITS.md) for concise submission text.
