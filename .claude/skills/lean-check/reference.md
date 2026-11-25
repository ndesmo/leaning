# Lean reference for this project

## Environment (Windows)

- **PowerShell 5.1:** there is no `&&`; use `;` or `if ($?) { … }`. Prepend elan to the path with
  `$env:Path = "$env:USERPROFILE\.elan\bin;$env:Path"` (`check.ps1` does this).
- **Antivirus slowdown:** `import Mathlib` normally takes 35–45 s.
  - If it takes minutes with Lean at low CPU, McAfee's `mc-pco-scanner` is throttling the 8,747
    `.olean` reads.
  - Run long checks with `run_in_background` and don't restart them in a loop.
  - It clears by itself. An antivirus exclusion for `halfline_lt\.lake` is the user's call.
- **Long paths are disabled,** so the Mathlib cache fails to unpack under a long path. Keep the
  project where it is.

## Finding Mathlib names

Mathlib renames often. Grep the pinned source instead of guessing, e.g. the pattern
`theorem le_or_gt\b` in `halfline_lt/.lake/packages/mathlib/Mathlib`.

| Old name | Use instead |
|---|---|
| `le_or_lt` | `le_or_gt` |
| `exp_nat_mul` | `exp_natCast_mul` |
| `div_le_div_iff` | `div_le_div_iff₀` |
| `push_neg` on `¬ a < b` | `not_lt.mp` |

## Tactic notes

- **Hyperbolic identities:** rewrite `rpow` powers to a common base with `rpow_add_one`, then
  `linear_combination (coeff) * cosh_sq x` closes polynomial goals in `sinh`, `cosh`, `cosh ^ r`.
- **`ℝ≥0` lemmas on `ℝ`:** `lift a to NNReal using ha`, then `exact_mod_cast`.
- **Slow goals:** avoid `field_simp; ring` on big goals. Prove the identity as a separate `have`
  (`rw [sub_div, div_self …]; ring`), then `linarith`.
- **Numeric side goals:** a side goal like `r (3/2) ≠ 0` can unfold into Cauchy sequences. Prove it
  first with `have h : … := by rw [r_three_halves]; norm_num`.
- **`linarith` and products:** it treats products of atoms as atoms, so pass the product facts you
  need (`mul_le_mul_of_nonneg_left …`).
- **Limits and existence:** `Filter.Tendsto … atTop atTop` with `.eventually_gt_atTop` and
  `.exists`; near a point, use `nhdsWithin x (Set.Ioi x)` with `self_mem_nhdsWithin`.
- **Executables (`HalflineNum`):** Float literals inside loops compile to `Float.ofScientific`
  calls, so hoist them to top-level constants (about 350× faster).
