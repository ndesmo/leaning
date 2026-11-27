# pass 12: per-n level conjecture sweep

`pern.py` drives `independent/dfs3.exe` over (n, p). For each pair it tries levels 0, 1, … up to
v_p(n/p) + 2 and stops at the first FOUND. Every FOUND witness is checked with
`independent/direct_check3.py`, and the witnesses are in `w/`.
- Raw results: `phaseB.txt` (n = 4..194) and `phaseA.txt` (n = 205).
- Commands: `COMMANDS.txt`.
- Summary: notes/smooth-colouring.md, pass 12.
