#!/usr/bin/env python3
"""Independent audits of the A007234 conjugacy-type recurrence."""

from __future__ import annotations

import argparse
import itertools
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cycle_type_recurrence import compute  # noqa: E402


PUBLISHED_PREFIX = [0, 1, 4, 16, 72, 522]
DIRECT_VALUES = {
    1: 0,
    2: 1,
    3: 4,
    4: 16,
    5: 72,
    6: 522,
    7: 3390,
    8: 29409,
    9: 267561,
    10: 2820600,
    11: 30658050,
}


def square(p: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[p[i]] for i in range(len(p)))


def cycle_type(p: tuple[int, ...]) -> tuple[int, ...]:
    seen = [False] * len(p)
    parts = []
    for start in range(len(p)):
        if seen[start]:
            continue
        v = start
        length = 0
        while not seen[v]:
            seen[v] = True
            length += 1
            v = p[v]
        parts.append(length)
    return tuple(sorted(parts, reverse=True))


def audit_fibers(n: int) -> None:
    perms = list(itertools.permutations(range(n)))
    fibers: dict[tuple[int, ...], Counter[tuple[int, ...]]] = defaultdict(Counter)
    targets: dict[tuple[int, ...], int] = {}
    for p in perms:
        target = square(p)
        fibers[target][cycle_type(p)] += 1
        targets[cycle_type(target)] = targets.get(cycle_type(target), 0) + 1

    by_target_type: dict[tuple[int, ...], Counter[tuple[int, ...]]] = {}
    for target, counts in fibers.items():
        target_type = cycle_type(target)
        if target_type in by_target_type:
            assert by_target_type[target_type] == counts
        else:
            by_target_type[target_type] = counts

    # Directly verify the z(lambda)/z(mu) formula for every nonzero fiber.
    def z(parts: tuple[int, ...]) -> int:
        c = Counter(parts)
        out = 1
        for j, multiplicity in c.items():
            out *= j**multiplicity * math.factorial(multiplicity)
        return out

    for lam, counts in by_target_type.items():
        for mu, count in counts.items():
            assert count == z(lam) // z(mu), (lam, mu, count, z(lam) // z(mu))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=25)
    args = parser.parse_args()
    values = [compute(n)[0] for n in range(1, args.through + 1)]
    assert values[: len(PUBLISHED_PREFIX)] == PUBLISHED_PREFIX
    for n, expected in DIRECT_VALUES.items():
        assert values[n - 1] == expected, (n, values[n - 1], expected)
    for n in range(1, min(8, args.through) + 1):
        assert 0 <= values[n - 1] <= math.factorial(n)
    audit_fibers(7)
    root = Path(__file__).resolve().parents[1]
    bfile = root / "certificates" / "sample_n1_n50.txt"
    recorded = []
    for line in bfile.read_text(encoding="utf-8").splitlines():
        if line and not line.startswith("#"):
            n, value = map(int, line.split())
            recorded.append((n, value))
    assert recorded == list(enumerate(values, 1)), "b-file differs from recurrence"
    print(f"partition recurrence checked through n={args.through}")
    print("direct permutation values checked through n=11")
    print("all square-root fibers and z(lambda)/z(mu) checked through n=7")
    print("b-file agrees byte-for-value with the recurrence")


if __name__ == "__main__":
    main()
