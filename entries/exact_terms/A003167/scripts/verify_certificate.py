#!/usr/bin/env python3
"""Standalone structural and arithmetic checker for the A003167(7) certificate."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path


def legal_next(prefix: tuple[int, ...], remaining: int) -> tuple[int, int]:
    value = Fraction(1, 2) - sum((Fraction(1, x) for x in prefix), Fraction())
    return (
        max(prefix[-1], value.denominator // value.numerator + 1),
        remaining * value.denominator // value.numerator,
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    args = parser.parse_args()
    record = json.loads(args.certificate.read_text(encoding="utf-8"))
    assert record["sequence"] == "A003167" and record["n"] == 7
    branches = record["branches"]
    assert len(branches) == record["branch_count"] == 262
    assert len({branch["branch"] for branch in branches}) == 262

    ordinary: set[tuple[int, ...]] = set()
    ranges: list[tuple[int, int]] = []
    total = 0
    for branch in branches:
        arguments = branch["arguments"]
        assert arguments[0] == 7
        total += branch["count"]
        assert branch["count"] >= 0
        assert branch["search_nodes"] >= branch["pair_calls"] >= 0
        if "--next-range" in arguments:
            marker = arguments.index("--next-range")
            assert tuple(arguments[1:marker]) == (3, 7, 43)
            ranges.append(tuple(arguments[marker + 1 : marker + 3]))
        else:
            ordinary.add(tuple(arguments[1:]))

    assert {(x,) for x in range(4, 15)} <= ordinary
    assert {(3, y) for y in range(8, 37)} <= ordinary
    assert {(3, 7, z) for z in range(44, 211)} <= ordinary
    assert len(ordinary) == 11 + 29 + 167
    assert legal_next((3,), 6) == (7, 36)
    assert legal_next((3, 7), 5) == (43, 210)
    assert legal_next((3, 7, 43), 4) == (1807, 7224)
    ranges.sort()
    assert ranges[0][0] == 1807 and ranges[-1][1] == 7224
    assert all(left[1] + 1 == right[0] for left, right in zip(ranges, ranges[1:]))
    assert total == record["a_n"] == 155068098
    print(
        "verified A003167(7)=155068098 from 262 disjoint exhaustive branches"
    )


if __name__ == "__main__":
    main()
