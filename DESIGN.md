# Design of the proof pages

How every page on the "Proofs by Claude" site looks, and why. The `/proof-page` skill follows this
file; so should anyone writing a page by hand. The reference page is
[`docs/central-2adic/index.html`](docs/central-2adic/index.html): copy it, don't restyle.

## Principles

- **Set like a mathematics textbook.** One reading column, theorem and proof blocks, numbered
  proof steps, and the key identities as displayed equations on their own lines.
- **The mathematics reads without interruption.** Evidence (what is checked in Lean, what is cited)
  is always shown, but on its own line under each statement or step, never inside a sentence.
- **Honest by construction.** Every statement and step carries an evidence label. The layout never
  hides a caveat: novelty and review detail sit in their own section, in full.
- **Dark by default.** A toggle (top right) switches to light; the choice is remembered per browser.
- **Works everywhere.** No horizontal scrolling at 390 px. Wide equations, tables and code scroll or
  wrap inside their own box. All assets are served from the site itself, except Google Fonts.

## Files

| File | What it is |
|---|---|
| `docs/assets/proof.css` | The one stylesheet for every page: tokens, both themes, all components. |
| `docs/assets/proof.js` | Renders the maths with KaTeX and adds the theme toggle. |
| `docs/assets/katex/` | KaTeX 0.16.9, vendored unmodified (MIT licence in that folder). |

Pages contain no `<style>` block and load no other scripts. A new component goes in `proof.css`,
for every page at once.

## Page head

Copy it from the reference page. In order: the theme one-liner script (so there is no flash of the
wrong theme), the Google Fonts link, `assets/katex/katex.min.css`, `assets/proof.css`, then three
`defer` scripts: `katex.min.js`, `contrib/auto-render.min.js`, `proof.js`. Paths are relative
(`../assets/` from a proof page).

## Typography

| Role | Font |
|---|---|
| Body text | STIX Two Text |
| Mathematics | KaTeX (Computer Modern) |
| Headings, labels, chips, captions | Archivo |
| Lean code and names | JetBrains Mono |

Body text uses old-style figures; tables use lining tabular figures.

## Mathematics

- **All maths is LaTeX**, rendered by KaTeX: `\( … \)` inline and `\[ … \]` displayed. Never build
  formulas from `<var>`, `<sup>`, `<sub>` or Unicode look-alikes.
- **Display anything a reader should stop and look at:** definitions, the identity a step proves,
  each line of a chain of inequalities. Inline maths is for short symbols and expressions.
- In HTML, write `<`, `>` and `&` inside maths as `&lt;`, `&gt;` and `&amp;`.
- Notation: `\binom{n}{k}` for binomial coefficients, `\mathbb{Z}`, `\mathbb{N}`, `\mathrm{cl}` for
  upright subscripts, `\operatorname{sech}`, `\lfloor … \rfloor`.
- Maths never goes inside `<code>`; Lean names never go inside maths.

## Page structure

1. **Masthead:** eyebrow (`<a href="../">Proofs by Claude</a> · <arXiv areas>`), `h1` title, byline
   (`Claude (AI model) · <date> · Not peer reviewed`), abstract, the `.facts` list (Method, Lean,
   Novelty with the re-check date and a link to the full search record, Review), and the chip legend.
2. **Setting:** definitions, notation, the source of the problem (quoted in a `.quote` block when it
   is a conjecture), prior results with their labels, and any numerical table.
3. **One section per result:** a kind label in the `h2`, then a `.thm` block, the verbatim Lean
   statement in `pre.lean`, then the proof.
4. **What remains open:** the exact gaps.
5. **What Lean checks:** versions, source link, how the Lean statement relates to the page, and the
   result → Lean-theorem table.
6. **Novelty and review:** the full search record from the notes: what was searched, read, related,
   and not checked.
7. **References**, then the **footer**.

## Components

**Theorem block.** The statement in italics with a rule on its left; its evidence line under it.

```html
<div class="thm">
  <p><span class="head">Theorem 1.</span> For every … ,</p>
  \[ … \]
  <p class="evidence"><span class="ev lean">Lean</span> <code>Namespace.theorem_name</code></p>
</div>
```

**Proof.** A `.proof` block. The first paragraph has `class="lead"` (the stylesheet prints
"Proof."). Each step is a `.step` with a run-in heading: a number and a short title that adds no
claim. The step's text follows, with its key formulas displayed, then `∎` on the last step, then the
evidence line.

```html
<div class="proof">
  <div><p class="lead">Write … . Define</p> \[ … \] </div>
  <div class="step">
    <p class="step-head"><span class="n">Step 1</span>A power-series identity.</p>
    <p>In \(\mathbb{Z}[[X]]\) put … . Then, for every \(j\),</p>
    \[ B^{2^j} G_j(z) = 1 + X^{2^j}. \]
    <p class="evidence"><span class="ev lean">Lean</span> <code>Bz</code>, <code>G_eval</code></p>
  </div>
  …
  <p class="qed">∎</p>  <!-- inside the last step, before its evidence line -->
</div>
```

**Evidence line** (`p.evidence`): one or more chips, each followed by what it covers.

| Chip | Meaning | Followed by |
|---|---|---|
| `ev lean` | Checked in Lean | the Lean names, in `<code>` |
| `ev paper` | Cited from a paper | the reference key, e.g. `[ELU14, Cor. 1.3]` |
| `ev std` "Standard" | Classical result, cited | the reference key |
| `ev std` "Own argument" | Our argument, not formalized as stated | who reviewed it, and when |
| `ev std` "Numerical" | Computed, not a proof | what was computed, and how |
| `ev conj` | Open | — |

An evidence label never claims more than the evidence. A step that is partly in Lean says which part.

**Lean source.** `<pre class="lean"><code>…</code></pre>`, verbatim from the source file. Long lines
wrap with a hanging indent; never edit the text to fit.

**Tables** sit in `.tbl-wrap`. **Figures** are inline SVG drawn to scale from the real functions,
using the `.fig` classes and theme colours, only when they show the mechanism.

## Colour

Tokens are defined once in `proof.css`, for both themes; pages never set colours. Green is reserved
for Lean, blue for papers and links, amber for open conjectures, grey for everything else.

## Checks

- CI (`check-pages.ps1`) checks that every cited Lean name exists, and that every page uses the shared
  stylesheet and vendored KaTeX, with no inline `<style>` and no external scripts.
- Before opening a PR, load the page in a browser at desktop width and at 390 px: no KaTeX errors (red
  text), no horizontal scrolling, both themes legible.
