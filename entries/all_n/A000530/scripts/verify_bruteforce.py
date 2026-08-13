#!/usr/bin/env python3
"""Independent literal-word verification of small A000530 terms."""

from __future__ import annotations

import argparse
import itertools


def longest_run(word: str, symbol: str) -> int:
    best = run = 0
    for char in word:
        run = run + 1 if char == symbol else 0
        best = max(best, run)
    return best


def predicate(n: int, symbol: str, word: str) -> bool:
    return word.count(symbol) >= 2 * n - longest_run(word, symbol)


def qualifies(n: int, word: str) -> bool:
    return (
        word.endswith("0")
        and predicate(n, "0", word)
        and all(
            not predicate(n, "0", word[:k])
            and not predicate(n, "1", word[:k])
            for k in range(len(word))
        )
    )


def count(n: int) -> int:
    # A safe word has fewer than 2*n occurrences after adding its longest run
    # for both symbols, hence no qualifying first hit exceeds 4*n-3 symbols.
    return sum(
        qualifies(n, "".join(bits))
        for length in range(1, 4 * n - 2)
        for bits in itertools.product("01", repeat=length)
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=5)
    args = parser.parse_args()
    known = [1, 5, 28, 226, 2077]
    got = [count(n) for n in range(1, args.max_n + 1)]
    assert got == known[: args.max_n], (got, known[: args.max_n])
    print("literal enumeration verified:", got)


if __name__ == "__main__":
    main()
