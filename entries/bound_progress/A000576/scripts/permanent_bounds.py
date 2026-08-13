#!/usr/bin/env python3
"""Exact permanent bounds for A000576; standard-library Python only."""

import argparse
import math
from fractions import Fraction


KNOWN = {(6, 12): 16790769154925929673725062021120}


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def floor_root_power(base, numerator, denominator):
    target = base**numerator
    lo, hi = 0, 1
    while hi**denominator <= target:
        hi *= 2
    while lo + 1 < hi:
        mid = (lo + hi) // 2
        if mid**denominator <= target:
            lo = mid
        else:
            hi = mid
    return lo


def extension_bounds(n, d):
    lo = ceil_fraction(Fraction((d-1)**((d-1)*n), d**((d-2)*n)))
    hi = floor_root_power(math.factorial(d), n, d)
    return lo, hi


def bounds(n, k=1, reduced=1):
    normalized = math.factorial(n-1)*reduced//math.factorial(n-k)
    lo = hi = normalized
    rows = []
    for d in range(n-k, 2, -1):
        x, y = extension_bounds(n, d)
        rows.append((d, x, y))
        lo *= x
        hi *= y
    scale = math.factorial(n-1)
    lo = ceil_fraction(Fraction(2*lo, scale))
    hi = 2*hi//scale
    divisor = math.factorial(n//2)
    return ceil_fraction(Fraction(lo, divisor))*divisor, hi//divisor*divisor, rows


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("n", type=int, nargs="?", default=12)
    p.add_argument("--from-known", action="store_true")
    p.add_argument("--details", action="store_true")
    a = p.parse_args()
    candidates = [(k,v) for (k,n),v in KNOWN.items() if n == a.n]
    k, value = max(candidates) if a.from_known and candidates else (1,1)
    lo, hi, rows = bounds(a.n, k, value)
    print(f"n={a.n}")
    print(f"exact starting count: R_{{{k},{a.n}}}={value}")
    if a.details:
        for d,x,y in rows:
            print(f"d={d}: {x} <= extensions <= {y}")
    print(f"{lo} <= A000576({a.n}) <= {hi}")
    print(f"divisor applied: {math.factorial(a.n//2)}")
