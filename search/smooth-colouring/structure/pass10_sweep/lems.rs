// pass 10: fast Rust re-implementation of pass9 lemS.py (exh / rand) plus a Knuth tree-size
// estimator and the targeted joint (g, h) search of lemS_target.py.
//
// T = T_n (exponent vectors of 1..n).  g: Z^k -> Z_m (m = n/p) with every fibre on T of size p.
// Singleton primes (2q > n) are dropped (Lemma R, pass9_lemmaS.md); they only fill holes.
// Gamma' = Z^{k'}/M' (k' = #non-singleton primes) has the same torsion as Gamma.
// Torsion test: SNF of M' over Z/p^E (E max with p^E < 2^62) gives the p-valuations of the
// elementary divisors with v_p < E; rank_Q(M') = max of ranks mod three 61-bit primes (rigorous:
// every minor is < 14^25 < 2^96 in absolute value, so it cannot vanish mod all three primes
// unless it is 0).  Asserted: #SNF pivots == rank_Q, so all valuations were seen.
//
// Modes:
//   lems exh  n p threads ckpt_file [depth]   exhaustive (g(2) restricted to 0 and divisors of m)
//   lems rand n p N seed cap threads          random-restart randomized DFS samples
//   lems est  n p probes seed [h]             Knuth estimator of tree size (h: joint (g,h) tree)
//   lems trand n p N seed cap threads         targeted joint (g,h) random restarts (p !| m)
use std::io::{BufRead, Write};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};

struct Inst {
    n: usize,
    p: u64,
    m: usize,
    primes: Vec<usize>,
    sing: Vec<usize>,      // indices into primes
    kp: usize,             // number of non-singleton primes (they are primes[0..kp])
    pts: Vec<Vec<i64>>,    // non-singleton points (numbers 2..n with no singleton factor), kp coords
    num: Vec<usize>,       // the number of each point
    pts_at: Vec<Vec<usize>>, // points whose largest prime index is t
}

fn primes_upto(n: usize) -> Vec<usize> {
    (2..=n).filter(|&x| (2..x).take_while(|d| d * d <= x).all(|d| x % d != 0)).collect()
}

impl Inst {
    fn new(n: usize, p: u64) -> Inst {
        assert!(n as u64 % p == 0);
        let primes = primes_upto(n);
        let kp = primes.iter().filter(|&&q| 2 * q <= n).count();
        let sing: Vec<usize> = (kp..primes.len()).collect();
        let mut pts = vec![];
        let mut num = vec![];
        let mut pts_at = vec![vec![]; kp];
        for x in 2..=n {
            let mut y = x;
            let mut v = vec![0i64; primes.len()];
            for (i, &q) in primes.iter().enumerate() {
                while y % q == 0 {
                    y /= q;
                    v[i] += 1;
                }
            }
            if v[kp..].iter().any(|&e| e > 0) {
                continue;
            }
            let t = (0..kp).rev().find(|&i| v[i] > 0).unwrap();
            pts_at[t].push(pts.len());
            pts.push(v[..kp].to_vec());
            num.push(x);
        }
        Inst { n, p, m: n / p as usize, primes, sing, kp, pts, num, pts_at }
    }
}

fn vp(mut x: u64, p: u64) -> u32 {
    let mut v = 0;
    while x % p == 0 && x > 0 {
        x /= p;
        v += 1;
    }
    v
}

fn mulmod(a: u64, b: u64, q: u64) -> u64 {
    ((a as u128 * b as u128) % q as u128) as u64
}

fn inv_mod(a: u64, q: u64) -> u64 {
    let (mut r0, mut r1) = (q as i128, a as i128);
    let (mut s0, mut s1) = (0i128, 1i128);
    while r1 != 0 {
        let qq = r0 / r1;
        let t = r0 - qq * r1;
        r0 = r1;
        r1 = t;
        let t = s0 - qq * s1;
        s0 = s1;
        s1 = t;
    }
    assert!(r0 == 1);
    (((s0 % q as i128) + q as i128) % q as i128) as u64
}

