# A273354

This folder proves the exact new term

```text
A273354(3) = 11177126654841000000.
```

The candidate has exactly three representations by two positive squares and
exactly three by two positive cubes.  Minimality follows by reducing every
smaller number with at least three cube representations to one of 110,969
cubic scalings of 6,177 primitive A003825 values, then certifying that none
has square multiplicity three.

Replay the independent verifier with:

```bash
python3 scripts/verify_minimality_certificate.py
```

The proof explicitly records the trust boundary: completeness uses the
external primitive A003825 b-file, while its cubic-scaling closure is
independently checked against all 100,000 supplied A018787 terms.
