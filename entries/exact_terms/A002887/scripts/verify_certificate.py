#!/usr/bin/env python3
"""Independent verifier for an A002887 edge-list certificate."""

import json
import sys


def components_without(adjacency, removed):
    unseen = set(range(len(adjacency)))
    unseen.remove(removed)
    sizes = []
    while unseen:
        seed = min(unseen)
        unseen.remove(seed)
        frontier = [seed]
        component = 0
        while frontier:
            vertex = frontier.pop()
            component += 1
            for neighbor in adjacency[vertex]:
                if neighbor in unseen:
                    unseen.remove(neighbor)
                    frontier.append(neighbor)
        sizes.append(component)
    return sorted(sizes, reverse=True)


def verify(path):
    with open(path, encoding="utf-8") as stream:
        record = json.load(stream)
    order = record["order"]
    edges = [tuple(edge) for edge in record["edges"]]
    assert len(edges) == order - 1
    assert len(set(edges)) == len(edges)
    adjacency = [set() for _ in range(order)]
    for left, right in edges:
        assert 0 <= left < right < order
        adjacency[left].add(right)
        adjacency[right].add(left)
    # A connected graph with N-1 edges is a tree.
    seen = {0}
    stack = [0]
    while stack:
        vertex = stack.pop()
        for neighbor in adjacency[vertex] - seen:
            seen.add(neighbor)
            stack.append(neighbor)
    assert len(seen) == order
    cuts = []
    for vertex in range(order):
        sizes = components_without(adjacency, vertex)
        cuts.append(sum(sizes[i] * sizes[j]
                        for i in range(len(sizes))
                        for j in range(i + 1, len(sizes))))
    maximum = max(cuts)
    center = [i for i, value in enumerate(cuts) if value == maximum]
    assert cuts == record["all_cutting_numbers"]
    assert maximum == record["actual_maximum"]
    assert center == record["actual_center"] == record["intended_center"]
    # The center itself must induce a path.
    center_set = set(center)
    center_degrees = [len(adjacency[v] & center_set) for v in center]
    if len(center) == 1:
        assert center_degrees == [0]
    else:
        assert sorted(center_degrees) == [1, 1] + [2] * (len(center) - 2)
    print(path, "verified: order", order, "center size", len(center),
          "cutting number", maximum)


if __name__ == "__main__":
    for filename in sys.argv[1:]:
        verify(filename)

