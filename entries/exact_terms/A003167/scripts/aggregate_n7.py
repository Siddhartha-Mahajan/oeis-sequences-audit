#!/usr/bin/env python3
"""Validate and aggregate all disjoint exact A003167(7) branches."""

from __future__ import annotations

import argparse
import json
from fractions import Fraction
from pathlib import Path

from run_n7_partition import Task, tasks


def parse(path: Path) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, value = line.split(" ", 1)
        fields[key] = value
    return fields


def remainder(prefix: tuple[int, ...]) -> Fraction:
    return Fraction(1, 2) - sum((Fraction(1, x) for x in prefix), Fraction())


def legal_next(prefix: tuple[int, ...], remaining: int) -> tuple[int, int]:
    value = remainder(prefix)
    lower = max(prefix[-1], value.denominator // value.numerator + 1)
    upper = remaining * value.denominator // value.numerator
    return lower, upper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input-dir", type=Path, default=Path("results/n7_exact_v2"))
    parser.add_argument("--output", type=Path, default=Path("results/n7_exact_certificate.json"))
    args = parser.parse_args()

    all_tasks = tasks()
    assert len({task.name for task in all_tasks}) == len(all_tasks)
    assert legal_next((3,), 6) == (7, 36)
    assert legal_next((3, 7), 5) == (43, 210)
    assert legal_next((3, 7, 43), 4) == (1807, 7224)

    # The top-level branch x=3 is refined; all other legal first denominators
    # appear once. Within x=3, y=7 is refined, and within (3,7), z=43 is
    # refined into consecutive ranges.
    assert [task.args for task in all_tasks[:11]] == [(7, x) for x in range(4, 15)]
    ranges = []
    records = []
    total = 0
    for task in all_tasks:
        path = args.input_dir / f"{task.name}.txt"
        if not path.exists() or not path.stat().st_size:
            raise SystemExit(f"missing branch: {path}")
        fields = parse(path)
        assert fields["n"] == "7"
        count = int(fields["count"])
        total += count
        if "--next-range" in task.args:
            marker = task.args.index("--next-range")
            expected_range = (int(task.args[marker + 1]), int(task.args[marker + 2]))
            actual_range = tuple(map(int, fields["next_range"].split()))
            assert actual_range == expected_range
            ranges.append(actual_range)
        else:
            expected_prefix = tuple(map(int, task.args[1:]))
            assert tuple(map(int, fields["prefix"].split())) == expected_prefix
            assert fields["next_range"] == "0 0"
        records.append(
            {
                "branch": task.name,
                "arguments": list(task.args),
                "count": count,
                "search_nodes": int(fields["search_nodes"]),
                "pair_calls": int(fields["pair_calls"]),
                "maximum_terminal_denominator": int(fields["maximum_terminal_denominator"]),
            }
        )
    assert sorted(ranges)[0][0] == 1807
    assert sorted(ranges)[-1][1] == 7224
    for left, right in zip(sorted(ranges), sorted(ranges)[1:]):
        assert left[1] + 1 == right[0]

    certificate = {
        "sequence": "A003167",
        "n": 7,
        "a_n": total,
        "branch_count": len(records),
        "partition": {
            "first_denominator": "x=4..14, with x=3 refined",
            "after_3": "y=8..36, with y=7 refined",
            "after_3_7": "z=44..210, with z=43 refined",
            "after_3_7_43": "w=1807..7224 in consecutive disjoint ranges",
        },
        "branches": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(certificate, indent=2) + "\n", encoding="utf-8")
    print(f"certified A003167(7)={total} from {len(records)} disjoint branches")


if __name__ == "__main__":
    main()
