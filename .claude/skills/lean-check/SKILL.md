---
name: lean-check
description: Formalize and verify proof steps in the Lean 4 + Mathlib project in halfline_lt/. Covers where new Lean files go, the no-sorry and axiom audit (check.ps1), and where to find Mathlib names and known tactic and Windows pitfalls. Use whenever writing or checking Lean for a proof.
---

# /lean-check: formalize and verify in Lean

Project: `halfline_lt/`, Lean 4.37.0-rc1, Mathlib `v4.37.0-rc1`. Fixes for names, tactics and the
Windows environment are in `reference.md`, next to this file. Check it before fighting an error.

## Where Lean code goes

- **Half-line results:** `halfline_lt/HalflineLt/Spec.lean`.
- **A new result:** `halfline_lt/Proofs/<Name>.lean`, with one `namespace <Name>` … `end <Name>`.
  The audit script assumes one namespace per file. Reuse existing work with
  `import HalflineLt.Spec`.
- **First new result only:** if `Proofs.lean` does not exist yet:
  - create it;
  - add `[[lean_lib]]` with `name = "Proofs"` to `lakefile.toml`;
  - add `"Proofs"` to `defaultTargets`.
- **Every new result:** add `import Proofs.<Name>` to `Proofs.lean`.

## Conventions

- Facts Mathlib cannot express, such as spectral theorems, enter as named hypotheses (`hELU`,
  `hOne`). The docstring cites each one.
- Use one `theorem` per claim the page attributes to Lean. Its statement must say what the page
  says it does.
- No `sorry`, `axiom` or `native_decide`.

## Verify

From the repo root, in PowerShell:

```
& .\.claude\skills\lean-check\check.ps1 -File HalflineLt\Spec.lean
```

The script compiles a copy of the file with `#print axioms` for every `theorem` and `lemma`. It
reports errors, `sorry`s and any axioms beyond `propext`, `Classical.choice`, `Quot.sound`, then a
one-line summary. It exits 1 if anything is wrong.

Before publishing, also run `lake build` in `halfline_lt/`. Run both in the background, because a
build can take minutes (see `reference.md`).
