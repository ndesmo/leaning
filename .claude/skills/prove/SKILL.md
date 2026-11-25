---
name: prove
description: Run the full pipeline for a new result on the "Proofs by Claude" site, from problem to published page, by calling /conjecture, /literature, /attack, /lean-check, /proof-page and /publish-proofs in order. Holds the standing rules for labels, credit and claims. Use when the user asks for a new proof or the next result; use a single stage skill when only that stage is wanted.
---

# /prove: problem to published proof

These results are published at https://ndesmo.github.io/leaning/ and credited to **Claude (AI
model)**, never to the user. Every page says it is not peer reviewed.

## Standing rules (apply in every stage)

- **Label every claim** with exactly one of these:
  - `[Lean]`: proved in Lean, no `sorry`, standard axioms only.
  - `[Lean | hyp: …]`: proved in Lean from named hypotheses, which are cited theorems.
  - `[paper: ref, Thm n]`: a published theorem, checked against the paper's own text.
  - `[preprint: ref, Thm n]`: an unrefereed preprint.
  - `[standard: ref]`: a classical textbook result.
  - `[numerical ± err]`: a computed value with its error bar.
  - `[conjecture]`: open.
- **Derive; don't search.** Numerics test claims; they never prove them. Write them in Lean, not
  Python.
- **Never overclaim.**
  - The strongest novelty statement allowed is "not found in the works searched".
  - A partial result is published as partial, with the gap stated exactly.
- **Keep one notes file per result,** `notes/<slug>.md`, with sections Statement, Setting, Claims
  ledger (a table: claim | label | where), Literature, Log. Date every log entry.

## Pipeline

| Stage | Skill | Done when |
|---|---|---|
| 0. Build on what exists | read `LEDGER.md` | The user has chosen a target: an open gap (G1, G2, …), an extension of a published result, or something new. Say whether it extends an existing page or gets a new slug. |
| 1. Hypothesis | `/conjecture` | A precise statement exists, with stress-test evidence and ranked provable targets. |
| 2. Prior work | `/literature` | Every theorem to be cited is quoted verbatim with its hypotheses, and the search scope is recorded. |
| 3. Proof | `/attack` | Every target has a step-by-step proof, each step labeled, and the edge-case audit is done. |
| 4. Lean | `/lean-check` | `check.ps1` reports CLEAN and `lake build` exits 0. |
| 5. Write-up | `/proof-page` | `docs/<slug>/` is written and the index and README are updated. |
| 6. Deploy | `/publish-proofs` | The pages return 200 on the live site. |

- **Stage 0.** Open with a short menu built from `LEDGER.md`:
  - two or three open gaps or ideas, each with a one-line assessment of how tractable it looks;
  - the option of something new.
- **Extending a published result.** Keep its slug. Extend its notes file, add theorems to its Lean
  file (or a new file that imports it), and revise its page. Don't start a parallel page.
- **Skipping stage 1.** If the user already has a precise statement, or the target is a precisely
  stated gap, skip it.
- If stage 3 stalls, return to stage 1's list of provable targets rather than forcing the full
  claim.
- Before stage 6, tell the user in one line what is about to go public.
