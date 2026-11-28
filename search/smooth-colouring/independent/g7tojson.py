"""g7tojson.py n p level gtile7_output.txt out.json : convert a gtile7 coset-mode 'solution q:h/f ...' line
(G = Z_{p^{level+1}} x Z_{n/p}) to the dfs3 witness JSON read by direct_check3.py / liftcheck3.py."""
import sys, re, json
n, p, lv = map(int, sys.argv[1:4]); K = n // p
line = [l for l in open(sys.argv[4]) if l.startswith("solution")][0]
phi = {q: [int(h), int(f)] for q, h, f in re.findall(r"(\d+):(\d+)/(\d+)", line)}
json.dump({"n": n, "p": p, "level": lv, "K": K, "dims": [p ** (lv + 1), K], "phi": phi}, open(sys.argv[5], "w"))
