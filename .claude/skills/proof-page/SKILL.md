---
name: proof-page
description: Write the public web page for a proof in docs/<slug>/index.html on the "Proofs by Claude" GitHub Pages site, with every step labeled by its evidence, and add it to the site index and README. Use after the Lean checks pass, or when revising a published proof page; /review comes next.
---

# /proof-page: write the proof page

Readers are mathematicians checking the work. Write for them: precise statements, short proofs,
and every step labeled so they can see what is machine-checked and what is cited.

## Re-check novelty first

Do this before writing the page, and again before updating a page that adds a result. A literature
pass from weeks ago is not enough, because new preprints and comments appear all the time.

1. **Search again.** Repeat the search recorded in the notes' Literature section, with the same
   sources plus anything new: the problem's source (paper, OEIS entry, forum thread) and its
   history, arXiv, the web, MathOverflow and Math.SE. Look for anything posted since the last
   search date.
2. **Read the sources not yet read.** Any source the notes list as "not accessed", "not checked"
   or "paraphrase only" that could already contain or imply the result: read it now (with
   `/literature`), or record why it cannot be read.
3. **Record it in the notes:** the date, the scope, what was found and a verdict for each source,
   with verbatim quotes for anything relevant.
4. **Act on it.**
   - An earlier proof found: credit it on the page, in the abstract and the Novelty line, and
     describe our work as an independent proof (plus a Lean formalization, if there is one).
     Never as new. Update `LEDGER.md` the same way.
   - A source that implies the result: say so where the result is stated.
   - A source that could not be read: name it on the page.

The page's **Novelty** line states the search date and scope, for example "Not found in the works
searched (OEIS, arXiv, MathOverflow; 2026-11-27)".

## Follow DESIGN.md

Read [`DESIGN.md`](../../../DESIGN.md) first; it is the design specification, and
`docs/central-2adic/index.html` is the reference page. Copy that page and replace the content. Don't
restyle per proof: there is one stylesheet (`docs/assets/proof.css`), and a new component goes there.

The essentials, set like a mathematics textbook:
- **All maths in LaTeX** (`\( … \)`, `\[ … \]`), rendered by the vendored KaTeX. Never `<var>`,
  `<sup>` or Unicode look-alikes for formulas. Display every identity a reader should stop at.
- **Statements** in a `.thm` block; the verbatim Lean statement in `pre.lean`.
- **Proofs** as numbered `.step` blocks, each with a short run-in title, its key formulas displayed
  on their own lines, and its evidence on a separate `p.evidence` line, never inside a sentence:
  - `ev lean` with the theorem names in `<code>`;
  - `ev paper` with a bracketed reference key;
  - `ev std` for classical results, own arguments and numerical checks;
  - `ev conj` for open claims.
- **Sections in order:** masthead (eyebrow, title, byline `Claude (AI model) · <date> · Not peer
  reviewed`, abstract saying plainly what is proved and what stays open, the `.facts` list Method /
  Lean / Novelty / Review, the chip legend), Setting, one section per result, What remains open, What
  Lean checks (versions, source link `https://github.com/ndesmo/leaning/blob/main/halfline_lt/...`,
  result → theorem table, cited theorems that enter Lean as hypotheses), Novelty and review (the full
  search record), References (keyed like `[ELU14]`, arXiv links where they exist), footer (credits
  Claude, says no expert has reviewed it, links to `../` and the repo).

## Rules

- **Numbers:** compute every number on the page with a script (PowerShell or Lean `#eval`), never by
  hand. Reuse the same values in the text and tables.
- **Figures:** inline SVG drawn by a small inline script from the real functions, to scale, with
  colors from the tokens (see the critical-envelope figure). Draw a figure only when it shows the
  mechanism.
- **External resources:** the only one allowed is Google Fonts. KaTeX is vendored in
  `docs/assets/katex/`; no scripts from CDNs, so the page keeps working.
- **Wording:** plain, active sentences; no hype. "Not found in the works searched", never "new" on
  its own.
- **Credit and privacy:** follow the shared rules in `/prove`.

## Add it to the site

1. **Index:** in `docs/index.html`, copy the existing `<li class="entry">` to the top of
   `<ol class="entries">`. Fill in the date, field, title link `<slug>/`, a two-sentence summary,
   status chips and links (Read the proofs, Lean source, Working notes `notes/<slug>.md`).
2. **README:** add a row at the top of the table in `README.md`.
3. **Check:**
   - Count open and close tags for `div`, `section`, `ol`, `ul`, `li`, `table`, `span` and `p`.
   - Run `node --check` on any extracted inline script.
   - Run `.claude/skills/lean-check/check-pages.ps1`: it checks the Lean names and the design rules.
   - Serve `docs/` (`python -m http.server --directory docs`) and load the page in a browser, if you
     have one, at desktop width and at 390 px: no red KaTeX errors, no horizontal scrolling, both
     themes legible. Say in the PR whether you did this.
4. **Next step:** `/review`, before `/publish-proofs`. The reviewer checks that the novelty
   re-check is recorded in the notes and dated within the last week.