fn rank_mod(rows: &[Vec<i64>], k: usize, l: u64) -> usize {
    let mut a: Vec<Vec<u64>> = rows
        .iter()
        .map(|r| r.iter().map(|&x| ((x % l as i64) + l as i64) as u64 % l).collect())
        .collect();
    let mut rk = 0;
    for c in 0..k {
        let piv = (rk..a.len()).find(|&i| a[i][c] != 0);
        let Some(pi) = piv else { continue };
        a.swap(rk, pi);
        let iv = inv_mod(a[rk][c], l);
        for i in rk + 1..a.len() {
            if a[i][c] != 0 {
                let f = mulmod(a[i][c], iv, l);
                for j in c..k {
                    let s = mulmod(f, a[rk][j], l);
                    a[i][j] = (a[i][j] + l - s) % l;
                }
            }
        }
        rk += 1;
    }
    rk
}

/// p-valuations of the elementary divisors of the row lattice that are nonzero mod p^E
fn snf_local(rows: &[Vec<i64>], k: usize, p: u64) -> Vec<u32> {
    let mut q: u64 = 1;
    while (q as u128) * (p as u128) < (1u128 << 62) {
        q *= p;
    }
    let mut a: Vec<Vec<u64>> = rows
        .iter()
        .map(|r| r.iter().map(|&x| (((x as i128 % q as i128) + q as i128) % q as i128) as u64).collect())
        .filter(|r: &Vec<u64>| r.iter().any(|&x| x != 0))
        .collect();
    let mut cols: Vec<bool> = vec![true; k];
    let mut vals = vec![];
    loop {
        let mut best: Option<(u32, usize, usize)> = None;
        'o: for (i, r) in a.iter().enumerate() {
            for j in 0..k {
                if cols[j] && r[j] != 0 {
                    let v = vp(r[j], p);
                    if best.map_or(true, |b| v < b.0) {
                        best = Some((v, i, j));
                        if v == 0 {
                            break 'o;
                        }
                    }
                }
            }
        }
        let Some((v, i, j)) = best else { break };
        vals.push(v);
        let r = a.swap_remove(i);
        let pv = p.pow(v);
        let u = r[j] / pv;
        let uinv = inv_mod(u % q, q);
        let mut na = Vec::with_capacity(a.len());
        for mut s in a.into_iter() {
            if s[j] != 0 {
                let c = mulmod(s[j] / pv, uinv, q);
                for t in 0..k {
                    let sub = mulmod(c, r[t], q);
                    s[t] = (s[t] + q - sub) % q;
                }
            }
            if s.iter().any(|&x| x != 0) {
                na.push(s);
            }
        }
        a = na;
        cols[j] = false;
    }
    vals
}

const L1: u64 = 2305843009213693951; // 2^61-1
const L2: u64 = 2305843009213693921;
const L3: u64 = 2305843009213693907;

/// returns (log_p exp(Gamma_p), rank_Q)
fn gamma_p(inst: &Inst, res: &[usize]) -> (u32, usize) {
    let k = inst.kp;
    let mut first: Vec<Option<usize>> = vec![None; inst.m];
    let mut rows: Vec<Vec<i64>> = vec![];
    // point 1 (zero vector) sits in class 0
    for (pi, &r) in res.iter().enumerate() {
        if r == 0 {
            rows.push(inst.pts[pi].clone());
        } else if let Some(f) = first[r] {
            rows.push(inst.pts[pi].iter().zip(&inst.pts[f]).map(|(a, b)| a - b).collect());
        } else {
            first[r] = Some(pi);
        }
    }
    let vals = snf_local(&rows, k, inst.p);
    let rq = if vals.len() == k {
        k
    } else {
        let r1 = rank_mod(&rows, k, L1);
        let r2 = rank_mod(&rows, k, L2);
        let r3 = rank_mod(&rows, k, L3);
        r1.max(r2).max(r3)
    };
    assert!(vals.len() == rq, "E too small or bug: pivots {} rankQ {}", vals.len(), rq);
    (vals.into_iter().max().unwrap_or(0), rq)
}

fn full_g(inst: &Inst, g: &[usize], cnt: &[u64]) -> Vec<usize> {
    let mut out = g.to_vec();
    let mut holes = vec![];
    for r in 0..inst.m {
        for _ in cnt[r]..inst.p {
            holes.push(r);
        }
    }
    assert!(holes.len() == inst.sing.len());
    for (&i, &r) in inst.sing.iter().zip(&holes) {
        out.push(r);
        let _ = i;
    }
    out
}

struct St {
    g: Vec<usize>,
    cnt: Vec<u64>,
    res: Vec<usize>,
}

