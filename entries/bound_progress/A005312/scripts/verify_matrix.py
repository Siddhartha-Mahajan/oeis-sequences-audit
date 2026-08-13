#!/usr/bin/env python3
"""Exact rational verifier for an A005312 matrix emitted by search_n8."""

from __future__ import annotations

import argparse
from fractions import Fraction
from pathlib import Path


def inverse(matrix: list[list[int]]) -> list[list[Fraction]]:
    n = len(matrix)
    a = [[Fraction(x) for x in row] + [Fraction(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    for col in range(n):
        pivot = next((row for row in range(col, n) if a[row][col]), None)
        if pivot is None:
            raise ValueError("singular matrix")
        a[col], a[pivot] = a[pivot], a[col]
        divisor = a[col][col]
        a[col] = [x / divisor for x in a[col]]
        for row in range(n):
            if row != col and a[row][col]:
                factor = a[row][col]
                a[row] = [x - factor * y for x, y in zip(a[row], a[col])]
    return [row[n:] for row in a]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    lines = args.path.read_text(encoding="utf-8").splitlines()
    rows = [[int(c) for c in line.strip()] for line in lines if len(line.strip()) == 8 and set(line.strip()) <= {"0", "1"}]
    assert len(rows) == 8 and all(len(row) == 8 for row in rows)
    assert rows == [list(row) for row in zip(*rows)], "matrix is not symmetric"
    inv = inverse(rows)
    score = sum(x*x for row in inv for x in row)
    assert score == 2670, score
    print(f"verified symmetric nonsingular 0-1 matrix; objective={score}")


if __name__ == "__main__":
    main()
