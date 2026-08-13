# A306795(5): certified real-eigenvalue lower bound

## Result

`A306795(5)>=283695`.

## Certificate

A deterministic sample of 150000 matrices over `{0,1,2}` produced 130618
distinct characteristic polynomials. Factoring them over the rationals gave
110573 distinct monic irreducible factors. Exact Sturm counts give 283695
real roots in total. Distinct monic irreducible polynomials over the
rationals have disjoint root sets.

Every factor record includes a base-3 encoded witness matrix. The verifier
decodes the witness, recomputes its characteristic polynomial, checks
divisibility and irreducibility, and recomputes the real-root count.

## Replay

After installing SymPy:

```bash
python3 scripts/verify_factor_certificate.py certificates/n5_sample_factors.json
```

Regenerating the deterministic sample is optional and much slower:

```bash
python3 scripts/sample_factors.py --samples 150000 --seed 20260809 --output certificates/n5_recomputed.json
```

This certifies a lower bound, not the exact value of `a(5)`.
