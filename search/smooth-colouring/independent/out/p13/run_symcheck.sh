#!/bin/sh
# symcheck3 (lex-leader soundness, exact orbit comparison) at p=3 level 4 and p=5 level 3
cd "$(dirname "$0")/../.."
export DFS3_EXE=./dfs3_p13c.exe
for n in 6 9 12 15 18 21 24 27; do python symcheck3.py $n 3 4 3; done
for n in 10 15 20 25 30; do python symcheck3.py $n 5 3 3; done
