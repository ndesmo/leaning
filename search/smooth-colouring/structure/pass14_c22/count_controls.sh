#!/bin/sh
# count controls: c22 --count vs naive brute_c.py (run from this directory)
for c in "6 2 1 3 1 1" "6 2 2 3 2 1" "30 2 1 3 1 5" "30 3 1 5 1 2" "30 2 2 3 0 5 --cap 3" "30 2 0 3 2 5 --cap 2" "30 2 2 3 1 5" "30 2 1 3 2 5" "30 3 2 5 1 2" "30 2 2 3 2 5" "30 3 2 5 2 2"; do
  set -- $c
  capv=1; [ "$7" = "--cap" ] && capv=$8
  ./c22.exe $c --count | tail -1
  python brute_c.py $1 $2 $3 $4 $5 $6 $capv
done
