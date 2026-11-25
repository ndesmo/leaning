---
name: conjecture
description: Find a problem worth proving and turn it into a precise, tested conjecture with provable partial targets. Covers mining open problems and paper remarks, stating the claim exactly, trying hard to break it with Lean numerics and explicit families, and recording the evidence. Use when choosing the next result or forming or testing a hypothesis.
---

# /conjecture: find, state and stress-test a hypothesis

The output is an entry in `notes/<slug>.md` that says what to try to prove, why it should be true,
how hard it was attacked, and which weaker statements are within reach.

## 1. Where to look

- **This repo first.** Read `LEDGER.md`:
  - its open gaps and ideas are ready-made targets;
  - its failed approaches tell you what not to repeat;
  - its published results suggest extensions: a wider class, another boundary condition, the next
    parameter range.
- **Explicit open questions:** survey papers (for Lieb–Thirring, Schimmer's "The state of the
  Lieb–Thirring conjecture", arXiv:2203.06051), and remarks like "it would be interesting to know
  whether…". Demirel-Frank's Remark (4) led to Corollary 2.
- **Edges of known results:**
  - a theorem proved for one range of parameters, asked for the next range;
  - a non-sharp constant;
  - a case the authors excluded.
- **Equality cases and explicit families:** what is the optimizer, and where does it stop being one?
  The half-soliton stops at γ = 5/2, and that edge is a resonance.
- Prefer problems where some piece is checkable in Lean: explicit functions, inequalities,
  algebra, limits.

## 2. State it exactly

Write down:
- the statement;
- every hypothesis and parameter range;
- the conjectured optimizer or extremal case;
- the claimed sharp constant as a formula;
- where you expect it to **fail**. A conjecture with no known failure boundary is usually stated too
  loosely.

## 3. Try to break it

- **Closed forms first.** Evaluate the claim exactly on explicit families wherever possible. Lean
  `norm_num` or `#eval` is a proof for those cases, so label them `[Lean]`, not numerics.
- **Numerics in Lean.** Use the `HalflineNum` pattern (`Solver`, `Optim`, the `search` executable)
  for families no closed form covers. Write families aimed at the likely failure mode:
  - two wells;
  - a bump plus a tail;
  - perturbations of the optimizer.
- **Grid checks.** Use two grids and Richardson extrapolation, and report every value as
  `[numerical ± err]`. Grid artifacts have produced fake counterexamples before. Penalize them in
  the objective.
- **Confirm the failure side.** Check that the claim does fail where you predicted, e.g. that
  γ = 3 beats 2L1. This validates the solver.
- **Record falsified variants** in the notes too. They mark the boundary.

## 4. Extract provable targets

Most of what gets published is partial. Before moving on, list statements weaker than the
conjecture that look provable now:
- an improved bound obtained by combining published inequalities (Theorem 1);
- the conjecture on a natural subclass (Theorem 3: potentials under a critical envelope);
- necessary conditions a counterexample must satisfy (Corollary 4);
- the endpoint or a limiting case.

## Output

- **Notes entry:**
  - the statement labeled `[conjecture]`;
  - the evidence with labels;
  - the attempts to break it and the predicted failure boundary;
  - the ranked list of provable targets.
- **Hand-off:** pass these to `/literature`, then `/attack`.
