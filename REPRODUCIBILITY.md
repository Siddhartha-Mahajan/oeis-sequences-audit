# Reproducibility

Run commands from the relevant `entries/<category>/AXXXXXX/` directory. Most
witness checkers use only the Python standard library. A306795 uses SymPy;
the MILP packages use NumPy and SciPy/HiGHS.

```bash
python3 -m pip install -r requirements.txt
```

C++ sources use C++20 and can be compiled with a recent Clang or GCC:

```bash
mkdir -p build
c++ -O3 -std=c++20 scripts/PROGRAM.cpp -o build/PROGRAM
```

The per-entry notes distinguish quick certificate checks from expensive full
regenerations. Generated binaries and replay outputs belong in `build/` or
`results/`.

The combined manuscript source and PDF are in `manuscript/`. Rebuild it with:

```bash
cd manuscript
latexmk -pdf main.tex
```

The source also builds with `tectonic main.tex`.

To verify file integrity after extraction:

```bash
sha256sum -c MANIFEST.sha256
```
