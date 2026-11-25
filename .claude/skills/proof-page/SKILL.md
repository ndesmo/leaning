---
name: proof-page
description: Write the public web page for a proof in docs/<slug>/index.html on the "Proofs by Claude" GitHub Pages site, with every step labeled by its evidence, and add it to the site index and README. Use after the Lean checks pass, or when revising a published proof page; /review comes next.
---

# /proof-page: write the proof page

Readers are mathematicians checking the work. Write for them: precise statements, short proofs,
and every step labeled so they can see what is machine-checked and what is cited.

## Start from the existing page

Copy the following from `docs/halfline-lieb-thirring/index.html`; don't restyle per proof:
- the whole `<head>`: fonts, the `:root` tokens and both dark-mode blocks;
- the masthead markup;
- the `.ev` chip classes.

Then replace the content. Every proof page keeps:
- **Masthead:**
  - an eyebrow `<a href="../">Proofs by Claude</a> · <arXiv area>`;
  - the `h1` title;
  - the byline `Claude (AI model) · <date> · Not peer reviewed`;
  - an abstract that says plainly what is proved and what stays open;
  - the status list (Method, Lean, Novelty, Review);
  - the chip legend.
- **Setting:** definitions and notation, and the prior results with their labels.
- **One section per result:**
  - a kind label (Theorem n, Corollary n);
  - the statement in italics;
  - a numbered proof. Each step ends with one or more chips:
    - `ev lean` with the theorem names in `<code>`;
    - `ev paper` with a bracketed reference key;
    - `ev std` for classical results;
    - `ev conj` for open claims.
- **What remains open:** the exact gap, plus any step whose uniformity or hypothesis is unchecked.
- **What Lean checks:**
  - the Lean version and a link to the source file on GitHub:
    `https://github.com/ndesmo/leaning/blob/main/halfline_lt/...`;
  - a result → theorem-names table;
  - the list of cited theorems that enter Lean as hypotheses.
- **References:** keyed like `[ELU14]`, with arXiv links where they exist.
- **Footer:** credits Claude, says no expert has reviewed it, and links to `../` and the repo.

## Rules

- **Numbers:** compute every number on the page with a script (PowerShell or Lean `#eval`), never by
  hand. Reuse the same values in the text and tables.
- **Figures:** inline SVG drawn by a small inline script from the real functions, to scale, with
  colors from the tokens (see the critical-envelope figure). Draw a figure only when it shows the
  mechanism.
- **External resources:** the only one allowed is Google Fonts. No scripts from CDNs, so the page
  keeps working.
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
   - Run `node --check` on the extracted inline script.
4. **Next step:** `/review`, before `/publish-proofs`.
