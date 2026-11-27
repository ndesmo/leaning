# search/smooth-colouring (P11, issue #31)

Problem: can ℤ⁺ be coloured with n = 195 colours so that a, 2a, …, na always get distinct colours?
The journal is in [notes/smooth-colouring.md](../../notes/smooth-colouring.md).

## Reformulation used by all searches

Write S ⊂ ℤ^k for the exponent vectors of 1, …, n (k = π(n)). Then a colouring exists iff S tiles
ℤ^k by translation (Wang–Wang, arXiv:2609.15081, Prop. 2.1; and CCP). A **periodic** tiling is
given by a homomorphism φ: ℤ^k → G (G finite abelian) that is injective on S, with
φ(S) ⊕ B = G. Then the colour of x is the unique a ∈ A = φ(S) with φ(x) + a ∈ B. This is valid
whenever (−A) ⊕ B = G, and the checker tests that directly.
- |B| = 1 gives the multiplicative (lattice) colourings.
- |B| = p > 1 gives "non-lattice" periodic colourings.

## Directories

- `multiplicative/`: exhaustive search for homomorphisms ℤ⁺ → G, |G| = n, that are injective on
  {1..n}. Build with `rustc -O search.rs -o search.exe` (`search2.exe` is the same source).
  - `out/scan_*.txt` holds one line per n. Every YES line carries a witness, checked by
    `check_colourings.py`.
  - n = 195 is NO, agreeing with CCP. Other NO values ≤ 250: 205, 211, 212, 214, 217, 218, 220,
    227, 229, 235, 242, 244, 246, 247, 248.
  - `minimise_primes.py` shows that the primes ≤ 47 already force NO at n = 195 (`out/minimal_P.txt`).
- `periodic/kper.rs`: search for φ: ℤ⁺ → ℤ_{np}, for p ‖ n, injective on {1..n}, such that
  φ({1..n}) ⊕ {0, q, …, (p−1)q} = ℤ_{np}, where q = n/p. This tests a cyclic quotient and a
  complement of size p.
  - **Exactly what the code tests** is stronger than the tiling: for distinct a, b ≤ n,
    φ(a) − φ(b) ∉ qℤ_N \ nℤ_N. This implies the tiling by {0, q, …, (p−1)q}.
  - The header cites a "Prop. 3" saying this class is exactly the non-lattice tilings of index p.
    That proposition was in a README lost when the first pass was interrupted. It is **unverified**,
    so a NONE result rules out only the class the code tests.
  - Build with `rustc -O kper.rs -o kper.exe`.
  - Run with `kper n=195 p=3 threads=20`.
  - `check_tiling_colouring.py n "<solution line>"` is the independent checker. It checks the
    tiling and then the colouring itself, straight from the definition, for all x ≤ 5000.
  - Sanity checks pass: n = 12 (p = 3) and n = 30 (p = 5) give solutions that the checker accepts.
  - Results are in `out/kper_runs.txt`.
- `general/gtile.rs`: a general periodic search. It looks for φ: ℤ⁺ → G = ℤ_{d1}×…, with
  φ([n]) ⊕ B = G, for one given B or for all |B| = 3 classes (`B=all3`).
  - Build with `rustc -O gtile.rs -o gtile4.exe` (output files were produced by gtile4).
  - Run with `gtile4 n=195 dims=9,5,13 B=all3 dil=1 limit=1000000000 slice=i/10`.
  - `dil=1` adds the dilation constraints t(B−B), for t coprime to |B|. `limit` caps nodes per B
    (TIMEOUT).
  - `check_general.py n dims B "<solution line>"` is the independent checker; use the `Bused=`
    printed on the solution line.
  - Results: `general/out/m3_{cyc,nc}_*.txt`, one line per B class. `out/old_unsound_sym/` is a
    superseded run with a symmetry bug; do not use it.
- `general/gtile5.rs` (pass 2): an exact search for |B| = 3 after reducing to B ⊂ the 3-Sylow
  subgroup. Run it with `run5.sh <Hdims> <B> <threads> <limit>`. `st1.rs` is a fibre-only test.
  `pass2.py` is an abandoned gtile4 driver; its outputs are `out/m3_pass2_{cyc,nc}.txt`, which
  you should ignore.
- `local/sa.rs` (pass 2): simulated annealing. Calibration failed (see the journal), so its
  output is not evidence of anything.
- `structure/pass2.md`: Lemma A, cited statements, and the obstructions to Wang–Wang §4.3 at
  three primes.
- `general/gtile6.rs` (pass 3): an exact search for |B| = p, p ∈ {5, 13}, after reducing to
  B ⊂ H (|H| = p²). Run it with `run6.sh <tag> <N> "<args>"`. `tiles_p2.py p` enumerates the
  tile classes of H. The summary is in `general/out/m5_summary.txt`.
- `structure/puretype_search.py` and `puretype_check.py` (pass 3): the mixed-type character
  certificate, `cert_N195_1_2_14.json`. Notes are in `structure/pass3_puretype.md`.
- `general/gtile7.rs` (pass 5): gtile6 with coset mode extended to Z_{p^{i+1}} (levels (b_i^p) of
  `structure/composite_B.md`). Run it with `run7.sh <tag> 20 "n=195 p=3 hd=27 mode=coset limit=…"`.
  Results are in `general/out/m{9_Z27,25_Z125,27_Z81}_coset_n195.txt`.
- `independent/dfs2.rs` (pass 5): an independent exact DFS for case (b), written from the note
  without reading gtile5/6. Build with `rustc -O -C target-cpu=native dfs2.rs -o dfs2.exe`; run
  `./dfs2.exe 195 P --threads 20 --split 3 --log out/dfs2_n195_pP.txt`. Controls are in
  `dfs2_controls.sh`, and there are `--nosym` and `--count` options.
- `structure/composite_B.md` and `composite_bruteforce.py` (pass 5): the prime-power |B| reduction.
- `independent/dfs3.rs` (pass 7): dfs2 extended to level i (`--level i`, `--resume LOG`, `--all`).
  Build with `rustc -O -C target-cpu=native dfs3.rs -o dfs3.exe`; run
  `./dfs3.exe 195 3 --level 2 --threads 18 --split 3 --log out/dfs3_n195_p3_L2.log`.
  `brute_count3.py`, `direct_check3.py`, `symcheck3.py` and `dfs3_controls.sh` are its validators.
  The per-task logs are gzipped (`out/*.log.gz`); gunzip one before using `--resume`.
- `general/out/m27_hd81_controls.txt` (pass 7): the hd = 81 controls for gtile7, and the n = 162
  level-3 witness.
- `structure/pass9_lemmaS.md` and `structure/pass9_lemmaS/` (pass 9): cex1 and cex2 refute Lemma S
  for general downsets; check them with `python cex_downset_check.py`. The refined conjecture S′ is
  for shifted downsets.
  - `lemS.py exh <n> <p>` runs the exhaustive T_n sweep, and `check_indep.py` is its independent
    checker.
- `independent/out/p9/` (pass 9): the n = 195 runs Z625×Z39 at level 3 and Z243×Z65 at level 4,
  both NONE. The commands are in `independent/out/pass9_runs.txt`.
