#!/usr/bin/env python3
"""Search A337433 as a binary MILP.

Each vertex receives one value.  If it receives k, every value 1,...,k-1
must occur at a neighboring vertex.  HiGHS supplies the primal solution and
the matching global bound used to certify optimality.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def vertices(n: int) -> list[tuple[int, int]]:
    return [(r, c) for r in range(n) for c in range(r + 1)]


def neighbors(v: tuple[int, int], universe: set[tuple[int, int]]) -> list[tuple[int, int]]:
    r, c = v
    candidates = [(r, c - 1), (r, c + 1), (r - 1, c - 1),
                  (r - 1, c), (r + 1, c), (r + 1, c + 1)]
    return [u for u in candidates if u in universe]


def solve(n: int, time_limit: float | None = None) -> dict:
    verts = vertices(n)
    universe = set(verts)
    index = {v: i for i, v in enumerate(verts)}
    max_label = 7
    var = lambda v, k: index[v] * max_label + (k - 1)
    nvars = len(verts) * max_label

    rows: list[tuple[dict[int, float], float, float]] = []
    for v in verts:
        rows.append(({var(v, k): 1.0 for k in range(1, max_label + 1)}, 1.0, 1.0))
        nbrs = neighbors(v, universe)
        for k in range(2, max_label + 1):
            for j in range(1, k):
                coeff = {var(v, k): 1.0}
                for u in nbrs:
                    coeff[var(u, j)] = coeff.get(var(u, j), 0.0) - 1.0
                rows.append((coeff, -np.inf, 0.0))

    matrix = lil_matrix((len(rows), nvars), dtype=float)
    lower = np.empty(len(rows))
    upper = np.empty(len(rows))
    for i, (coeff, lo, hi) in enumerate(rows):
        for j, value in coeff.items():
            matrix[i, j] = value
        lower[i] = lo
        upper[i] = hi

    objective = np.zeros(nvars)
    for v in verts:
        for k in range(1, max_label + 1):
            objective[var(v, k)] = -k
    options = {"disp": False}
    if time_limit is not None:
        options["time_limit"] = time_limit
    result = milp(
        c=objective,
        integrality=np.ones(nvars),
        bounds=Bounds(np.zeros(nvars), np.ones(nvars)),
        constraints=LinearConstraint(matrix.tocsr(), lower, upper),
        options=options,
    )

    assignment = {}
    if result.x is not None:
        for v in verts:
            assignment[f"{v[0]},{v[1]}"] = 1 + int(np.argmax(
                result.x[index[v] * max_label:(index[v] + 1) * max_label]
            ))
    return {
        "n": n,
        "status": int(result.status),
        "message": result.message,
        "objective": None if result.fun is None else int(round(-result.fun)),
        "mip_gap": getattr(result, "mip_gap", None),
        "mip_node_count": getattr(result, "mip_node_count", None),
        "assignment": assignment,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("--time-limit", type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    record = solve(args.n, args.time_limit)
    text = json.dumps(record, indent=2, sort_keys=True)
    print(text)
    if args.output:
        args.output.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
