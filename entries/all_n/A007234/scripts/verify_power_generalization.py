#!/usr/bin/env python3
"""Independent checks for the fixed-power conjugacy-type recurrence."""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from cycle_type_recurrence import compute as compute_square  # noqa: E402
from power_map_recurrence import compute as compute_power  # noqa: E402


def compose(p: tuple[int, ...], q: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[q[i]] for i in range(len(p)))


def power(p: tuple[int, ...], d: int) -> tuple[int, ...]:
    result = tuple(range(len(p)))
    base = p
    while d:
        if d & 1:
            result = compose(base, result)
        base = compose(base, base)
        d >>= 1
    return result


def path_dp(weights: list[tuple[int, int]]) -> int:
    no, yes = 0, -10**30
    for excluded, included in weights:
        no, yes = max(no, yes) + excluded, no + included
    return max(no, yes)


def cycle_dp(weights: list[tuple[int, int]]) -> int:
    if len(weights) == 1:
        return weights[0][0]
    best_excluded = weights[0][0] + path_dp(weights[1:])
    if len(weights) == 2:
        best_included = weights[0][1] + weights[1][0]
    else:
        middle = path_dp(weights[2:-1]) if len(weights) > 3 else 0
        best_included = weights[0][1] + weights[1][0] + middle + weights[-1][0]
    return max(best_excluded, best_included)


def direct(n: int, d: int) -> int:
    perms = list(itertools.permutations(range(n)))
    index = {p: i for i, p in enumerate(perms)}
    image = [index[power(p, d)] for p in perms]
    size = len(perms)
    children: list[list[int]] = [[] for _ in range(size)]
    indegree = [0] * size
    for v, u in enumerate(image):
        children[u].append(v)
        indegree[u] += 1

    stack = [v for v in range(size) if indegree[v] == 0]
    order: list[int] = []
    while stack:
        v = stack.pop()
        order.append(v)
        u = image[v]
        indegree[u] -= 1
        if indegree[u] == 0:
            stack.append(u)

    on_cycle = bytearray(b"\x01") * size
    for v in order:
        on_cycle[v] = 0
    excluded = [0] * size
    included = [1] * size
    for v in order:
        excluded[v] = sum(max(excluded[c], included[c]) for c in children[v])
        included[v] = 1 + sum(excluded[c] for c in children[v])
    for root in range(size):
        if on_cycle[root]:
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
    for n in range(1, 13):
        generic = compute_power(n, 2)
        specialized = compute_square(n)[0]
        assert generic == specialized, (n, generic, specialized)
    print("generic d=2 recurrence agrees with A007234 through n=12")

    for d in (2, 3, 4, 6):
        for n in range(1, 8):
            recurrence = compute_power(n, d)
            brute = direct(n, d)
            assert recurrence == brute, (n, d, recurrence, brute)
        print(f"d={d}: direct functional graphs agree through S_7")


if __name__ == "__main__":
    main()