impl St {
    fn new(inst: &Inst) -> St {
        let mut cnt = vec![0u64; inst.m];
        cnt[0] = 1;
        St { g: vec![0; inst.kp], cnt, res: vec![usize::MAX; inst.pts.len()] }
    }
    // try assigning value a at level t; returns number of points added (all ok) or None (undone)
    fn push(&mut self, inst: &Inst, t: usize, a: usize) -> bool {
        self.g[t] = a;
        let m = inst.m;
        let at = &inst.pts_at[t];
        for (c, &pi) in at.iter().enumerate() {
            let x = &inst.pts[pi];
            let mut r = 0usize;
            for j in 0..=t {
                r += self.g[j] * x[j] as usize;
            }
            r %= m;
            if self.cnt[r] >= inst.p {
                for &pj in &at[..c] {
                    self.cnt[self.res[pj]] -= 1;
                }
                return false;
            }
            self.cnt[r] += 1;
            self.res[pi] = r;
        }
        true
    }
    fn pop(&mut self, inst: &Inst, t: usize) {
        for &pi in &inst.pts_at[t] {
            self.cnt[self.res[pi]] -= 1;
        }
    }
}

fn cands(inst: &Inst, t: usize) -> Vec<usize> {
    if t == 0 {
        (0..inst.m).filter(|&d| d == 0 || inst.m % d == 0).collect()
    } else {
        (0..inst.m).collect()
    }
}

struct Acc {
    nodes: u64,
    sols: u64,
    hist: [u64; 64],
    samples: Vec<(u32, Vec<usize>)>,
    seen: [bool; 64],
}

fn dfs(inst: &Inst, st: &mut St, t: usize, acc: &mut Acc) {
    acc.nodes += 1;
    if t == inst.kp {
        acc.sols += 1;
        let (e, _) = gamma_p(inst, &st.res);
        acc.hist[e as usize] += 1;
        let bound = vp(inst.m as u64, inst.p);
        if e > bound || !acc.seen[e as usize] {
            acc.seen[e as usize] = true;
            acc.samples.push((e, full_g(inst, &st.g, &st.cnt)));
        }
        if e > bound {
            eprintln!("VIOLATION e={} g={:?}", e, full_g(inst, &st.g, &st.cnt));
        }
        return;
    }
    for a in cands(inst, t) {
        if st.push(inst, t, a) {
            dfs(inst, st, t + 1, acc);
            st.pop(inst, t);
        }
    }
}

fn gen_tasks(inst: &Inst, st: &mut St, t: usize, depth: usize, pre: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
    if t == depth || t == inst.kp {
        out.push(pre.clone());
        return;
    }
    for a in cands(inst, t) {
        if st.push(inst, t, a) {
            pre.push(a);
            gen_tasks(inst, st, t + 1, depth, pre, out);
            pre.pop();
            st.pop(inst, t);
        }
    }
}

fn fmt_g(g: &[usize]) -> String {
    g.iter().map(|x| x.to_string()).collect::<Vec<_>>().join(",")
}

fn exh(n: usize, p: u64, threads: usize, ck: &str, depth: usize) {
    let inst = Arc::new(Inst::new(n, p));
    let mut st = St::new(&inst);
    let mut tasks = vec![];
    gen_tasks(&inst, &mut st, 0, depth.min(inst.kp), &mut vec![], &mut tasks);
    let mut done = std::collections::HashSet::new();
    if let Ok(f) = std::fs::File::open(ck) {
        for line in std::io::BufReader::new(f).lines() {
            let line = line.unwrap();
            let w: Vec<&str> = line.split_whitespace().collect();
            if w.first() == Some(&"T") {
                done.insert(w[1].parse::<usize>().unwrap());
            }
        }
    }
    let ntask = tasks.len();
    eprintln!("n={} p={} m={} kp={} tasks={} already done={}", n, p, inst.m, inst.kp, ntask, done.len());
    let file = Arc::new(Mutex::new(
        std::fs::OpenOptions::new().create(true).append(true).open(ck).unwrap(),
    ));
    let todo: Arc<Vec<usize>> = Arc::new((0..ntask).filter(|i| !done.contains(i)).collect());
    let tasks = Arc::new(tasks);
    let next = Arc::new(AtomicUsize::new(0));
    let mut hs = vec![];
    for _ in 0..threads {
        let (inst, tasks, todo, next, file) = (inst.clone(), tasks.clone(), todo.clone(), next.clone(), file.clone());
        hs.push(std::thread::spawn(move || loop {
            let i = next.fetch_add(1, Ordering::SeqCst);
            if i >= todo.len() {
                break;
            }
            let ti = todo[i];
            let pre = &tasks[ti];
            let mut st = St::new(&inst);
            for (t, &a) in pre.iter().enumerate() {
                assert!(st.push(&inst, t, a));
            }
            let mut acc = Acc { nodes: 0, sols: 0, hist: [0; 64], samples: vec![], seen: [false; 64] };
            dfs(&inst, &mut st, pre.len(), &mut acc);
            let mut s = String::new();
            for (e, g) in &acc.samples {
                s += &format!("S {} {} {}\n", ti, e, fmt_g(g));
            }
            let h: Vec<String> = (0..64).filter(|&e| acc.hist[e] > 0).map(|e| format!("{}:{}", e, acc.hist[e])).collect();
            s += &format!("T {} {} {} {}\n", ti, acc.nodes, acc.sols, h.join(","));
            let mut f = file.lock().unwrap();
            f.write_all(s.as_bytes()).unwrap();
            f.flush().unwrap();
        }));
    }
    for h in hs {
        h.join().unwrap();
    }
    summarize(&inst, ck, ntask);
}

