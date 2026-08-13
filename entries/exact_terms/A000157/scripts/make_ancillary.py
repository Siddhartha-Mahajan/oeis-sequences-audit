#!/usr/bin/env python3
"""Create the OEIS-sized ancillary table and checksum manifest."""

from __future__ import annotations

import hashlib
from pathlib import Path


HERE = Path(__file__).resolve().parent
INPUT = HERE / "candidate_b000157_through_16.txt"


def main() -> None:
    rows = []
    for line in INPUT.read_text().splitlines():
        n_text, decimal = line.split()
        n = int(n_text)
        if n >= 12:
            rows.append((n, decimal))
    table_lines = [
        "# A000157: exact terms too long for the b-file\n",
        "# Format: n a(n)\n",
        "# Computed independently by burnside_a000157.py and signed_cycle_type_check.py.\n",
    ]
    hash_lines = ["n,digits,sha256\n"]
    for n, decimal in rows:
        table_lines.append(f"{n} {decimal}\n")
        hash_lines.append(
            f"{n},{len(decimal)},{hashlib.sha256(decimal.encode()).hexdigest()}\n"
        )
    (HERE / "a000157_terms_12_16.txt").write_text("".join(table_lines))
    (HERE / "a000157_terms_12_16_sha256.csv").write_text("".join(hash_lines))


if __name__ == "__main__":
    main()
