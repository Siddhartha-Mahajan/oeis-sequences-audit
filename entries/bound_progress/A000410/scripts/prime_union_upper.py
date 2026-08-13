#!/usr/bin/env python3
"""Exact prime-field hyperplane union bounds for A000410."""

import argparse
import math


def weak_compositions(total, parts, prefix=()):
    if parts == 1:
        yield prefix + (total,)
        return
    for first in range(total + 1):
        yield from weak_compositions(total - first, parts - 1, prefix + (first,))


def multinomial(histogram):
    answer = math.factorial(sum(histogram))
    for count in histogram:
        answer //= math.factorial(count)
    return answer


def section_size(histogram, prime):
    counts = [0] * prime
    counts[0] = 1
    for coefficient, multiplicity in enumerate(histogram):
        for _ in range(multiplicity):
            updated = counts[:]
            for residue, count in enumerate(counts):
                updated[(residue + coefficient) % prime] += count
            counts = updated
    return counts[0]


def prime_union_upper(n, prime):
    labeled_normals_sum = 0
    for histogram in weak_compositions(n, prime):
        if histogram[0] == n:
            continue
        cube_points = section_size(histogram, prime)
        if cube_points - 1 >= n:
            labeled_normals_sum += multinomial(histogram) * math.comb(cube_points - 1, n)
    assert labeled_normals_sum % (prime - 1) == 0
    return labeled_normals_sum // (prime - 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=10)
    parser.add_argument("--primes", type=int, nargs="+", default=[2, 3, 5, 7, 11, 13])
    args = parser.parse_args()
    values = []
    for prime in args.primes:
        value = prime_union_upper(args.n, prime)
        values.append((value, prime))
        print(f"n={args.n} prime={prime} upper={value}")
    value, prime = min(values)
    print(f"best_prime={prime} best_upper={value}")


if __name__ == "__main__":
    main()
