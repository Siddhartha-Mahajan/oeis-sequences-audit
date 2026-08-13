#!/usr/bin/env python3
"""Generate minimally 2-edge-connected simple graphs by ear addition.

Each order is canonicalized with nauty's labelg.  A cycle of every order is
inserted as a possible initial block; all other candidates arise by adding an
open ear (new internal vertices between two old vertices) or a closed ear (a
new cycle attached at one old vertex) to a smaller accepted graph.
"""

import argparse
import subprocess
from pathlib import Path


def encode_graph6(adj):
    n = len(adj)
    assert n <= 62
    bits = []
    for j in range(1, n):
        for i in range(j):
            bits.append((adj[i] >> j) & 1)
    while len(bits) % 6:
        bits.append(0)
    payload = []
    for start in range(0, len(bits), 6):
        value = 0
        for bit in bits[start:start + 6]:
            value = (value << 1) | bit
        payload.append(chr(value + 63))
    return chr(n + 63) + "".join(payload)


def decode_graph6(text):
    raw = [ord(c) - 63 for c in text.strip()]
    n = raw[0]
    bits = []
    for value in raw[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adj = [0] * n
    pos = 0
    for j in range(1, n):
        for i in range(j):
            if bits[pos]:
                adj[i] |= 1 << j
                adj[j] |= 1 << i
            pos += 1
    return adj


def edges(adj):
    for u, row in enumerate(adj):
        for v in range(u + 1, len(adj)):
            if (row >> v) & 1:
                yield u, v


def bridge_count(adj, omitted=None):
    n = len(adj)
    discovery = [-1] * n
    low = [0] * n
    timer = 0
    bridges = 0

    def dfs(v, parent):
        nonlocal timer, bridges
        discovery[v] = low[v] = timer
        timer += 1
        row = adj[v]
        while row:
            bit = row & -row
            u = bit.bit_length() - 1
            row ^= bit
            if omitted is not None and ((v == omitted[0] and u == omitted[1]) or
                                        (v == omitted[1] and u == omitted[0])):
                continue
            if discovery[u] < 0:
                dfs(u, v)
                low[v] = min(low[v], low[u])
                if low[u] > discovery[v]:
                    bridges += 1
            elif u != parent:
                low[v] = min(low[v], discovery[u])

    dfs(0, -1)
    if any(value < 0 for value in discovery):
        return bridges + 1
    return bridges


def is_minimal_2edge(adj):
    if bridge_count(adj) != 0:
        return False
    return all(bridge_count(adj, edge) > 0 for edge in edges(adj))


def cycle(order):
    adj = [0] * order
    for u in range(order):
        v = (u + 1) % order
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def add_ear(base, target, left, right):
    old = len(base)
    internal = target - old
    adj = base[:] + [0] * internal
    path = [left] + list(range(old, target)) + [right]
    for u, v in zip(path, path[1:]):
        if u == v or ((adj[u] >> v) & 1):
            return None
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    return adj


def raw_candidates(layers, target):
    yield cycle(target)
    for old_order in range(3, target):
        internal = target - old_order
        for code in layers[old_order]:
            base = decode_graph6(code)
            # Open ears have distinct endpoints and at least one new vertex.
            for left in range(old_order):
                for right in range(left + 1, old_order):
                    candidate = add_ear(base, target, left, right)
                    if candidate is not None and is_minimal_2edge(candidate):
                        yield candidate
            # A simple closed ear needs at least two new vertices.
            if internal >= 2:
                for root in range(old_order):
                    candidate = add_ear(base, target, root, root)
                    if candidate is not None and is_minimal_2edge(candidate):
                        yield candidate


def canonicalize(candidates, labelg, work):
    raw = work / "raw.g6"
    canonical = work / "canonical.g6"
    count = 0
    with raw.open("w", encoding="ascii") as stream:
        for candidate in candidates:
            stream.write(candidate if isinstance(candidate, str)
                         else encode_graph6(candidate))
            stream.write("\n")
            count += 1
    with canonical.open("w", encoding="ascii") as output:
        subprocess.run([str(labelg), "-q", str(raw)], stdout=output, check=True)
    unique = sorted(set(canonical.read_text(encoding="ascii").splitlines()))
    return count, unique


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-order", type=int, required=True)
    parser.add_argument("--labelg", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    published = {3: 1, 4: 1, 5: 3, 6: 4, 7: 11, 8: 23, 9: 63,
                 10: 159, 11: 459, 12: 1331, 13: 4083, 14: 12750}
    layers = {}
    for order in range(3, args.max_order + 1):
        order_dir = args.output / f"n{order}"
        order_dir.mkdir(exist_ok=True)
        raw_count, layers[order] = canonicalize(
            raw_candidates(layers, order), args.labelg, order_dir)
        final = order_dir / "graphs.g6"
        final.write_text("".join(code + "\n" for code in layers[order]),
                         encoding="ascii")
        expected = published.get(order)
        status = "" if expected is None else f" expected={expected}"
        print(f"n={order} raw={raw_count} unique={len(layers[order])}{status}",
              flush=True)
        if expected is not None and len(layers[order]) != expected:
            raise AssertionError((order, len(layers[order]), expected))


if __name__ == "__main__":
    main()

