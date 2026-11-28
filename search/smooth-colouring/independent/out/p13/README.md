# Pass 13: controls for the two single-program levels (dfs3), p = 3 level 4 and p = 5 level 3

Scope: the n = 195 NONE results for (b_4^3), G = Z243 × Z65, and (b_3^5), G = Z625 × Z39
(`../pass9_runs.txt`). Both are dfs3 runs with lex-leader symmetry. Before this pass they had no genuine
controls at those levels. All commands below run from `search/smooth-colouring/independent/`. Binaries
`dfs3_p13a.exe` and `dfs3_p13c.exe` are byte copies of `dfs3.exe`, renamed so that they can be killed
safely. `gtile7_p13.exe` is a copy of `general/gtile7.exe`.

New scripts:
- `../../liftcheck3.py` defines "lift". A witness is a *plain lift* if every h(q) ∈ pZ_{p^{i+1}}, so that
  φ = (×p, id)∘ψ with ψ a level-(i−1) solution. It is a *level-0 lift* if every h(q) ∈ p^iZ.
  **NOT_A_LIFT_strong** means that H = ⟨φ(q)⟩ contains an element whose order has p-part p^{i+1} >
  p^max(i, v_p K). Then H does not embed in Z_{p^i} × Z_K, so φ is not j∘ψ for ANY injective
  homomorphism j from a level-(i−1) group. The test is run on both H_small (primes with 2q ≤ n) and
  H_all.
- `../../brute_count3b.py n p level [q0]` is a brute-force count over all primes ≤ n. It uses no
  large-prime shortcut and no symmetry, and is written from the definition. Its pruning uses only
  necessary conditions, and every leaf gets the full definition check. With q0 it counts only solutions
  where h(q0) is a unit. It reproduces every earlier `../brute3.txt` count (validated this pass).
- `../../p13_controls.py MODE p level n1 n2 [timeout] [threads]`. MODE `sym` is plain dfs3. MODE `genu`
  is `dfs3 --nosym --first U`, where U is the set of elements with a unit h for the first search
  variable (prime 2). This is a sound restriction to a subset of the solutions, used to force non-lift
  witnesses. Every FOUND witness goes through direct_check3.py and liftcheck3.py.
- `../../g7tojson.py` converts a gtile7 solution line to the witness JSON.
- `../../symcheck3.py` now honours the `DFS3_EXE` environment variable (default `./dfs3.exe`).

## 1. Genuine level-3 witness at n = 162, p = 3
    ./dfs3_p13a.exe 162 3 --level 3 --threads 6 --split 2 --out out/p13/w/w_162_3_L3.json --log out/p13/dfs3_162_3_L3.log
    python direct_check3.py out/p13/w/w_162_3_L3.json ; python liftcheck3.py out/p13/w/w_162_3_L3.json
Result: **FOUND** in 5.57 s, 256,104 nodes, 706/8608 tasks, 6 threads. (The pass-6 control used an 8 s
timeout with 4 threads.) DIRECT3 OK. liftcheck gives plain_lift=False and NOT_A_LIFT_strong=True:
H_small contains elements of order 81 (h(2) = 1), and v_3(54) = 3. dfs3 itself finds level 2 NONE at
n = 162 (`../dfs3_controls_extra.txt`). Files: `dfs3_162_3_L3.txt`, `.log`, `w/w_162_3_L3.json`.

## 2. Level-4 (p=3) and level-3 (p=5) controls for dfs3
Positive, plain mode (`ctl_sym_p3_L4.txt`, `ctl_sym_p5_L3.txt`):
    python p13_controls.py sym 3 4 3 90 60 4 ; python p13_controls.py sym 5 3 5 100 60 4
p=3 L4: FOUND for all n = 3..90 (30/30); p=5 L3: FOUND for all n = 5..100 (20/20). All pass DIRECT3.
**All of them are level-0 lifts** (h ∈ p^iZ), so on their own they are weak controls.

Positive, forced non-lift (`ctl_genu_p3_L4.txt`, `ctl_genu_p5_L3.txt`):
    python p13_controls.py genu 3 4 6 90 60 4 ; python p13_controls.py genu 5 3 10 60 60 4
- p=3 L4: FOUND at n = 12–54 (every multiple of 3) and at n = 60, 16 witnesses in total. All pass DIRECT3
  and all are NOT_A_LIFT_strong (p-exp(H) = 3^5). The restricted search is NONE (exhaustive) at
  n = 6, 9, 57. It timed out at 60 s for n = 63–90.
- p=5 L3: FOUND at n = 25, 40, 45. All pass DIRECT3 and all are NOT_A_LIFT_strong (5^4). The
  restricted search is NONE (exhaustive) at n = 10, 15, 20, 30, 35, 50, 55, 60. For n ≥ 65 the
  `--first` argument exceeds the Windows command-line length limit, so these were not run.

Counts, dfs3 --count vs brute force (`counts_L4p3_L3p5.txt`, `run_counts.sh`): all agree.
- p=3 L4: n=3: 2, n=6: 490, n=9: 48, n=12: 5896.
- p=5 L3: n=5: 8, n=10: 20, n=15: 10336.
- Also p=3 L3: n=9: 48, n=12: 2008; and p=5 L2: n=10: 20.

Restricted counts with h(2) a unit, `dfs3 --count --first U` vs `brute_count3b.py n p l 2`
(`unitcounts.txt`, `run_unitcounts.sh`): all agree.
- p=3 L4: n=6: 0, n=9: 0, n=12: 3888, n=15: 12960, n=18: 23328.
- p=5 L3: n=10: 0, n=15: 0, n=20: 0.
- p=3 L3: n=9: 0, n=12: 1296.
- **The zeros are the negative controls**: dfs3 reports NONE/0 and brute force confirms it.
  Unrestricted negatives do not exist at these sizes, because every n tried is L0-solvable and lifts
  to every level.

Symmetry soundness, symcheck3 (`symcheck_L4p3_L3p5.txt`, `run_symcheck.sh`, `DFS3_EXE=./dfs3_p13c.exe`):
- PASS at p=3 L4 for n = 6, 9, 12, 15, 18, 21. In the largest case, n = 21, 6168 nosym solutions fall
  into 50 orbits, and these equal the 50 sym solutions.
- PASS at p=5 L3 for n = 10, 15, 20, 30. At n = 30, 24224 solutions fall into 596 orbits.
- Not completed: p=3 L4 n = 24 (stopped by hand after about 15 min), n = 27 (not run), and p=5 L3
  n = 25 (300 s timeout).

## 3. Second program: gtile7 hd=243 (p=3 level 4) at n = 195
Controls: `general/out/g7_n195_hd243/ctl_n*.txt` and `ctl_splits.txt`.
- n = 12, 30, 60: EXISTS. All witnesses pass DIRECT3.
- Of the 60 split runs, 13 witnesses are NOT_A_LIFT_strong.

Main run: 400 parts, split=i/400, resumable, 4 workers, `general/out/g7_n195_hd243/`.
    sh ../general/out/g7_n195_hd243/run.sh 4 400      # start or resume (skips finished parts)
    sh ../general/out/g7_n195_hd243/status.sh         # progress
    taskkill //F //IM gtile7_p13.exe                  # stop; unfinished parts (*.tmp) are redone on resume
A part counts as done only when `part_i.txt` exists and contains `result=`. Each part took about 80 s,
about 4.4·10⁹ nodes. The rough estimate is 400 parts ≈ 9 CPU hours.
Progress at end of pass 13 (see status.sh for live numbers):
    parts done: 18
         18 result=NONE
    nodes=8.046e+10 cpu_secs=1443
