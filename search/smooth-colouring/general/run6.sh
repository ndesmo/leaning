#!/bin/sh
# run all split=i/N parts of gtile6 in parallel; output to out/<tag>.txt
# usage: sh run6.sh <tag> <N> "<gtile6 args>"
cd "$(dirname "$0")"
for i in $(seq 0 $(($2-1))); do
  ( ./gtile6.exe $3 split=$i/$2 2>/dev/null > out/g6_$1_$i.part ) &
done
wait
cat out/g6_$1_*.part > out/$1.txt && rm out/g6_$1_*.part
grep -o "result=[A-Z]*" out/$1.txt | sort | uniq -c
