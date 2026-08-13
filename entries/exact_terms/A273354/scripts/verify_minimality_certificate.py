#!/usr/bin/env python3
"""Independently verify the A273354(3) finite minimality certificate."""

from __future__ import annotations

import argparse
import json
from collections import Counter
from math import isqrt
from pathlib import Path


N0 = 11_177_126_654_841_000_000
ROOT = 3_343_221_000
CUBE_PAIRS = [(279_300, 2_234_400), (790_020, 2_202_480), (1_256_850, 2_094_750)]


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        if a % n == 0:
            continue
        x = pow(a, d, n)
        if x in (1, n - 1):
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True


def parse_bfile(path: Path) -> list[int]:
    values = []
    for line in path.read_text(encoding="utf-8").splitlines():
        fields = line.split()
        if len(fields) == 2 and fields[0].isdigit():
            values.append(int(fields[1]))
    assert values == sorted(values) and len(values) == len(set(values))
    return values


def parse_factors(text: str) -> dict[int, int]:
    result = {}
    for item in text.split(","):
        p, e = map(int, item.split("^"))
        assert p not in result and e > 0 and is_prime(p)
        result[p] = e
    return result


def square_pair_count(n: int, factors: dict[int, int]) -> int:
    rebuilt = 1
    product = 1
    forbidden = False
    for p, e in factors.items():
        rebuilt *= p**e
        if p % 4 == 3 and e % 2:
            forbidden = True
        if p % 4 == 1:
            product *= e + 1
    assert rebuilt == n
    if forbidden:
        return 0
    square = isqrt(n) ** 2 == n
    twice_square = n % 2 == 0 and isqrt(n // 2) ** 2 == n // 2
    return (product - square + twice_square) // 2


def direct_cube_pairs(n: int) -> list[tuple[int, int]]:
    # This is used only for N0; integer binary search avoids floating point.
    def icbrt(m: int) -> int:
        lo, hi = 0, 1
        while hi**3 <= m:
            hi *= 2
        while lo + 1 < hi:
            mid = (lo + hi) // 2
            if mid**3 <= m:
                lo = mid
            else:
                hi = mid
        return lo

    result = []
    for x in range(1, icbrt(n // 2) + 1):
        y = icbrt(n - x**3)
        if y >= x and x**3 + y**3 == n:
            result.append((x, y))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    root = Path(__file__).parents[1]
    parser.add_argument("--primitive", type=Path, default=root / "sources" / "A003825_bfile.txt")
    parser.add_argument("--all", type=Path, default=root / "sources" / "A018787_bfile.txt")
    parser.add_argument("--summary", type=Path, default=root / "certificates" / "below_candidate.json")
    parser.add_argument("--factors", type=Path, default=root / "certificates" / "below_candidate.json.factors.tsv")
    args = parser.parse_args()

    primitive_all = parse_bfile(args.primitive)
    assert primitive_all[-1] > N0
    primitive = [m for m in primitive_all if m < N0]
    expected = set()
    for m in primitive:
        k = 1
        while m * k**3 < N0:
            expected.add(m * k**3)
            k += 1
    expected = sorted(expected)

    certified = []
    histogram = Counter()
    for line in args.factors.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        n_text, factors_text, count_text = line.split("\t")
        n, reported = int(n_text), int(count_text)
        factors = parse_factors(factors_text)
        actual = square_pair_count(n, factors)
        assert actual == reported
        certified.append(n)
        histogram[actual] += 1
    assert certified == expected
    assert histogram[3] == 0

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    assert summary["exclusive_limit"] == N0
    assert summary["primitive_bases_below_limit"] == len(primitive) == 6177
    assert summary["distinct_primitive_cube_scalings"] == len(expected) == 110969
    assert summary["square_multiplicity_three_candidates"] == []
    assert summary["solutions_below_limit"] == []

    # Independent 100000-term decomposition audit.
    all_values = parse_bfile(args.all)
    endpoint = all_values[99_999]
    generated = set()
    for m in primitive_all:
        if m > endpoint:
            break
        k = 1
        while m * k**3 <= endpoint:
            generated.add(m * k**3)
            k += 1
    assert sorted(generated) == all_values[:100_000]

    candidate_factors = {2: 6, 3: 6, 5: 6, 7: 6, 19: 4}
    assert ROOT**2 == N0
    assert square_pair_count(N0, candidate_factors) == 3
    assert direct_cube_pairs(N0) == CUBE_PAIRS
    print(
        "verified 110969 smaller primitive cubic scalings, the independent "
        "100000-term A018787 decomposition, and exactly three square and cube "
        "representations for the candidate"
    )


if __name__ == "__main__":
    main()