fn summarize(inst: &Inst, ck: &str, ntask: usize) {
    let f = std::fs::File::open(ck).unwrap();
    let (mut nodes, mut sols, mut hist, mut nt) = (0u64, 0u64, [0u64; 64], 0usize);
    let mut seen = std::collections::HashSet::new();
    for line in std::io::BufReader::new(f).lines() {
        let line = line.unwrap();
        let w: Vec<&str> = line.split_whitespace().collect();
        if w.first() == Some(&"T") && seen.insert(w[1].to_string()) {
            nt += 1;
            nodes += w[2].parse::<u64>().unwrap();
            sols += w[3].parse::<u64>().unwrap();
            if w.len() > 4 {
                for kv in w[4].split(',') {
                    let mut it = kv.split(':');
                    let e: usize = it.next().unwrap().parse().unwrap();
                    hist[e] += it.next().unwrap().parse::<u64>().unwrap();
                }
            }
        }
    }
    let bound = vp(inst.m as u64, inst.p);
    let viol: u64 = (bound as usize + 1..64).map(|e| hist[e]).sum();
    let h: Vec<String> = (0..64).filter(|&e| hist[e] > 0).map(|e| format!("{}: {}", e, hist[e])).collect();
    println!(
        "n={} p={} m={} k={} singletons={} tasks_done={}/{} nodes={} solutions={} histogram={{{}}} bound={} violations={} {}",
        inst.n, inst.p, inst.m, inst.primes.len(), inst.sing.len(), nt, ntask, nodes, sols, h.join(", "), bound, viol,
        if nt == ntask { "COMPLETE" } else { "INCOMPLETE" }
    );
}

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 {
        self.0 ^= self.0 << 13;
        self.0 ^= self.0 >> 7;
        self.0 ^= self.0 << 17;
        self.0
    }
    fn below(&mut self, k: usize) -> usize {
        (self.next() % k as u64) as usize
    }
    fn shuffle<T>(&mut self, v: &mut [T]) {
        for i in (1..v.len()).rev() {
            let j = self.below(i + 1);
            v.swap(i, j);
        }
    }
}

