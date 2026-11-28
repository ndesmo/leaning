#!/bin/sh
cd "$(dirname "$0")"; echo "parts done: $(ls part_*.txt 2>/dev/null | wc -l)"; cat part_*.txt 2>/dev/null | grep -o "result=[A-Z]*" | sort | uniq -c
cat part_*.txt 2>/dev/null | awk '{for(i=1;i<=NF;i++){if($i~/^nodes=/){split($i,a,"=");s+=a[2]} if($i~/^secs=/){split($i,b,"=");t+=b[2]}}} END{printf "nodes=%.3e cpu_secs=%.0f\n",s,t}'
