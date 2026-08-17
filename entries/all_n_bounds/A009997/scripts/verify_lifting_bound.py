#!/usr/bin/env python3
"""Exact arithmetic check for the ternary chamber-lifting theorem."""


def factor(n: int) -> int:
    return (3 ** (n - 1) + 1) // 2


def main() -> None:
    factors = [factor(n) for n in range(1, 8)]
    assert factors == [1, 2, 5, 14, 41, 122, 365]
    a7 = 214_580_603
    a8_lower = factor(7) * a7
    assert a8_lower == 78_321_920_095
    print("lifting factors n=1..7:", factors)
    print("A009997(8) >=", a8_lower)


if __name__ == "__main__":
    main()
