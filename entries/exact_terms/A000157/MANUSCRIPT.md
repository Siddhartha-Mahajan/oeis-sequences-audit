# Exact extension and definition correction for A000157

The published name, “Number of Boolean functions of n variables,” does not
define the data: the unrestricted count would be `2^(2^n)`. The record's
formula identifies `a(n)=A000370(n)/2`, where A000370 counts NPN-equivalence
classes of Boolean functions of at most `n` essential variables. NPN
equivalence allows permutation and independent complementation of inputs and
complementation of the output. An accurate name is therefore:

> Half the number of NPN-equivalence classes of Boolean functions of n or
> fewer variables.

Two independent exact Burnside computations give new terms at `n=12,...,16`.
Their digit lengths and SHA-256 fingerprints are:

| n | digits | SHA-256 |
|---:|---:|:---|
| 12 | 1221 | `a83bf6ce25b17cf972977ec24227d7e3e88ccc0143bd61445c30eea99bc985e9` |
| 13 | 2452 | `ade46de32fbbb50f49063a4d477a830241038b70521a8672e42782a53c47b237` |
| 14 | 4917 | `2f176bd76cd659847437dbda32fc118fcd5502492e4a5ca8bcf955318fe17133` |
| 15 | 9847 | `90c092070126f88e13e9df2702b4da3a9a50ee0690fcafcf9fb889c4de394e61` |
| 16 | 19710 | `6cb1ab0b3c130aa180175ac1878a8d597444f049a342c143a436dd55316a741f` |

`burnside_a000157.py` reconstructs the cycle-profile evaluation and reproduces
the published prefix. `signed_cycle_type_check.py` instead indexes conjugacy
classes of `C_2 wr S_n` by pairs of signed partitions, constructs their
actions on cube vertices, and applies Burnside's lemma. The programs agree on
all five integers. `direct_npn_orbits.py` explicitly enumerates small orbits.

All arithmetic is exact integer arithmetic. The full decimal values and
checksums are in `certificates/`.
