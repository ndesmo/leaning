# Proofs by Claude

Mathematical results found and proved by Claude, an AI model made by Anthropic. Steps that can be
checked by machine are verified in Lean 4 with Mathlib; steps that rest on published theorems cite
them. Nothing here has been peer reviewed.

**Site:** https://ndesmo.github.io/leaning/

## Proofs

| Date | Proof | Lean |
|---|---|---|
| 2026-11-25 | [Sharp Lieb–Thirring bounds on the Neumann half-line](https://ndesmo.github.io/leaning/halfline-lieb-thirring/) ([RESULTS.md](RESULTS.md)) | [`halfline_lt/HalflineLt/Spec.lean`](halfline_lt/HalflineLt/Spec.lean) |

## Layout

- [`LEDGER.md`](LEDGER.md) indexes every result, the reusable Lean lemmas, the open gaps and the
  approaches that failed.
- `docs/` is the GitHub Pages site. `docs/index.html` lists the proofs, and each proof has its own
  folder, `docs/<slug>/index.html`.
- `halfline_lt/` is the Lean project (Lean 4.37.0-rc1, Mathlib v4.37.0-rc1).
- `RESULTS.md` holds the half-line statements and proofs; `notes/<slug>.md` is each result's working log; `results/` holds
  numerics output.

## Checking the Lean

```
cd halfline_lt
lake exe cache get
lake build
```

The build should report no `sorry`. `#print axioms` on each theorem shows only `propext`,
`Classical.choice` and `Quot.sound`. Spectral theorems that Mathlib lacks enter the Lean statements
as explicit hypotheses; each proof page says which ones.

## Adding a proof

1. Put the write-up in `docs/<slug>/index.html`, labeling each step as Lean, paper or standard.
2. Add an entry at the top of the list in `docs/index.html` and a row to the table above.
3. Push to `main`; the site updates within a few minutes.
