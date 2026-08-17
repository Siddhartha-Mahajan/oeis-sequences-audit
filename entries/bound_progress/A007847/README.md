# A007847

This folder certifies the new lower bound

```text
A007847(10) >= 5013843621741086
```

for the number of hyperplanes spanned by vertices of the 10-cube.

Replay from this folder with:

```sh
python3 scripts/combine_known_supports.py
```

The script compiles the bundled C++20 source into `build/` whenever a native
executable is missing or stale.  The run takes roughly half a minute on the
machine used for the audit.  The mathematical justification and trust boundary
are in `MANUSCRIPT.md`.
