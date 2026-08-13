#!/usr/bin/env python3
"""Independent audits for the A005787 intersection theorem and recurrence."""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from math import comb
from pathlib import Path


PUBLISHED = [2, 8, 112, 5856, 869824]
ENUMERATED_A6 = 323041664
ENUMERATED_I6 = {1: 55668736, 2: 749568, 3: 14336, 4: 1024, 5: 256, 6: 128}


def affine(d: int) -> set[int]:
    result = set()
    for parameter in range(1 << (d + 1)):
        mask = parameter & ((1 << d) - 1)
        constant = (parameter >> d) & 1
        truth = 0
        for x in range(1 << d):
            if ((mask & x).bit_count() & 1) ^ constant:
                truth |= 1 << x
        result.add(truth)
    return result


def combine(n: int, coordinate: int, zero: int, one: int) -> int:
    truth = 0
    for y in range(1 << (n - 1)):
        low = y & ((1 << coordinate) - 1)
        high = y >> coordinate
        x0 = low | (high << (coordinate + 1))
        truth |= ((zero >> y) & 1) << x0
        truth |= ((one >> y) & 1) << (x0 | (1 << coordinate))
    return truth


def explicit_families(last_n: int = 4) -> tuple[list[set[int]], list[list[set[int]]]]:
    families = [{0}]
    all_e: list[list[set[int]]] = [[]]
    for n in range(1, last_n + 1):
        aff = affine(n - 1)
        e_sets = [
            {
                combine(n, coordinate, zero, one)
                for zero in families[n - 1]
                for one in aff
            }
            for coordinate in range(n)
        ]
        families.append(set().union(*e_sets))
        all_e.append(e_sets)
    return families, all_e


def recurrence(last_n: int) -> list[int]:
    a = [1]
    for n in range(1, last_n + 1):
        intersections = {
            1: (1 << n) * a[n - 1],
            **{k: (1 << (n + 1)) * a[n - k] for k in range(2, n + 1)},
        }
        a.append(sum(
            (-1) ** (k + 1) * comb(n, k) * intersections[k]
            for k in range(1, n + 1)
        ))
    return a


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--certificate",
        type=Path,
        default=Path(__file__).parents[1] / "certificates" / "recurrence_terms.json",
    )
    args = parser.parse_args()

    families, all_e = explicit_families()
    for n in range(1, 5):
        linear_forms = {truth for truth in affine(n) if (truth & 1) == 0}
        assert all(
            (f ^ linear) in families[n]
            for f in families[n]
            for linear in linear_forms
        )
        for k in range(1, n + 1):
            actual = {
                len(set.intersection(*(all_e[n][i] for i in chosen)))
                for chosen in combinations(range(n), k)
            }
            expected = (
                (1 << n) * len(families[n - 1])
                if k == 1
                else (1 << (n + 1)) * len(families[n - k])
            )
            assert actual == {expected}, (n, k, actual, expected)

    a = recurrence(20)
    assert a[1:6] == PUBLISHED
    assert a[6] == ENUMERATED_A6
    for k, actual in ENUMERATED_I6.items():
        expected = (1 << 6) * a[5] if k == 1 else (1 << 7) * a[6 - k]
        assert actual == expected, (k, actual, expected)

    payload = json.loads(args.certificate.read_text(encoding="utf-8"))
    certified = [payload["a0_auxiliary"]] + [
        payload["terms"][str(n)] for n in range(1, 21)
    ]
    assert certified == a
    print(
        "verified all intersections through n=4, the preserved n=6 table, "
        "all published terms, and recurrence values through n=20"
    )


if __name__ == "__main__":
    main()
