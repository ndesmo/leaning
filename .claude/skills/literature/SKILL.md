---
name: literature
description: Check what is known about a target and extract the exact statement and hypotheses of every theorem the proof will cite, reading papers in parallel with fetch subagents that must return verbatim quotes. Records the search scope so novelty claims stay accurate. Use before attacking a problem, before citing a theorem, and before calling a result new.
---

# /literature: what is known, stated exactly

Follow the shared rules in `/prove`. Its `lessons.md` has examples for this stage.

## Search

- Start from the problem's survey and key papers. Follow citations both ways: the references, and
  the works citing them.
- Search recent preprints and the problem's terms of art.

## Read papers through subagents

Paper text fills context fast. Read each paper with its own fetch subagent, run them in parallel,
and keep only what they report. Use the `web-fetch` agent if available, otherwise
`general-purpose`.

- **Brief each agent with:**
  - the URL (an arXiv abs, ar5iv HTML or PDF link);
  - the theorem numbers wanted, or the question;
  - this instruction: *"Quote each statement verbatim, including every hypothesis (parameter ranges,
    parity, boundary conditions, integrability, sign conventions). Give the theorem number and say
    where in the paper it appears. If the text is unreadable, say so. Do not paraphrase."*
- **Spot-check the decisive hypotheses yourself.** A summary can drop the one condition that
  matters. Fetch the passage directly for any hypothesis the proof depends on.
- **Don't retry a site that refuses fetches.** If a paper won't load, record it as not accessed.

## Record in `notes/<slug>.md`, Literature section

- Each cited theorem: verbatim statement, source link, label (`[paper]`, `[preprint]` or
  `[standard]`).
- Any hypothesis check that isn't immediate.
- Known results bearing on the target.
- The search scope and what was not accessed.
- A one-line verdict on what is open. Novelty is "not found in: …".
