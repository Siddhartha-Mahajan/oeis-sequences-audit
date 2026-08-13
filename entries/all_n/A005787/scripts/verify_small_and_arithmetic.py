#!/usr/bin/env python3
"""Independent small-n recurrence check and n=6 inclusion-exclusion audit."""

from __future__ import annotations

import argparse
from math import comb
from pathlib import Path


def affine(d: int) -> set[int]:
    values = set()
    for mask in range(1 << d):
        for constant in (0, 1):
            truth = 0
            for x in range(1 << d):
                if ((mask & x).bit_count() & 1) ^ constant:
                    truth |= 1 << x
            values.add(truth)
    return values


def combine(d: int, coordinate: int, zero: int, one: int) -> int:
    truth = 0
    for y in range(1 << d):
        low = y & ((1 << coordinate) - 1)
        high = y >> coordinate
        x0 = low | (high << (coordinate + 1))
        if (zero >> y) & 1:
            truth |= 1 << x0
        if (one >> y) & 1:
            truth |= 1 << (x0 | (1 << coordinate))
    return truth


def small_families(max_n: int = 4) -> list[set[int]]:
    families = [{0}]
    for n in range(1, max_n + 1):
        nxt = {
            combine(n - 1, coordinate, zero, one)
            for coordinate in range(n)
            for zero in families[-1]
            for one in affine(n - 1)
        }
        families.append(nxt)
    return families


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--result", type=Path)
    args = parser.parse_args()
    sizes = [len(family) for family in small_families()]
    assert sizes == [1, 2, 8, 112, 5856], sizes

    result = args.result or (Path(__file__).parents[1] / "certificates" / "count_n1_n6_exact_intersections.txt")
    fields: dict[int, int] = {}
    reported = None
    for line in result.read_text(encoding="utf-8").splitlines():
        if line.startswith("I(6,"):
            left, right = line.split("=")
            fields[int(left[4:-1])] = int(right)
        elif line.startswith("a(6)="):
            reported = int(line.split("=")[1])
    assert set(fields) == set(range(1, 7))
    total = sum((-1) ** (k + 1) * comb(6, k) * fields[k] for k in range(1, 7))
    assert total == reported == 323041664
    print("verified recurrence through n=4 and n=6 inclusion-exclusion arithmetic")


if __name__ == "__main__":
    main()
