#!/usr/bin/env python3
"""Build a SHA-256 manifest for the stable repository artifacts."""

import hashlib
from pathlib import Path

root = Path(__file__).resolve().parents[1]
target = root / "MANIFEST.sha256"
rows = []
for path in sorted(root.rglob("*")):
    if (not path.is_file() or path == target or path.name == ".DS_Store"
            or path.name in {"OEIS_EDIT.md", "OEIS_EDITS.md"}
            or any(part in {".git", "__pycache__", "build", "results", ".venv"}
                   for part in path.parts)):
        continue
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    rows.append(f"{digest.hexdigest()}  {path.relative_to(root)}")
target.write_text("\n".join(rows) + "\n", encoding="utf-8")
print(f"hashed {len(rows)} files into {target}")
