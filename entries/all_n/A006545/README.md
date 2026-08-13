# A006545

This folder proves an exact all-`n` ordinary generating function for stable
unlabeled unicyclic graphs.  It extends the published data by

```text
a(9)=176, a(10)=500, a(11)=1425, a(12)=4078,
```

The stored coefficient table through `n=100` is a verification sample. The
same exact series code writes the submission b-file; its intended endpoint is
`n=10000`.

Quick exact replay:

```bash
python3 scripts/generating_function.py --max-n 100 --check --bfile build/sample_n3_n100.txt
python3 scripts/generating_function.py --max-n 10000 --bfile build/b006545.txt
```

Independent finite replay through `n=12`:

```bash
mkdir -p build
c++ -O3 -std=c++20 scripts/verify_group_counts.cpp -o build/verify_group_counts
build/verify_group_counts 1 certificates/unicyclic_n3.g6
build/verify_group_counts 2 certificates/unicyclic_n4.g6
build/verify_group_counts 3 certificates/unicyclic_n5.g6
build/verify_group_counts 8 certificates/unicyclic_n6.g6
build/verify_group_counts 22 certificates/unicyclic_n7.g6
build/verify_group_counts 62 certificates/unicyclic_n8.g6
build/verify_group_counts 176 certificates/unicyclic_n9.g6
build/verify_group_counts 500 certificates/unicyclic_n10.g6
build/verify_group_counts 1425 certificates/unicyclic_n11.g6
build/verify_group_counts 4078 certificates/unicyclic_n12.g6
```

See [`MANUSCRIPT.md`](MANUSCRIPT.md) for the proof and
[`OEIS_EDITS.md`](OEIS_EDITS.md) for concise submission text.
