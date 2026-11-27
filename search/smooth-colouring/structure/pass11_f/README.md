# Pass 11 (f): do the Lemma-S′ violators carry an admissible f?

Not /reviewed. p = 2 throughout, so the admissible f is unique: f(x − y) = 1 on every block.

## Result

All violators of S′ from the exhaustive pass-10 sweep (`../pass10_sweep/ck/exh_{54,58,60}_2.ck`) were tested.

| (n,p) | bound v_2(m) | violators | no admissible f | min level 0 | min level 1 |
|---|---|---|---|---|---|
| (54,2) | 0 | 1936 | 1834 | 72 | **30** |
| (58,2) | 0 | 86 | 86 | 0 | 0 |
| (60,2) | 1 | 16 | 16 | 0 | 0 |

- **The per-partition level bound is false.** There are 30 partitions of T_54 whose admissible f
  has minimal level 1 > v_2(27) = 0. So S″ (S′ restricted to g that carry an admissible f) is
  false, and Prop. 1 plus any exp-Γ_p bound cannot give "level ≤ v_p(n/p)" partition by partition.
- **The per-n statement is not refuted at n = 54.** T_54 has level-0 solutions (the 72 records
  above), so "(b_i) for some i ⇒ (b_{v_p(n/p)})" still holds there. It would only be refuted by
  an n where every solvable partition needs level > v_p(n/p).
- Certificate: `cex_level1_T54.json`, with
  g = (3,5,11,23,3,23,22,10,21,4,5,7,12,18,20,24) mod 27 and
  F = (2,0,2,1,0,3,2,2,0,1,2,1,2,0,2,0) mod 4 on the primes 2..53.
  - ψ = (F, g) solves (b_1^2). The colouring with 54 colours gives a, 2a, …, 54a distinct
    colours for every a ≤ 20000.
  - Level 0 is impossible, and this can be checked by hand. The blocks {1,51}, {5,12}, {27,32},
    {30,49}, {17,25} are 5 (odd) blocks whose ratio product (51·12·32·49·25)/(1·5·27·30·17) is a
    rational square. So the sum of their differences is in 2Z^k, and f would have to take the
    value 5 ≡ 1 there, which is impossible at level 0.

## Reproduce (from this directory; about 3 min total)
    python fcheck.py w176 ../pass8_level/runs/w_176_2_L3.json   # sanity: min level 3 (also L4 file -> 3)
    python fcheck.py w176 ../pass8_level/runs/w_184_2_L2.json   # sanity: 2
    python fcheck.py w162 ../pass8_level/runs/w162_hd81_gtile7.txt  # sanity p=3, witness f: 3
    python mkcerts.py ../pass10_sweep/ck/exh_54_2.ck 1 certs_54_2.json
    python mkcerts.py ../pass10_sweep/ck/exh_58_2.ck 1 certs_58_2.json
    python mkcerts.py ../pass10_sweep/ck/exh_60_2.ck 2 certs_60_2.json
    python verify.py certs_54_2.json 3000; python verify.py certs_58_2.json; python verify.py certs_60_2.json
    python verify.py cex_level1_T54.json 20000

## Scripts
- `fcheck.py` finds the minimal level for each g. It solves F(d) = 2^i (mod 2^{i+1}) on the block
  differences using its own Smith form over Z/2^{i+1}. For every level it outputs either an
  explicit F or a dual certificate c, where c·D ≡ 0 (mod 2^{i+1}) and Σc is odd.
- `mkcerts.py` also computes the exact integer left kernel of D, using integer row reduction with
  a unimodular transform. "No f" means some exact relation c·D = 0 has odd Σc. This test does not
  depend on Prop. 1, and it agrees with fcheck on all 2038 records (asserted).
- `verify.py` is the independent checker. It imports nothing from the other two scripts and
  checks every record from the definitions:
  - the fibres;
  - the exact relations;
  - injectivity of ψ and the coset condition;
  - level 0 impossible, by F_2 rank of [D | 1] and by the stored certificate;
  - the tiling of Z_4 × Z_27;
  - the colouring condition for all a ≤ A.
  Mutation tests (a corrupted F, a false level 0, a corrupted relation) are all rejected.
