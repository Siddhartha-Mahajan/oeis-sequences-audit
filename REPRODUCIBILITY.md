# Reproducibility

Run commands from the relevant `entries/<category>/AXXXXXX/` directory. Python witness
checkers use the standard library except A306795, whose certificate verifier
uses SymPy. The two MILP solvers use NumPy and SciPy/HiGHS.

Install optional Python dependencies with:

```bash
python3 -m pip install -r requirements.txt
```

C++ sources use C++20 and can be compiled with any recent Clang or GCC:

```bash
mkdir -p build
c++ -O3 -std=c++20 scripts/PROGRAM.cpp -o build/PROGRAM
```

The per-entry manuscripts give exact commands and distinguish quick witness
checks from expensive exhaustive reruns. Generated binaries and replay outputs
belong in `build/` or `results/` and are intentionally excluded.

To verify file integrity after a release:

```bash
shasum -a 256 -c MANIFEST.sha256
```
