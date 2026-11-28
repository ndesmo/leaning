#!/bin/sh
# restricted counts: solutions with h(2) a unit mod p (prime 2 = first dfs3 search variable here).
# dfs3 --count --first U (U = all elements with unit h) vs brute_count3b.py n p level 2.
# Zero counts here are the NEGATIVE controls (dfs3 NONE in the restricted space, confirmed by brute force).
cd "$(dirname "$0")/../.."
for a in "6 3 4" "9 3 4" "12 3 4" "15 3 4" "18 3 4" "10 5 3" "15 5 3" "20 5 3" "9 3 3" "12 3 3"; do
  set -- $a; K=$(($1/$2)); Q=$(python -c "print($2**($3+1))")
  U=$(python -c "print(','.join(str(h*$K+g) for h in range($Q) if h%$2 for g in range($K)))")
  d=$(./dfs3_p13c.exe $1 $2 --level $3 --count --first $U --threads 2 2>/dev/null | grep '^dfs3' | sed 's/.*result=\(COUNT=[0-9]*\).*/\1/')
  b=$(python -c "import subprocess,sys
try: print(subprocess.run([sys.executable,'brute_count3b.py','$1','$2','$3','2'],capture_output=True,text=True,timeout=900).stdout.strip())
except subprocess.TimeoutExpired: print('BRUTE3B TIMEOUT900s')")
  echo "$1 $2 L$3 unit-h(2): dfs3 ${d:-none} | $b"
done
