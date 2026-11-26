// dfs2_dump.rs -- COPY of dfs2.rs whose only change: with --all, print every leaf (element indices
// enc(h,f)=h*K+f, in search order) as a line 'SOL ...'. Used by symcheck.py.
// Second change: --from N starts the task queue at prefix index N (tasks < N assumed done elsewhere;
// 'tasks_done' then counts them as done). Used to resume nosym_n195_p3.
// dfs2.rs -- independent exact search for case (b) of structure/prime_B_reduction.md.
//
// Written from the definition in that note only (gtile*.rs not consulted).
//
// DEFINITION (note, Theorem, case (b)).  p prime, p | n, K = n/p, G = Z_{p^2} x Z_K.
// Find a homomorphism phi: Z^{pi(n)} -> G (i.e. values phi(q) in G on the primes q <= n,
// extended completely multiplicatively) such that phi is injective on T = {t(1),...,t(n)} and
// for every k in Z_K the fibre phi(T) ∩ (Z_{p^2} x {k}) is a coset of pZ_{p^2} x {k}.
//
// REFORMULATION used here (elementary, proved in this comment).
//  Write phi(m) = (h(m), f(m)).  Since |T| = n = pK and cosets of pZ_{p^2} have p elements, the
//  condition "phi injective on T and every one of the K fibres is a coset" is equivalent to
//      (P)  for all m != m' in [n]:  f(m) = f(m')  =>  h(m) - h(m') ∈ pZ_{p^2} \ {0}.
//  (=>) same fibre => both in one coset => difference in pZ_{p^2}; injective => nonzero.
//  (<=) (P) gives injectivity (same f forces h different) and each fibre lies in one coset of
//  pZ_{p^2}, so has <= p elements; there are K fibres and n = pK elements, so each fibre has
//  exactly p elements, i.e. is the whole coset.
//  As phi is a homomorphism, phi(m) - phi(m') = phi(t(m) - t(m')).  So (P) says: for every
//  difference vector r = t(m) - t(m') (m != m'), phi(r) ∉ F, where
//      F = { (h, 0) : h ∉ pZ_{p^2} } ∪ { (0,0) }       (|F| = p^2 - p + 1, and F = -F).
//
// LARGE PRIMES (soundness of leaving them out).  A prime q with 2q > n divides exactly one
//  m <= n, namely m = q.  Let S = the set of m <= n all of whose prime factors are "small"
//  (2q <= n).  Then [n] = S ⊔ {large primes}.  Claim: phi on small primes extends to a solution
//  iff (P) holds for all pairs in S.  Necessity is clear.  Sufficiency: (P) on S gives each fibre
//  V_k = {h(m) : m ∈ S, f(m) = k} distinct elements in a single coset c_k + pZ_{p^2} (choose
//  c_k arbitrarily if V_k is empty).  The cosets c_k + pZ_{p^2} x {k} (k ∈ Z_K) have pK = n
//  slots in total, |S| are used, and there are exactly n - |S| large primes.  Since each large
//  prime q occurs in T only as t(q) = e_q, its value phi(e_q) can be any element of G
//  independently; assign the large primes bijectively to the free slots.  Then the image of [n]
//  is exactly the union of the K cosets, phi is injective, and each fibre is a coset.  So the
//  search runs only over the small primes, and completion is constructed explicitly for
//  witnesses.  #completions = L! * p^{e} (L = #large primes, e = #empty fibres in S's image),
//  used in --count mode to compare with brute_count.py.
//
// SYMMETRY.  Gamma = U(Z_{p^2}) x U(Z_K) acting coordinatewise, (u,v).(h,f) = (uh, vf).  Each
//  gamma is a group automorphism of G, and gamma(F) = F (u unit: uh ∉ pZ iff h ∉ pZ; uh = 0 iff
//  h = 0; vf = 0 iff f = 0).  So gamma∘phi is a solution iff phi is.  Lex-leader: for any
//  solution X = (x_0, ..., x_{s-1}) (values in search order, compared by element index), the
//  lex-minimum Y of its Gamma-orbit is a solution, and satisfies at every depth d:
//  y_d <= gamma(y_d) for all gamma ∈ Stab(y_0..y_{d-1}).  (If gamma fixes y_0..y_{d-1} and
//  gamma(y_d) < y_d, gamma(Y) would be lex-smaller.)  We only explore values satisfying this,
//  so no orbit is lost (find mode only; --count disables symmetry).  Note Gamma need not be all
//  of Aut(G) when gcd(p,K) > 1 (controls); using a subgroup is still sound.
//
// SEARCH.  Variables = small primes, in an order chosen by --order (default "greedy": next prime
//  is the one completing the most difference constraints, ties to the LARGER prime).  Forward
//  checking: each constraint r (support sorted by search position) with last variable a and
//  second-to-last variable b is applied when b is assigned, removing from dom(a) all x with
//  c_a x + s ∉ ... i.e. with c_a x + s ∈ F (s = phi of the rest of r).  Constraints with a single
//  variable filter the initial domain.  Hence every assigned value satisfies every constraint
//  whose support is assigned.  A full independent re-check of (P) is done at every leaf.
//
// Build: rustc -O -C target-cpu=native dfs2.rs -o dfs2.exe
// Run:   dfs2.exe n p [--order greedy|asc|desc] [--threads T] [--split D] [--count] [--nosym]
//                     [--out witness.json] [--log logfile] [--all]
use std::collections::{HashMap, HashSet};
use std::io::Write;
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Instant;

