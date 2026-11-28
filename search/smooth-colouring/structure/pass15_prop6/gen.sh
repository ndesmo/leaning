#!/bin/sh
# generate n=30 tilings (pass-13 exp2_tn.py) for the R-analogue tiles in B_rho3.txt / B_rho2.txt
# usage (from pass15_prop6/): sh gen.sh ; outputs gen/exp2_n30_4x9_<label>_r.json
cd gen
i=0
for rho in 3 2; do
  while read -r B; do
    i=$((i+1))
    BPRIME="$B" RESTARTS=20 python ../../pass13_mixed/exp2_tn.py 30 2 3 4,9 $((100*rho+i)) 10 > log_$((100*rho+i)).txt 2>&1 &
    if [ $((i % 4)) -eq 0 ]; then wait; fi
  done < ../B_rho$rho.txt
done
wait
