#!/usr/bin/env python3
"""Exact all-n generating function for stable unlabeled unicyclic graphs.

McAvaney's theorem says that a cactus is stable iff it has a transposition
automorphism.  This script counts unicyclic graphs with such a transposition
by subtracting the transposition-free cycle-decorated rooted trees.

All coefficients are computed with Fraction arithmetic.  No graph generator
or automorphism package is used.
"""

import argparse
from fractions import Fraction
from math import gcd


def add(a, b, n):
    return [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0)
            for i in range(n + 1)]


def scale(a, c, n):
    return [(a[i] if i < len(a) else 0) * c for i in range(n + 1)]


def mul(a, b, n):
    result = [Fraction(0) for _ in range(n + 1)]
    for i, ai in enumerate(a[:n + 1]):
        if not ai:
            continue
        for j, bj in enumerate(b[:n + 1 - i]):
            if bj:
                result[i + j] += ai * bj
    return result


def power(a, exponent, n):
    result = [Fraction(1)] + [Fraction(0)] * n
    base = a
    while exponent:
        if exponent & 1:
            result = mul(result, base, n)
        exponent >>= 1
        if exponent:
            base = mul(base, base, n)
    return result


def substitute_power(a, k, n):
    result = [Fraction(0) for _ in range(n + 1)]
    for i in range(min(len(a), n // k + 1)):
        result[i * k] = a[i]
    return result


def exp_series(a, n):
    """Formal exp(a), assuming a[0] == 0."""
    result = [Fraction(0) for _ in range(n + 1)]
    result[0] = 1
    for m in range(1, n + 1):
        result[m] = sum(Fraction(k) * a[k] * result[m - k]
                        for k in range(1, m + 1)) / m
    return result


def rooted_series(n, forbid_repeated_leaves=False):
    """Rooted unlabeled trees, optionally with at most one leaf child/node."""
    f = [Fraction(0) for _ in range(n + 1)]
    for _ in range(n + 1):
        exponent = [Fraction(0) for _ in range(n + 1)]
        for k in range(1, n + 1):
            fk = substitute_power(f, k, n)
            exponent = add(exponent, scale(fk, Fraction(1, k), n), n)
        rhs = exp_series(exponent, n)
        shifted = [Fraction(0)] + rhs[:n]
        if forbid_repeated_leaves:
            # Replace the arbitrary multiset of leaf children, 1/(1-x), by
            # a leaf multiplicity of zero or one, 1+x: multiply by 1-x^2.
            for degree in range(3, n + 1):
                shifted[degree] -= rhs[degree - 3]
        f = shifted
    return f


def phi(n):
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def divisors(n):
    return [d for d in range(1, n + 1) if n % d == 0]


def unoriented_cycles(f, n):
    """Cycles of length >=3 decorated by objects with OGF f."""
    result = [Fraction(0) for _ in range(n + 1)]
    f2 = substitute_power(f, 2, n)
    for k in range(3, n + 1):
        rotation = [Fraction(0) for _ in range(n + 1)]
        for d in divisors(k):
            term = power(substitute_power(f, d, n), k // d, n)
            rotation = add(rotation, scale(term, phi(d), n), n)
        if k % 2:
            reflection = mul(f, power(f2, (k - 1) // 2, n), n)
            reflection = scale(reflection, k, n)
        else:
            fixed_two = mul(power(f, 2, n), power(f2, (k - 2) // 2, n), n)
            fixed_none = power(f2, k // 2, n)
            reflection = scale(add(fixed_two, fixed_none, n), Fraction(k, 2), n)
        result = add(result, scale(add(rotation, reflection, n), Fraction(1, 2 * k), n), n)
    return result


def stable_series(n):
    rooted = rooted_series(n)
    no_leaf_twins = rooted_series(n, forbid_repeated_leaves=True)
    all_unicyclic = unoriented_cycles(rooted, n)
    twin_free = unoriented_cycles(no_leaf_twins, n)

    # In a 3-cycle, any two bare cycle vertices form a transposition; their
    # orbit contribution is x^2 B(x).  In a 4-cycle, two opposite bare cycle
    # vertices form a transposition; the other opposite pair is an unordered
    # pair of B-objects.
    bad_three = [Fraction(0), Fraction(0)] + no_leaf_twins[:n - 1]
    bad_three = bad_three[:n + 1]
    b2 = mul(no_leaf_twins, no_leaf_twins, n)
    bx2 = substitute_power(no_leaf_twins, 2, n)
    unordered_pair = scale(add(b2, bx2, n), Fraction(1, 2), n)
    bad_four = [Fraction(0), Fraction(0)] + unordered_pair[:n - 1]
    bad_four = bad_four[:n + 1]
    stable = add(add(all_unicyclic, scale(twin_free, -1, n), n),
                 add(bad_three, bad_four, n), n)
    return rooted, no_leaf_twins, all_unicyclic, stable


def integer_coefficients(series):
    if any(value.denominator != 1 for value in series):
        raise AssertionError("nonintegral coefficient")
    return [int(value) for value in series]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=30)
    parser.add_argument("--bfile")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rooted, restricted, all_unicyclic, stable = stable_series(args.max_n)
    rooted = integer_coefficients(rooted)
    restricted = integer_coefficients(restricted)
    all_unicyclic = integer_coefficients(all_unicyclic)
    stable = integer_coefficients(stable)
    if args.check:
        expected_rooted = [1, 1, 2, 4, 9, 20, 48, 115, 286, 719]
        expected_unicyclic = [1, 2, 5, 13, 33, 89, 240, 657, 1806, 5026]
        expected_stable = [1, 2, 3, 8, 22, 62, 176, 500, 1425, 4078]
        assert rooted[1:11] == expected_rooted
        assert all_unicyclic[3:13] == expected_unicyclic
        assert stable[3:13] == expected_stable
        print("all exact checkpoints passed")
    if args.bfile:
        with open(args.bfile, "w", encoding="ascii") as output:
            for index in range(3, args.max_n + 1):
                output.write(f"{index} {stable[index]}\n")
    print("rooted:", ", ".join(map(str, rooted[1:])))
    print("leaf-twin-free rooted:", ", ".join(map(str, restricted[1:])))
    print("all unicyclic:", ", ".join(map(str, all_unicyclic[3:])))
    print("stable unicyclic:", ", ".join(map(str, stable[3:])))


if __name__ == "__main__":
    main()
