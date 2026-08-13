#!/usr/bin/env python3
"""Compute A005787 from the proved intersection recurrence."""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path


def terms(last_n: int) -> list[int]:
    a = [1]
    for n in range(1, last_n + 1):
        value = n * (1 << n) * a[n - 1]
        value += (1 << (n + 1)) * sum(
            (-1) ** (k + 1) * comb(n, k) * a[n - k]
            for k in range(2, n + 1)
        )
        a.append(value)
    return a


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--last-n", type=int, default=20)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    values = terms(args.last_n)
    payload = {
        "sequence": "A005787",
        "a0_auxiliary": values[0],
        "terms": {str(n): values[n] for n in range(1, len(values))},
        "recurrence": (
            "a(n)=n*2^n*a(n-1)+2^(n+1)*Sum_{k=2..n}"
            "(-1)^(k+1)*C(n,k)*a(n-k), a(0)=1"
        ),
    }
    rendered = json.dumps(payload, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
