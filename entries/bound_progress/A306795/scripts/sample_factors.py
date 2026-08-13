#!/usr/bin/env python3
"""Certified lower bound from deterministic sampled 5x5 ternary matrices.

Distinct irreducible factors over Q have disjoint algebraic root sets.  Summing
the exact number of real roots of each factor therefore gives a rigorous lower
bound, even though the matrices themselves are sampled heuristically.
"""

from __future__ import annotations
import argparse,json,random
from pathlib import Path
import sympy as sp

def mul(a,b,n=5):
    return [[sum(a[i][k]*b[k][j] for k in range(n)) for j in range(n)] for i in range(n)]

def charpoly_coeffs(a):
    n=5;power=[row[:] for row in a];traces=[]
    for k in range(1,n+1):
        traces.append(sum(power[i][i] for i in range(n)))
        if k<n:power=mul(power,a,n)
    e=[1]
    for k in range(1,n+1):
        numerator=sum((1 if i%2 else -1)*e[k-i]*traces[i-1] for i in range(1,k+1))
        assert numerator%k==0;e.append(numerator//k)
    return tuple([1]+[((-1)**k)*e[k] for k in range(1,n+1)])

def main():
    p=argparse.ArgumentParser();p.add_argument('--samples',type=int,default=150000);p.add_argument('--seed',type=int,default=20260809);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    rng=random.Random(a.seed);polys={}
    for _ in range(a.samples):
        m=[[rng.randrange(3) for _ in range(5)] for _ in range(5)]
        code=sum(m[i][j]*3**(5*i+j) for i in range(5) for j in range(5))
        polys.setdefault(charpoly_coeffs(m),code)
    x=sp.symbols('x');factors={}
    for coeff,code in polys.items():
        poly=sp.Poly.from_list(coeff,gens=x,domain=sp.ZZ)
        for factor,_multiplicity in sp.factor_list(poly)[1]:
            factors.setdefault(tuple(int(c) for c in factor.monic().all_coeffs()),code)
    records=[];total=0
    for coeff in sorted(factors):
        poly=sp.Poly.from_list(coeff,gens=x,domain=sp.QQ)
        real=int(poly.count_roots(-sp.oo,sp.oo));total+=real
        records.append({'coefficients':coeff,'real_roots':real,'witness_matrix_base3':factors[coeff]})
    result={'samples':a.samples,'seed':a.seed,'distinct_characteristic_polynomials':len(polys),'distinct_irreducible_factors':len(factors),'certified_distinct_real_eigenvalues':total,'factors':records}
    a.output.write_text(json.dumps(result,separators=(',',':'))+'\n')
    print(json.dumps({k:v for k,v in result.items() if k!='factors'},indent=2))
if __name__=='__main__':main()
