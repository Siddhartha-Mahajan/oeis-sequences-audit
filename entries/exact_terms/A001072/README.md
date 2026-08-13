# A001072

This folder proves `A001072(15)=41142`. Complete open/closed-ear generation
reproduces every published count from `n=3` through `n=14`; nauty canonical
labeling gives 41,142 isomorphism classes at `n=15`. A separate verifier
checks every graph directly from the definition.

Quick replay:

```bash
python3 scripts/verify_independent.py certificates/n15_graphs.g6 --expected 41142
```
