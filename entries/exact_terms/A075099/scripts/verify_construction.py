#!/usr/bin/env python3
import itertools,json,sys
r=json.load(open(sys.argv[1]));n=r['n'];available={'0','1'};selected=set(r['intermediates'])
for length in range(2,n):
    for w in sorted(x for x in selected if len(x)==length):
        assert any(w[:cut] in available and w[cut:] in available for cut in range(1,length)),w
        available.add(w)
for bits in itertools.product('01',repeat=n):
    w=''.join(bits)
    assert any(w[:cut] in available and w[cut:] in available for cut in range(1,n)),w
assert r['objective']==2**n+len(selected)
if r.get('status') == 0:
    assert 'Optimal' in r['message']
    assert r['mip_gap'] == 0
    assert r['dual_bound_total'] == r['objective']
print(f"verified construction with {len(selected)} intermediates and {2**n} targets: {r['objective']} multiplications")
