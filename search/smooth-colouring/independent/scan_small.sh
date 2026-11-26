#!/bin/sh
# scan dfs2 (with symmetry) over n = p*m for p in 2,3,5,7,11,13, n <= ${1:-120}; 20s cap each
cd "$(dirname "$0")"
for p in 2 3 5 7 11 13; do m=1; while [ $((p*m)) -le ${1:-120} ]; do
  timeout 20 ./dfs2.exe $((p*m)) $p --threads 20 --split 2 2>/dev/null | grep '^dfs2' || echo "dfs2 n=$((p*m)) p=$p TIMEOUT20"
  m=$((m+1)); done; done
