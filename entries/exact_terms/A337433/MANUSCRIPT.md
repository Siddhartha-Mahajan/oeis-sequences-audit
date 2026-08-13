# A337433(7): exact triangular-lattice labeling optimum

## Result

`A337433(7)=87`. The same formulation reproduces all six published terms.

## Method

The 28 triangular-lattice nodes receive exactly one label in `{1,...,7}`.
If a node receives label `k`, binary constraints require every label below
`k` among its neighbors. The objective maximizes the label sum. HiGHS returns
87 with matching global bound and zero MIP gap. The certificate contains the
complete 28-node labeling.

## Replay

Quick witness check:

```bash
python3 scripts/verify_witness.py certificates/n7_milp.json
```

Full MILP replay after installing NumPy and SciPy:

```bash
python3 scripts/solve_milp.py 7 --output certificates/n7_recomputed.json
```

The witness checker certifies attainability; global optimality is the
integer optimizer's zero-gap conclusion for the included model.
