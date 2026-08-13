# An all-n formula for A000530

Put `N=2*n-1`. For `r>=1`, define

```text
q_N(r) = #{(x_1,...,x_r) in Z_{>0}^r :
           Sum_i x_i + max_i x_i <= N},
```

and put `q_N(0)=1`. Then

```text
a(n) = 1
       + Sum_{r>=1} q_N(r)^2
       + Sum_{r>=0} q_N(r)*q_N(r+1).                 (1)
```

All sums are finite: `q_N(r)=0` for `r>=N`.

## Explicit binomial sum

Let

```text
B(r,m,T) = Sum_{j=0..r} (-1)^j*binomial(r,j)
                         *binomial(T-j*m,r),          (2)
```

where a binomial coefficient is zero when its top argument is smaller than
its bottom argument or is negative. For `r>=1`,

```text
q_N(r) = Sum_{m=1..floor((N-r+1)/2)}
         (B(r,m,N-m)-B(r,m-1,N-m)).                 (3)
```

Equations (1)--(3) are therefore an explicit finite all-`n` formula involving
only integer arithmetic and binomial coefficients.

## Proof

Call a binary word safe when, for both symbols `s`, its number `c_s` of
occurrences plus its longest `s`-run `m_s` is at most `N`. Safe words form the
internal vertices of a finite rooted binary tree. Appending a bit to a safe
word either remains safe or produces a first hit. Every internal vertex has
two children, so if the number of safe words is `S_n`, the tree has `S_n+1`
terminal children. Bit complementation pairs terminals ending in zero with
terminals ending in one. The former are precisely the words counted by
A000530, hence

```text
a(n)=(S_n+1)/2.                                    (4)
```

If a symbol occurs in `r` runs, its ordered run-length vector is a positive
`r`-tuple whose sum is `c_s` and whose maximum is `m_s`. It is safe exactly
when that vector is counted by `q_N(r)`. A nonempty binary word either has the
same number `r` of zero- and one-runs (two choices of first symbol), or has
`r+1` runs of one symbol and `r` of the other (two choices of the majority-run
symbol). Therefore

```text
S_n = 1 + 2*Sum_{r>=1} q_N(r)^2
          + 2*Sum_{r>=0} q_N(r)*q_N(r+1).
```

Combining this with (4) gives (1).

For (3), classify a positive `r`-tuple by its maximum `m`. The number with
all parts at most `m` and sum at most `T` is `B(r,m,T)`: subtract one from
each part, add a slack variable, and apply inclusion-exclusion to the `r`
upper bounds. Taking the difference between maxima at most `m` and at most
`m-1`, with `T=N-m`, gives (3).

## Verification

`scripts/formula.py` implements (1)--(3). It agrees term-for-term with the
independently derived state DP for every `n<=50`:

```bash
python3 scripts/formula.py --max-n 50 \
  --compare certificates/dp_n1_n50.json \
  --output build/formula_n1_n50.json
```

This comparison audits the implementation; the proof above establishes the
formula for every positive `n`.
