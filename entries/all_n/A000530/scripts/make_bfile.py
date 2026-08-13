#!/usr/bin/env python3
"""Write a standard OEIS b-file for A000530 from the proved formula."""

from __future__ import annotations

import argparse
from pathlib import Path

from formula import a


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--last-n", type=int, default=10000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="ascii") as handle:
        for n in range(1, args.last_n + 1):
            handle.write(f"{n} {a(n)}\n")


if __name__ == "__main__":
    main()
