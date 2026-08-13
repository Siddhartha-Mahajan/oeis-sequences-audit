# A000157

This folder corrects the underdefined sequence name and supplies five exact
new values, `a(12)` through `a(16)`. The values have respectively 1,221,
2,452, 4,917, 9,847, and 19,710 decimal digits, so they belong in an OEIS
ancillary a-file rather than DATA or the ordinary b-file.

Two exact Burnside implementations agree on every new value. One reproduces
all published terms through `a(11)`; direct NPN-orbit enumeration checks the
interpretation for up to three variables.

Replay everything with `python3 scripts/replay.py`.
