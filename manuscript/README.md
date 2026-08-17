# Combined manuscript

The publication-ready manuscript is:

- `oeis_sequence_advancements.pdf`
- LaTeX source: `main.tex`, `references.bib`, and `sections/`
- Logo asset: `lossfunk-logo.png`

Build from this directory with:

```bash
latexmk -pdf -interaction=nonstopmode main.tex
```

or

```bash
tectonic main.tex
```

The manuscript links the public code and certificate repository:

<https://github.com/Siddhartha-Mahajan/oeis-sequences-audit>
