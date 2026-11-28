# pass14_c22: exact search for the family (c_{x,y}) (pass13_mixed.md §2), target (c_{2,2}) at n = 195

Status: written 2026-11-28 (explorer pass 14 subagent), not reviewed.

(c_{x,y}): a homomorphism psi: Z^{pi(n)} -> G = Z_{p^x} x Z_{q^y} x Z_r, injective on T = {1..n},
with every Z_r-fibre of psi(T) a coset of P x {k}, P = p^{x-1}Z x q^{y-1}Z (order pq). n = 195:
p, q, r = 3, 5, 13; (c_{2,2}) lives in Z9 x Z25 x Z13. The finite constraint system that the code tests
(label equality within fibres, injectivity, fibre size <= pq), with the proof that it is equivalent,
the large-prime completion, and the symmetry argument are in the header of `c22.rs`.

## Files

- `c22.rs` / `c22.exe`: the search (DFS over primes <= n/2, in increasing order; Aut(G) orbit reps for
  psi(2); tasks = (psi(2), psi(3)); checkpoint log, `--resume`, `--time`).
- `brute_c.py`: naive independent counter (all primes enumerated, including the large ones; leaf test by
  explicit coset comparison). Shares no code with c22.rs.
- `check_colouring.py`: independent witness checker. It checks the (c) property, the tiling A (+) B = G,
  and the colouring itself for all x <= 5000 (primes > n get random values). Shares no code with c22.rs.
- `count_controls.sh`: runs c22 `--count` against brute_c.py. Output: `out/count_controls.out`.
- `wit/`: witnesses. `bad_w30.txt` is a perturbed witness, which the checker must reject.
- `out/`: logs (one `TASK id done` line per finished task).

## Commands (from this directory; at most 3 threads were used)

```
rustc -O -C target-cpu=native c22.rs -o c22.exe
# positive controls (witnesses + independent check)
./c22.exe 30 2 2 3 2 5 --genuine --wit wit/w30_22_genuine.txt
./c22.exe 42 2 2 3 2 7 --genuine --wit wit/w42_23_genuine.txt
./c22.exe 30 2 2 3 2 5 --wit wit/w30_22.txt
./c22.exe 105 3 2 5 2 7 --wit wit/w105_22.txt
python check_colouring.py wit/<file> 5000          # bad_w30.txt must FAIL
# count controls
sh count_controls.sh > out/count_controls.out
# n = 195
./c22.exe 195 3 2 5 2 13 --threads 2 --log out/n195_c22_sym.log2          # (c_{2,2}), symmetry on
./c22.exe 195 3 2 5 2 13 --nosym --time 2400 --log out/n195_c22_nosym.log  # (c_{2,2}), no symmetry
./c22.exe 195 3 1 5 1 13 ; ./c22.exe 195 3 2 5 1 13 ; ./c22.exe 195 3 1 5 2 13   # consistency
./c22.exe 195 3 3 5 2 13 --time 900 --log out/n195_c32.log                 # (c_{3,2})
# resume an unfinished run: add --resume <same log> (and --log <same log>)
```

Results: see the pass-14 journal entry, and the tails of the logs in `out/`.
