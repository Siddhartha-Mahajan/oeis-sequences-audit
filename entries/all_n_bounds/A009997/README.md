# A009997

This folder proves the all-dimensions recurrence

```text
a(n+1) >= ((3^(n-1)+1)/2)*a(n)  for n>=1,
```

and hence the frontier bound

```text
a(8) >= 78321920095.
```

The proof uses all positive ternary signed-sum walls of the form
`x=w_n+sum epsilon_i*w_i`; it strictly strengthens the earlier subset-only
lifting factor `2^(n-1)`.

Quick arithmetic replay:

```bash
python3 scripts/verify_lifting_bound.py
```
