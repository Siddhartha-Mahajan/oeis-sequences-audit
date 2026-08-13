#!/usr/bin/env python3
"""Third exact method: tree DP plus cycle DP on functional components.

Unlike independent_check.py, this does not use the leaf-removal theorem.  It
computes include/exclude values on every reverse tree and then solves a weighted
independent-set problem on each directed cycle.  Loops force exclusion.
"""

from __future__ import annotations

import argparse
import itertools


def square(p: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[p[i]] for i in range(len(p)))


def path_dp(weights: list[tuple[int, int]]) -> int:
    """Weighted independent set on a path; pair is (exclude, include)."""
    no, yes = 0, -10**30
    for exclude, include in weights:
        no, yes = max(no, yes) + exclude, no + include
    return max(no, yes)


def cycle_dp(weights: list[tuple[int, int]]) -> int:
    if len(weights) == 1:
        return weights[0][0]  # loop: its endpoint cannot be chosen
    # First vertex excluded.
    best_excluded = weights[0][0] + path_dp(weights[1:])
    # First vertex included, so both its neighbors are excluded.
    if len(weights) == 2:
        best_included = weights[0][1] + weights[1][0]
    else:
        middle = path_dp(weights[2:-1]) if len(weights) > 3 else 0
        best_included = (
            weights[0][1] + weights[1][0] + middle + weights[-1][0]
        )
    return max(best_excluded, best_included)


def compute(n: int) -> int:
    perms = list(itertools.permutations(range(n)))
    index = {p: i for i, p in enumerate(perms)}
    image = [index[square(p)] for p in perms]
    size = len(perms)
    children: list[list[int]] = [[] for _ in range(size)]
    indegree = [0] * size
    for v, u in enumerate(image):
        children[u].append(v)
        indegree[u] += 1

    # Kahn elimination identifies noncycle vertices and gives child-before-parent
    # order for the reverse-tree DP.
    stack = [v for v in range(size) if indegree[v] == 0]
    order: list[int] = []
    while stack:
        v = stack.pop()
        order.append(v)
        u = image[v]
        indegree[u] -= 1
        if indegree[u] == 0:
            stack.append(u)

    excluded = [0] * size
    included = [1] * size
    on_cycle = bytearray(b"\x01") * size
    for v in order:
        on_cycle[v] = 0
    for v in order:
        # By Kahn order, every noncycle reverse child has already been processed.
        excluded[v] = sum(max(excluded[c], included[c]) for c in children[v])
        included[v] = 1 + sum(excluded[c] for c in children[v])

    # Add every noncycle child tree to its cycle root's local weights.
    for root in range(size):
        if not on_cycle[root]:
            continue
        tree_children = [c for c in children[root] if not on_cycle[c]]
        excluded[root] = sum(max(excluded[c], included[c]) for c in tree_children)
        included[root] = 1 + sum(excluded[c] for c in tree_children)

    answer = 0
    seen = bytearray(size)
    for start in range(size):
        if not on_cycle[start] or seen[start]:
            continue
        cycle: list[int] = []
        v = start
        while not seen[v]:
            seen[v] = 1
            cycle.append(v)
            v = image[v]
        if v != start:
            raise AssertionError("bad functional component")
        answer += cycle_dp([(excluded[v], included[v]) for v in cycle])
    return answer


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    args = parser.parse_args()
    print(f"a({args.n})={compute(args.n)}")


if __name__ == "__main__":
    main()
