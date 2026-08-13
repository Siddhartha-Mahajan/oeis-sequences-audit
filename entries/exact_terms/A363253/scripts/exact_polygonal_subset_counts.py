#!/usr/bin/env python3
"""Find A363253(n) by exact, capped distinct-subset-sum counting.

For each positive n-gonal number P_n(k), count representations as a sum of
distinct positive n-gonal numbers.  Counts are capped at n+1: this preserves
the predicate "exactly n" while keeping integers small.  Because all summands
are positive, after P_n(k) is tested no later summand can affect its count.
Thus the first hit is accompanied by a finite minimality certificate.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def polygonal(sides: int, index: int) -> int:
    return ((sides - 2) * index * index - (sides - 4) * index) // 2


def find_term(sides: int, max_index: int) -> dict[str, object]:
    cap = sides + 1
    # dp[x] is the number of subsets of already inserted polygonal numbers
    # summing to x, capped at cap.  The empty subset is retained only as the
    # seed; targets and inserted summands are positive.
    max_value = polygonal(sides, max_index)
    dp = [0] * (max_value + 1)
    dp[0] = 1
    checked: list[dict[str, int]] = []

    for index in range(1, max_index + 1):
        target = polygonal(sides, index)
        # Before insertion, dp[target] counts representations using strictly
        # smaller polygonal numbers.  Inserting target adds the singleton.
        count = min(cap, dp[target] + 1)
        checked.append({"index": index, "value": target, "count": count})
        if count == sides:
            return {
                "sides": sides,
                "status": "found",
                "index": index,
                "value": target,
                "representations": count,
                "checked_through_index": index,
                "checked": checked,
            }

        # Retain sums above the current target as well: those combinations of
        # smaller summands can contribute to a later polygonal target.
        for subtotal in range(max_value, target - 1, -1):
            old = subtotal - target
            if dp[old]:
                dp[subtotal] = min(cap, dp[subtotal] + dp[old])

    return {
        "sides": sides,
        "status": "not_found",
        "checked_through_index": max_index,
        "checked_through_value": polygonal(sides, max_index),
        "checked": checked,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("sides", type=int)
    parser.add_argument("--max-index", type=int, default=100_000)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if args.sides < 3 or args.max_index < 1:
        parser.error("sides must be >= 3 and max-index must be positive")

    result = find_term(args.sides, args.max_index)
    # A digest of the complete checked (index,value,count) trace makes reruns
    # easy to compare without trusting a terse terminal transcript.
    trace = json.dumps(result["checked"], separators=(",", ":")).encode()
    result["trace_sha256"] = hashlib.sha256(trace).hexdigest()
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print(payload, end="")


if __name__ == "__main__":
    main()
