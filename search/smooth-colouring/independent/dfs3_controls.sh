#!/bin/sh
# positive controls for dfs3 (find mode with symmetry) at levels 2 and 3; every witness -> direct_check3.py
cd "$(dirname "$0")"; mkdir -p out/dfs3_w
run() { n=$1; p=$2; l=$3; f=out/dfs3_w/w_${n}_${p}_L${l}.json; rm -f $f
  r=$(timeout ${TO:-120} ./dfs3.exe $n $p --level $l --threads ${TH:-4} --split 2 --out $f 2>/dev/null | grep '^dfs3'); echo "$n $p L$l: ${r:-TIMEOUT}"
  if echo "$r" | grep -q FOUND; then python direct_check3.py $f; fi; }
for m in $(seq 1 64); do run $((3*m)) 3 2; done
for m in $(seq 1 38); do run $((5*m)) 5 2; done
for m in $(seq 1 14); do run $((13*m)) 13 2; done
for m in $(seq 1 64); do run $((3*m)) 3 3; done
