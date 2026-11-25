---
name: conjecture
description: Find a problem worth proving and turn it into a precise, stress-tested conjecture with ranked provable partial targets. Covers mining LEDGER.md and the literature for targets, stating the claim exactly, trying to break it with closed forms and Lean numerics, and recording the evidence. Use when choosing the next result, or forming or testing a hypothesis.
---

# /conjecture: find, state and stress-test a hypothesis

Follow the shared rules in `/prove`. Its `lessons.md` has examples for this stage.

## Find a target

- **This repo first.** In `LEDGER.md`:
  - the open gaps and ideas are ready-made targets;
  - published results suggest extensions (a wider class, another boundary condition, the next
    parameter range);
  - the failed approaches say what not to repeat.
- **Elsewhere:**
  - open questions in surveys, and remarks in papers ("it would be interesting to know…");
  - edges of known theorems: the next parameter range, a non-sharp constant, an excluded case;
  - the point where a known optimizer stops being optimal.
- Prefer targets with pieces Lean can check.

## State it exactly

Write down:
- the statement, every hypothesis and parameter range;
- the conjectured extremal case and constant;
- where it should **fail**.

## Try to break it

- **Closed forms first.** Evaluate the claim exactly on explicit families. Results checked with
  Lean `norm_num` or `#eval` are `[Lean]`.
- **Then numerics in Lean.** Follow the `HalflineNum` pattern, with families aimed at the likely
  failure mode. Use two grids with extrapolation and report every value with an error bar.
- **Validate the method.** Confirm it detects failure where failure is predicted.
- **Record falsified variants.** They mark the boundary.

## Output

Write a notes entry containing:
- the statement, labeled `[conjecture]`;
- the evidence;
- the failure boundary;
- a ranked list of weaker statements that look provable now: an improved bound, a subclass,
  necessary conditions for a counterexample, an endpoint.
