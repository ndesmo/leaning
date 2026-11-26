#!/bin/sh
cd "$(dirname "$0")"; mkdir -p out
for m in $(seq 1 11); do n=$((13*m)); B=$(python -c "print(','.join(f'{j}/0' for j in range(13)))")
  r=$(WORKERS=${W:-4} python cpsat_coset.py $n 13 300 --out out/w_${n}_13.json); echo "$r" | head -1
  if echo "$r" | grep -q EXISTS; then python direct_check.py out/w_${n}_13.json
    python ../general/check_general.py $n 169,$m "$B" "$(echo "$r" | grep SOL)" 300; fi; done
