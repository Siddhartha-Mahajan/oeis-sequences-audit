#!/usr/bin/env python3
"""Brute-force NPN orbit enumeration for Boolean functions with n <= 3."""

from __future__ import annotations

import argparse
import itertools


def domain_permutation(n: int, coordinate_permutation, input_mask: int) -> tuple[int, ...]:
    image = []
    for vertex in range(1 << n):
        transformed = 0
        for destination, source in enumerate(coordinate_permutation):
            bit = ((vertex >> source) & 1) ^ ((input_mask >> source) & 1)
            transformed |= bit << destination
        image.append(transformed)
    return tuple(image)


def transform_function(table: int, domain_action: tuple[int, ...], output_flip: int) -> int:
    transformed = 0
    for vertex, source in enumerate(domain_action):
        bit = ((table >> source) & 1) ^ output_flip
        transformed |= bit << vertex
    return transformed


def npn_orbit_count(n: int) -> int:
    if n > 3:
        raise ValueError("this deliberate brute-force check is restricted to n <= 3")
    actions = [
        domain_permutation(n, permutation, input_mask)
        for permutation in itertools.permutations(range(n))
        for input_mask in range(1 << n)
    ]
    unseen = set(range(1 << (1 << n)))
    count = 0
    while unseen:
        representative = next(iter(unseen))
        orbit = {
            transform_function(representative, action, output_flip)
            for action in actions
            for output_flip in (0, 1)
        }
        unseen.difference_update(orbit)
        count += 1
    return count


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=3)
    args = parser.parse_args()
    expected = {0: 1, 1: 2, 2: 4, 3: 14}
    for n in range(args.through + 1):
        value = npn_orbit_count(n)
        if value != expected[n]:
            raise AssertionError((n, value, expected[n]))
        print(f"n={n}: NPN orbits={value}; A000157(n)={value // 2 if n else 'not indexed'}")


if __name__ == "__main__":
    main()

