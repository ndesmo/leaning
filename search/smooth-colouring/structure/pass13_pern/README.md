# pass 13: per-n level conjecture at n >= 205 (p || n)

Binary: `independent/dfs3_pern.exe` = copy of `independent/dfs3.exe` (pass 12 build). Level Lk = `dfs3 --level k`.
L0 (multiplicative into Z_p x Z_{n/p} = Z_n when p || n) is NONE for every n here by the multiplicative-NO list (not rerun, except 205 in pass 12).

## Commands (run from this directory)
    ../../independent/dfs3_pern.exe 205 5  --level 2 --threads 5 --split 2 --log L2_205_5.log  --out w/w_205_5_L2.json   # NONE 2099/2099, 61.8 s
    ../../independent/dfs3_pern.exe 205 41 --level 1 --threads 5 --split 2 --log L1_205_41.log --out w/w_205_41_L1.json  # NONE 263/263, 41.5 s
    ../../independent/dfs3_pern.exe 205 41 --level 2 --threads 5 --split 2 --log L2_205_41.log --out w/w_205_41_L2.json  # killed after ~28 min still in SETUP (no task started, 2.5 GB RAM; |G|=344605, |Gamma|=268960) -- not feasible with dfs3 as is
    python pern13.py L1_sweep.txt 2 2 300 1 217:7 217:31 235:5 235:47 247:13 247:19 212:53 214:2 214:107 218:2 218:109 220:5 220:11 242:2 244:61 246:2 246:3 246:41 248:31
        # stopped by hand at the end of the pass (time); the two ERR lines for 220:11 and 218:109 are those kills, not failures
    ../../independent/dfs3_pern.exe 235 47 --level 1 --threads 4 --split 2 --log logs/L1_235_47.log --resume logs/L1_235_47.log --out w/w_235_47_L1.json   # finished: NONE 311/311
Raw: L1_sweep.txt, L2_205_5.out, L1_205_41.out, L1_235_47_resume.out, logs/.

## Resume (dfs3 appends to --log, so resume onto the same file)
    ../../independent/dfs3_pern.exe 212 53  --level 1 --threads 4 --split 2 --log logs/L1_212_53.log  --resume logs/L1_212_53.log  --out w/w_212_53_L1.json   # 259/402 done
    ../../independent/dfs3_pern.exe 214 107 --level 1 --threads 4 --split 2 --log logs/L1_214_107.log --resume logs/L1_214_107.log --out w/w_214_107_L1.json  # 99/348
    ../../independent/dfs3_pern.exe 218 109 --level 1 --threads 4 --split 2 --log logs/L1_218_109.log --resume logs/L1_218_109.log --out w/w_218_109_L1.json  # 84/356
    ../../independent/dfs3_pern.exe 220 11  --level 1 --threads 4 --split 2 --log logs/L1_220_11.log  --resume logs/L1_220_11.log  --out w/w_220_11_L1.json   # 218/855
    python pern13.py L1_sweep2.txt 2 2 600 1 242:2 244:61 246:2 246:3 246:41 248:31   # not started
(`pern13.py` resumes automatically when logs/L{lv}_{n}_{p}.log exists.)

## Checker
`colour_check.py` (fresh, no shared code): colours every a <= LIMIT (default 20000) by psi(a) - psi(m) in B = {(j,0): 0<=j<p^level}
(A = psi([n]), A+B = G asserted direct) and asserts a,2a,...,na get n distinct colours. Validated: OK on pass-12 witnesses
w_121_11_L1 (a<=20000) and w_100_5_L0 (a<=2000); a perturbed copy of w_121_11_L1 (phi(3) h+1) is rejected.
No FOUND occurred in pass 13, so no new witness to check.
