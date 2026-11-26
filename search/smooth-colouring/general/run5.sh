#!/bin/sh
# run all top-level splits of gtile5 for one B in parallel; append to out/m3_pass2_gtile5.txt
# usage: sh run5.sh "<hd>" "<B>" <ntop> <limit>
cd "$(dirname "$0")"
for i in $(seq 0 $(($3-1))); do
  ( ./gtile5.exe hd=$1 B=$2 top=$i limit=$4 2>/dev/null > out/g5_tmp_$i.txt ) &
done
wait
