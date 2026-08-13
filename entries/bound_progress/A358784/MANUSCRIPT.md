# A358784(4): improved three-generator Boolean-semigroup bound

## Result

`A358784(4)>=42514`, improving the published lower bound 24846.

## Witness

With rows separated by `/`, the generators are

```text
0001/1000/0100/0010
0011/0001/0100/1000
0000/0001/0010/0100
```

Exact breadth-first closure under right Boolean-matrix multiplication has
42514 members. The Python verifier is independent of the C++ search code and
records the sorted member-set SHA-256 digest.

## Replay

```bash
python3 scripts/verify_42514.py
```

This is a constructive lower bound, not an exact value for `a(4)`.
