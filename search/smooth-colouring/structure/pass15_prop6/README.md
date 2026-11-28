# Pass 15: the Prop-6 test of `../pass14_struct/NOTE.md`

Status: written 2026-11-28 by a pass-15 subagent. Not reviewed.

## What Prop 6 actually asks, and what this can and cannot settle

Prop 6 is a test on **one given tiling**: its data are (T, φ, the K-fibres). There are three versions.
- **F** (the hypothesis of Prop 6): some hom f_ρ: M → Z_ρ is injective on every row.
- **L** (the "corrected candidate" in §5): some hom f_ρ with f_ρ = φ_ρ/ρ on the row-difference lattice R.
  This is one F_ρ-linear system.
- **literal**: NOTE.md's criterion, ρv ∉ R + ρM_ρ for v ∈ M minus M_ρ.

L ⇔ literal [own argument, unreviewed; also checked numerically below]. L ⇒ F ⇒ (c_{x,y}) via
Theorem 3' of pass 13.

At n = 195 there are **no tilings to feed in**: a tiling there would already make 195 satisfactory.
So running the test cannot exclude the pure-C_s part of R. Excluding R would need either a proof
that F (or L) holds for every hypothetical R-tiling at 195, or an exhaustive search over R-tilings
at 195. Neither is done here. What is done is the n = 30 analogue (H = Z4 × Z9, K = Z5, |B'| = 6).

## Files

- `prop6.py` runs, for each tiling:
  - fibre classification (pure-C with row prime ρ, or not);
  - L by linear algebra (own HNF, then Gaussian elimination over F_ρ);
  - the literal criterion (own HNF, then lattice membership);
  - an independent brute force (sympy HNF basis, then all of Hom(M, Z_ρ)) that decides L and F
    from the definitions. For every F-witness it also checks that (f_ρ, φ_σ/σ) is injective on
    every fibre, i.e. Prop 6's proof steps 1–2.

  It asserts that all three L decisions agree.
- `pick_B.py` lists the aperiodic tiles B ⊂ Z36 in the R-analogue. There are 468 with rows
  along 3 and 270 with rows along 2, the same counts as the NOTE.md table.
- `gen.sh` generates tilings with pass-13 `exp2_tn.py` for the tiles in `B_rho3.txt` and
  `B_rho2.txt`. Output goes to `gen/`.
- `diag_shift.py` lists which t are "shifted" off the majority residue in each fibre.
- Outputs: `synthetic.out`, `pass13_samples.out`, `gen_results.out`.

## Reproduction (from this directory; Python 3, sympy 1.14; about 1 minute in total)

    python prop6.py --synthetic 3 300 7  >  synthetic.out
    python prop6.py --synthetic 3 200 1  >> synthetic.out
    python prop6.py --synthetic 2 200 2  >> synthetic.out
    for f in ../pass13_mixed/exp2_n30_4x9_*.json; do for r in 2 3; do python prop6.py $f $r; done; done > pass13_samples.out
    python pick_B.py 3 6 1 > B_rho3.txt; python pick_B.py 2 4 1 > B_rho2.txt; sh gen.sh
    for f in gen/*.json; do python ../pass13_mixed/verify.py $f; done      # independent tiling check: all pass
    (for f in gen/exp2_n30_4x9_30*_r.json; do python prop6.py $f 3; done; for f in gen/exp2_n30_4x9_2*_r.json; do python prop6.py $f 2; done) > gen_results.out

## Results

1. **Control on the test itself** (`synthetic.out`): 700 random instances with C-type fibres
   that are not tilings. The three L implementations agree on all of them. Both outcomes occur.
   - For ρ = 3: 44 of 500 instances have F true but L false. So **L is strictly stronger than
     Prop 6's hypothesis**: the per-row sign freedom f_ρ = ±φ_ρ/ρ is lost.
   - For ρ = 2: L = F, as expected, since there is no sign freedom mod 2.
   - Every F-witness gives an f that is injective on every fibre.
2. **pass-13 samples** (`pass13_samples.out`).
   - `exp2_n30_4x9_1*.json` has B' with Φ_12 | B', Φ_18 ∤ B'. This is the exact analogue of
     195's pure-C_s case, with rows of 3 points.
     - All 230 tilings are pure-C for ρ = 3, as Theorem 4 predicts.
     - 108 of them have non-P-coset fibres. L holds for all 108, and F holds for all of them by
       brute force.
   - `exp2_n30_4x9_3_r.json` (Φ_18 | B', Φ_12 ∤ B') is pure-C for ρ = 2: 30 of 30, of which 14
     are non-trivial. L holds for all of them.
   - `exp2_n30_4x9_2_r.json` (S_B' = {3, 4}) is not in R, as expected.
   - The n = 105 file has 0 tilings, so there is nothing to test at |B'| = 15.
3. **New samples** (`gen_results.out`): 200 tilings over 10 new R-analogue tiles, all verified by
   pass-13 `verify.py`.
   - All 200 are pure-C for the predicted ρ.
   - 83 are non-trivial (37 with ρ = 3, 46 with ρ = 2).
   - L holds in every one, and brute-force F holds in every one.

**Caveat on the samples.** They come from random-restart DFS. The shifted points are often the
free primes 17, 19, 23, 29 (`diag_shift.py`), where L holds trivially. But some tilings
have shifts on composite t, e.g. {16, 20, 25} or {22, 28, 29}. No L or F failure was seen on any
real tiling.
