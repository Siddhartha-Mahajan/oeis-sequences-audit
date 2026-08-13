#!/usr/bin/env python3
import json,sys,sympy as sp
from sample_factors import charpoly_coeffs
r=json.load(open(sys.argv[1]));x=sp.symbols('x');seen=set();total=0
for item in r['factors']:
    coeff=tuple(item['coefficients']);assert coeff not in seen and coeff[0]==1;seen.add(coeff)
    p=sp.Poly.from_list(coeff,gens=x,domain=sp.QQ)
    assert p.is_irreducible
    code=item['witness_matrix_base3'];digits=[]
    for _ in range(25):digits.append(code%3);code//=3
    matrix=[digits[5*i:5*i+5] for i in range(5)]
    witness=sp.Poly.from_list(charpoly_coeffs(matrix),gens=x,domain=sp.QQ)
    assert witness.rem(p).is_zero
    real=int(p.count_roots(-sp.oo,sp.oo));assert real==item['real_roots'];total+=real
assert total==r['certified_distinct_real_eigenvalues']
print(f'verified {len(seen)} distinct irreducible factors with {total} distinct real roots')
