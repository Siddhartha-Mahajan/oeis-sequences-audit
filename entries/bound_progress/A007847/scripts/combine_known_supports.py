#!/usr/bin/env python3
"""Combine exact lower-dimensional totals with a bounded full-support count."""

import math
import re
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
EXE = HERE / "bounded_normals"
KNOWN = [0, 2, 6, 20, 140, 3254, 252434, 71343208,
         86246755608, 448691419804586]


def main():
    n, bound = 10, 12
    full = [0] * len(KNOWN)
    for d in range(1, len(KNOWN)):
        full[d] = KNOWN[d] - sum(
            math.comb(d, k) * full[k] for k in range(1, d)
        )
        assert full[d] >= 0
    zero_support = sum(math.comb(n, k) * full[k] for k in range(1, n))
    output = subprocess.check_output([str(EXE), str(n), str(bound)], text=True)
    line = output.strip().splitlines()[-1]
    match = re.search(r"full_support_lower_bound=(\d+)$", line)
    if not match:
        raise RuntimeError(line)
    bounded_full = int(match.group(1))
    total = zero_support + bounded_full
    print(f"known zero-support hyperplanes in dimension {n}: {zero_support}")
    print(f"full-support hyperplanes certified with max |normal coefficient| <= {bound}: {bounded_full}")
    print(f"certified A007847({n}) >= {total}")


if __name__ == "__main__":
    main()
