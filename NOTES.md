# NOTES: sharp Lieb–Thirring constant, Neumann half-line

Labels: [Lean], [Lean | hyp: …], [paper: ref, Thm], [preprint: ref, Thm],
[numerical ± err], [conjecture]. See `prompt.txt` for definitions.

## Task 0: setup (2026-11-24)

- Lean 4.37.0-rc1 (commit 0b77e129), Mathlib tag v4.37.0-rc1
  (commit 31ce06eaadf4a200c0e1407c5f10953cf606b8f8).
- Project `halfline_lt/`: library `HalflineLt` (`Basic`, `Spec`), executable `search`
  (core Lean only; placeholder `Search.lean`).
- `lake build` succeeds. The only warnings are 8 `sorry`s in `HalflineLt/Spec.lean` and one
  "consider adding `module`" hint per file importing Mathlib. Mathlib's style linters are off.
- `#print axioms` on the proved theorems of the spec shows only `propext`,
  `Classical.choice`, `Quot.sound`.
- Machine note: long paths are disabled. A project under a ~120-character path failed to
  unpack 25 Mathlib cache files; `subst` drives don't help because Lake resolves them.

## Claims ledger

| Claim | Label | Where |
|---|---|---|
| Completed square (Read–Schulz identity) and its real-exponent version | [Lean] | `Spec.lean` §1 |
| Riccati form only at m = 3; m(1) = 3; m ∈ [3/2, 2) on (3/2, 5/2] | [Lean] | `Spec.lean` §1 |
| L1 = r·Lcl; r(3/2) = 1; r(5/2) = 8/9 | [Lean] | `Spec.lean` §2 |
| r strictly decreasing on (1/2, ∞); r < 1 for γ > 3/2; r > 2/e > 1/2 | [Lean] | `Spec.lean` §2 |
| L^N_γ ≤ Lcl + L1 for γ ≥ 3/2 | [Lean \| hyp: ELU (1.6), one-bound-state bound] | `Spec.lean` §3 |
| A potential beating 2·L1 has e > 2 − 1/r(γ) (7/8 at γ = 5/2) | [Lean \| hyp: ELU (1.6)] | `Spec.lean` §3 |
| (a)–(d) in abstract form | [Lean \| hyp: spectral facts] | `Spec.lean` §4 |
| ∫_ℝ V(\|x\|)^p = 2 ∫_0^∞ V^p | [Lean] | `Spec.lean` §4 |
| Soliton bonus factors at γ = 3, 5 | [Lean] | `Spec.lean` §6 |
| Conjecture: L^N_γ = 2·L1(γ) on [3/2, 5/2] | [conjecture] | — |

## Open `sorry`s (8, all Task 3)

`L1_one`, `L1_two`, `two_L1_one_bounds`, `two_L1_two_bounds`, `pt_ground_state`,
`pt_second_even_state`, `pt_second_even_state_sq_integrable`, `sech2_family_opt`.
