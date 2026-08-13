#!/usr/bin/env python3
"""Verify a rank-list A007234 witness without using the MIS computation."""

from __future__ import annotations

import argparse
import itertools


def square(p: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[p[i]] for i in range(len(p)))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("witness")
    parser.add_argument("expected", type=int)
    args = parser.parse_args()
    ranks = []
    with open(args.witness, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if line and not line.startswith("#"):
                ranks.append(int(line))
    assert len(ranks) == args.expected
    assert ranks == sorted(set(ranks))
    selected = set(ranks)
    perms = list(itertools.permutations(range(args.n)))
    index = {p: i for i, p in enumerate(perms)}
    for rank in ranks:
        assert 0 <= rank < len(perms)
        assert index[square(perms[rank])] not in selected
    print(f"verified {len(ranks)} selected permutations in S_{args.n}")
    print("no selected permutation has its square selected")


if __name__ == "__main__":
    main()
