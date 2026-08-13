#!/usr/bin/env python3
"""Replay the A000410 primitive-normal lower bound from its source sprint."""

import runpy
from pathlib import Path


SOURCE = (
    Path(__file__).resolve().parents[4]
    / "hard_open_hf_audit_2026_08_09"
    / "sequence_audits"
    / "A000410_singular_binary_row_sets"
    / "sprints"
    / "sprint_05_primitive_normal_types"
    / "evaluate_cutoff_bound.py"
)

if not SOURCE.exists():
    raise SystemExit(
        "The lower-bound source sprint is not present. Copy its evaluator and "
        "normal-type enumerator into this package before publishing it."
    )

runpy.run_path(str(SOURCE), run_name="__main__")
