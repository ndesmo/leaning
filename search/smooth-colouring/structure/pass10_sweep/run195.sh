#!/bin/sh
cd "$(dirname "$0")"
for p in 13 5 3; do
  ./lems.exe rand 195 $p 100000 11 200000 6 n195/rand_p$p.txt 2>>n195/stderr.txt | tee -a n195/summary.txt
  ./lems.exe trand 195 $p 3000 12 200000 6 n195/trand_p$p.txt 2>>n195/stderr.txt | tee -a n195/summary.txt
done
