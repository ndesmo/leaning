// K-periodic tile search (index m = p prime, p || n).
//
// Searches for homomorphisms phi: (Z^+, x) -> Z_N, N = n*p, q = n/p, such that
// for all distinct a, b in {1..n}:
//     phi(a) != phi(b), and  phi(a) == phi(b) mod q  ==>  phi(a) == phi(b) mod n.
// (Equivalently phi(a)-phi(b) is never in D = {0} u (qZ_N \ nZ_N).)
// By README.md (Prop. 3) these are exactly the injective phi whose image
// A = phi({1..n}) tiles Z_N with a complement B of size p that cannot be
// replaced by a subgroup ("non-lattice" tilings of index p).
//
// Build: rustc -O kper.rs -o kper.exe
// Run:   kper n=195 p=3 [all=1] [nosym=1] [allprimes=1] [threads=T]
//   all=1        count all solutions instead of stopping at the first
//   nosym=1      no symmetry breaking (for raw counts)
//   allprimes=1  branch on all primes <= n (default: primes <= n/2; the primes
//                in (n/2, n] can always be completed, see README.md)
//
// Symmetry breaking: stabiliser chain under Aut(Z_N) = units (all preserve D).

use std::env;
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Instant;

fn gcd(a: usize, b: usize) -> usize { if b == 0 { a } else { gcd(b, a % b) } }

fn primes_upto(n: usize) -> Vec<usize> {
    (2..=n).filter(|&p| (2..p).take_while(|d| d * d <= p).all(|d| p % d != 0)).collect()
}

#[derive(Clone)]
struct Ctx {
    n: usize,
    big: usize, // N
    q: usize,
    primes: Vec<usize>,
    items: Vec<Vec<(usize, usize)>>,
    units: Arc<Vec<usize>>,
    phi: Vec<u32>,
    used: Vec<u8>,
    cnt: Vec<u16>,
    rep: Vec<u32>,
    nodes: u64,
    nsol: u64,
    all: bool,
    sym: bool,
    sol: Option<Vec<u32>>,
    stop: Arc<AtomicBool>,
}

impl Ctx {
    // try to assign prime k -> g; returns number of items inserted and ok flag
    fn assign(&mut self, k: usize, g: usize) -> (usize, bool) {
        let p = self.primes[k];
        self.phi[p] = g as u32;
        let nit = self.items[k].len();
        for idx in 0..nit {
            let (m, r) = self.items[k][idx];
            let mut v = g + self.phi[r] as usize;
            if v >= self.big { v -= self.big; }
            self.phi[m] = v as u32;
            if self.used[v] != 0 { return (idx, false); }
            let c = v % self.q;
            let vn = (v % self.n) as u32;
            if self.cnt[c] > 0 && self.rep[c] != vn { return (idx, false); }
            self.cnt[c] += 1;
            self.rep[c] = vn;
            self.used[v] = 1;
        }
        (nit, true)
    }
    fn undo(&mut self, k: usize, done: usize) {
        for idx in 0..done {
            let (m, _) = self.items[k][idx];
            let v = self.phi[m] as usize;
            self.used[v] = 0;
            self.cnt[v % self.q] -= 1;
        }
    }
    fn minimal(&self, g: usize, stab: &[usize]) -> bool {
        stab.iter().all(|&u| (u * g) % self.big >= g)
    }
    fn dfs(&mut self, k: usize, stab: &[usize]) -> bool {
        self.nodes += 1;
        if self.nodes & 0xfffff == 0 && self.stop.load(Ordering::Relaxed) { return true; }
        if k == self.primes.len() {
            self.nsol += 1;
            if self.sol.is_none() { self.sol = Some(self.phi.clone()); }
            if !self.all { self.stop.store(true, Ordering::Relaxed); }
            return !self.all;
        }
        let usesym = self.sym && stab.len() > 1;
        for g in 0..self.big {
            if usesym && !self.minimal(g, stab) { continue; }
            let (done, ok) = self.assign(k, g);
            let mut found = false;
            if ok {
                if usesym {
                    let ns: Vec<usize> = stab.iter().cloned().filter(|&u| (u * g) % self.big == g).collect();
                    found = self.dfs(k + 1, &ns);
                } else {
                    found = self.dfs(k + 1, stab);
                }
            }
            self.undo(k, done);
            if found { return true; }
        }
        false
    }
}

