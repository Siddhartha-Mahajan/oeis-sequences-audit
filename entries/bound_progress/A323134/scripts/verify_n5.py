#!/usr/bin/env python3
"""Independent Python recount of the first discrepant A323134 case."""
M=((1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1),(-2,1),(-1,2));MI={p:i for i,p in enumerate(M)}
def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
def between(a,b,c):return min(a,b)<=c<=max(a,b)
def hit(a,b,c,d):
 x1,x2,x3,x4=cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
 if x1*x2<0 and x3*x4<0:return True
 return (x1==0 and between(a[0],b[0],c[0]) and between(a[1],b[1],c[1])) or (x2==0 and between(a[0],b[0],d[0]) and between(a[1],b[1],d[1])) or (x3==0 and between(c[0],d[0],a[0]) and between(c[1],d[1],a[1])) or (x4==0 and between(c[0],d[0],b[0]) and between(c[1],d[1],b[1]))
def tf(p,t):
 x,y=p
 if t>=4:x=-x
 for _ in range(t%4):x,y=-y,x
 return x,y
def canon(path):
 moves=[(path[(i+1)%len(path)][0]-path[i][0],path[(i+1)%len(path)][1]-path[i][1]) for i in range(len(path))]
 out=[]
 for t in range(8):
  f=[MI[tf(p,t)] for p in moves];r=[MI[tuple(-v for v in tf(moves[-1-i],t))] for i in range(len(moves))]
  for s in (f,r):out += [tuple(s[k:]+s[:k]) for k in range(len(s))]
 return min(out)
path=[(0,0),(1,2)];seen=set(path);forms=set();rooted=0;L=10
def clear(a,b,closing=False):
 for i in range(len(path)-1):
  if i==len(path)-2 or (closing and i==0):continue
  if hit(a,b,path[i],path[i+1]):return False
 return True
def dfs():
 global rooted
 here=path[-1]
 if len(path)==L:
  d=(-here[0],-here[1])
  if d in MI and clear(here,(0,0),True):rooted+=1;forms.add(canon(path))
  return
 for dx,dy in M:
  q=(here[0]+dx,here[1]+dy)
  if q not in seen and clear(here,q):seen.add(q);path.append(q);dfs();path.pop();seen.remove(q)
dfs();assert rooted==58840 and len(forms)==3034
print('independent Python recount: rooted=58840 inequivalent=3034')
