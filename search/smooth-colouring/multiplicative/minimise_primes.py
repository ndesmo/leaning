"""Greedy minimisation of a set P of primes such that no homomorphism to Z_195
is injective on the P-smooth numbers <= 195.  Uses search2.exe (mode one).
Usage: python minimise_primes.py   (run from this directory)"""
import subprocess, sys

def run(P, timeout=300):
    try:
        out = subprocess.run(["./search2.exe", "one", "dims=195", "m=195",
                              "primes=" + ",".join(map(str, P))],
                             capture_output=True, text=True, timeout=timeout).stdout
    except subprocess.TimeoutExpired:
        return "TIMEOUT", ""
    line = [l for l in out.splitlines() if l.startswith("result=")][0]
    return line.split()[0].split("=")[1], line

P = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
print("start", P, run(P), flush=True)
for p in sorted(P, reverse=True):
    Q = [q for q in P if q != p]
    r, line = run(Q)
    print("remove", p, "->", r, line, flush=True)
    if r == "NONE":
        P = Q
print("minimal (w.r.t. single removals, greedy from the top):", P, run(P), flush=True)
