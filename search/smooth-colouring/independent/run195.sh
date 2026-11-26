#!/bin/sh
# n=195 for (p,K) in (3,65),(5,39),(13,15); concurrent, 7 workers each, timeout ${1:-1500}s
cd "$(dirname "$0")"; mkdir -p out
for p in 3 5 13; do WORKERS=7 python cpsat_coset.py 195 $p ${1:-1500} --out out/w_195_$p.json > out/n195_p$p.txt 2>&1 & done; wait
