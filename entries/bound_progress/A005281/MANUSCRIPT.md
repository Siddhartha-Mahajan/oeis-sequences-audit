# A 58-symbol lower bound for A005281(7)

## Result

Under the convention of A005281, adjacent symbols must differ and no two
symbols may alternate in seven or more runs. The word in
`certificates/n7_length58.txt` has length 58 on seven symbols and satisfies
both requirements. Consequently `A005281(7) >= 58`.

This is a construction only; it neither supplies an upper bound nor asserts
that 58 is optimal.

## Verification

For each of the 21 unordered symbol pairs, the verifier projects the word to
that pair and counts its runs. The forbidden alternating subsequence of length
seven exists exactly when this run count is at least seven. All pairwise run
counts in the certificate are at most six.

The certificate was found by randomized delete-and-refill local search. Search
randomness is outside the proof: the short certificate and exhaustive pairwise
checker are the complete evidence needed for the lower bound. The search source
is retained so that the discovery process is also reproducible.

