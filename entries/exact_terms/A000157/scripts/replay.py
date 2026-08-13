#!/usr/bin/env python3
"""Replay every certificate used for the A000157 audit."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BUILD = ROOT / "build"
BUILD.mkdir(exist_ok=True)


def run(*arguments: str) -> None:
    subprocess.run([sys.executable, *arguments], cwd=ROOT, check=True)


def main() -> None:
    run(str(HERE / "direct_npn_orbits.py"), "--through", "3")
    run(
        str(HERE / "burnside_a000157.py"),
        "--through",
        "12",
        "--verify-bfile",
        str(ROOT / "sources" / "b000157_2026_08_13.txt"),
        "--output",
        str(BUILD / "replay_b000157_through_12.txt"),
    )
    primary = {
        int(line.split()[0]): line.split()[1]
        for line in (BUILD / "replay_b000157_through_12.txt").read_text().splitlines()
    }
    # The primary output above stops at 12 to keep this quick replay compact;
    # load the frozen full primary calculation for 13..16 as well.
    primary.update(
        {
            int(line.split()[0]): line.split()[1]
            for line in (ROOT / "certificates" / "candidate_b000157_through_16.txt").read_text().splitlines()
        }
    )
    expected = {
        12: (1221, "a83bf6ce25b17cf972977ec24227d7e3e88ccc0143bd61445c30eea99bc985e9"),
        13: (2452, "ade46de32fbbb50f49063a4d477a830241038b70521a8672e42782a53c47b237"),
        14: (4917, "2f176bd76cd659847437dbda32fc118fcd5502492e4a5ca8bcf955318fe17133"),
        15: (9847, "90c092070126f88e13e9df2702b4da3a9a50ee0690fcafcf9fb889c4de394e61"),
        16: (19710, "6cb1ab0b3c130aa180175ac1878a8d597444f049a342c143a436dd55316a741f"),
    }
    for n in range(12, 17):
        independent_path = BUILD / f"replay_independent_a000157_{n}.txt"
        run(
            str(HERE / "signed_cycle_type_check.py"),
            str(n),
            "--summary-only",
            "--value-output",
            str(independent_path),
        )
        independent = independent_path.read_text().split()[1]
        if primary[n] != independent:
            raise AssertionError(f"the independent n={n} values differ")
        digits, expected_digest = expected[n]
        digest = hashlib.sha256(independent.encode()).hexdigest()
        if len(independent) != digits or digest != expected_digest:
            raise AssertionError(f"unexpected n={n} fingerprint")
    ancillary = ROOT / "certificates" / "a000157_terms_12_16.txt"
    ancillary_values = {
        int(line.split()[0]): line.split()[1]
        for line in ancillary.read_text().splitlines()
        if line and not line.startswith("#")
    }
    assert ancillary_values == {n: primary[n] for n in range(12, 17)}
    print("all A000157 checks passed")


if __name__ == "__main__":
    main()
