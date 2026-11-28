// Exhaustive search for "valid" n-sets of residues mod N (Fonollosa, Conjecture 1).
// See README.md. Build: rustc -O -C target-cpu=native search.rs
//
// A = {a_0 < ... < a_{n-1}} in Z_N is valid iff no nonzero c in Z^n with c_i >= -1,
// sum c_i = 0 has sum c_i a_i == 0 (mod N)  ([Fon26] Lemma 1; c = k - 1).
//
// DP: for a prefix P = (a_0..a_{j-1}) keep, for each s, the bitset B[s] of residues
// sum c_i a_i over NONZERO c supported on P with c_i >= -1 and sum c_i = s.
// Adding x: new[s] = U_{t>=-1} rot(B[s-t], t*x)  U  {s*x if s != 0}  (the second term is
// c = 0 on P, c_x = s). Prefix P is valid iff bit 0 of B[0] is clear. Any balanced c
// supported on a prefix is a balanced c of every extension, so pruning is sound.
// Only s <= n - j is kept (each later element contributes c_i >= -1, so a prefix sum
// s > n - j can never be cancelled), and s >= -j holds automatically.
//
// Symmetry ("canon" mode): if A is valid, let d = a_i - a_k be a difference with minimal
// g = gcd(d, N). In Z_N, d = u*g for a unit u (checked by assert_associates for each N).
// Then u^{-1}(A - a_k) is valid, contains 0 and g, and all its differences have gcd >= g
// (scaling by a unit preserves gcds). An element e with 0 < e < g would give a difference
// with gcd(e,N) <= e < g, so a_1 = g. Hence it suffices to search, for each divisor g of N,
// sets 0 = a_0 < g = a_1 < a_2 < ... with gcd(a_i - a_k, N) >= g for all i != k.
// "plain" mode: only a_0 = 0 (translation), all a_1 in 1..N-1.

use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Instant;

type BS = [u64; 4];
const MAXN: usize = 12; // max set size n
const S: usize = 2 * MAXN + 1; // s index range, offset MAXN

#[inline]
fn shl(b: &BS, k: usize) -> BS {
    let (w, o) = ((k >> 6) as isize, (k & 63) as u32);
    let mut r = [0u64; 4];
    for i in 0..4isize {
        let s = i - w;
        let cur = if s >= 0 { b[s as usize] } else { 0 };
        let prev = if s >= 1 { b[(s - 1) as usize] } else { 0 };
        r[i as usize] = (cur << o) | ((prev >> 1) >> (63 - o));
    }
    r
}
#[inline]
fn shr(b: &BS, k: usize) -> BS {
    let (w, o) = ((k >> 6) as usize, (k & 63) as u32);
    let mut r = [0u64; 4];
    for i in 0..4usize {
        let s = i + w;
        let cur = if s < 4 { b[s] } else { 0 };
        let next = if s + 1 < 4 { b[s + 1] } else { 0 };
        r[i] = (cur >> o) | ((next << 1) << (63 - o));
    }
    r
}
fn mask(nm: usize) -> BS {
    let mut m = [0u64; 4];
    for i in 0..nm { m[i / 64] |= 1u64 << (i % 64); }
    m
}
#[inline]
fn rot(b: &BS, k: usize, nm: usize, m: &BS) -> BS {
    // bit i -> bit (i + k) mod nm, 0 <= k < nm, b supported on [0, nm)
    if k == 0 { return *b; }
    let a = shl(b, k);
    let c = shr(b, nm - k);
    [(a[0] | c[0]) & m[0], (a[1] | c[1]) & m[1], (a[2] | c[2]) & m[2], (a[3] | c[3]) & m[3]]
}

struct Ctx { n: usize, nm: usize, m: BS }