// ---------------- joint (g,h) state for the targeted search (p !| m) ----------------
struct HSt {
    g: Vec<usize>,
    h: Vec<u64>,
    cnt: Vec<u64>,
    hv: Vec<u64>, // u64::MAX = unset
    res: Vec<usize>,
    prev_hv: Vec<u64>,
}
impl HSt {
    fn new(inst: &Inst) -> HSt {
        let mut cnt = vec![0u64; inst.m];
        cnt[0] = 1;
        let mut hv = vec![u64::MAX; inst.m];
        hv[0] = 0;
        HSt { g: vec![0; inst.kp], h: vec![0; inst.kp], cnt, hv, res: vec![0; inst.pts.len()], prev_hv: vec![0; inst.pts.len()] }
    }
    fn push(&mut self, inst: &Inst, t: usize, a: usize, b: u64) -> bool {
        self.g[t] = a;
        self.h[t] = b;
        let at = &inst.pts_at[t];
        for (c, &pi) in at.iter().enumerate() {
            let x = &inst.pts[pi];
            let (mut r, mut hx) = (0usize, 0u64);
            for j in 0..=t {
                r += self.g[j] * x[j] as usize;
                hx += self.h[j] * x[j] as u64;
            }
            r %= inst.m;
            hx %= inst.p;
            if self.cnt[r] >= inst.p || (self.hv[r] != u64::MAX && self.hv[r] != hx) {
                for &pj in at[..c].iter().rev() {
                    self.cnt[self.res[pj]] -= 1;
                    self.hv[self.res[pj]] = self.prev_hv[pj];
                }
                return false;
            }
            self.prev_hv[pi] = self.hv[r];
            self.cnt[r] += 1;
            self.hv[r] = hx;
            self.res[pi] = r;
        }
        true
    }
    fn pop(&mut self, inst: &Inst, t: usize) {
        for &pi in inst.pts_at[t].iter().rev() {
            self.cnt[self.res[pi]] -= 1;
            self.hv[self.res[pi]] = self.prev_hv[pi];
        }
    }
}

fn rand_dfs(inst: &Inst, st: &mut St, t: usize, rng: &mut Rng, nodes: &mut u64, cap: u64) -> bool {
    *nodes += 1;
    if t == inst.kp {
        return true;
    }
    let mut c: Vec<usize> = (0..inst.m).collect();
    rng.shuffle(&mut c);
    for a in c {
        if *nodes > cap {
            return false;
        }
        if st.push(inst, t, a) {
            if rand_dfs(inst, st, t + 1, rng, nodes, cap) {
                return true;
            }
            st.pop(inst, t);
        }
    }
    false
}

fn hrand_dfs(inst: &Inst, st: &mut HSt, t: usize, fi: usize, rng: &mut Rng, nodes: &mut u64, cap: u64) -> bool {
    *nodes += 1;
    if t == inst.kp {
        return true;
    }
    let mut c: Vec<(usize, u64)> = vec![];
    for a in 0..inst.m {
        if t == fi {
            c.push((a, 1));
        } else {
            for b in 0..inst.p {
                c.push((a, b));
            }
        }
    }
    rng.shuffle(&mut c);
    for (a, b) in c {
        if *nodes > cap {
            return false;
        }
        if st.push(inst, t, a, b) {
            if hrand_dfs(inst, st, t + 1, fi, rng, nodes, cap) {
                return true;
            }
            st.pop(inst, t);
        }
    }
    false
}

fn rand_mode(n: usize, p: u64, nsamp: usize, seed: u64, cap: u64, threads: usize, target: bool, out: &str) {
    let inst = Arc::new(Inst::new(n, p));
    if target {
        assert!(inst.m as u64 % p != 0);
    }
    let next = Arc::new(AtomicUsize::new(0));
    let file = Arc::new(Mutex::new(std::fs::OpenOptions::new().create(true).append(true).open(out).unwrap()));
    let tot = Arc::new(Mutex::new((0u64, 0u64, [0u64; 64])));
    let mut hs = vec![];
    for _ in 0..threads {
        let (inst, next, file, tot) = (inst.clone(), next.clone(), file.clone(), tot.clone());
        hs.push(std::thread::spawn(move || loop {
            let i = next.fetch_add(1, Ordering::SeqCst);
            if i >= nsamp {
                break;
            }
            let mut rng = Rng(seed.wrapping_mul(0x9E3779B97F4A7C15) ^ (i as u64 + 1).wrapping_mul(0xD1B54A32D192ED03) | 1);
            for _ in 0..10 {
                rng.next();
            }
            let mut nodes = 0u64;
            let res;
            let (ok, g, cnt) = if target {
                let fi = rng.below(inst.kp);
                let mut st = HSt::new(&inst);
                let ok = hrand_dfs(&inst, &mut st, 0, fi, &mut rng, &mut nodes, cap);
                res = st.res.clone();
                (ok, st.g.clone(), st.cnt.clone())
            } else {
                let mut st = St::new(&inst);
                let ok = rand_dfs(&inst, &mut st, 0, &mut rng, &mut nodes, cap);
                res = st.res.clone();
                (ok, st.g.clone(), st.cnt.clone())
            };
            let mut line = String::new();
            let mut tt = tot.lock().unwrap();
            tt.0 += nodes;
            if ok {
                let (e, _) = gamma_p(&inst, &res);
                tt.1 += 1;
                tt.2[e as usize] += 1;
                let fg = full_g(&inst, &g, &cnt);
                line = format!("S {} {} {}\n", i, e, fmt_g(&fg));
                if e > vp(inst.m as u64, inst.p) {
                    eprintln!("VIOLATION e={} g={:?}", e, fg);
                }
            }
            drop(tt);
            line += &format!("R {} {} {}\n", i, nodes, ok as u8);
            let mut f = file.lock().unwrap();
            f.write_all(line.as_bytes()).unwrap();
        }));
    }
    for h in hs {
        h.join().unwrap();
    }
    let tt = tot.lock().unwrap();
    let h: Vec<String> = (0..64).filter(|&e| tt.2[e] > 0).map(|e| format!("{}: {}", e, tt.2[e])).collect();
    println!(
        "{} n={} p={} m={} restarts={} cap={} nodes={} samples={} histogram={{{}}} bound={}",
        if target { "trand" } else { "rand" }, n, p, inst.m, nsamp, cap, tt.0, tt.1, h.join(", "), vp(inst.m as u64, p)
    );
}

