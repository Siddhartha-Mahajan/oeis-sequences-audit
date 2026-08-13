#!/usr/bin/env python3
"""Replay the exact A002887(5)..A002887(10) package."""

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXPECTED = {5: 48, 6: 48, 7: 122, 8: 122, 9: 264, 10: 264}

for center_size, order in EXPECTED.items():
    search = subprocess.run(
        [sys.executable, str(HERE / "profile_search.py"), str(center_size),
         "--max-order", str(order)], check=True, capture_output=True, text=True)
    first = search.stdout.splitlines()[0]
    assert first == f"order {order} profiles 1", (center_size, first)
    certificate = ROOT / "certificates" / f"candidate_center{center_size}_order{order}.json"
    subprocess.run([sys.executable, str(HERE / "verify_certificate.py"),
                    str(certificate)], check=True)

print("certified A002887(5..10) = 48,48,122,122,264,264")
