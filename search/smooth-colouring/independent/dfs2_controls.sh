#!/bin/sh
# positive controls for dfs2: find mode (with symmetry), then direct_check on the witness
cd "$(dirname "$0")"; mkdir -p out/dfs2_w
run() { n=$1; p=$2; r=$(./dfs2.exe $n $p --threads 20 --split 2 --out out/dfs2_w/w_${n}_${p}.json 2>/dev/null | grep '^dfs2'); echo "$r"
  if echo "$r" | grep -q FOUND; then python direct_check.py out/dfs2_w/w_${n}_${p}.json; fi; }
for m in $(seq 1 64); do run $((3*m)) 3; done
for m in $(seq 1 38); do [ $((m%5)) -ne 0 ] && run $((5*m)) 5; done
for m in $(seq 1 14); do run $((13*m)) 13; done
