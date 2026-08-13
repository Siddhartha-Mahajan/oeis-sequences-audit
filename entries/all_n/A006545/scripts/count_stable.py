#!/usr/bin/env python3
"""Count stable graphs from an unlabeled graph6 stream.

Stability is the classical automorphism-group notion.  A graph G is
semistable at v iff every automorphism of G-v preserves N_G(v).  It is stable
iff it admits a vertex-deletion ordering in which every current graph is
semistable at the next deleted vertex.
"""

import argparse
from functools import lru_cache
from pathlib import Path


def decode_graph6(line):
    values = [ord(c) - 63 for c in line.strip()]
    n = values[0]
    bits = []
    for value in values[1:]:
        bits.extend((value >> shift) & 1 for shift in range(5, -1, -1))
    adjacency = [0] * n
    cursor = 0
    for high in range(1, n):
        for low in range(high):
            if bits[cursor]:
                adjacency[low] |= 1 << high
                adjacency[high] |= 1 << low
            cursor += 1
    return adjacency


def refine_colors(vertices, adjacency):
    colors = {v: (sum((adjacency[v] >> u) & 1 for u in vertices),)
              for v in vertices}
    while True:
        signatures = {}
        for v in vertices:
            neighbor_colors = sorted(colors[u] for u in vertices
                                     if (adjacency[v] >> u) & 1)
            signatures[v] = (colors[v], tuple(neighbor_colors))
        palette = {signature: index for index, signature in
                   enumerate(sorted(set(signatures.values())))}
        new_colors = {v: palette[signatures[v]] for v in vertices}
        old_partition = [[u for u in vertices if colors[u] == colors[v]]
                         for v in vertices]
        new_partition = [[u for u in vertices if new_colors[u] == new_colors[v]]
                         for v in vertices]
        if old_partition == new_partition:
            return new_colors
        colors = new_colors


def automorphism_exists(vertices, adjacency, source, target):
    """Return whether the induced graph has an automorphism source -> target."""
    colors = refine_colors(vertices, adjacency)
    if colors[source] != colors[target]:
        return False
    mapping = {source: target}
    used = {target}

    def compatible(u, image):
        if colors[u] != colors[image]:
            return False
        return all(((adjacency[u] >> old) & 1) ==
                   ((adjacency[image] >> new) & 1)
                   for old, new in mapping.items())

    def search():
        if len(mapping) == len(vertices):
            return True
        best_u = None
        best_candidates = None
        for u in vertices:
            if u in mapping:
                continue
            candidates = [image for image in vertices if image not in used
                          and compatible(u, image)]
            if not candidates:
                return False
            if best_candidates is None or len(candidates) < len(best_candidates):
                best_u, best_candidates = u, candidates
        for image in best_candidates:
            mapping[best_u] = image
            used.add(image)
            if search():
                return True
            used.remove(image)
            del mapping[best_u]
        return False

    return search()


def stable_graph(adjacency):
    n = len(adjacency)
    full = (1 << n) - 1
    choice = {}

    @lru_cache(None)
    def stable(mask):
        if mask == 0:
            return True
        vertices = [v for v in range(n) if (mask >> v) & 1]
        for deleted in vertices:
            remainder = mask & ~(1 << deleted)
            rem_vertices = [v for v in vertices if v != deleted]
            neighbors = adjacency[deleted] & remainder
            semistable = True
            neighbor_vertices = [v for v in rem_vertices
                                 if (neighbors >> v) & 1]
            nonneighbors = [v for v in rem_vertices
                            if not ((neighbors >> v) & 1)]
            for u in neighbor_vertices:
                if not semistable:
                    break
                for w in nonneighbors:
                    if automorphism_exists(rem_vertices, adjacency, u, w):
                        semistable = False
                        break
            if semistable and stable(remainder):
                choice[mask] = deleted
                return True
        return False

    result = stable(full)
    sequence = []
    mask = full
    while result and mask:
        deleted = choice[mask]
        sequence.append(deleted)
        mask &= ~(1 << deleted)
    return result, sequence


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--stable-output", type=Path)
    parser.add_argument("--sequences-output", type=Path)
    args = parser.parse_args()
    lines = args.input.read_text(encoding="ascii").splitlines()
    stable_lines = []
    sequences = []
    for index, line in enumerate(lines, 1):
        adjacency = decode_graph6(line)
        is_stable, sequence = stable_graph(adjacency)
        if is_stable:
            stable_lines.append(line)
            sequences.append((line, sequence))
    if args.stable_output:
        args.stable_output.write_text("".join(x + "\n" for x in stable_lines),
                                      encoding="ascii")
    if args.sequences_output:
        args.sequences_output.write_text("".join(
            f"{line} {' '.join(map(str, sequence))}\n"
            for line, sequence in sequences), encoding="ascii")
    print(f"input={len(lines)} stable={len(stable_lines)}")


if __name__ == "__main__":
    main()