struct Prob {
    n: usize,
    p: i64,
    p2: i64,
    k: i64,
    ng: usize,            // |G|
    w: usize,             // words per bitset
    nv: usize,            // number of search variables (small primes)
    order_primes: Vec<usize>, // prime at search position
    large: Vec<usize>,
    s_vecs: Vec<(usize, Vec<i64>)>, // (m, exponent vector over search positions)
    init_dom: Vec<u64>,   // nv * w
    // triggers[d] = list of (target position a, coef c_a, rest: Vec<(pos, coef)>)
    triggers: Vec<Vec<(usize, i64, Vec<(usize, i64)>)>>,
    // mask[(c)] [s] = bitset of x with c*x + s ∈ F
    masks: HashMap<i64, Vec<u64>>,
    gamma: Vec<(i64, i64)>,
    sym: bool,
    count: bool,
    all: bool,
}

fn gcd(a: i64, b: i64) -> i64 { if b == 0 { a.abs() } else { gcd(b, a % b) } }

impl Prob {
    fn enc(&self, h: i64, f: i64) -> usize { (h.rem_euclid(self.p2) * self.k + f.rem_euclid(self.k)) as usize }
    fn dec(&self, e: usize) -> (i64, i64) { ((e as i64) / self.k, (e as i64) % self.k) }
    fn add(&self, a: usize, b: usize) -> usize { let (h1, f1) = self.dec(a); let (h2, f2) = self.dec(b); self.enc(h1 + h2, f1 + f2) }
    fn mul(&self, c: i64, a: usize) -> usize { let (h, f) = self.dec(a); self.enc(c * h, c * f) }
    fn in_f(&self, e: usize) -> bool { let (h, f) = self.dec(e); f == 0 && (h % self.p != 0 || h == 0) }
    fn act(&self, g: (i64, i64), e: usize) -> usize { let (h, f) = self.dec(e); self.enc(g.0 * h, g.1 * f) }
}

fn primes_upto(n: usize) -> Vec<usize> { (2..=n).filter(|&q| (2..q).take_while(|r| r * r <= q).all(|r| q % r != 0)).collect() }

