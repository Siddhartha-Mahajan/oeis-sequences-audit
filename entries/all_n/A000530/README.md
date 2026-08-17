# A000530 reproducibility package

This folder proves an all-`n` formula for A000530. An exact finite-state
dynamic program independently checks the formerly unknown terms `a(9)` through
`a(50)`. See
[MANUSCRIPT.md](MANUSCRIPT.md) for the proof and trust boundary and

It also proves a finite binomial-sum formula valid for every positive `n`; see
[ALL_N_FORMULA.md](ALL_N_FORMULA.md). The formula and the independently
derived state DP agree through `n=50`. The stored table through `n=100` is a
verification sample; `scripts/make_bfile.py` is the submission b-file writer.

Replay:

```bash
mkdir -p build
python3 scripts/count_dp.py --max-n 50 --output build/dp_recomputed.json
python3 scripts/formula.py --max-n 100 --output build/formula_recomputed.json
python3 scripts/formula.py --max-n 50 --compare certificates/dp_n1_n50.json
python3 scripts/verify_bruteforce.py --max-n 5
python3 scripts/make_bfile.py --last-n 10000 --output build/b000530.txt
```
