# A323560(19): trapped self-avoiding knight paths

## Result

`A323560(19)=36001752`. The same exact program reproduces the four published
values at 15 through 18 moves.

## Method

Reverse the path so the trap square is the origin and fix the first knight
move. The other seven neighbors of the trap square must all have been
visited. Exact depth-first enumeration maintains self-avoidance; a Held-Karp
subset dynamic program on knight distances supplies an admissible lower bound
for visiting the remaining required squares and prunes impossible branches.

## Replay

```bash
mkdir -p build
c++ -O3 -std=c++20 scripts/count_trapped.cpp -o build/count_trapped
for n in 15 16 17 18 19; do ./build/count_trapped "$n"; done
```
