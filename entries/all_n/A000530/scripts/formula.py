#!/usr/bin/env python3
"""All-n finite binomial-sum formula for A000530."""

from __future__ import annotations

import argparse
import json
from math import comb
from pathlib import Path


def binomial(n: int, k: int) -> int:
    return comb(n, k) if n >= k >= 0 else 0


def bounded_compositions(parts: int, maximum_part: int, total_bound: int) -> int:
    """Positive parts <= maximum_part with sum <= total_bound."""
    if parts == 0:
        return int(total_bound >= 0)
    if maximum_part <= 0:
        return 0
    return sum(
        (-1) ** j
        * binomial(parts, j)
        * binomial(total_bound - j * maximum_part, parts)
        for j in range(parts + 1)
    )


def q(n_bound: int, runs: int) -> int:
    """Positive run vectors x with sum(x)+max(x) <= n_bound."""
    if runs == 0:
        return 1
    return sum(
        bounded_compositions(runs, maximum, n_bound - maximum)
        - bounded_compositions(runs, maximum - 1, n_bound - maximum)
        for maximum in range(1, (n_bound - runs + 1) // 2 + 1)
    )


def a(n: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    bound = 2 * n - 1
    counts = [q(bound, runs) for runs in range(bound)]
    return (
        1
        + sum(value * value for value in counts[1:])
        + sum(counts[runs] * counts[runs + 1] for runs in range(bound - 1))
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=50)
    parser.add_argument("--compare", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    values = [{"n": n, "a_n": a(n)} for n in range(1, args.max_n + 1)]
    if args.compare:
        expected = json.loads(args.compare.read_text(encoding="utf-8"))
        expected_values = [row["a_n"] for row in expected[: args.max_n]]
        assert [row["a_n"] for row in values] == expected_values
    text = json.dumps(values, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
