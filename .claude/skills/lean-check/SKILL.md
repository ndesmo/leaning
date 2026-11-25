---
name: lean-check
description: Formalize and verify proof steps in the Lean 4 + Mathlib project in halfline_lt/ on this Windows machine. Covers where new Lean files go, building, the no-sorry and axiom audit (check.ps1), finding Mathlib names, and known tactic and environment pitfalls. Use whenever writing or checking Lean for a proof.
---

# /lean-check: formalize and verify in Lean

Project: `halfline_lt/`, Lean 4.37.0-rc1, Mathlib `v4.37.0-rc1`.

## Where Lean code goes

- **Existing half-line results:** `halfline_lt/HalflineLt/Spec.lean`.
- **New proof:** `halfline_lt/Proofs/<Name>.lean`, with `import Mathlib`, `open Real` as needed, and
  exactly one `namespace <Name>` … `end <Name>`. The axiom script assumes one namespace per file.
- **First new proof only:** if `halfline_lt/Proofs.lean` does not exist yet, set the library up:
  - create `Proofs.lean`;
  - add `[[lean_lib]]` with `name = "Proofs"` to `lakefile.toml`;
  - add `"Proofs"` to `defaultTargets`.
- **Every new proof:** add `import Proofs.<Name>` to `Proofs.lean`.

## Conventions

- Statements are self-contained and readable. Facts that Mathlib cannot express, such as spectral
  theorems, enter as hypotheses named like `hELU` or `hOne`. The docstring cites each one.
- One `theorem` per claim in the page's Lean table. Docstrings say what the theorem means
  mathematically.
- No `sorry`, `axiom` or `native_decide` in published proofs.

## Verify

Run from PowerShell (absolute path, so the working directory doesn't matter):

```
& C:\Users\nicho\leaning\.claude\skills\lean-check\check.ps1 -File HalflineLt\Spec.lean
```

The script compiles a copy of the file with `#print axioms` appended for every `theorem` and
`lemma`. It prints:
- errors;
- `sorry` warnings;
- any theorem whose axioms go beyond `propext`, `Classical.choice`, `Quot.sound`;
- a one-line summary.

It exits 1 if anything is wrong.

Before publishing, also run `lake build` in `halfline_lt/` and confirm it exits 0.

## Environment (Windows)

- PowerShell 5.1 has no `&&`; use `;` or `if ($?) { … }`. Put `$env:Path =
  "$env:USERPROFILE\.elan\bin;$env:Path"` first; `check.ps1` already does this.
- `import Mathlib` normally takes 35–45 s. If it takes minutes with Lean at low CPU, McAfee's
  `mc-pco-scanner` is throttling the 8,747 `.olean` reads.
  - Run long compiles with `run_in_background`, and don't restart them in a loop.
  - It clears by itself. An antivirus exclusion for `halfline_lt\.lake` is the user's call.
- Never build under a long path. Long paths are disabled, and the Mathlib cache fails to unpack.

## Finding Mathlib names

Mathlib renames often, so grep the pinned source instead of guessing:

```
Grep pattern "theorem le_or_gt\b" in halfline_lt/.lake/packages/mathlib/Mathlib
```

Known renames on this pin:

| Old name | Use instead |
|---|---|
| `le_or_lt` | `le_or_gt` |
| `exp_nat_mul` | `exp_natCast_mul` |
| `div_le_div_iff` | `div_le_div_iff₀` |
| `push_neg` on `¬ a < b` | `not_lt.mp` |

## Tactic notes from this project

- **Hyperbolic identities:** `linear_combination (coeff) * cosh_sq x` closes polynomial goals in
  `sinh`, `cosh` and `cosh ^ r`, after the `rpow` powers are rewritten to a common base with
  `rpow_add_one`.
- **`ℝ≥0` lemmas on `ℝ`:** `lift a to NNReal using ha`, then `exact_mod_cast` the `NNReal` lemma.
- **Slow goals:** avoid `field_simp; ring` on big goals. Prove the identity as a separate `have` by
  `rw [sub_div, div_self …]; ring`, then finish with `linarith`.
- **Numeric side goals:** a side goal like `r (3/2) ≠ 0` can unfold into Cauchy sequences. Prove it
  first with `have h : … := by rw [r_three_halves]; norm_num`.
- **`linarith` and products:** it treats products of atoms as atoms, so pass products you need as
  hypotheses (`mul_le_mul_of_nonneg_left …`).
- **Limits and existence:** `Filter.Tendsto … atTop atTop` plus `.eventually_gt_atTop` and
  `.exists`; near a point, use `nhdsWithin x (Set.Ioi x)` with `self_mem_nhdsWithin`.
- **Executables in `HalflineNum`:** Float literals inside loops compile to `Float.ofScientific`
  calls, so hoist them to top-level constants (about 350× faster).
