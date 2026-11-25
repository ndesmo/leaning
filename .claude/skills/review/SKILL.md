---
name: review
description: Independent adversarial review of a proof page before publishing. Runs two fresh subagents that see only the page, the cited theorem statements and the Lean source, never the derivation, and hunt for mathematical errors, unmet hypotheses, Lean-statement mismatches and overclaims. Every finding must be fixed or rebutted. Required before /publish-proofs, and useful on any published page.
---

# /review: independent check before publishing

No human reviews this site, so this is the main check. It works only if the reviewers are not
anchored on the author's reasoning: give them the code and the page, never the derivation or the
conclusions you expect.

## Inputs to hand over

Pass file paths, not summaries:
- the page, `docs/<slug>/index.html`;
- the Literature section of `notes/<slug>.md`, which holds the verbatim cited statements;
- the Lean file or files the page names.

Do **not** pass the notes' Log, the derivation, or your opinion of which parts are solid.

## Run two reviewers in parallel

Use the `general-purpose` agent for both, in one message.

1. **Mathematics.** *"You are refereeing this proof. Check every step.
   - Inequality directions; division by quantities that could be zero or negative.
   - Whether each cited theorem's hypotheses (quoted in the notes) are actually met in this
     setting.
   - Edge cases: parameter endpoints, degenerate inputs, infinite spectra, both directions of each
     equality case.
   - Hidden uniformity or limit-exchange assumptions.
   - Whether the 'What remains open' section omits anything the proof silently assumes.
   Report only concrete problems."*
2. **Claims and Lean.** *"Check that the page claims no more than is shown.
   - For every Lean theorem name on the page, find it in the Lean source and say whether its
     statement actually establishes what the page says it does. Mismatched hypotheses, special
     cases sold as general and missing conditions all count.
   - Check that every step carries an evidence label, that novelty claims are limited to the
     search scope, and that the numbers in the text and tables agree.
   Report only concrete problems."*

Ask each reviewer to return a list. For each finding: location, the claim, why it is wrong or
unsupported, how severe it is (blocks publishing, or fix wording), and a suggested fix. If nothing
is wrong, an empty list.

## Handle the findings

- **Verify each finding.** Reviewers can be confidently wrong.
- **Fix or rebut every one.** Either fix it (page, Lean or notes), or rebut it in the notes' Review
  section with the reason.
- **If a fix changed a theorem statement or a proof step,** rerun `/lean-check`. Run one more
  review on the changed sections only, then stop. Don't loop.
- **Record the review.** Add a dated entry to the notes' Review section: the findings, what was
  fixed, what was rebutted and why.
