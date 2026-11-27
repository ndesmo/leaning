# min_modulus: exhaustive search for valid residue sets

Exhaustive search for Fonollosa's minimum-modulus problem (notes/min-modulus.md, issue #87).
A = {a_0 < … < a_{n−1}} ⊆ ℤ_N is *valid* if no nonzero c with c_i ≥ −1, Σ c_i = 0 has
Σ c_i a_i ≡ 0 (mod N). The method is described in the header comment of `search.rs` and in
notes/min-modulus.md, N4.

No C compiler was available on the machine used, so the search is in Rust (std only, no crates).

## Build

    rustc -O -C target-cpu=native search.rs -o mm.exe

## Run

    mm.exe search <n> <Nlo> <Nhi> [canon|plain] [outfile]   # one line per N, then a SUMMARY line
    mm.exe check <N> <a_0> ... <a_{n-1}>                    # DP and brute-force validity of one set
    mm.exe crosscheck <trials> [seed]                       # DP vs brute force on random sets

- `canon` (default) fixes 0 and g = a_1 as the pair with the least gcd(difference, N), using
  translation plus unit scaling. `plain` fixes only a_0 = 0 (translation only).
- `THREADS=k` sets the thread count (default: all cores).
- `VERIFY=1` also runs the full DP update on candidates the quick filter rejects, and asserts
  that the two agree on every candidate.

Reproduce the n = 8 result (about 3.5 min on 22 threads):

    mm.exe search 8 8 248 canon n8.txt

`n8_results.txt` holds the recorded output of the runs cited in the notes.
