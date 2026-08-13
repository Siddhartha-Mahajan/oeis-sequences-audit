#!/usr/bin/env python3
"""Exact straight-line-program MILP for A075099."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix


def words(length: int) -> list[str]:
    return [format(i, f"0{length}b") for i in range(1 << length)]


def solve(n: int, time_limit: float | None) -> dict:
    if n == 1:
        return {"n": 1, "objective": 0, "intermediates": [], "status": 0,
                "message": "the two generators are initially available", "mip_gap": 0.0}
    intermediate = [w for length in range(2, n) for w in words(length)]
    x_index = {w: i for i, w in enumerate(intermediate)}
    split_vars = []
    for length in range(2, n + 1):
        for w in words(length):
            for cut in range(1, length):
                split_vars.append((w, cut))
    y_index = {item: len(intermediate) + i for i, item in enumerate(split_vars)}
    nvars = len(intermediate) + len(split_vars)

    rows: list[tuple[dict[int, float], float, float]] = []
    # Every selected intermediate, and every required target, has a usable split.
    for length in range(2, n + 1):
        for w in words(length):
            coeff = {y_index[(w, cut)]: 1.0 for cut in range(1, length)}
            if length < n:
                coeff[x_index[w]] = -1.0
                rows.append((coeff, 0.0, np.inf))
            else:
                rows.append((coeff, 1.0, np.inf))
    # A claimed split can use only already-selected non-generator pieces.
    for w, cut in split_vars:
        y = y_index[(w, cut)]
        for piece in (w[:cut], w[cut:]):
            if len(piece) > 1:
                rows.append(({y: 1.0, x_index[piece]: -1.0}, -np.inf, 0.0))

    matrix = lil_matrix((len(rows), nvars), dtype=float)
    lo = np.empty(len(rows)); hi = np.empty(len(rows))
    for r, (coeff, lower, upper) in enumerate(rows):
        for c, value in coeff.items(): matrix[r, c] = value
        lo[r] = lower; hi[r] = upper
    objective = np.zeros(nvars)
    objective[:len(intermediate)] = 1.0
    options = {"disp": False}
    if time_limit is not None: options["time_limit"] = time_limit
    # Only intermediate-selection variables need to be integral. Once those
    # are binary, the split variables merely witness a usable cut and may be
    # continuous in [0,1] without changing the feasible selected families.
    integrality = np.zeros(nvars)
    integrality[:len(intermediate)] = 1
    result = milp(
        c=objective, integrality=integrality,
        bounds=Bounds(np.zeros(nvars), np.ones(nvars)),
        constraints=LinearConstraint(matrix.tocsr(), lo, hi), options=options)
    selected = [] if result.x is None else [w for w, i in x_index.items() if result.x[i] > 0.5]
    return {
        "n": n, "status": int(result.status), "message": result.message,
        "intermediate_count": None if result.fun is None else int(round(result.fun)),
        "objective": None if result.fun is None else (1 << n) + int(round(result.fun)),
        "dual_bound_total": None if getattr(result, "mip_dual_bound", None) is None
                            else (1 << n) + result.mip_dual_bound,
        "mip_gap": getattr(result, "mip_gap", None),
        "mip_node_count": getattr(result, "mip_node_count", None),
        "intermediates": selected,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("n", type=int)
    parser.add_argument("--time-limit", type=float)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    record = solve(args.n, args.time_limit)
    text = json.dumps(record, indent=2)
    print(text)
    if args.output: args.output.write_text(text + "\n", encoding="utf-8")


if __name__ == "__main__": main()
