#!/bin/sh
# run all split=i/N parts of gtile7 in parallel; output to out/<tag>.txt
# usage: sh run7.sh <tag> <N> "<gtile7 args>"
cd "$(dirname "$0")"
for i in $(seq 0 $(($2-1))); do
  ( ./gtile7.exe $3 split=$i/$2 2>/dev/null > out/g7_$1_$i.part ) &
done
wait
cat out/g7_$1_*.part > out/$1.txt && rm out/g7_$1_*.part
grep -o "result=[A-Z]*" out/$1.txt | sort | uniq -c
