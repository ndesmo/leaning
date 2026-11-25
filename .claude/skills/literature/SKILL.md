---
name: literature
description: Check what is already known about a conjecture or target theorem, and extract the exact statements of every theorem the proof will cite, from the sources themselves. Records search scope and supports a careful novelty claim. Use before attacking a problem, before citing any theorem, and before claiming a result is new.
---

# /literature: what is known, stated exactly

## Search

- Start from the problem's survey and its key papers. Follow citations both ways: references, and
  works citing them (Semantic Scholar lists citing works).
- Run web searches on the problem's terms of art, covering the last 10–15 years and recent preprints.
- Check the obvious places a result could hide, such as a book's comments sections or a remark after
  a theorem. Record which of them you could not access.

## Extract each theorem you will use

- **Read the source itself.** Fetch the arXiv abstract, the ar5iv HTML or the PDF. Write into
  `notes/<slug>.md`:
  - the theorem's number;
  - its verbatim statement;
  - every hypothesis: parameter ranges, parity, boundary conditions, integrability, sign
    conventions.
- **Check that it applies.** Confirm your setting meets each hypothesis. Write the check down when
  it isn't immediate. Example: ELU's Cor. 1.3 is lifted from γ = 3/2 by Aizenman–Lieb, which needs
  the weights to be ≥ 0.
- **Label by source.** Refereed sources are `[paper]`, unrefereed ones `[preprint]` (say so on the
  page), and textbook facts `[standard]`.

## Novelty

- Write the conclusion as "not found in: <list of works searched>", plus the list of works not
  accessed.
- If a result turns up in the literature, record it as known and cite it. The page can still give a
  proof, but it must not claim the result as new.
- Watch for loose statements in papers, e.g. "for all N" that cannot include N = 1. Note them, but
  don't build on them.

## Output

The notes' Literature section contains:
- the known results with labels;
- the cited theorems, verbatim;
- the search scope and what was not accessed;
- a one-line verdict on what is open.
