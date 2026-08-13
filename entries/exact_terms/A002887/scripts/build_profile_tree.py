#!/usr/bin/env python3
"""Build and directly verify the first arithmetic-profile tree."""

import argparse
import json

import profile_search


def add_rooted(adj, parent, size, witness):
    root = len(adj)
    adj.append(set())
    if parent is not None:
        adj[root].add(parent)
        adj[parent].add(root)
    for child_size in witness[size]:
        add_rooted(adj, root, child_size, witness)
    return root


def cutting_numbers(adj):
    n = len(adj)
    values = []
    for removed in range(n):
        unseen = set(range(n)) - {removed}
        sizes = []
        while unseen:
            root = unseen.pop()
            stack = [root]
            size = 0
            while stack:
                v = stack.pop()
                size += 1
                for u in adj[v]:
                    if u != removed and u in unseen:
                        unseen.remove(u)
                        stack.append(u)
            sizes.append(size)
        values.append(sum(a * b for i, a in enumerate(sizes)
                          for b in sizes[i + 1:]))
    return values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("center_size", type=int)
    parser.add_argument("order", type=int)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()
    spectra = profile_search.square_partition_bits(args.order)
    result = profile_search.profiles(args.center_size, args.order, spectra, 1)
    if not result:
        raise SystemExit("no profile")
    profile, common_k, expected_cut, top_branches, witness = result[0]
    adj = []
    centers = []
    for _ in profile:
        centers.append(len(adj))
        adj.append(set())
    for a, b in zip(centers, centers[1:]):
        adj[a].add(b)
        adj[b].add(a)
    for root, branches in zip(centers, top_branches):
        for size in branches:
            add_rooted(adj, root, size, witness)
    assert len(adj) == args.order
    cuts = cutting_numbers(adj)
    maximum = max(cuts)
    actual_center = [i for i, value in enumerate(cuts) if value == maximum]
    edges = [[i, j] for i in range(len(adj)) for j in adj[i] if i < j]
    record = {
        "order": len(adj), "profile": profile, "common_k": common_k,
        "expected_cut": expected_cut, "actual_maximum": maximum,
        "intended_center": centers, "actual_center": actual_center,
        "center_cutting_numbers": [cuts[i] for i in centers],
        "edges": edges, "all_cutting_numbers": cuts,
    }
    with open(args.output, "w", encoding="utf-8") as stream:
        json.dump(record, stream, indent=2)
        stream.write("\n")
    print(json.dumps({k: record[k] for k in record if k != "edges" and
                      k != "all_cutting_numbers"}, indent=2))
    assert maximum == expected_cut
    assert actual_center == centers


if __name__ == "__main__":
    main()

