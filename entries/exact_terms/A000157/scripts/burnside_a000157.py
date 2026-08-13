#!/usr/bin/env python3
"""Exact Burnside evaluator for A000157 and its related sequences.

This is a dependency-free transcription and clarification of Gregory Morse's
Python program on A000370.  It uses integer arithmetic throughout.
"""

from __future__ import annotations

import argparse
import functools
import hashlib
import math
import operator
import sys
from pathlib import Path


if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(0)


def mobius(n: int) -> int:
    """Return the Moebius function of a positive integer n."""
    if n < 1:
        raise ValueError("mobius expects n >= 1")
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
    if n > 1:
        result = -result
    return result


def divisors(n: int) -> tuple[int, ...]:
    small: list[int] = []
    large: list[int] = []
    d = 1
    while d * d <= n:
        if n % d == 0:
            small.append(d)
            if d * d != n:
                large.append(n // d)
        d += 1
    return tuple(small + large[::-1])


def partition_lin(n: int, d: int, depth: int = 0):
    """Yield multiplicity vectors for integer partitions, as in A000370."""
    if d == depth:
        if n == 0:
            yield ()
    else:
        for i in range(n + 1):
            for item in partition_lin(n - i * (depth + 1), d, depth + 1):
                yield item + (i,)


@functools.cache
def e(k: int) -> int:
    return sum((1 << d) * mobius(k // d) for d in divisors(k)) // k


@functools.cache
def g(two_k: int) -> int:
    return sum(
        (1 << (d // 2)) * mobius(two_k // d)
        for d in divisors(two_k)
        if (two_k // 2) % d != 0
    ) // two_k


def _combine_cycle_profiles(left, right):
    return [
        [
            (math.lcm(p, q), math.gcd(p, q) * ip * jq)
            for p, ip in a
            for q, jq in b
        ]
        for a in left
        for b in right
    ]


def np_or_self_complementary_count(n: int, self_complementary: bool = False) -> int:
    """A000616(n) if false; A000610(n) if true."""
    numerator = 0
    group_order = math.factorial(n) * (1 << n)
    for part in partition_lin(n, n):
        class_multiplier = group_order // functools.reduce(
            operator.mul,
            (
                math.factorial(multiplicity) * (2 * (n - i)) ** multiplicity
                for i, multiplicity in enumerate(part)
            ),
            1,
        )
        if n == 0:
            profiles = [[(1, 1)]]
        else:
            factors = []
            for i in range(1, n + 1):
                for _ in range(part[n - i]):
                    factors.append(
                        [
                            [(d, e(d)) for d in divisors(i)],
                            [(d, g(d)) for d in divisors(2 * i) if i % d != 0],
                        ]
                    )
            profiles = functools.reduce(_combine_cycle_profiles, factors)
        fixed_sum = 0
        for profile in profiles:
            factors = []
            for cycle_length, cycle_count in profile:
                if self_complementary and cycle_length & 1:
                    factors.append(0)
                else:
                    factors.append(1 << cycle_count)
            fixed_sum += functools.reduce(operator.mul, factors, 1)
        numerator += class_multiplier * fixed_sum
    quotient, remainder = divmod(numerator, group_order)
    if remainder:
        raise ArithmeticError("Burnside average was not integral")
    return quotient


def a000370(n: int) -> int:
    np_count = np_or_self_complementary_count(n, False)
    sc_count = np_or_self_complementary_count(n, True)
    total, remainder = divmod(np_count + sc_count, 2)
    if remainder:
        raise ArithmeticError("NPN count was not integral")
    return total


def a000157(n: int) -> int:
    total, remainder = divmod(a000370(n), 2)
    if remainder:
        raise ArithmeticError("A000370(n)/2 was not integral")
    return total


def load_bfile(path: Path) -> dict[int, int]:
    result = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            index, value = line.split()
            result[int(index)] = int(value)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--through", type=int, default=8)
    parser.add_argument("--verify-bfile", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    expected = load_bfile(args.verify_bfile) if args.verify_bfile else {}
    lines = []
    for n in range(1, args.through + 1):
        value = a000157(n)
        if n in expected and expected[n] != value:
            raise AssertionError(f"n={n}: expected {expected[n]}, got {value}")
        decimal = str(value)
        digest = hashlib.sha256(decimal.encode()).hexdigest()
        status = " verified" if n in expected else ""
        print(f"n={n} digits={len(decimal)} sha256={digest}{status}", flush=True)
        lines.append(f"{n} {decimal}\n")
    if args.output:
        args.output.write_text("".join(lines))


if __name__ == "__main__":
    main()
