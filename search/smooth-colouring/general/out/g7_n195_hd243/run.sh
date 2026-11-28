#!/bin/sh
# pass 13: gtile7 (second program family) on (b_4^3), G = Z243 x Z65, n = 195, coset mode.
# Resumable: N parts (split=i/N); a part is done iff part_i.txt exists (written atomically via .tmp).
# usage: sh run.sh [workers=4] [N=400]       stop: taskkill //F //IM gtile7_p13.exe
cd "$(dirname "$0")"; W=${1:-4}; N=${2:-400}
seq 0 $((N-1)) | xargs -P $W -I{} sh -c '[ -f part_{}.txt ] || { ../../gtile7_p13.exe n=195 p=3 hd=243 mode=coset split={}/'$N' > part_{}.tmp 2>/dev/null && grep -q "result=" part_{}.tmp && mv part_{}.tmp part_{}.txt; }'
cat part_*.txt 2>/dev/null | grep -o "result=[A-Z]*" | sort | uniq -c