fn main() {
    let mut n = 195usize;
    let mut p = 3usize;
    let mut all = false;
    let mut sym = true;
    let mut allprimes = false;
    let mut threads = std::thread::available_parallelism().map(|x| x.get()).unwrap_or(4);
    for a in env::args().skip(1) {
        let kv: Vec<&str> = a.splitn(2, '=').collect();
        match kv[0] {
            "n" => n = kv[1].parse().unwrap(),
            "p" => p = kv[1].parse().unwrap(),
            "all" => all = kv[1] == "1",
            "nosym" => sym = kv[1] != "1",
            "allprimes" => allprimes = kv[1] == "1",
            "threads" => threads = kv[1].parse().unwrap(),
            _ => panic!("unknown key"),
        }
    }
    assert!(n % p == 0 && (n / p) % p != 0, "need p || n");
    let big = n * p;
    let q = n / p;
    let primes = primes_upto(if allprimes { n } else { n / 2 });
    let mut items = vec![vec![]; primes.len()];
    for x in 2..=n {
        let mut r = x;
        let mut last = None;
        for (k, &pr) in primes.iter().enumerate() {
            if r % pr == 0 { last = Some(k); while r % pr == 0 { r /= pr; } }
        }
        if r == 1 { let k = last.unwrap(); items[k].push((x, x / primes[k])); }
    }
    let units: Vec<usize> = (1..big).filter(|&u| gcd(u, big) == 1).collect();
    let stop = Arc::new(AtomicBool::new(false));
    let mut base = Ctx {
        n, big, q, primes: primes.clone(), items, units: Arc::new(units.clone()),
        phi: vec![0; n + 1], used: vec![0; big], cnt: vec![0; q], rep: vec![0; q],
        nodes: 0, nsol: 0, all, sym, sol: None, stop: stop.clone(),
    };
    base.used[0] = 1; base.cnt[0] = 1; base.rep[0] = 0; // the number 1
    let t0 = Instant::now();
    // tasks: valid prefixes of depth d
    let d = primes.len().min(2);
    let mut tasks: Vec<Vec<usize>> = vec![];
    {
        let full: Vec<usize> = if sym { units.clone() } else { vec![1] };
        fn gen(c: &mut Ctx, k: usize, d: usize, stab: &[usize], pre: &mut Vec<usize>, out: &mut Vec<Vec<usize>>) {
            if k == d { out.push(pre.clone()); return; }
            for g in 0..c.big {
                if c.sym && stab.len() > 1 && !c.minimal(g, stab) { continue; }
                let (done, ok) = c.assign(k, g);
                if ok {
                    let ns: Vec<usize> = stab.iter().cloned().filter(|&u| (u * g) % c.big == g).collect();
                    pre.push(g);
                    gen(c, k + 1, d, &ns, pre, out);
                    pre.pop();
                }
                c.undo(k, done);
            }
        }
        let mut c = base.clone();
        gen(&mut c, 0, d, &full, &mut vec![], &mut tasks);
    }
    let ntasks = tasks.len();
    let tasks = Arc::new(tasks);
    let next = Arc::new(AtomicUsize::new(0));
    let total_nodes = Arc::new(AtomicU64::new(0));
    let total_sol = Arc::new(AtomicU64::new(0));
    let finished = Arc::new(AtomicUsize::new(0));
    let sol: Arc<Mutex<Option<Vec<u32>>>> = Arc::new(Mutex::new(None));
    let mut hs = vec![];
    for _ in 0..threads {
        let (tasks, next, total_nodes, total_sol, sol, base, stop, finished) =
            (tasks.clone(), next.clone(), total_nodes.clone(), total_sol.clone(), sol.clone(), base.clone(), stop.clone(), finished.clone());
        hs.push(std::thread::Builder::new().stack_size(64 << 20).spawn(move || loop {
            let i = next.fetch_add(1, Ordering::SeqCst);
            if i >= tasks.len() || stop.load(Ordering::Relaxed) { break; }
            let mut c = base.clone();
            let mut stab: Vec<usize> = if c.sym { c.units.as_ref().clone() } else { vec![1] };
            for (k, &g) in tasks[i].iter().enumerate() {
                let (_, ok) = c.assign(k, g);
                assert!(ok);
                stab = stab.iter().cloned().filter(|&u| (u * g) % c.big == g).collect();
            }
            c.dfs(tasks[i].len(), &stab);
            total_nodes.fetch_add(c.nodes, Ordering::SeqCst);
            total_sol.fetch_add(c.nsol, Ordering::SeqCst);
            if !stop.load(Ordering::Relaxed) || c.nsol > 0 {
                let f = finished.fetch_add(1, Ordering::SeqCst) + 1;
                if f % 50 == 0 { eprintln!("tasks finished {}/{}", f, tasks.len()); }
            }
            if let Some(s) = c.sol { let mut l = sol.lock().unwrap(); if l.is_none() { *l = Some(s); } }
        }).unwrap());
    }
    for h in hs { h.join().unwrap(); }
    let nsol = total_sol.load(Ordering::SeqCst);
    let complete = nsol > 0 && !all || finished.load(Ordering::SeqCst) == ntasks;
    println!("n={} p={} N={} q={} primes<={} sym={} all={} tasks={} finished={} complete={}",
        n, p, big, q, primes.last().cloned().unwrap_or(0), sym, all, ntasks, finished.load(Ordering::SeqCst), complete);
    println!("result={} solutions_seen={} nodes={} secs={:.2}",
        if nsol > 0 { "EXISTS" } else { "NONE" }, nsol, total_nodes.load(Ordering::SeqCst), t0.elapsed().as_secs_f64());
    let got = sol.lock().unwrap().clone();
    if let Some(mut phi) = got {
        // complete the primes in (n/2, n]: put each into any free slot
        let mut used = vec![false; big];
        let mut rep: Vec<Option<usize>> = vec![None; q];
        let allp = primes_upto(n);
        let small = |x: usize| { let mut r = x; for &pr in &primes { while r % pr == 0 { r /= pr; } } r == 1 };
        for x in 1..=n { if small(x) { let v = phi[x] as usize; used[v] = true; rep[v % q] = Some(v % n); } }
        for &pr in &allp {
            if small(pr) { continue; }
            let mut placed = false;
            'o: for c in 0..q {
                for v in (0..big).filter(|v| v % q == c) {
                    if used[v] { continue; }
                    if let Some(r) = rep[c] { if r != v % n { continue; } }
                    used[v] = true; rep[c] = Some(v % n); phi[pr] = v as u32; placed = true;
                    break 'o;
                }
            }
            assert!(placed);
        }
        let s: Vec<String> = allp.iter().map(|&pr| format!("{}:{}", pr, phi[pr])).collect();
        println!("solution N={} B={:?} primes {}", big, (0..p).map(|j| j * q).collect::<Vec<_>>(), s.join(" "));
    }
}
