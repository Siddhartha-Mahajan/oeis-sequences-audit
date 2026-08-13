#!/usr/bin/env python3
"""Independent verifier for an A001072 graph6 certificate.

This intentionally does not use the generator's Tarjan bridge routine.  It
checks the definition by ordinary reachability after deleting one or two
edges: G is bridgeless, and for every edge e there is another edge f for
which G-{e,f} is disconnected.
"""

import argparse
import hashlib
from collections import Counter
from pathlib import Path


def read_graph6(line):
    data = [ord(ch) - 63 for ch in line.strip()]
    if not data or not 0 <= data[0] <= 62:
        raise ValueError("only short graph6 records are supported")
    n = data[0]
    stream = []
    for value in data[1:]:
        stream.extend((value >> bit) & 1 for bit in (5, 4, 3, 2, 1, 0))
    graph = [set() for _ in range(n)]
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if stream[cursor]:
                graph[low].add(high)
                graph[high].add(low)
            cursor += 1
    return graph


def edge_list(graph):
    return [(u, v) for u in range(len(graph)) for v in graph[u] if u < v]


def connected_without(graph, omitted):
    n = len(graph)
    seen = {0}
    stack = [0]
    while stack:
        u = stack.pop()
        for v in graph[u]:
            edge = (u, v) if u < v else (v, u)
            if edge in omitted or v in seen:
                continue
            seen.add(v)
            stack.append(v)
    return len(seen) == n


def verify_graph(graph):
    n = len(graph)
    if n < 3 or any(u in graph[u] for u in range(n)):
        return False, "invalid order or loop"
    if any(u not in graph[v] for u in range(n) for v in graph[u]):
        return False, "asymmetric adjacency"
    edges = edge_list(graph)
    if any(len(graph[u]) < 2 for u in range(n)):
        return False, "minimum degree below two"
    for edge in edges:
        if not connected_without(graph, {edge}):
            return False, f"edge {edge} is a bridge"
        if not any(not connected_without(graph, {edge, other})
                   for other in edges if other != edge):
            return False, f"deleting {edge} leaves a bridgeless graph"
    return True, len(edges)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("certificate", type=Path)
    parser.add_argument("--expected", type=int, required=True)
    args = parser.parse_args()

    raw = args.certificate.read_bytes()
    lines = raw.decode("ascii").splitlines()
    if len(lines) != args.expected:
        raise SystemExit(f"count {len(lines)} != expected {args.expected}")
    if len(set(lines)) != len(lines):
        raise SystemExit("duplicate graph6 records")
    distribution = Counter()
    for index, line in enumerate(lines, 1):
        ok, detail = verify_graph(read_graph6(line))
        if not ok:
            raise SystemExit(f"record {index}: {detail}")
        distribution[detail] += 1
    digest = hashlib.sha256(raw).hexdigest()
    print(f"verified {len(lines)} minimally 2-edge-connected graphs")
    print("edge-count distribution:",
          " ".join(f"m={m}:{count}" for m, count in sorted(distribution.items())))
    print(f"sha256 {digest}")


if __name__ == "__main__":
    main()
