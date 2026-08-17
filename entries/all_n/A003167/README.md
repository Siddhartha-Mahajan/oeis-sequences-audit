# A003167

This package proves the exact value

```text
A003167(7)=155068098
```

and records an exact finite recursion valid for every dimension. The recursion
counts nondecreasing Egyptian-fraction solutions of
`1/x_1+...+1/x_n=1/2`; the final two denominators are accelerated by the
factorization `(p*x-q)(p*y-q)=q^2`.

Quick certificate replay:

```bash
python3 scripts/aggregate_n7.py --input-dir certificates/branches \
  --output build/n7_exact_certificate.json
python3 scripts/verify_certificate.py build/n7_exact_certificate.json
```

See `ALL_N_RECURRENCE.md` for the formal recurrence.
