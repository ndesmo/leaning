#!/bin/sh
# controls: n=p*m; run with symmetry, verify every witness by direct_check + check_general
cd "$(dirname "$0")"; mkdir -p out
run() { n=$1; p=$2; K=$((n/p)); B=$(python -c "print(','.join(f'{j}/0' for j in range($p)))")
  r=$(python cpsat_coset.py $n $p 600 --out out/w_${n}_${p}.json); echo "$r" | head -1
  if echo "$r" | grep -q EXISTS; then python direct_check.py out/w_${n}_${p}.json
    python ../general/check_general.py $n $((p*p)),$K "$B" "$(echo "$r" | grep SOL)" 300; fi; }
for m in $(seq 1 27); do run $((3*m)) 3; done
for m in $(seq 1 29); do [ $((m%5)) -ne 0 ] && run $((5*m)) 5; done
for m in $(seq 1 11); do run $((13*m)) 13; done
