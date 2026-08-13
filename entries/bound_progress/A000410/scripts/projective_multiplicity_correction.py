#!/usr/bin/env python3
"""Multiplicity correction for the A000410 projective union bound."""

import math


def stirling_tables(n):
    second = [[0] * (n + 1) for _ in range(n + 1)]
    first = [[0] * (n + 1) for _ in range(n + 1)]
    second[0][0] = first[0][0] = 1
    for i in range(1, n + 1):
        for k in range(1, i + 1):
            second[i][k] = second[i - 1][k - 1] + k * second[i - 1][k]
            first[i][k] = first[i - 1][k - 1] - (i - 1) * first[i - 1][k]
    return first, second


def column_class_counts(n):
    first, second = stirling_tables(n + 1)
    counts = []
    for k in range(n + 1):
        surjective = sum(
            first[k + 1][j] * math.comb(2 ** (j - 1) - 1, n)
            for j in range(1, k + 2)
        )
        counts.append(second[n + 1][k + 1] * surjective)
    assert sum(counts) == math.comb(2**n - 1, n)
    return counts


def correction(n, prime):
    counts = column_class_counts(n)
    return sum(
        (((prime ** (n - k) - 1) // (prime - 1)) - 1) * counts[k]
        for k in range(n - 1)
    )


if __name__ == "__main__":
    n, prime = 10, 7
    raw = 118121286496007494503870
    overlap = correction(n, prime)
    print(f"raw={raw}")
    print(f"forced_overcount={overlap}")
    print(f"corrected_upper={raw-overlap}")