impl Ctx {
    // old = B for a prefix of length j; writes B for the prefix extended by x into new.
    // Returns true iff the extended prefix is still valid.
    #[inline]
    fn extend(&self, old: &[BS; S], new: &mut [BS; S], j: usize, x: usize) -> bool {
        // Horner form. Let R = rotation by x and old' = old with the zero vector added at
        // s = 0 (old'[0] = old[0] U {0}). Then the union over t >= -1 of R^t old'[s - t] is
        //   U[s] U R^{-1} old'[s+1],  where U[s] = old'[s] U R U[s-1]  (t >= 0 part).
        // The zero vector of the extended prefix arises only at s = 0, t = 0; so
        //   new[0] = old[0] U R U[-1] U R^{-1} old'[1], and new[s] = U[s] U R^{-1} old'[s+1] else.
        let n = self.n as i64; let nm = self.nm; let m = &self.m;
        let j = j as i64;
        let off = MAXN as i64;
        let (slo, shi) = (-(j + 1), n - (j + 1));
        let (olo, ohi) = (-j, n - j);
        let oldp = |s: i64| -> BS {
            if s < olo || s > ohi { return [0; 4]; }
            let mut b = old[(s + off) as usize];
            if s == 0 { b[0] |= 1; }
            b
        };
        let kf = x % nm; // R
        let kb = (nm - kf) % nm; // R^{-1}
        let mut u: BS = [0; 4]; // U[slo - 1] = 0
        for s in slo..=shi {
            let ru = rot(&u, kf, nm, m);
            let cur = oldp(s);
            let back = rot(&oldp(s + 1), kb, nm, m);
            let mut v = [0u64; 4];
            if s == 0 {
                let o0 = old[off as usize];
                for w in 0..4 { v[w] = o0[w] | ru[w] | back[w]; }
            } else {
                for w in 0..4 { v[w] = cur[w] | ru[w] | back[w]; }
            }
            for w in 0..4 { u[w] = cur[w] | ru[w]; }
            new[(s + off) as usize] = v;
        }
        // clear entries outside the kept window so stale data can never leak
        for s in -off..slo { new[(s + off) as usize] = [0; 4]; }
        for s in (shi + 1)..=off { new[(s + off) as usize] = [0; 4]; }
        new[off as usize][0] & 1 == 0
    }
}

fn gcd(a: usize, b: usize) -> usize { if b == 0 { a } else { gcd(b, a % b) } }

/// Full DP validity test of a set (any order, distinct residues).
fn valid_dp(a: &[usize], nm: usize) -> bool {
    let n = a.len();
    let ctx = Ctx { n, nm, m: mask(nm) };
    let mut cur = [[0u64; 4]; S];
    let mut ok = true;
    for (j, &x) in a.iter().enumerate() {
        let mut nxt = [[0u64; 4]; S];
        if !ctx.extend(&cur, &mut nxt, j, x % nm) { ok = false; }
        cur = nxt;
    }
    let fin = cur[MAXN][0] & 1 == 0;
    assert!(ok || !fin, "prefix invalid but full set valid?!");
    fin
}

/// Brute force: enumerate all k >= 0 with sum k = n; valid iff only k = 1 hits p.
fn valid_brute(a: &[usize], nm: usize) -> bool {
    let n = a.len();
    let p = a.iter().sum::<usize>() % nm;
    let mut k = vec![0usize; n];
    fn rec(i: usize, left: usize, val: usize, a: &[usize], nm: usize, p: usize, k: &mut Vec<usize>, hits: &mut usize) {
        let n = a.len();
        if i == n - 1 {
            k[i] = left;
            if (val + left * a[i]) % nm == p && k.iter().any(|&v| v != 1) { *hits += 1; }
            return;
        }
        for t in 0..=left {
            k[i] = t;
            rec(i + 1, left - t, (val + t * a[i]) % nm, a, nm, p, k, hits);
        }
    }
    let mut hits = 0;
    rec(0, n, 0, a, nm, p, &mut k, &mut hits);
    hits == 0
}

fn assert_associates(nm: usize) {
    // every d in Z_N equals u * gcd(d, N) for some unit u
    for d in 1..nm {
        let g = gcd(d, nm);
        assert!((1..nm).any(|u| gcd(u, nm) == 1 && (u * g) % nm == d), "associates fail N={} d={}", nm, d);
    }
}

struct Search<'a> { verify: bool, gt: Vec<usize>, ctx: Ctx, g: usize, canon: bool, nodes: u64, found: u64, first: Option<Vec<usize>>, a: Vec<usize>, lv: &'a mut Vec<[BS; S]> }

