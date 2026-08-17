# Live OEIS audit

Audit date: 2026-08-14.

The current records were read from the official OEIS JSON endpoint
`https://oeis.org/search?q=id:AXXXXXX&fmt=json`. The packaged claims were
compared with DATA, COMMENTS, FORMULA, and EXTENSIONS for every entry folder;
the companion entries A368353 and A368354 were checked separately as well.

## Removed

- A175554: the package independently verified
  `a(5)=905697107804160`. That value, its verification comment, the Mutoh
  reference, and the extension credit are already present in approved OEIS
  revision 13, dated 2026-08-10. Its folder was therefore removed.

## Retained

None of the packaged results for the following entries was present in its
approved record at the time of the check:

```text
A000530 A001072 A002887 A003167
A005281 A005312 A005787 A006545 A007234 A007847 A009997
A075099 A202140 A273354 A306795 A323134 A323560 A337433
A343777 A358784 A363253 A365910 A368353 A368354 A368355
A380991
```

This is a submission-status audit, not a fresh validation of the mathematics
inside each retained package.
