# A363253 reproducibility package

This folder proves the two missing exact terms

```text
A363253(6) = -1,
A363253(7) = -1.
```

See the [short manuscript](MANUSCRIPT.md) for the conductor argument. Replay
all exact finite-prefix and interval checks with:

```bash
python3 scripts/prove_a6_a7.py --output certificates/a6_a7_certificate.replay.json
```
