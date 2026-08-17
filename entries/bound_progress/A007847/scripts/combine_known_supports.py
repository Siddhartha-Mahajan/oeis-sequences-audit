#!/usr/bin/env python3
"""Combine exact lower-dimensional totals with a bounded full-support count.

The bundled C++ enumerator is compiled automatically when the executable is
missing or older than its source. All arithmetic after enumeration is exact.
"""

from __future__ import annotations

import math
import os
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "bounded_normals.cpp"
BUILD = HERE.parent / "build"
EXE = BUILD / "bounded_normals"
KNOWN = [0, 2, 6, 20, 140, 3254, 252434, 71343208,
         86246755608, 448691419804586]


def ensure_executable() -> Path:
    """Return a native executable, compiling the bundled source when needed.

    Prebuilt binaries are deliberately not used: an archive may have been
    produced on a different operating system or processor architecture.
    """
    if EXE.exists() and os.access(EXE, os.X_OK):
        if EXE.stat().st_mtime_ns >= SOURCE.stat().st_mtime_ns:
            return EXE
    compiler = shutil.which("c++") or shutil.which("g++") or shutil.which("clang++")
    if compiler is None:
        raise RuntimeError("no C++ compiler found; install a C++20 compiler")
    BUILD.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [compiler, "-O3", "-std=c++20", str(SOURCE), "-o", str(EXE)],
        check=True,
    )
    return EXE


def main() -> None:
    n, bound = 10, 12
    full = [0] * len(KNOWN)
    for d in range(1, len(KNOWN)):
        full[d] = KNOWN[d] - sum(math.comb(d, k) * full[k] for k in range(1, d))
        if full[d] < 0:
            raise ArithmeticError(f"negative full-support count in dimension {d}")
    zero_support = sum(math.comb(n, k) * full[k] for k in range(1, n))
    exe = ensure_executable()
    output = subprocess.check_output([str(exe), str(n), str(bound)], text=True)
    line = output.strip().splitlines()[-1]
    match = re.search(r"full_support_lower_bound=(\d+)$", line)
    if not match:
        raise RuntimeError(f"unexpected enumerator output: {line}")
    bounded_full = int(match.group(1))
    total = zero_support + bounded_full
    print(f"known zero-support hyperplanes in dimension {n}: {zero_support}")
    print(f"full-support hyperplanes certified with max |normal coefficient| <= {bound}: {bounded_full}")
    print(f"certified A007847({n}) >= {total}")


if __name__ == "__main__":
    main()
