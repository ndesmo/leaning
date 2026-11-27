#!/bin/sh
# usage: sh sweep.sh N0 N1   (resumable: checkpoint files ck/exh_n_p.ck)
cd "$(dirname "$0")"
for n in $(seq $1 $2); do
  for p in 2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97; do
    if [ $p -lt $n ] && [ $((n % p)) -eq 0 ]; then
      ./lems.exe exh $n $p 20 ck/exh_${n}_${p}.ck 4 2>>ck/stderr.txt | tee -a sweep_out.txt
    fi
  done
done
