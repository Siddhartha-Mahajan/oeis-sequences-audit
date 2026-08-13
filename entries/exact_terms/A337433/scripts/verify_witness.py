#!/usr/bin/env python3
import json,sys
record=json.load(open(sys.argv[1]))
n=record['n']; a={tuple(map(int,k.split(','))):v for k,v in record['assignment'].items()}
assert len(a)==n*(n+1)//2 and sum(a.values())==record['objective']
steps=((0,-1),(0,1),(-1,-1),(-1,0),(1,0),(1,1))
for (r,c),value in a.items():
    neighbor_values={a[(r+dr,c+dc)] for dr,dc in steps if (r+dr,c+dc) in a}
    assert set(range(1,value))<=neighbor_values
print(f"verified n={n} objective={sum(a.values())}")
