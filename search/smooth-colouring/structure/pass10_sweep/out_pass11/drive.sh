#!/bin/sh
# usage: sh drive.sh SECONDS "n:p n:p ..."   (resumable; checkpoints ck/exh_n_p.ck; depth must stay 4)
cd "$(dirname "$0")"
T=$1; shift
for np in $*; do
  n=${np%:*}; p=${np#*:}
  timeout $T ./lems.exe exh $n $p 20 ck/exh_${n}_${p}.ck 4 2>>ck/stderr.txt >>sweep_out.txt
  # timeout kills before summary; print a summary line for partial runs
  ./lems.exe exh $n $p 0 ck/exh_${n}_${p}.ck 4 2>>ck/stderr.txt >>sweep_out.txt
done
