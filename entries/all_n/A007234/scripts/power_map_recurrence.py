#!/usr/bin/env python3
"""Exact conjugacy-type recurrence for power-map-free subsets of S_n.

For fixed d>=2, compute the maximum size of X subset S_n such that
sigma in X implies sigma**d not in X.  The d=2 specialization is A007234.
"""

from __future__ import annotations

import argparse
import math
from collections import defaultdict
from typing import Iterable

Type = tuple[int, ...]


def partitions(n: int, largest: int | None = None) -> Iterable[tuple[int, ...]]:
    if n == 0:
        yield ()
        return
    if largest is None or largest > n:
        largest = n
    for first in range(largest, 0, -1):
        for rest in partitions(n - first, first):
            yield (first,) + rest


def to_type(parts: tuple[int, ...], n: int) -> Type:
    counts = [0] * n
    for j in parts:
        counts[j - 1] += 1
    return tuple(counts)


def power_type(mu: Type, d: int) -> Type:
    n = len(mu)
    out = [0] * n
    for j, count in enumerate(mu, 1):
        if not count:
            continue
        g = math.gcd(j, d)
        out[j // g - 1] += g * count
    return tuple(out)


def centralizer_size(lam: Type) -> int:
    result = 1
    for j, count in enumerate(lam, 1):
        result *= j**count * math.factorial(count)
    return result


def prime_divisors(d: int) -> tuple[int, ...]:
    result: list[int] = []
    p = 2
    while p * p <= d:
        if d % p == 0:
            result.append(p)
            while d % p == 0:
                d //= p
        p = 3 if p == 2 else p + 2
    if d > 1:
        result.append(d)
    return tuple(result)


def valuation(j: int, p: int) -> int:
    result = 0
    while j % p == 0:
        result += 1
        j //= p
    return result


def height(lam: Type, primes: tuple[int, ...]) -> int:
    total = 0
    for p in primes:
        maximum = 0
        for j, count in enumerate(lam, 1):
            if count:
                maximum = max(maximum, valuation(j, p))
        total += maximum
    return total


def permutation_order(lam: Type) -> int:
    result = 1
    for j, count in enumerate(lam, 1):
        if count:
            result = math.lcm(result, j)
    return result


def multiplicative_order(a: int, modulus: int) -> int:
    if modulus == 1:
        return 1
    if math.gcd(a, modulus) != 1:
        raise ValueError("base and modulus must be coprime")
    value = a % modulus
    result = 1
    while value != 1:
        value = (value * a) % modulus
        result += 1
    return result


def compute(n: int, d: int) -> int:
    if n < 1:
        raise ValueError("n must be positive")
    if d < 2:
        raise ValueError("d must be at least 2")

    types = [to_type(parts, n) for parts in partitions(n)]
    z = {lam: centralizer_size(lam) for lam in types}
    parent = {lam: power_type(lam, d) for lam in types}
    children: dict[Type, list[Type]] = defaultdict(list)
    for mu in types:
        children[parent[mu]].append(mu)

    primes = prime_divisors(d)
    h = {lam: height(lam, primes) for lam in types}
    excluded: dict[Type, int] = {}
    included: dict[Type, int] = {}

    nonperiodic = [lam for lam in types if h[lam] > 0]
    nonperiodic.sort(key=h.__getitem__, reverse=True)
    for lam in nonperiodic:
        ex = 0
        inc = 1
        for mu in children[lam]:
            if mu == lam:
                raise AssertionError("nonperiodic type cannot be fixed")
            if h[mu] <= h[lam] or mu not in excluded:
                raise AssertionError("height is not reverse-topological")
            if z[lam] % z[mu]:
                raise AssertionError("nonintegral root fiber")
            multiplicity = z[lam] // z[mu]
            ex += multiplicity * max(excluded[mu], included[mu])
            inc += multiplicity * excluded[mu]
        excluded[lam], included[lam] = ex, inc

    factorial = math.factorial(n)
    answer = 0
    periodic = [lam for lam in types if h[lam] == 0]
    for lam in periodic:
        ex = 0
        inc = 1
        same_type_predecessors = 0
        for mu in children[lam]:
            if mu == lam:
                same_type_predecessors += 1
                continue
            if mu not in excluded:
                raise AssertionError("missing attached reverse-tree state")
            if z[lam] % z[mu]:
                raise AssertionError("nonintegral root fiber")
            multiplicity = z[lam] // z[mu]
            ex += multiplicity * max(excluded[mu], included[mu])
            inc += multiplicity * excluded[mu]
        if same_type_predecessors != 1:
            raise AssertionError("periodic type must have one same-type predecessor")
        excluded[lam], included[lam] = ex, inc

        order = permutation_order(lam)
        cycle_length = multiplicative_order(d, order)
        class_size = factorial // z[lam]
        if class_size % cycle_length:
            raise AssertionError("class does not split into equal power-map cycles")
        cycle_count = class_size // cycle_length
        gain = max(0, inc - ex)
        per_component = cycle_length * ex
        if cycle_length > 1:
            per_component += (cycle_length // 2) * gain
        answer += cycle_count * per_component

    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, nargs="?")
    parser.add_argument("--d", type=int, default=2)
    parser.add_argument("--through", type=int)
    args = parser.parse_args()
    if (args.n is None) == (args.through is None):
        parser.error("give exactly one of n or --through")
    if args.through is not None:
        for n in range(1, args.through + 1):
            print(n, compute(n, args.d))
    else:
        print(f"maximum({args.n}, d={args.d})={compute(args.n, args.d)}")


if __name__ == "__main__":
    main()
