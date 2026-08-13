# A005281 reproducibility package

This folder proves the new lower bound `a(7) >= 58`.

The certificate is a literal 58-symbol word. The standard-library verifier
checks its alphabet, forbids adjacent equal symbols, and checks every
two-symbol projection for the degree-6 alternation condition. No exact-value
claim is made.

Replay:

```bash
python3 scripts/verify_sequence.py certificates/n7_length58.txt
```

