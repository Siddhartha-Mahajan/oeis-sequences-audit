# A007847

This folder certifies the new lower bound

```text
A007847(10) >= 5013843621741086
```

for the number of hyperplanes spanned by vertices of the 10-cube.

Build and replay from this folder with:

```sh
clang++ -O3 -std=c++20 scripts/bounded_normals.cpp -o scripts/bounded_normals
python3 scripts/combine_known_supports.py
```

The run takes roughly half a minute on the machine used for the audit.  The
mathematical justification and trust boundary are in `MANUSCRIPT.md`.