impl<'a> Search<'a> {
    fn rec(&mut self, j: usize, lo: usize) {
        // j elements placed in self.a[0..j]; place a[j] >= lo
        let n = self.ctx.n; let nm = self.ctx.nm;
        if j == n {
            self.found += 1;
            if self.first.is_none() { self.first = Some(self.a.clone()); }
            return;
        }
        if nm < lo + (n - j) { return; }
        // Quick filter. The extended prefix is invalid iff some nonzero balanced c on it has
        // value 0; c restricted to the old prefix cannot (old prefix valid), so c_x = t != 0 and
        // the old part is an element of old'[-t] (zero vector allowed; -t != 0 here):
        // invalid iff x in old[1] (t = -1) or -t*x in old[-t] for some 1 <= t <= j.
        let off = MAXN;
        let bit = |b: &BS, v: usize| (b[v >> 6] >> (v & 63)) & 1 == 1;
        let verify = self.verify;
        for x in lo..=(nm - (n - j)) {
            if self.canon && self.a[..j].iter().any(|&y| self.gt[x - y] < self.g) { continue; }
            self.nodes += 1;
            let old = &self.lv[j];
            let mut bad = bit(&old[off + 1], x);
            let mut tx = 0usize;
            for t in 1..=j {
                if bad { break; }
                tx += x; if tx >= nm { tx -= nm; }
                bad = bit(&old[off - t], (nm - tx) % nm);
            }
            if bad && !verify { continue; }
            let (l, r) = self.lv.split_at_mut(j + 1);
            let ok = self.ctx.extend(&l[j], &mut r[0], j, x);
            assert_eq!(ok, !bad, "quick filter disagrees with DP at N={} prefix={:?} x={}", nm, &self.a[..j], x);
            if ok {
                self.a[j] = x;
                self.rec(j + 1, x + 1);
            }
        }
    }
}

/// Run the subtree below a fixed prefix; returns (nodes, found, first example)
fn run_prefix(n: usize, nm: usize, g: usize, canon: bool, prefix: &[usize]) -> (u64, u64, Option<Vec<usize>>) {
    let ctx = Ctx { n, nm, m: mask(nm) };
    let mut lv = vec![[[0u64; 4]; S]; n + 1];
    let mut nodes = 0u64;
    for (j, &x) in prefix.iter().enumerate() {
        let (l, r) = lv.split_at_mut(j + 1);
        nodes += 1;
        if !ctx.extend(&l[j], &mut r[0], j, x) { return (nodes, 0, None); }
    }
    let mut a = vec![0usize; n];
    a[..prefix.len()].copy_from_slice(prefix);
    let lo = prefix.last().unwrap() + 1;
    let gt: Vec<usize> = (0..nm).map(|d| gcd(d, nm)).collect();
    let verify = std::env::var("VERIFY").is_ok();
    let mut s = Search { verify, gt, ctx, g, canon, nodes: 0, found: 0, first: None, a, lv: &mut lv };
    s.rec(prefix.len(), lo);
    (nodes + s.nodes, s.found, s.first)
}

#[derive(Clone, Default)]
struct Res { nodes: u64, found: u64, first: Option<Vec<usize>>, tasks_left: usize }

fn search_range(n: usize, nlo: usize, nhi: usize, canon: bool, threads: usize, out: Option<&str>) {
    // tasks: (N, g, a1, a2) with a0 = 0 fixed
    let mut tasks: Vec<(usize, usize, usize, usize)> = vec![];
    for nm in nlo..=nhi {
        if nm < n { continue; }
        assert_associates(nm);
        let gs: Vec<usize> = if canon { (1..nm).filter(|g| nm % g == 0).collect() } else { vec![0] };
        for &g in &gs {
            let a1s: Vec<usize> = if canon { vec![g] } else { (1..nm).collect() };
            for &a1 in &a1s {
                if n == 2 { tasks.push((nm, g, a1, 0)); continue; }
                for a2 in a1 + 1..nm {
                    if canon && (gcd(a2, nm) < g || gcd(a2 - a1, nm) < g) { continue; }
                    tasks.push((nm, g, a1, a2));
                }
            }
        }
    }
    tasks.sort_by(|a, b| b.0.cmp(&a.0).then(a.3.cmp(&b.3))); // big N first
    let mut per: std::collections::BTreeMap<usize, Res> = Default::default();
    for t in &tasks { per.entry(t.0).or_default().tasks_left += 1; }
    let per = Arc::new(Mutex::new(per));
    let tasks = Arc::new(tasks);
    let idx = Arc::new(AtomicUsize::new(0));
    let t0 = Instant::now();
    let out = out.map(|s| s.to_string());
    let mut hs = vec![];
    for _ in 0..threads {
        let (per, tasks, idx, out) = (per.clone(), tasks.clone(), idx.clone(), out.clone());
        hs.push(std::thread::spawn(move || loop {
            let i = idx.fetch_add(1, Ordering::SeqCst);
            if i >= tasks.len() { break; }
            let (nm, g, a1, a2) = tasks[i];
            let pre: Vec<usize> = if n == 2 { vec![0, a1] } else { vec![0, a1, a2] };
            let tt = Instant::now();
            let (nodes, found, first) = run_prefix(n, nm, g, canon, &pre);
            let dt = tt.elapsed().as_secs_f64();
            let mut p = per.lock().unwrap();
            let r = p.get_mut(&nm).unwrap();
            r.nodes += nodes; r.found += found;
            if r.first.is_none() { r.first = first; }
            r.tasks_left -= 1;
            let _ = dt;
            if r.tasks_left == 0 {
                let line = format!("n={} N={} mode={} valid_found={} nodes={} finished_at={:.1}s example={:?}",
                    n, nm, if canon { "canon" } else { "plain" }, r.found, r.nodes, t0.elapsed().as_secs_f64(), r.first);
                println!("{}", line);
                if let Some(f) = &out {
                    use std::io::Write;
                    let mut fh = std::fs::OpenOptions::new().create(true).append(true).open(f).unwrap();
                    writeln!(fh, "{}", line).unwrap();
                }
            }
        }));
    }
    for h in hs { h.join().unwrap(); }
    let p = per.lock().unwrap();
    let least = p.iter().find(|(_, r)| r.found > 0).map(|(nm, _)| *nm);
    let total: u64 = p.values().map(|r| r.nodes).sum();
    println!("SUMMARY n={} N={}..{} least_valid_N={:?} total_nodes={} total_time={:.1}s threads={}",
        n, nlo, nhi, least, total, t0.elapsed().as_secs_f64(), threads);
}

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 { self.0 ^= self.0 << 13; self.0 ^= self.0 >> 7; self.0 ^= self.0 << 17; self.0 }
    fn below(&mut self, m: usize) -> usize { (self.next() % m as u64) as usize }
}

