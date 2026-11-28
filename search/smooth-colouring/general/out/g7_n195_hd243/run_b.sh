#!/bin/sh
# pass 14: same as run.sh, but skips parts listed in $SKIP (parts still running under an older driver).
cd "$(dirname "$0")"; W=${1:-4}; N=${2:-400}; SKIP=" ${3:-} "
seq 0 $((N-1)) | while read k; do case "$SKIP" in *" $k "*) ;; *) echo $k;; esac; done | xargs -P $W -I{} sh -c '[ -f part_{}.txt ] || { ../../gtile7_p13.exe n=195 p=3 hd=243 mode=coset split={}/'$N' > part_{}.tmp 2>/dev/null && grep -q "result=" part_{}.tmp && mv part_{}.tmp part_{}.txt; }'
cat part_*.txt 2>/dev/null | grep -o "result=[A-Z]*" | sort | uniq -c