fn build(n: usize, p: i64, order: &str, sym: bool, count: bool, all: bool) -> Prob {
    assert!(n as i64 % p == 0, "p must divide n");
    let k = n as i64 / p; let p2 = p * p; let ng = (p2 * k) as usize; let w = (ng + 63) / 64;
    let pr = primes_upto(n);
    let small: Vec<usize> = pr.iter().cloned().filter(|&q| 2 * q <= n).collect();
    let large: Vec<usize> = pr.iter().cloned().filter(|&q| 2 * q > n).collect();
    let ns = small.len();
    // smooth set S with exponent vectors over `small` (natural index)
    let mut s_nat: Vec<(usize, Vec<i64>)> = vec![];
    for m in 1..=n {
        let mut x = m; let mut e = vec![0i64; ns];
        for (i, &q) in small.iter().enumerate() { while x % q == 0 { x /= q; e[i] += 1; } }
        if x == 1 { s_nat.push((m, e)); }
    }
    assert_eq!(s_nat.len() + large.len(), n);
    // difference vectors, sign-normalised (F = -F), deduped
    let mut rs: HashSet<Vec<i64>> = HashSet::new();
    for i in 0..s_nat.len() { for j in (i + 1)..s_nat.len() {
        let mut r: Vec<i64> = (0..ns).map(|t| s_nat[j].1[t] - s_nat[i].1[t]).collect();
        let first = r.iter().find(|&&x| x != 0).cloned().unwrap();
        if first < 0 { for x in r.iter_mut() { *x = -*x; } }
        rs.insert(r);
    }}
    let rs: Vec<Vec<i64>> = rs.into_iter().collect();
    // variable order (natural index -> position)
    let mut ord: Vec<usize> = vec![];
    match order {
        "asc" => ord = (0..ns).collect(),
        "desc" => ord = (0..ns).rev().collect(),
        _ => {
            let mut used = vec![false; ns];
            for _ in 0..ns {
                let mut best = (-1i64, 0usize);
                for c in 0..ns { if used[c] { continue; }
                    let cnt = rs.iter().filter(|r| r[c] != 0 && (0..ns).all(|t| r[t] == 0 || used[t] || t == c)).count() as i64;
                    if cnt > best.0 || (cnt == best.0 && small[c] > small[best.1]) { best = (cnt, c); }
                }
                used[best.1] = true; ord.push(best.1);
            }
        }
    }
    let mut pos_of = vec![0usize; ns]; for (ps, &i) in ord.iter().enumerate() { pos_of[i] = ps; }
    let order_primes: Vec<usize> = ord.iter().map(|&i| small[i]).collect();
    let s_vecs: Vec<(usize, Vec<i64>)> = s_nat.iter().map(|(m, e)| { let mut v = vec![0i64; ns]; for i in 0..ns { v[pos_of[i]] = e[i]; } (*m, v) }).collect();
    let mut pb = Prob { n, p, p2, k, ng, w, nv: ns, order_primes, large, s_vecs, init_dom: vec![], triggers: vec![vec![]; ns],
        masks: HashMap::new(), gamma: vec![], sym, count, all };
    // gamma
    for u in 1..p2 { if gcd(u, p2) != 1 { continue; } for v in 0..k.max(1) { if gcd(v, k) != 1 && k > 1 { continue; } pb.gamma.push((u, if k == 1 { 1 } else { v })); } }
    // init domains: all of G
    let mut dom = vec![0u64; ns * w];
    for v in 0..ns { for e in 0..ng { dom[v * w + e / 64] |= 1u64 << (e % 64); } }
    let mut coefs: HashSet<i64> = HashSet::new();
    let mut unary = 0usize;
    for r in rs.iter() {
        let mut sup: Vec<(usize, i64)> = (0..ns).filter(|&i| r[i] != 0).map(|i| (pos_of[i], r[i])).collect();
        sup.sort();
        let (a, ca) = *sup.last().unwrap();
        coefs.insert(ca);
        if sup.len() == 1 {
            unary += 1;
            for x in 0..ng { if pb.in_f(pb.mul(ca, x)) { dom[a * w + x / 64] &= !(1u64 << (x % 64)); } }
        } else {
            let b = sup[sup.len() - 2].0;
            let rest: Vec<(usize, i64)> = sup[..sup.len() - 1].to_vec();
            pb.triggers[b].push((a, ca, rest));
        }
    }
    pb.init_dom = dom;
    for &c in coefs.iter() {
        let mut m = vec![0u64; ng * w];
        for s in 0..ng { for x in 0..ng { if pb.in_f(pb.add(pb.mul(c, x), s)) { m[s * w + x / 64] |= 1u64 << (x % 64); } } }
        pb.masks.insert(c, m);
    }
    eprintln!("n={} p={} K={} |G|={} small={} large={} |S|={} constraints={} (unary {}) |Gamma|={} order={:?}",
        n, p, k, ng, ns, pb.large.len(), pb.s_vecs.len(), rs.len(), unary, pb.gamma.len(), pb.order_primes);
    pb
}

