# Pass 10: exhaustive T_n sweep n = 44 … 60, and T_195 search

Status: written 2026-11-27 (explorer pass 10, computational). Not /reviewed.

## Headline: conjecture S′ is false for T_n itself

**T_54, p = 2, m = 27** (v_2(27) = 0), `cex_T54_p2.json`:
g = (3, 25, 22, 13, 24, 13, 9, 15, 2, 5, 6, 8, 10, 14, 17, 21) on the primes 2 … 53.
Γ = Z^16/M is finite of order 54, so Γ_2 = Z_2 ≠ 0.
- Hand-checkable certificate: h = v_7 + v_13 + v_37 + v_43 mod 2 is constant on every block.
  Its support {7, 13, 14, 21, 26, 28, 35, 37, 39, 42, 43, 52} is the union of the blocks
  {7,13}, {14,26}, {21,39}, {28,52}, {35,37}, {42,43}. Since rank_Q M = 16, h has no lift to Z.
- Verified three ways: `lems.rs`; `../pass9_lemmaS/check_indep.py` (sympy SNF over all pairs);
  and `tiny_check.py`, written fresh from the definition with no sympy (exact Fraction rank 16,
  F_2 rank 15, index 54).

All 1936 T_54 violators and all 86 T_58 violators (p = 2, m = 29) were confirmed by both
independent checkers. At n = 60, p = 2 (bound v_2(30) = 1), there are 16 maps with exp Γ_2 = 4.
check_indep confirms exponent 4. tiny_check confirms only Γ_2 ≠ 0, because M has rank 16 < 17
and it computes no exponent.

All violations so far have p = 2.

## Sweep table [numerical: lems.rs; it reproduces the pass-9 Python histograms exactly for n ≤ 44]

Counts are up to the unit symmetry on g(2). Values are histograms of log_p exp(Γ_p).

| n | p | bound | solutions | histogram | viol |
|---|---|---|---|---|---|
| 44 | 2 | 1 | 583887 | 0:59296 1:524591 | 0 |
| 44 | 11 | 0 | 15333 | 0:all | 0 |
| 45 | 3 | 1 | 1236515 | 0:28458 1:1208057 | 0 |
| 45 | 5 | 0 | 468616 | 0:all | 0 |
| 46 | 2 | 0 | 1360296 | 0:all | 0 |
| 46 | 23 | 0 | 337 | 0:all | 0 |
| 48 | 2 | 3 | 13912500 | 0:1451196 1:403596 2:268473 3:11789235 | 0 |
| 48 | 3 | 0 | 12098204 | 0:all | 0 |
| 49 | 7 | 1 | 668844 | 0:2133 1:666711 | 0 |
| 50 | 2 | 0 | 4568550 | 0:all | 0 |
| 50 | 5 | 1 | 4216400 | 0:44045 1:4172355 | 0 |
| 51 | 3 | 0 | 3680061 | 0:all | 0 |
| 51 | 17 | 0 | 6672 | 0:all | 0 |
| 52 | 2 | 1 | 1979974 | 0:79768 1:1900206 | 0 |
| 52 | 13 | 0 | 48175 | 0:all | 0 |
| **54** | **2** | **0** | 7314726 | 0:7312790 **1:1936** | **1936** |
| 54 | 3 | 2 | 21713913 | 0:277602 1:992203 2:20444108 | 0 |
| 55 | 5 | 0 | 3968473 | 0:all | 0 |
| 55 | 11 | 0 | 158363 | 0:all | 0 |
| 56 | 2 | 2 | 5333609 | 0:128872 1:29057 2:5175680 | 0 |
| 56 | 7 | 0 | 2898705 | 0:all | 0 |
| 57 | 3 | 0 | 4605315 | 0:all | 0 |
| 57 | 19 | 0 | 6906 | 0:all | 0 |
| **58** | **2** | **0** | 7192618 | 0:7192532 **1:86** | **86** |
| 58 | 29 | 0 | 687 | 0:all | 0 |
| **60** | **2** | **1** | 81583240 | 0:1955020 1:79628204 **2:16** | **16** |
| 60 | 3 | 1 | — | INCOMPLETE: 345 tasks done in `ck/exh_60_3.ck` (no violation among them) | — |
| 60 | 5 | 0 | — | not started | — |

Complete: every (n, p) with 44 ≤ n ≤ 58, and (60, 2). Full lines are in `sweep_out.txt`.
Samples were cross-checked with check_indep.py, with 0 disagreements: 120 samples each for
(48,2), (54,3) and (50,5), and 94 for (49,7), stratified by exponent (`xc_*.json`).

## T_195 [numerical: lems.rs single implementation; sampling, NOT exhaustive]

The Knuth tree-size estimator (`lems est 195 p 2000 7 [h]`, 2000 probes) gives, after the
25-prime reduction:
- p = 3: about 3·10^27 nodes for g, and about 6·10^27 for the joint (g, h) tree.
- p = 5: about 2·10^29 for g, and about 1·10^29 for (g, h).
- p = 13: about 1·10^26 for g, and about 1·10^25 for (g, h).

Exhaustive search is infeasible by more than 15 orders of magnitude.

Sampling results:
- `rand`, p = 13: 99952 samples, all Γ_13 = 0.
- `rand`, p = 5: 5778 samples (run killed early), all Γ_5 = 0.
- `trand` (joint (g, h), h ≠ 0 block-constant), p = 13: 2228 restarts gave 1711 hits, all with
  Γ_13 = 0 (killed early).
- p = 3 was not run this pass.

The sampling is biased (randomized DFS), so this is weak evidence.

## Reproduce (from this directory)
    rustc -O -C target-cpu=native lems.rs -o lems.exe
    sh sweep.sh 44 60          # resumable; checkpoints ck/exh_<n>_<p>.ck (lines T = finished task)
    python mk_samples.py ck/exh_54_2.ck x.json 200 && python ../pass9_lemmaS/check_indep.py x.json
    python tiny_check.py cex_T54_p2.json
    ./lems.exe est 195 13 2000 7 h
    sh run195.sh               # n=195 rand/trand batches -> n195/
To resume n = 60, p = 3, run `./lems.exe exh 60 3 20 ck/exh_60_3.ck 4`. The depth argument
must stay 4, because task ids depend on it.

## Consequence
S′ (Lemma S for shifted downsets) fails already on T_54. So no proof of the pass-8 level bound can
go through S′ for all g. Two open questions:
1. Do the violators carry an admissible f (the only case pass 8 needs)?
2. Do violations ever occur for odd p (none seen for n ≤ 60)?

The n = 195 exclusion still rests on the explicit level-1/2/3/4 NONE searches.
