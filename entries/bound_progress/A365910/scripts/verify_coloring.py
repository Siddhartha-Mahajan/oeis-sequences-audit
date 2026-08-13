#!/usr/bin/env python3
import itertools,re,sys
classes=[]
for line in open(sys.argv[1]):
    blocks=[frozenset(map(int,x.split(','))) for x in re.findall(r'\{([0-9,]+)\}',line)]
    if blocks:classes.append(blocks)
assert len(classes)==48
flat=[b for cls in classes for b in cls]
assert len(flat)==210 and len(set(flat))==210
assert set(flat)=={frozenset(c) for c in itertools.combinations(range(1,11),4)}
for cls in classes:
    assert all(len(a&b)<=1 for a,b in itertools.combinations(cls,2))
print('verified partition of all 210 four-subsets into 48 valid classes')
