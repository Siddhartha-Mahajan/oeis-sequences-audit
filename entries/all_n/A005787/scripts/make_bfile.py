#!/usr/bin/env python3
"""Write a standard OEIS b-file for A005787 from the exact recurrence."""

from __future__ import annotations

import argparse
from pathlib import Path

from compute_recurrence import terms


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--last-n", type=int, default=20)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    values = terms(args.last_n)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="ascii") as handle:
        for n in range(1, args.last_n + 1):
            handle.write(f"{n} {values[n]}\n")


if __name__ == "__main__":
    main()
