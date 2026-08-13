#!/usr/bin/env python3
"""Independent exact checker for A007234 using Python tuple permutations.

This intentionally shares neither permutation ranking nor graph construction
code with compute_a007234.cpp.  It implements the leaf/cycle algorithm directly
on the directed functional graph sigma -> sigma^2.
"""

from __future__ import annotations

import argparse
import itertools
from collections import Counter, deque


def square(p: tuple[int, ...]) -> tuple[int, ...]:
    return tuple(p[p[i]] for i in range(len(p)))


def compute(n: int) -> tuple[int, Counter[int], dict[str, int]]:
    perms = list(itertools.permutations(range(n)))
    index = {p: i for i, p in enumerate(perms)}
    image = [index[square(p)] for p in perms]
    size = len(perms)

    incoming: list[set[int]] = [set() for _ in range(size)]
    for v, u in enumerate(image):
        incoming[u].add(v)

    active = bytearray(b"\x01") * size
    indegree = [len(xs) for xs in incoming]
    queue = deque(v for v in range(size) if indegree[v] == 0)
    answer = 0

    def remove(v: int) -> None:
        if not active[v]:
            return
        active[v] = 0
        u = image[v]
        if active[u]:
            indegree[u] -= 1
            if indegree[u] == 0:
                queue.append(u)

    while queue:
        v = queue.popleft()
        if not active[v] or indegree[v] != 0:
            continue
        answer += 1
        u = image[v]
        remove(v)
        remove(u)

    # Remaining vertices are directed cycles, including loops.  A loop yields
    # floor(1/2)=0 and is therefore automatically excluded.
    seen = bytearray(size)
    cycles: Counter[int] = Counter()
    for start in range(size):
        if not active[start] or seen[start]:
            continue
        v = start
        length = 0
        while not seen[v]:
            if not active[v]:
                raise AssertionError("remaining component is not a cycle")
            seen[v] = 1
            length += 1
            v = image[v]
        if v != start:
            raise AssertionError("two remaining cycles in one component")
        cycles[length] += 1
        answer += length // 2

    stats = {
        "vertices": size,
        "selected_before_cycles": answer
        - sum((k // 2) * count for k, count in cycles.items()),
        "cycle_components": sum(cycles.values()),
        "cycle_vertices": sum(k * count for k, count in cycles.items()),
    }
    return answer, cycles, stats


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    args = parser.parse_args()
    answer, cycles, stats = compute(args.n)
    print(f"n={args.n}")
    for key, value in stats.items():
        print(f"{key}={value}")
    for length, count in sorted(cycles.items()):
        print(f"directed_cycles_length_{length}={count}")
    print(f"a({args.n})={answer}")


if __name__ == "__main__":
    main()
