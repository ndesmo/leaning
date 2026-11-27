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
  - the status list (Method, Lean, Novelty, Review). Novelty gives the re-check's date and scope;
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
4. **Next step:** `/review`, before `/publish-proofs`. The reviewer checks that the novelty
   re-check is recorded in the notes and dated within the last week.
