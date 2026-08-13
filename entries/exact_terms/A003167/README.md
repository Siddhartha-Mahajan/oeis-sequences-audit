# A003167 reproducibility package

This folder proves the new exact value

```text
A003167(7) = 155068098.
```

Equivalently, it counts the nondecreasing positive integer solutions of
`1/2=Sum_{i=1..7} 1/x_i`. See [MANUSCRIPT.md](MANUSCRIPT.md) for the proof,
partition, and trust boundary.

Quick certificate check:

```bash
python3 scripts/verify_certificate.py certificates/n7_exact_certificate.json
```

Full replay:

```bash
mkdir -p build
clang++ -O3 -std=c++17 scripts/count_pair_terminal.cpp -o build/count_pair_terminal
python3 scripts/run_n7_partition.py --binary build/count_pair_terminal \
  --output-dir results/n7_exact --workers 5
python3 scripts/aggregate_n7.py --input-dir results/n7_exact \
  --output build/n7_reaggregated.json
```
