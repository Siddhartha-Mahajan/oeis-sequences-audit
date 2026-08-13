#!/usr/bin/env python3
"""Exact proof certificate for A363253(6)=A363253(7)=-1."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def polygonal(sides: int, index: int) -> int:
    return ((sides - 2) * index * index - (sides - 4) * index) // 2


PARAMETERS = {
    6: {"basis_end": 11, "interval": (268, 678), "late_start": 68},
    7: {"basis_end": 13, "interval": (388, 1523), "late_start": 79},
}


def certify(sides: int) -> dict[str, object]:
    cfg = PARAMETERS[sides]
    basis_end = cfg["basis_end"]
    lo, hi = cfg["interval"]
    late_start = cfg["late_start"]

    reachable = 1
    for index in range(1, basis_end + 1):
        reachable |= reachable << polygonal(sides, index)
    assert all((reachable >> value) & 1 for value in range(lo, hi + 1))

    # Materialize one independently checkable subset mask for every value in
    # the conductor interval.  There are at most 2^13 masks here.
    interval_witness_masks = {}
    for mask in range(1 << basis_end):
        total = sum(
            polygonal(sides, index + 1)
            for index in range(basis_end)
            if mask & (1 << index)
        )
        if lo <= total <= hi and total not in interval_witness_masks:
            interval_witness_masks[total] = mask
    assert set(interval_witness_masks) == set(range(lo, hi + 1))
    for value, mask in interval_witness_masks.items():
        assert value == sum(
            polygonal(sides, index + 1)
            for index in range(basis_end)
            if mask & (1 << index)
        )
    interval_length = hi - lo + 1
    next_value = polygonal(sides, basis_end + 1)
    assert next_value <= interval_length
    assert all(
        2 * polygonal(sides, j) > polygonal(sides, j + 1)
        for j in range(basis_end + 1, late_start + 1)
    )

    max_value = polygonal(sides, late_start - 1)
    cap = sides + 1
    dp = [0] * (max_value + 1)
    dp[0] = 1
    finite_counts = []
    for index in range(1, late_start):
        value = polygonal(sides, index)
        count = min(cap, dp[value] + 1)
        finite_counts.append({"index": index, "value": value, "capped_count": count})
        assert count != sides
        for subtotal in range(max_value, value - 1, -1):
            if dp[subtotal - value]:
                dp[subtotal] = min(cap, dp[subtotal] + dp[subtotal - value])

    late_checks = []
    for d in range(1, sides + 1):
        remainder = polygonal(sides, late_start) - polygonal(sides, late_start - d)
        largest = polygonal(sides, late_start - d)
        assert remainder >= lo
        assert remainder < largest
        assert late_start > 2 * d + 1
        late_checks.append(
            {"d": d, "remainder_at_threshold": remainder, "split_polygonal_value": largest}
        )

    trace = json.dumps(finite_counts, separators=(",", ":")).encode()
    return {
        "sides": sides,
        "conclusion": f"A363253({sides})=-1",
        "basis_indices": [1, basis_end],
        "certified_subset_sum_interval": [lo, hi],
        "interval_witness_masks": interval_witness_masks,
        "interval_length": interval_length,
        "next_polygonal_value": next_value,
        "late_threshold_index": late_start,
        "finite_prefix_last_index": late_start - 1,
        "finite_prefix_trace_sha256": hashlib.sha256(trace).hexdigest(),
        "finite_counts": finite_counts,
        "late_split_checks": late_checks,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = {"certificates": [certify(6), certify(7)]}
    payload = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    print("certified A363253(6)=-1")
    print("certified A363253(7)=-1")
    print("all exact finite-prefix and conductor checks passed")


if __name__ == "__main__":
    main()
