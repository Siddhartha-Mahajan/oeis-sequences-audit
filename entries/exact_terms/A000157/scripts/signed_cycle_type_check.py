#!/usr/bin/env python3
"""Independent Burnside check using conjugacy classes of signed permutations.

The hyperoctahedral group C_2 wr S_n acts on the vertices of the n-cube.
Its conjugacy classes are indexed by a pair of partitions: lengths of positive
and negative signed cycles.  For each class this program explicitly constructs
one representative permutation of all 2^n cube vertices, measures its orbit
lengths, and applies Burnside's lemma.  This route is deliberately different
from ``burnside_a000157.py``.
"""

from __future__ import annotations

import argparse
import collections
import functools
import hashlib
import math
import sys
from pathlib import Path


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


@functools.cache
def partitions(n: int, maximum: int | None = None) -> tuple[tuple[int, ...], ...]:
    if n == 0:
        return ((),)
    if maximum is None or maximum > n:
        maximum = n
    result = []
    for first in range(maximum, 0, -1):
        for rest in partitions(n - first, first):
            result.append((first,) + rest)
    return tuple(result)


def z(partition: tuple[int, ...]) -> int:
    counts = collections.Counter(partition)
    result = 1
    for length, multiplicity in counts.items():
        result *= length**multiplicity * math.factorial(multiplicity)
    return result


def class_size(n: int, positive: tuple[int, ...], negative: tuple[int, ...]) -> int:
    centralizer = (
        (1 << (len(positive) + len(negative))) * z(positive) * z(negative)
    )
    return (1 << n) * math.factorial(n) // centralizer


def coordinate_map(
    positive: tuple[int, ...], negative: tuple[int, ...]
) -> tuple[tuple[int, bool], ...]:
    """Return (source coordinate, toggle) for each output coordinate."""
    result: list[tuple[int, bool] | None] = [None] * (sum(positive) + sum(negative))
    start = 0
    for is_negative, parts in ((False, positive), (True, negative)):
        for length in parts:
            coordinates = tuple(range(start, start + length))
            for i, source in enumerate(coordinates):
                destination = coordinates[(i + 1) % length]
                result[destination] = (source, is_negative and destination == coordinates[0])
            start += length
    assert all(item is not None for item in result)
    return tuple(item for item in result if item is not None)


def transform(vertex: int, mapping: tuple[tuple[int, bool], ...]) -> int:
    image = 0
    for destination, (source, toggle) in enumerate(mapping):
        bit = ((vertex >> source) & 1) ^ toggle
        image |= bit << destination
    return image


def compose(
    outer: tuple[tuple[int, bool], ...],
    inner: tuple[tuple[int, bool], ...],
) -> tuple[tuple[int, bool], ...]:
    """Return the affine coordinate map outer(inner(x))."""
    return tuple(
        (inner[source][0], toggle ^ inner[source][1])
        for source, toggle in outer
    )


def mapping_power(
    mapping: tuple[tuple[int, bool], ...], exponent: int
) -> tuple[tuple[int, bool], ...]:
    result = tuple((i, False) for i in range(len(mapping)))
    base = mapping
    while exponent:
        if exponent & 1:
            result = compose(base, result)
        base = compose(base, base)
        exponent >>= 1
    return result


def fixed_vertices(mapping: tuple[tuple[int, bool], ...]) -> int:
    """Number of x satisfying mapping(x)=x, from coordinate cycles."""
    seen = bytearray(len(mapping))
    cycles = 0
    for start in range(len(mapping)):
        if seen[start]:
            continue
        cycles += 1
        parity = False
        coordinate = start
        while not seen[coordinate]:
            seen[coordinate] = 1
            source, toggle = mapping[coordinate]
            parity ^= toggle
            coordinate = source
        if parity:
            return 0
    return 1 << cycles


def totient(n: int) -> int:
    result = n
    p = 2
    while p * p <= n:
        if n % p == 0:
            result -= result // p
            while n % p == 0:
                n //= p
        p += 1 if p == 2 else 2
    if n > 1:
        result -= result // n
    return result


def divisors(n: int) -> tuple[int, ...]:
    small = []
    large = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d * d != n:
                large.append(n // d)
        d += 1
    return tuple(small + large[::-1])


def mobius(n: int) -> int:
    result = 1
    p = 2
    while p * p <= n:
        if n % p == 0:
            n //= p
            result = -result
            if n % p == 0:
                return 0
            while n % p == 0:
                n //= p
        p += 1 if p == 2 else 2
    return -result if n > 1 else result


def cube_orbit_profile(
    positive: tuple[int, ...], negative: tuple[int, ...]
) -> tuple[int, bool]:
    """Return number of cube-vertex orbits and whether all have even size.

    Burnside over the cyclic group generated by the signed permutation uses
    fixed vertices of its divisor-indexed powers.  Moebius inversion detects
    whether any vertex has odd orbit size.
    """
    mapping = coordinate_map(positive, negative)
    order = math.lcm(
        *(positive or (1,)),
        *(tuple(2 * length for length in negative) or (1,)),
    )
    power_fixed = {
        d: fixed_vertices(mapping_power(mapping, d)) for d in divisors(order)
    }
    orbit_numerator = sum(
        totient(order // d) * fixed for d, fixed in power_fixed.items()
    )
    orbit_count, remainder = divmod(orbit_numerator, order)
    if remainder:
        raise ArithmeticError("cyclic Burnside average was not integral")
    all_even = True
    for length in divisors(order):
        if length & 1:
            exact_points = sum(
                mobius(length // d) * power_fixed[d] for d in divisors(length)
            )
            if exact_points:
                all_even = False
                break
    return orbit_count, all_even


def counts(n: int) -> tuple[int, int, int, int]:
    order = (1 << n) * math.factorial(n)
    np_numerator = 0
    self_complementary_numerator = 0
    types = 0
    total_elements = 0
    for positive_sum in range(n + 1):
        for positive in partitions(positive_sum):
            for negative in partitions(n - positive_sum):
                types += 1
                multiplicity = class_size(n, positive, negative)
                total_elements += multiplicity
                orbit_count, all_even = cube_orbit_profile(positive, negative)
                fixed_colorings = 1 << orbit_count
                np_numerator += multiplicity * fixed_colorings
                if all_even:
                    self_complementary_numerator += multiplicity * fixed_colorings
    if total_elements != order:
        raise AssertionError((total_elements, order))
    np_count, np_remainder = divmod(np_numerator, order)
    sc_count, sc_remainder = divmod(self_complementary_numerator, order)
    if np_remainder or sc_remainder:
        raise ArithmeticError("nonintegral Burnside average")
    npn_count, parity = divmod(np_count + sc_count, 2)
    if parity:
        raise ArithmeticError("nonintegral NPN orbit count")
    a157, parity = divmod(npn_count, 2)
    if parity:
        raise ArithmeticError("odd A000370 value")
    return types, np_count, sc_count, a157


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("--value-output", type=Path)
    parser.add_argument("--summary-only", action="store_true")
    args = parser.parse_args()
    types, np_count, sc_count, value = counts(args.n)
    decimal = str(value)
    print(f"n={args.n}")
    print(f"signed_cycle_types={types}")
    if not args.summary_only:
        print(f"A000616={np_count}")
        print(f"A000610={sc_count}")
    print(f"A000157_digits={len(decimal)}")
    print(f"A000157_sha256={hashlib.sha256(decimal.encode()).hexdigest()}")
    if not args.summary_only:
        print(f"A000157={decimal}")
    if args.value_output:
        args.value_output.write_text(f"{args.n} {decimal}\n")


if __name__ == "__main__":
    main()