fn crosscheck(trials: usize, seed: u64) {
    let mut rng = Rng(seed | 1);
    let (mut agree, mut nvalid) = (0, 0);
    let mut by_n = [[0usize; 2]; 9];
    for it in 0..trials {
        let n = 2 + rng.below(7); // 2..8
        let lo = 1usize << (n - 1); // valid sets need N >= 2^(n-1) (L3); sample around there
        let nm = (lo + rng.below(lo + 1)).max(n).min(256);
        let mut a: Vec<usize> = vec![];
        if it % 4 == 0 { a = (0..n).map(|k| ((1usize << k) - 1) % nm).collect(); a.sort(); a.dedup(); }
        if a.len() != n {
            a.clear();
            while a.len() < n { let x = rng.below(nm); if !a.contains(&x) { a.push(x); } }
        }
        for i in (1..n).rev() { let j = rng.below(i + 1); a.swap(i, j); } // order must not matter
        let d = valid_dp(&a, nm); let b = valid_brute(&a, nm);
        if d != b { println!("MISMATCH n={} N={} A={:?} dp={} brute={}", n, nm, a, d, b); std::process::exit(1); }
        agree += 1; if d { nvalid += 1; }
        by_n[n][d as usize] += 1;
    }
    println!("crosscheck: {} random trials agree ({} valid, {} invalid)", agree, nvalid, agree - nvalid);
    for n in 2..9 { println!("  n={}: invalid={} valid={}", n, by_n[n][0], by_n[n][1]); }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let threads = std::env::var("THREADS").ok().and_then(|s| s.parse().ok()).unwrap_or(
        std::thread::available_parallelism().map(|x| x.get()).unwrap_or(1));
    match args.get(1).map(|s| s.as_str()) {
        Some("search") => {
            let n: usize = args[2].parse().unwrap();
            let nlo: usize = args[3].parse().unwrap();
            let nhi: usize = args[4].parse().unwrap();
            let canon = args.get(5).map(|s| s != "plain").unwrap_or(true);
            assert!(n >= 2 && n <= MAXN && nhi <= 256);
            search_range(n, nlo, nhi, canon, threads, args.get(6).map(|s| s.as_str()));
        }
        Some("check") => {
            let nm: usize = args[2].parse().unwrap();
            let a: Vec<usize> = args[3..].iter().map(|s| s.parse::<usize>().unwrap() % nm).collect();
            println!("N={} A={:?} dp_valid={} brute_valid={}", nm, a, valid_dp(&a, nm), valid_brute(&a, nm));
        }
        Some("crosscheck") => {
            crosscheck(args[2].parse().unwrap(), args.get(3).map(|s| s.parse().unwrap()).unwrap_or(12345));
        }
        _ => eprintln!("usage: search n Nlo Nhi [canon|plain] [outfile] | check N a0 a1 ... | crosscheck trials [seed]"),
    }
}
