#!/usr/bin/env python3
"""Exact finite-state counter for A000530."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


# State: (count0, count1, maxrun0, maxrun1, last, current_run).
# last is -1 only for the empty word.
State = tuple[int, int, int, int, int, int]


def extend(state: State, bit: int) -> State:
    c0, c1, m0, m1, last, run = state
    new_run = run + 1 if last == bit else 1
    if bit == 0:
        return c0 + 1, c1, max(m0, new_run), m1, 0, new_run
    return c0, c1 + 1, m0, max(m1, new_run), 1, new_run


def predicates(n: int, state: State) -> tuple[bool, bool]:
    c0, c1, m0, m1, _last, _run = state
    return c0 >= 2 * n - m0, c1 >= 2 * n - m1


def count(n: int) -> dict[str, int]:
    safe: dict[State, int] = {(0, 0, 0, 0, -1, 0): 1}
    answer = 0
    safe_words = 1
    max_length = 0
    transitions = 0
    length = 0
    while safe:
        nxt: dict[State, int] = defaultdict(int)
        for state, multiplicity in safe.items():
            for bit in (0, 1):
                transitions += 1
                child = extend(state, bit)
                p0, p1 = predicates(n, child)
                if bit == 0 and p0:
                    answer += multiplicity
                if not p0 and not p1:
                    nxt[child] += multiplicity
        length += 1
        if nxt:
            max_length = length
            safe_words += sum(nxt.values())
        safe = nxt
    return {
        "n": n,
        "a_n": answer,
        "maximum_safe_prefix_length": max_length,
        "safe_prefixes_with_multiplicity": safe_words,
        "state_transitions": transitions,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=9)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    records = [count(n) for n in range(1, args.max_n + 1)]
    text = json.dumps(records, indent=2)
    print(text)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
