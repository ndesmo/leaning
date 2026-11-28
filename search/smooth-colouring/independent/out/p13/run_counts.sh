#!/bin/sh
# dfs3 --count (no symmetry) vs brute_count3b.py at p=3 level 4 and p=5 level 3 (and p=3 L3 sanity)
cd "$(dirname "$0")/../.."
for a in "3 3 4" "6 3 4" "9 3 4" "12 3 4" "5 5 3" "10 5 3" "15 5 3" "9 3 3" "12 3 3" "10 5 2"; do
  set -- $a
  d=$(./dfs3_p13c.exe $1 $2 --level $3 --count --threads 2 2>/dev/null | grep '^dfs3' | sed 's/.*result=\(COUNT=[0-9]*\).*/\1/')
  b=$(python -c "import subprocess,sys
try: print(subprocess.run([sys.executable,'brute_count3b.py','$1','$2','$3'],capture_output=True,text=True,timeout=900).stdout.strip())
except subprocess.TimeoutExpired: print('BRUTE3B TIMEOUT900s')")
  echo "$1 $2 L$3 dfs3 $d | $b"
done
