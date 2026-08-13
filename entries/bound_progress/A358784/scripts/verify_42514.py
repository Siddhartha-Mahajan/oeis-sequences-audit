#!/usr/bin/env python3
"""Independent Python verifier for the 42,514-element A358784 witness."""

from __future__ import annotations

import hashlib
import json
from collections import deque
from pathlib import Path


WITNESS = (
    "0001/1000/0100/0010",
    "0011/0001/0100/1000",
    "0000/0001/0010/0100",
)


def parse(rows: str) -> tuple[int, int, int, int]:
    return tuple(int(row, 2) for row in rows.split("/"))  # type: ignore[return-value]


def multiply(a: tuple[int, ...], b: tuple[int, ...]) -> tuple[int, ...]:
    out = []
    for row in a:
        image = 0
        for k in range(4):
            # int(row, 2) uses the conventional leftmost bit as column 0.
            if row & (1 << (3 - k)):
                image |= b[k]
        out.append(image)
    return tuple(out)


def encode(a: tuple[int, ...]) -> int:
    value = 0
    for row in a:
        value = (value << 4) | row
    return value


def main() -> None:
    generators = tuple(parse(x) for x in WITNESS)
    distance = {g: 1 for g in generators}
    queue = deque(generators)
    while queue:
        x = queue.popleft()
        for g in generators:
            y = multiply(x, g)
            if y not in distance:
                distance[y] = distance[x] + 1
                queue.append(y)

    histogram: dict[int, int] = {}
    for d in distance.values():
        histogram[d] = histogram.get(d, 0) + 1
    members = b"".join(x.to_bytes(2, "big") for x in sorted(map(encode, distance)))
    result = {
        "dimension": 4,
        "generators": WITNESS,
        "closure_size": len(distance),
        "maximum_shortest_word_length": max(distance.values()),
        "shortest_word_length_histogram": histogram,
        "sorted_member_set_sha256": hashlib.sha256(members).hexdigest(),
        "verified": len(distance) == 42514,
    }
    target = Path(__file__).resolve().parents[1] / "certificates" / "verify_42514.json"
    target.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if not result["verified"]:
        raise SystemExit("witness did not generate the claimed number of matrices")


if __name__ == "__main__":
    main()
