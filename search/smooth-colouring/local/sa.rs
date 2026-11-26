// Simulated annealing for periodic tilings phi([n]) (+) B = G.
// Variables: phi(p) in G for every prime p <= n, and B (|B| = m, B[0] = 0) unless B fixed.
// Objective: number of colliding pairs in the multiset {phi(a)+b : a<=n, b in B}
// (zero iff A (+) B = G with phi injective on [n], since n*m = |G|).
// Usage: sa n=195 dims=3,25,13 m=5 seed=1 iters=200000000 [B=fixed list b/b/..,..] [Bmode=free|fixed|ap]
//        [restarts=R] [t0=..] [t1=..]
use std::env;
use std::time::Instant;

struct Rng(u64);
impl Rng {
    fn next(&mut self) -> u64 { self.0 ^= self.0 << 13; self.0 ^= self.0 >> 7; self.0 ^= self.0 << 17; self.0 }
    fn below(&mut self, k: usize) -> usize { (self.next() % k as u64) as usize }
    fn f(&mut self) -> f64 { (self.next() >> 11) as f64 / (1u64 << 53) as f64 }
}

fn main() {
    let mut n = 195usize; let mut dims: Vec<usize> = vec![3, 25, 13]; let mut m = 5usize;
    let mut seed = 1u64; let mut iters = 100_000_000u64; let mut bmode = "free".to_string();
    let mut bfixed: Vec<Vec<usize>> = vec![]; let mut restarts = 1000000usize;
    let mut t0 = 2.0f64; let mut t1 = 0.05f64; let mut tlimit = 1e9f64;
    for a in env::args().skip(1) {
        let (k, v) = a.split_once('=').unwrap();
        match k {
            "n" => n = v.parse().unwrap(),
            "dims" => dims = v.split(',').map(|x| x.parse().unwrap()).collect(),
            "m" => m = v.parse().unwrap(),
            "seed" => seed = v.parse().unwrap(),
            "iters" => iters = v.parse().unwrap(),
            "Bmode" => bmode = v.to_string(),
            "B" => { bfixed = v.split(',').map(|t| t.split('/').map(|c| c.parse().unwrap()).collect()).collect(); bmode = "fixed".into(); }
            "restarts" => restarts = v.parse().unwrap(),
            "t0" => t0 = v.parse().unwrap(),
            "t1" => t1 = v.parse().unwrap(),
            "secs" => tlimit = v.parse().unwrap(),
            _ => panic!("bad arg {}", k),
        }
    }
    let g: usize = dims.iter().product();
    assert_eq!(g, n * m, "|G| must be n*m");
    let r = dims.len();
    let enc = |c: &Vec<usize>| -> usize { let mut x = 0; for i in 0..r { x = x * dims[i] + c[i] % dims[i]; } x };
    let dec = |mut x: usize| -> Vec<usize> { let mut c = vec![0; r]; for i in (0..r).rev() { c[i] = x % dims[i]; x /= dims[i]; } c };
    // addition table
    let decs: Vec<Vec<usize>> = (0..g).map(|x| dec(x)).collect();
    let mut add = vec![0u16; g * g];
    for x in 0..g { for y in 0..g {
        let c: Vec<usize> = (0..r).map(|i| (decs[x][i] + decs[y][i]) % dims[i]).collect();
        add[x * g + y] = enc(&c) as u16; } }
    let neg: Vec<usize> = (0..g).map(|x| enc(&(0..r).map(|i| (dims[i] - decs[x][i]) % dims[i]).collect())).collect();
    let mul = |k: usize, x: usize| -> usize { let mut s = 0; for _ in 0..k { s = add[s * g + x] as usize; } s };
    // primes and factorizations
    let primes: Vec<usize> = (2..=n).filter(|&p| (2..p).all(|d| p % d != 0)).collect();
    let np = primes.len();
    let mut fac: Vec<Vec<(usize, usize)>> = vec![vec![]; n + 1]; // (prime idx, exp)
    for a in 1..=n { let mut x = a; for (i, &p) in primes.iter().enumerate() { let mut e = 0; while x % p == 0 { x /= p; e += 1; } if e > 0 { fac[a].push((i, e)); } } }
    let mut mults: Vec<Vec<(usize, usize)>> = vec![vec![]; np]; // (a, exp)
    for a in 1..=n { for &(i, e) in &fac[a] { mults[i].push((a, e)); } }
    let mut rng = Rng(seed.wrapping_mul(0x9E3779B97F4A7C15) | 1);
    let start = Instant::now();
    let mut global_best = usize::MAX;
    for rs in 0..restarts {
        if start.elapsed().as_secs_f64() > tlimit { break; }
        let mut ph: Vec<usize> = (0..np).map(|_| rng.below(g)).collect();
        let mut b: Vec<usize> = if bmode == "fixed" { bfixed.iter().map(|c| enc(c)).collect() } else {
            let mut v = vec![0]; while v.len() < m { let x = rng.below(g); if !v.contains(&x) { v.push(x); } } v };
        if bmode == "ap" { let d = b[1]; b = (0..m).map(|k| mul(k, d)).collect(); }
        let mut pa = vec![0usize; n + 1];
        let recompute_pa = |ph: &Vec<usize>, pa: &mut Vec<usize>| { for a in 1..=n { let mut s = 0; for &(i, e) in &fac[a] { for _ in 0..e { s = add[s * g + ph[i]] as usize; } } pa[a] = s; } };
        recompute_pa(&ph, &mut pa);
        let mut cnt = vec![0i32; g];
        let mut cost: i64 = 0;
        for a in 1..=n { for &bb in &b { let c = add[pa[a] * g + bb] as usize; cost += cnt[c] as i64; cnt[c] += 1; } }
        let mut best = cost; let mut bestph = ph.clone(); let mut bestb = b.clone();
        let mut newpa: Vec<(usize, usize)> = Vec::with_capacity(n);
        let nb_moves = if bmode == "free" { m - 1 } else if bmode == "ap" { 1 } else { 0 };
        for it in 0..iters {
            let frac = it as f64 / iters as f64;
            let t = t0 * (t1 / t0).powf(frac);
            let pick = rng.below(np + nb_moves * 4);
            if pick < np {
                let i = pick; let nv = rng.below(g); let old = ph[i];
                if nv == old { continue; }
                // delta v = nv - old
                let dv = add[nv * g + neg[old]] as usize;
                let mut delta: i64 = 0;
                newpa.clear();
                for &(a, e) in &mults[i] { let mut s = pa[a]; for _ in 0..e { s = add[s * g + dv] as usize; } newpa.push((a, s)); }
                for &(a, _) in &newpa { for &bb in &b { let c = add[pa[a] * g + bb] as usize; cnt[c] -= 1; delta -= cnt[c] as i64; } }
                for &(_, s) in &newpa { for &bb in &b { let c = add[s * g + bb] as usize; delta += cnt[c] as i64; cnt[c] += 1; } }
                if delta <= 0 || rng.f() < (-(delta as f64) / t).exp() {
                    ph[i] = nv; for &(a, s) in &newpa { pa[a] = s; } cost += delta;
                } else {
                    for &(_, s) in &newpa { for &bb in &b { let c = add[s * g + bb] as usize; cnt[c] -= 1; } }
                    for &(a, _) in &newpa { for &bb in &b { let c = add[pa[a] * g + bb] as usize; cnt[c] += 1; } }
                }
            } else {
                // B move
                let nbv: Vec<usize> = if bmode == "free" {
                    let j = 1 + rng.below(m - 1); let x = rng.below(g); if b.contains(&x) { continue; }
                    let mut v = b.clone(); v[j] = x; v
                } else { let d = rng.below(g); let v: Vec<usize> = (0..m).map(|k| mul(k, d)).collect();
                    let mut s = v.clone(); s.sort(); s.dedup(); if s.len() < m { continue; } v };
                let mut delta: i64 = 0;
                for a in 1..=n { for &bb in &b { let c = add[pa[a] * g + bb] as usize; cnt[c] -= 1; delta -= cnt[c] as i64; } }
                for a in 1..=n { for &bb in &nbv { let c = add[pa[a] * g + bb] as usize; delta += cnt[c] as i64; cnt[c] += 1; } }
                if delta <= 0 || rng.f() < (-(delta as f64) / t).exp() { b = nbv; cost += delta; } else {
                    for a in 1..=n { for &bb in &nbv { let c = add[pa[a] * g + bb] as usize; cnt[c] -= 1; } }
                    for a in 1..=n { for &bb in &b { let c = add[pa[a] * g + bb] as usize; cnt[c] += 1; } }
                }
            }
            if cost < best { best = cost; bestph = ph.clone(); bestb = b.clone(); if best == 0 { break; } }
        }
        if (best as usize) < global_best { global_best = best as usize; }
        let fmt = |x: usize| decs[x].iter().map(|c| c.to_string()).collect::<Vec<_>>().join("/");
        let bs = bestb.iter().map(|&x| fmt(x)).collect::<Vec<_>>().join(",");
        if best == 0 {
            let phs = (0..np).map(|i| format!("{}:{}", primes[i], fmt(bestph[i]))).collect::<Vec<_>>().join(" ");
            println!("SOLUTION n={} dims={} Bused={} phi= {}", n, dims.iter().map(|d| d.to_string()).collect::<Vec<_>>().join(","), bs, phs);
            return;
        }
        println!("restart {} best={} global={} B={} secs={:.1}", rs, best, global_best, bs, start.elapsed().as_secs_f64());
    }
    println!("DONE global_best={}", global_best);
}