struct Shared { stop: AtomicBool, nodes: AtomicU64, sols: Mutex<u128>, wit: Mutex<Option<Vec<usize>>> }

fn factorial(x: usize) -> u128 { (1..=x as u128).product() }

// full independent check of (P) on S; returns number of empty fibres
fn leaf_check(pb: &Prob, val: &[usize]) -> Option<usize> {
    let mut img: Vec<usize> = vec![];
    for (_, e) in pb.s_vecs.iter() {
        let (mut h, mut f) = (0i64, 0i64);
        for i in 0..pb.nv { if e[i] != 0 { let (a, b) = pb.dec(val[i]); h += e[i] * a; f += e[i] * b; } }
        img.push(pb.enc(h, f));
    }
    let mut fib: HashMap<i64, Vec<i64>> = HashMap::new();
    for &x in img.iter() { let (h, f) = pb.dec(x); fib.entry(f).or_default().push(h); }
    for (_, v) in fib.iter() {
        let set: HashSet<i64> = v.iter().cloned().collect();
        if set.len() != v.len() { return None; }
        if v.iter().any(|&h| (h - v[0]).rem_euclid(pb.p) != 0) { return None; }
    }
    Some(pb.k as usize - fib.len())
}

fn dfs(pb: &Prob, sh: &Shared, d: usize, doms: &mut Vec<Vec<u64>>, val: &mut Vec<usize>, stab: &Vec<(i64, i64)>, prefix: &[usize], local_nodes: &mut u64) {
    if sh.stop.load(Ordering::Relaxed) { return; }
    if d == pb.nv {
        let e = leaf_check(pb, val).expect("BUG: leaf failed independent check");
        if pb.count {
            let c = factorial(pb.large.len()) * (pb.p as u128).pow(e as u32);
            *sh.sols.lock().unwrap() += c;
        } else {
            *sh.sols.lock().unwrap() += 1;
            if pb.all { let line: Vec<String> = val.iter().map(|x| x.to_string()).collect(); println!("SOL {}", line.join(" ")); }
            let mut wl = sh.wit.lock().unwrap(); if wl.is_none() { *wl = Some(val.clone()); }
            if !pb.all { sh.stop.store(true, Ordering::Relaxed); }
        }
        return;
    }
    let w = pb.w;
    let cands: Vec<usize> = if d < prefix.len() { vec![prefix[d]] } else {
        let mut c = vec![];
        for wi in 0..w { let mut b = doms[d][d * w + wi]; while b != 0 { let t = b.trailing_zeros() as usize; b &= b - 1; c.push(wi * 64 + t); } }
        c
    };
    for x in cands {
        if (doms[d][d * w + x / 64] >> (x % 64)) & 1 == 0 { continue; } // prefix value must be in domain
        let mut nstab: Vec<(i64, i64)> = vec![];
        if pb.sym && !stab.is_empty() {
            let mut ok = true;
            for &g in stab.iter() { let y = pb.act(g, x); if y < x { ok = false; break; } if y == x { nstab.push(g); } }
            if !ok { continue; }
        }
        *local_nodes += 1;
        if *local_nodes & 0xFFFF == 0 { sh.nodes.fetch_add(0x10000, Ordering::Relaxed); }
        val[d] = x;
        let (lo, hi) = doms.split_at_mut(d + 1);
        let nd = &mut hi[0]; nd.copy_from_slice(&lo[d]);
        let mut dead = false;
        for (a, ca, rest) in pb.triggers[d].iter() {
            let mut s = 0usize;
            for &(ps, c) in rest.iter() { s = pb.add(s, pb.mul(c, val[ps])); }
            let m = &pb.masks[ca][s * w..(s + 1) * w];
            let mut any = 0u64;
            for wi in 0..w { nd[a * w + wi] &= !m[wi]; any |= nd[a * w + wi]; }
            if any == 0 { dead = true; break; }
        }
        if !dead { dfs(pb, sh, d + 1, doms, val, &nstab, prefix, local_nodes); }
        if sh.stop.load(Ordering::Relaxed) { return; }
    }
}

