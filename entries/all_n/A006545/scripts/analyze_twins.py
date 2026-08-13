#!/usr/bin/env python3
"""Compare graph stability with the presence of an automorphic transposition.

For a simple graph, swapping two vertices and fixing all others is an
automorphism exactly when the two vertices have identical adjacency to every
third vertex.  This script compares that elementary condition with the stable
graph certificates produced by count_stable.py.
"""

import argparse
from pathlib import Path

from count_stable import decode_graph6


def has_transposition(adjacency):
    n = len(adjacency)
    for u in range(n):
        for v in range(u + 1, n):
            outside = ((1 << n) - 1) & ~(1 << u) & ~(1 << v)
            if ((adjacency[u] ^ adjacency[v]) & outside) == 0:
                return True
    return False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("all_graphs", type=Path)
    parser.add_argument("stable_graphs", type=Path)
    args = parser.parse_args()

    all_lines = args.all_graphs.read_text(encoding="ascii").splitlines()
    stable = set(args.stable_graphs.read_text(encoding="ascii").splitlines())
    with_transposition = {
        line for line in all_lines if has_transposition(decode_graph6(line))
    }
    print(
        f"input={len(all_lines)} stable={len(stable)} "
        f"transposition={len(with_transposition)} "
        f"stable_without={len(stable - with_transposition)} "
        f"transposition_without_stable={len(with_transposition - stable)}"
    )


if __name__ == "__main__":
    main()
