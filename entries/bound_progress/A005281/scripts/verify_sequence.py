#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    args = parser.parse_args()
    fields = dict(
        line.split(" ", 1) for line in args.path.read_text(encoding="utf-8").splitlines()
    )
    n = int(fields["n"])
    word = fields["sequence"].strip()
    assert len(word) == int(fields["length"])
    assert set(word) <= {chr(ord("a") + i) for i in range(n)}
    assert all(a != b for a, b in zip(word, word[1:]))
    for i in range(n):
        for j in range(i + 1, n):
            a, b = chr(97 + i), chr(97 + j)
            projection = [x for x in word if x in {a, b}]
            runs = sum(
                k == 0 or projection[k] != projection[k - 1]
                for k in range(len(projection))
            )
            assert runs <= 6, (a, b, runs)
    print(
        f"verified degree-6 Davenport--Schinzel word of length {len(word)} "
        f"on {n} symbols"
    )


if __name__ == "__main__":
    main()
