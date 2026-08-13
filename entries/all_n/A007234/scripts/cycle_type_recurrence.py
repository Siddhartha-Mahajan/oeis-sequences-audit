#!/usr/bin/env python3
"""Exact partition recurrence for A007234.

The algorithm uses p(n) conjugacy types, rather than n! permutations.  See
THEOREM.md for the derivation.
"""

from __future__ import annotations

import argparse
import math
import csv
from collections import defaultdict
from functools import reduce


Type = tuple[int, ...]  # m_j at position j-1


def partitions(n: int, largest: int | None = None):
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


def square_type(mu: Type) -> Type:
    n = len(mu)
    out = [0] * n
    for j, count in enumerate(mu, 1):
        if j % 2:
            out[j - 1] += count
        else:
            out[j // 2 - 1] += 2 * count
    return tuple(out)


def centralizer_size(lam: Type) -> int:
    z = 1
    for j, count in enumerate(lam, 1):
        z *= j**count * math.factorial(count)
    return z


def max_two_adic_valuation(lam: Type) -> int:
    result = 0
    for j, count in enumerate(lam, 1):
        if count:
            result = max(result, (j & -j).bit_length() - 1)
    return result


def permutation_order(lam: Type) -> int:
    order = 1
    for j, count in enumerate(lam, 1):
        if count:
            order = math.lcm(order, j)
    return order


def order_of_two(modulus: int) -> int:
    if modulus == 1:
        return 1
    if modulus % 2 == 0:
        raise ValueError("modulus must be odd")
    x = 2 % modulus
    length = 1
    while x != 1:
        x = (2 * x) % modulus
        length += 1
    return length


def format_type(lam: Type) -> str:
    pieces = []
    for j, count in enumerate(lam, 1):
        if count:
            pieces.append(str(j) if count == 1 else f"{j}^{count}")
    return " ".join(pieces)


def compute(n: int, verbose: bool = False) -> tuple[int, list[dict[str, int | str]]]:
    types = [to_type(parts, n) for parts in partitions(n)]
    z = {lam: centralizer_size(lam) for lam in types}
    parent = {lam: square_type(lam) for lam in types}
    children: dict[Type, list[Type]] = defaultdict(list)
    for mu in types:
        children[parent[mu]].append(mu)

    excluded: dict[Type, int] = {}
    included: dict[Type, int] = {}

    # Strictly nonperiodic types.  Reverse children have larger maximum v_2.
    nonperiodic = [lam for lam in types if max_two_adic_valuation(lam) > 0]
    nonperiodic.sort(key=max_two_adic_valuation, reverse=True)
    for lam in nonperiodic:
        ex = 0
        inc = 1
        for mu in children[lam]:
            if mu == lam:
                raise AssertionError("nonperiodic type cannot be periodic")
            if mu not in excluded:
                raise AssertionError("type order is not reverse-topological")
            numerator = z[lam]
            denominator = z[mu]
            if numerator % denominator:
                raise AssertionError("nonintegral square-root fiber")
            multiplicity = numerator // denominator
            ex += multiplicity * max(excluded[mu], included[mu])
            inc += multiplicity * excluded[mu]
        excluded[lam], included[lam] = ex, inc

    factorial = math.factorial(n)
    answer = 0
    rows: list[dict[str, int | str]] = []
    periodic = [lam for lam in types if max_two_adic_valuation(lam) == 0]
    for lam in periodic:
        ex = 0
        inc = 1
        for mu in children[lam]:
            if mu == lam:
                # Squaring is a bijection on the odd-order conjugacy class;
                # this single predecessor belongs to the directed cycle.
                continue
            if mu not in excluded:
                raise AssertionError("missing attached-tree type")
            if z[lam] % z[mu]:
                raise AssertionError("nonintegral square-root fiber")
            multiplicity = z[lam] // z[mu]
            ex += multiplicity * max(excluded[mu], included[mu])
            inc += multiplicity * excluded[mu]
        excluded[lam], included[lam] = ex, inc

        cycle_length = order_of_two(permutation_order(lam))
        class_size = factorial // z[lam]
        if class_size % cycle_length:
            raise AssertionError("conjugacy class does not split into cycles")
        cycle_count = class_size // cycle_length
        gain = max(0, inc - ex)
        per_component = cycle_length * ex
        if cycle_length > 1:
            per_component += (cycle_length // 2) * gain
        contribution = cycle_count * per_component
        answer += contribution
        rows.append(
            {
                "type": format_type(lam),
                "z": z[lam],
                "class_size": class_size,
                "cycle_length": cycle_length,
                "cycle_count": cycle_count,
                "exclude": ex,
                "include": inc,
                "contribution": contribution,
            }
        )

    if verbose:
        for row in rows:
            print(" ".join(f"{k}={v}" for k, v in row.items()))
    return answer, rows


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int, nargs="?")
    parser.add_argument("--through", type=int)
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--certificate")
    parser.add_argument("--bfile")
    args = parser.parse_args()
    if (args.n is None) == (args.through is None):
        parser.error("give exactly one of n or --through")
    if args.through is not None:
        bfile_rows = []
        for n in range(1, args.through + 1):
            answer, _ = compute(n)
            print(f"{n} {answer}")
            bfile_rows.append((n, answer))
        if args.bfile:
            with open(args.bfile, "w", encoding="utf-8") as handle:
                handle.write("# A007234: maximum size of a squaring-free subset of S_n\n")
                for n, answer in bfile_rows:
                    handle.write(f"{n} {answer}\n")
    else:
        answer, rows = compute(args.n, args.verbose)
        print(f"a({args.n})={answer}")
        if args.certificate:
            with open(args.certificate, "w", newline="", encoding="utf-8") as handle:
                writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)


if __name__ == "__main__":
    main()
