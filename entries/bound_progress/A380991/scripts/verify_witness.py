#!/usr/bin/env python3
import math,re,sys
points=set((int(x),int(y)) for x,y in re.findall(r'\((-?\d+),(-?\d+)\)',open(sys.argv[1]).read()))
assert len(points)==71
seen={next(iter(points))}
while True:
    new=seen|{(x+dx,y+dy) for x,y in seen for dx,dy in ((1,0),(-1,0),(0,1),(0,-1)) if (x+dx,y+dy) in points}
    if new==seen:break
    seen=new
assert seen==points
for p in points:
    counts={}
    for q in points:
        if p==q:continue
        dx,dy=q[0]-p[0],q[1]-p[1];g=math.gcd(abs(dx),abs(dy));dx//=g;dy//=g
        if dx<0 or (dx==0 and dy<0):dx,dy=-dx,-dy
        counts[(dx,dy)]=counts.get((dx,dy),0)+1
    assert max(counts.values(),default=0)<=4
print('verified 71 connected cells; every line contains at most 5 centers')