fn est_mode(n: usize, p: u64, probes: usize, seed: u64, hmode: bool) {
    let inst = Inst::new(n, p);
    let mut rng = Rng(seed | 1);
    let (mut sn, mut sl) = (0f64, 0f64);
    let mut lvl = vec![0f64; inst.kp + 1];
    for _ in 0..probes {
        let mut w = 1f64;
        let mut nodes = 1f64;
        lvl[0] += 1.0;
        if hmode {
            let fi = rng.below(inst.kp);
            let mut st = HSt::new(&inst);
            w *= inst.kp as f64; // average over the choice of q_first
            let mut t = 0;
            while t < inst.kp {
                let mut ok = vec![];
                for a in 0..inst.m {
                    for b in 0..inst.p {
                        if t == fi && b != 1 {
                            continue;
                        }
                        if st.push(&inst, t, a, b) {
                            ok.push((a, b));
                            st.pop(&inst, t);
                        }
                    }
                }
                if ok.is_empty() {
                    w = 0.0;
                    break;
                }
                w *= ok.len() as f64;
                nodes += w;
                lvl[t + 1] += w;
                let (a, b) = ok[rng.below(ok.len())];
                assert!(st.push(&inst, t, a, b));
                t += 1;
            }
        } else {
            let mut st = St::new(&inst);
            let mut t = 0;
            while t < inst.kp {
                let mut ok = vec![];
                for a in cands(&inst, t) {
                    if st.push(&inst, t, a) {
                        ok.push(a);
                        st.pop(&inst, t);
                    }
                }
                if ok.is_empty() {
                    w = 0.0;
                    break;
                }
                w *= ok.len() as f64;
                nodes += w;
                lvl[t + 1] += w;
                let a = ok[rng.below(ok.len())];
                assert!(st.push(&inst, t, a));
                t += 1;
            }
        }
        sn += nodes;
        sl += if w > 0.0 { w } else { 0.0 };
    }
    let pr = probes as f64;
    println!(
        "est{} n={} p={} m={} kp={} probes={} est_nodes={:.3e} est_leaves={:.3e}",
        if hmode { "(g,h)" } else { "" }, n, p, inst.m, inst.kp, probes, sn / pr, sl / pr
    );
    let l: Vec<String> = lvl.iter().map(|x| format!("{:.2e}", x / pr)).collect();
    println!("  per-level est: {}", l.join(" "));
}

fn main() {
    let a: Vec<String> = std::env::args().collect();
    let n: usize = a[2].parse().unwrap();
    let p: u64 = a[3].parse().unwrap();
    match a[1].as_str() {
        "exh" => exh(n, p, a[4].parse().unwrap(), &a[5], a.get(6).map_or(3, |s| s.parse().unwrap())),
        "rand" | "trand" => rand_mode(n, p, a[4].parse().unwrap(), a[5].parse().unwrap(), a[6].parse().unwrap(),
            a[7].parse().unwrap(), a[1] == "trand", &a[8]),
        "est" => est_mode(n, p, a[4].parse().unwrap(), a[5].parse().unwrap(), a.len() > 6),
        _ => panic!("mode"),
    }
}