// enumerate prefixes of length `split` (with FC + symmetry), returns list of prefixes
fn gen_prefixes(pb: &Prob, d: usize, split: usize, doms: &mut Vec<Vec<u64>>, val: &mut Vec<usize>, stab: &Vec<(i64, i64)>, out: &mut Vec<Vec<usize>>) {
    if d == split { out.push(val[..split].to_vec()); return; }
    let w = pb.w;
    let mut c = vec![];
    for wi in 0..w { let mut b = doms[d][d * w + wi]; while b != 0 { let t = b.trailing_zeros() as usize; b &= b - 1; c.push(wi * 64 + t); } }
    for x in c {
        let mut nstab = vec![];
        if pb.sym && !stab.is_empty() {
            let mut ok = true;
            for &g in stab.iter() { let y = pb.act(g, x); if y < x { ok = false; break; } if y == x { nstab.push(g); } }
            if !ok { continue; }
        }
        val[d] = x;
        let (lo, hi) = doms.split_at_mut(d + 1);
        let nd = &mut hi[0]; nd.copy_from_slice(&lo[d]);
        let mut dead = false;
        for (a, ca, rest) in pb.triggers[d].iter() {
            let mut s = 0usize;
            for &(ps, cc) in rest.iter() { s = pb.add(s, pb.mul(cc, val[ps])); }
            let m = &pb.masks[ca][s * w..(s + 1) * w];
            let mut any = 0u64;
            for wi in 0..w { nd[a * w + wi] &= !m[wi]; any |= nd[a * w + wi]; }
            if any == 0 { dead = true; break; }
        }
        if !dead { gen_prefixes(pb, d + 1, split, doms, val, &nstab, out); }
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let n: usize = args[1].parse().unwrap(); let p: i64 = args[2].parse().unwrap();
    let get = |k: &str| args.iter().position(|a| a == k).map(|i| args[i + 1].clone());
    let has = |k: &str| args.iter().any(|a| a == k);
    let order = get("--order").unwrap_or("greedy".into());
    let threads: usize = get("--threads").map(|s| s.parse().unwrap()).unwrap_or(1);
    let count = has("--count"); let sym = !has("--nosym") && !count; let all = has("--all");
    let pb = Arc::new(build(n, p, &order, sym, count, all));
    let split: usize = get("--split").map(|s| s.parse().unwrap()).unwrap_or(2).min(pb.nv);
    let log = get("--log");
    let t0 = Instant::now();
    let fresh = || -> Vec<Vec<u64>> { let mut v = vec![pb.init_dom.clone()]; for _ in 0..pb.nv { v.push(vec![0u64; pb.nv * pb.w]); } v };
    let full_stab = if pb.sym { pb.gamma.clone() } else { vec![] };
    let mut prefixes = vec![];
    { let mut doms = fresh(); let mut val = vec![0usize; pb.nv]; gen_prefixes(&pb, 0, split, &mut doms, &mut val, &full_stab, &mut prefixes); }
    let ntask = prefixes.len();
    eprintln!("split={} tasks={} threads={}", split, ntask, threads);
    let sh = Arc::new(Shared { stop: AtomicBool::new(false), nodes: AtomicU64::new(0), sols: Mutex::new(0), wit: Mutex::new(None) });
    let from: usize = get("--from").map(|s| s.parse().unwrap()).unwrap_or(0); let next = Arc::new(AtomicUsize::new(from)); let done = Arc::new(AtomicUsize::new(from));
    let prefixes = Arc::new(prefixes);
    let logf = Arc::new(Mutex::new(log.as_ref().map(|f| std::fs::OpenOptions::new().create(true).append(true).open(f).unwrap())));
    if let Some(f) = logf.lock().unwrap().as_mut() { writeln!(f, "START n={} p={} order={} sym={} count={} split={} tasks={} threads={} vars={:?}", n, p, order, sym, count, split, ntask, threads, pb.order_primes).unwrap(); }
    let mut hs = vec![];
    for _ in 0..threads {
        let (pb, sh, next, done, prefixes, logf, full_stab) = (pb.clone(), sh.clone(), next.clone(), done.clone(), prefixes.clone(), logf.clone(), full_stab.clone());
        hs.push(std::thread::spawn(move || {
            let mut doms = { let mut v = vec![pb.init_dom.clone()]; for _ in 0..pb.nv { v.push(vec![0u64; pb.nv * pb.w]); } v };
            let mut val = vec![0usize; pb.nv];
            let mut total_local = 0u64;
            loop {
                let i = next.fetch_add(1, Ordering::SeqCst); if i >= prefixes.len() || sh.stop.load(Ordering::Relaxed) { break; }
                let mut ln = 0u64;
                dfs(&pb, &sh, 0, &mut doms, &mut val, &full_stab, &prefixes[i], &mut ln);
                total_local += ln;
                sh.nodes.fetch_add(ln & 0xFFFF, Ordering::Relaxed);
                let dn = done.fetch_add(1, Ordering::SeqCst) + 1;
                if let Some(f) = logf.lock().unwrap().as_mut() { writeln!(f, "task {} done nodes={} completed={}/{} stopped={}", i, ln, dn, prefixes.len(), sh.stop.load(Ordering::Relaxed)).unwrap(); f.flush().unwrap(); }
            }
            total_local
        }));
    }
    let mut tot = 0u64; for h in hs { tot += h.join().unwrap(); }
    let secs = t0.elapsed().as_secs_f64();
    let sols = *sh.sols.lock().unwrap();
    let dn = done.load(Ordering::SeqCst);
    let res = if count { format!("COUNT={}", sols) } else if sols > 0 { "FOUND".to_string() } else if dn == ntask { "NONE".to_string() } else { "INCOMPLETE".to_string() };
    let line = format!("dfs2 n={} p={} K={} order={} sym={} result={} sols_small={} nodes={} tasks_done={}/{} secs={:.2}", n, p, pb.k, order, sym, res, sols, tot, dn, ntask, secs);
    println!("{}", line);
    if let Some(f) = logf.lock().unwrap().as_mut() { writeln!(f, "{}", line).unwrap(); }
    let witv = sh.wit.lock().unwrap().clone();
    if let Some(v) = witv {
        // completion for large primes
        let mut used = vec![false; pb.ng]; let mut fib_res: HashMap<i64, i64> = HashMap::new();
        for (_, e) in pb.s_vecs.iter() {
            let (mut h, mut f) = (0i64, 0i64);
            for i in 0..pb.nv { if e[i] != 0 { let (a, b) = pb.dec(v[i]); h += e[i] * a; f += e[i] * b; } }
            let x = pb.enc(h, f); used[x] = true; let (hh, ff) = pb.dec(x); fib_res.insert(ff, hh % pb.p);
        }
        let mut free = vec![];
        for f in 0..pb.k { let c = *fib_res.get(&f).unwrap_or(&0); for j in 0..pb.p { let x = pb.enc(c + pb.p * j, f); if !used[x] { free.push(x); } } }
        assert_eq!(free.len(), pb.large.len());
        let mut parts = vec![];
        for i in 0..pb.nv { let (h, f) = pb.dec(v[i]); parts.push((pb.order_primes[i], h, f)); }
        for (j, &q) in pb.large.iter().enumerate() { let (h, f) = pb.dec(free[j]); parts.push((q, h, f)); }
        parts.sort();
        let body: Vec<String> = parts.iter().map(|(q, h, f)| format!("\"{}\": [{}, {}]", q, h, f)).collect();
        let json = format!("{{\"n\": {}, \"p\": {}, \"K\": {}, \"dims\": [{}, {}], \"phi\": {{{}}}}}", n, p, pb.k, pb.p2, pb.k, body.join(", "));
        println!("WITNESS {}", json);
        if let Some(o) = get("--out") { std::fs::write(o, json).unwrap(); }
    }
}
