// c22.rs -- exact search for the family (c_{x,y}) of structure/pass13_mixed.md §2 (pass 14).
//
// DEFINITION (pass13_mixed.md §2).  n = p*q*r with p, q, r pairwise coprime (p, q prime).
// G = Z_{p^x} x Z_{q^y} x Z_r,  P = p^{x-1}Z_{p^x} x q^{y-1}Z_{q^y}  (order p*q).
// T = {1..n}.  Find a homomorphism psi: Z^{pi(n)} -> G, i.e. values psi(l) in G for each prime
// l <= n, extended additively over exponent vectors (psi(ab) = psi(a)+psi(b), psi(1) = 0), with
//   (C1) psi injective on T;
//   (C2) for every k in Z_r the fibre F_k = { psi(a) : a in T, psi_r(a) = k } is a coset
//        (u_k + P) x {k}.
// Since |T| = n = r*|P|, (C1)+(C2) <=> the following finite constraint system, which is what
// the code tests (proof: (=>) clear; (<=) each fibre lies in one coset of P, has distinct
// elements, so <= pq elements; r fibres, n = r*pq elements total, so each fibre is a full coset):
//   (S1) [label]   for a, b in T with psi_r(a) = psi_r(b):  psi(a) - psi(b) in P,
//                  i.e. lab(psi(a)) = lab(psi(b)) where lab(g) = (g_p mod p^{x-1}, g_q mod q^{y-1})
//                  is the image of g in (Z_{p^x} x Z_{q^y})/P;
//   (S2) [inject]  psi(a) != psi(b) for a != b in T;
//   (S3) [size]    |F_k| <= pq for every k   (implied by S1+S2; used as a prune).
// For n = 195: p = 3, q = 5, r = 13, (x,y) = (2,2): G = Z9 x Z25 x Z13, |G| = 2925, P = 3Z9 x 5Z25,
// labels in Z3 x Z5, 44 primes; (c_{2,2}) is the target.
//
// RELAXATION MODE (necessary conditions only, used for extra evidence): y = 0 drops the q-part
// (Z_{q^0} = 0) and --cap q replaces (S2) by "each value of G is taken at most q times"
// (projection of a (c_{x,y}) solution to Z_{p^x} x Z_r maps each fibre q-to-1 onto a coset of
// p^{x-1}Z).  Likewise x = 0 with --cap p.  With cap > 1 a NONE excludes (c_{x,y}) for every y;
// a FOUND means nothing.
//
// LARGE PRIMES.  A prime l with 2l > n occurs in T only as a = l, and psi(l) is unconstrained by
// the rest.  The search runs over the primes l <= n/2 only and stops when every a in T other than a
// large prime is placed.  Completion always exists: fibres that are nonempty have a fixed label,
// empty fibres take any label (L = p^{x-1} q^{y-1} choices); total capacity r*pq*... = n slots
// (counting multiplicity cap), |placed| used, and #large primes = n - |placed| slots remain; assign
// the large primes bijectively to the free slots.  #completions = L^e * f! / prod_g (free slots at g)!
// (f = #large primes, e = #empty fibres); used by --count.
//
// SEARCH.  Primes l <= n/2 in increasing order.  Assigning psi(l) = g places every a <= n whose
// largest prime factor is l (a = l*m, m earlier in the same list or with smaller prime factors), in
// increasing order, checking S1-S3 incrementally; backtrack on failure.
//
// SYMMETRY (find mode only; --nosym or --count disables).  Aut(G) = U(p^x) x U(q^y) x U(r) acting
// coordinatewise preserves P and maps fibres to fibres, so it preserves (S1)-(S3) and the property
// "genuine" below.  Hence psi(2) may be taken to be an orbit representative: in each coordinate
// Z_m the orbit of v is determined by gcd(v, m), rep = gcd(v,m) mod m.
//
// GENUINE (--genuine): additionally require, among nonempty fibres at completion, a label with
// p-part != 0 (if x >= 2) and one with q-part != 0 (if y >= 2).  Without that, psi(T) lies in
// P x Z_r up to labels 0 and the witness is a lift of a (c_{x-1,.}) / (c_{.,y-1}) solution.
// Aut-invariant (units preserve nonzero-ness of a mod p^{x-1}).
//
// TASKS / CHECKPOINT.  Tasks = (psi(2), psi(3)) pairs that survive placement (psi(2) over orbit
// reps).  Each finished task is logged "TASK id done nodes=.. sols=.." ; --resume LOG skips them.
// --time S stops at S seconds; unfinished tasks are not logged as done (TIMEOUT).
//
// Usage: c22 n p x q y r [--cap c] [--count] [--nosym] [--genuine] [--threads t] [--log F]
//            [--resume F] [--time S] [--wit F]

use std::collections::HashSet;
use std::fs::OpenOptions;
use std::io::Write;
use std::sync::atomic::{AtomicBool, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use std::time::Instant;

fn gcd(a: usize, b: usize) -> usize { if b == 0 { a } else { gcd(b, a % b) } }

#[derive(Clone)]
struct Prob {
    n: usize, p: usize, x: u32, q: usize, y: u32, r: usize, cap: u8, fib: usize,
    mp: usize, mq: usize, lp: usize, lq: usize, gsz: usize,
    add: Vec<u16>, fibre: Vec<u16>, lab: Vec<u16>,
    vars: Vec<usize>,              // small primes in order
    groups: Vec<Vec<(usize, usize)>>, // for each var: list of (a, m) with psi(a) = psi(m) + psi(var)
    nlarge: usize,
    coset_elems: Vec<Vec<u16>>,   // [label * r + k] -> elements of G with that label in fibre k
    fibre_elems: Vec<Vec<u16>>,   // [k] -> elements of fibre k
    genuine: bool,
}

impl Prob {
    fn enc(&self, a: usize, b: usize, c: usize) -> usize { (a * self.mq + b) * self.r + c }
    fn dec(&self, g: usize) -> (usize, usize, usize) {
        let c = g % self.r; let t = g / self.r; (t / self.mq, t % self.mq, c)
    }
}

struct State {
    psi: Vec<u16>, mult: Vec<u8>, fcount: Vec<u16>, flabel: Vec<u16>,
}

impl State {
    fn new(pr: &Prob) -> State {
        let mut s = State { psi: vec![0; pr.n + 1], mult: vec![0; pr.gsz], fcount: vec![0; pr.r], flabel: vec![0; pr.r] };
        // a = 1 -> 0
        s.mult[0] = 1; s.fcount[0] = 1; s.flabel[0] = pr.lab[0];
        s
    }
    #[inline]
    fn place(&mut self, pr: &Prob, g: usize) -> bool {
        if self.mult[g] >= pr.cap { return false; }
        let k = pr.fibre[g] as usize;
        let c = self.fcount[k] as usize;
        if c >= pr.fib { return false; }
        if c > 0 && self.flabel[k] != pr.lab[g] { return false; }
        self.mult[g] += 1;
        if c == 0 { self.flabel[k] = pr.lab[g]; }
        self.fcount[k] += 1;
        true
    }
    #[inline]
    fn unplace(&mut self, pr: &Prob, g: usize) {
        self.mult[g] -= 1;
        self.fcount[pr.fibre[g] as usize] -= 1;
    }
    // assign var i = g; place its group; returns number placed (all if success)
    fn assign(&mut self, pr: &Prob, i: usize, g: usize) -> (bool, usize) {
        let mut placed = 0;
        for &(a, m) in &pr.groups[i] {
            let v = if m == 0 { g } else { pr.add[self.psi[m] as usize * pr.gsz + g] as usize };
            if !self.place(pr, v) { return (false, placed); }
            self.psi[a] = v as u16;
            placed += 1;
        }
        (true, placed)
    }
    fn unassign(&mut self, pr: &Prob, i: usize, placed: usize) {
        for j in (0..placed).rev() {
            let a = pr.groups[i][j].0;
            self.unplace(pr, self.psi[a] as usize);
        }
    }
    fn is_genuine(&self, pr: &Prob) -> bool {
        let mut okp = pr.x < 2; let mut okq = pr.y < 2;
        for k in 0..pr.r {
            if self.fcount[k] > 0 {
                let l = self.flabel[k] as usize;
                if l / pr.lq != 0 { okp = true; }
                if l % pr.lq != 0 { okq = true; }
            }
        }
        okp && okq
    }
    fn completions(&self, pr: &Prob) -> u128 {
        // L^e * f! / prod (free slots)!
        let fact = |k: usize| -> u128 { (1..=k as u128).product::<u128>().max(1) };
        let ll = (pr.lp * pr.lq) as u128;
        let mut num = fact(pr.nlarge);
        let mut den: u128 = 1;
        let mut e = 0u32;
        for g in 0..pr.gsz {
            let k = pr.fibre[g] as usize;
            if self.fcount[k] > 0 && self.flabel[k] == pr.lab[g] {
                den *= fact((pr.cap - self.mult[g]) as usize);
            }
        }
        for k in 0..pr.r { if self.fcount[k] == 0 { e += 1; } }
        // empty fibre: |P|-many values (pq/cap-adjusted) each with cap slots
        let per_coset = (pr.gsz / pr.r) / (pr.lp * pr.lq); // values per coset
        for _ in 0..e { den *= fact(pr.cap as usize).pow(per_coset as u32); num *= ll; }
        num / den
    }
}

struct Shared {
    stop: AtomicBool,
    nodes: AtomicUsize,
    found: Mutex<Option<String>>,
    log: Mutex<Option<std::fs::File>>,
    start: Instant,
    tlimit: f64,
    timed_out: AtomicBool,
}

fn witness_string(pr: &Prob, st: &State) -> String {
    // fill large primes into free slots
    let mut mult = st.mult.clone();
    let mut flabel = st.flabel.clone();
    let mut fcount = st.fcount.clone();
    let mut out = String::new();
    for &l in &pr.vars { let (a, b, c) = pr.dec(st.psi[l] as usize); out += &format!(" {}={},{},{}", l, a, b, c); }
    for l in 2..=pr.n {
        if is_prime(l) && 2 * l > pr.n {
            let mut chosen = None;
            for g in 0..pr.gsz {
                let k = pr.fibre[g] as usize;
                if mult[g] >= pr.cap || fcount[k] as usize >= pr.fib { continue; }
                if fcount[k] > 0 && flabel[k] != pr.lab[g] { continue; }
                chosen = Some(g); break;
            }
            let g = chosen.expect("completion failed");
            let k = pr.fibre[g] as usize;
            mult[g] += 1; if fcount[k] == 0 { flabel[k] = pr.lab[g]; } fcount[k] += 1;
            let (a, b, c) = pr.dec(g); out += &format!(" {}={},{},{}", l, a, b, c);
        }
    }
    out
}

fn dfs(pr: &Prob, st: &mut State, i: usize, sh: &Shared, count_mode: bool, nodes: &mut usize, sols: &mut u128) {
    if sh.stop.load(Ordering::Relaxed) { return; }
    *nodes += 1;
    if *nodes & 0xFFFFF == 0 {
        sh.nodes.fetch_add(0x100000, Ordering::Relaxed);
        if sh.start.elapsed().as_secs_f64() > sh.tlimit { sh.timed_out.store(true, Ordering::Relaxed); sh.stop.store(true, Ordering::Relaxed); return; }
    }
    if i == pr.vars.len() {
        if pr.genuine && !st.is_genuine(pr) { return; }
        if count_mode { *sols += st.completions(pr); return; }
        *sols += 1;
        let w = witness_string(pr, st);
        let mut f = sh.found.lock().unwrap();
        if f.is_none() { *f = Some(w); }
        sh.stop.store(true, Ordering::Relaxed);
        return;
    }
    // Candidates for psi(var): only values where var itself can be placed: in a non-full fibre,
    // and in that fibre's label coset if the fibre is nonempty (any value of an empty fibre).
    // assign() re-checks everything, so this is purely a filter of values that would fail anyway.
    for k in 0..pr.r {
        let c = st.fcount[k] as usize;
        if c >= pr.fib { continue; }
        let list: &Vec<u16> = if c > 0 { &pr.coset_elems[st.flabel[k] as usize * pr.r + k] } else { &pr.fibre_elems[k] };
        for &g in list {
            let g = g as usize;
            let (ok, placed) = st.assign(pr, i, g);
            if ok { dfs(pr, st, i + 1, sh, count_mode, nodes, sols); }
            st.unassign(pr, i, placed);
            if sh.stop.load(Ordering::Relaxed) { return; }
        }
    }
}

fn is_prime(n: usize) -> bool { n >= 2 && (2..).take_while(|d| d * d <= n).all(|d| n % d != 0) }

fn main() {
    let args: Vec<String> = std::env::args().collect();
    let num = |i: usize| -> usize { args[i].parse().unwrap() };
    let (n, p, x, q, y, r) = (num(1), num(2), num(3) as u32, num(4), num(5) as u32, num(6));
    let mut cap = 1u8; let mut count_mode = false; let mut sym = true; let mut genuine = false;
    let mut threads = 1usize; let mut logf: Option<String> = None; let mut resume: Option<String> = None;
    let mut tlimit = 1e18f64; let mut witf: Option<String> = None;
    let mut i = 7;
    while i < args.len() {
        match args[i].as_str() {
            "--cap" => { cap = args[i + 1].parse().unwrap(); i += 1; }
            "--count" => { count_mode = true; }
            "--nosym" => { sym = false; }
            "--genuine" => { genuine = true; }
            "--threads" => { threads = args[i + 1].parse().unwrap(); i += 1; }
            "--log" => { logf = Some(args[i + 1].clone()); i += 1; }
            "--resume" => { resume = Some(args[i + 1].clone()); i += 1; }
            "--time" => { tlimit = args[i + 1].parse().unwrap(); i += 1; }
            "--wit" => { witf = Some(args[i + 1].clone()); i += 1; }
            s => panic!("unknown arg {}", s),
        }
        i += 1;
    }
    if count_mode { sym = false; }
    assert!(n % r == 0);
    let fib = n / r;
    let pw = |b: usize, e: u32| b.pow(e);
    let (mp, mq) = (pw(p, x), pw(q, y));
    let lp = if x == 0 { 1 } else { pw(p, x - 1) };
    let lq = if y == 0 { 1 } else { pw(q, y - 1) };
    // sanity: fibre size must equal |P| * cap
    let psz = (mp / lp) * (mq / lq);
    assert_eq!(psz * cap as usize, fib, "fibre size n/r must equal |P|*cap");
    assert!(gcd(mp, mq) == 1 && gcd(mp * mq, r) == 1, "orders must be coprime");
    let gsz = mp * mq * r;
    assert!(gsz < 65536);
    let mut pr = Prob { n, p, x, q, y, r, cap, fib, mp, mq, lp, lq, gsz, add: vec![], fibre: vec![], lab: vec![],
        vars: vec![], groups: vec![], nlarge: 0, genuine, coset_elems: vec![], fibre_elems: vec![] };
    let mut add = vec![0u16; gsz * gsz];
    for g in 0..gsz { for h in 0..gsz {
        let (a, b, c) = pr.dec(g); let (d, e, f) = pr.dec(h);
        add[g * gsz + h] = pr.enc((a + d) % mp, (b + e) % mq, (c + f) % r) as u16;
    } }
    pr.add = add;
    pr.fibre = (0..gsz).map(|g| pr.dec(g).2 as u16).collect();
    pr.lab = (0..gsz).map(|g| { let (a, b, _) = pr.dec(g); ((a % lp) * lq + (b % lq)) as u16 }).collect();
    pr.coset_elems = vec![vec![]; lp * lq * r];
    pr.fibre_elems = vec![vec![]; r];
    for g in 0..gsz { let k = pr.fibre[g] as usize; pr.coset_elems[pr.lab[g] as usize * r + k].push(g as u16); pr.fibre_elems[k].push(g as u16); }
    // variables and groups
    let lpf = |a: usize| -> usize { let mut m = a; let mut best = 1; let mut d = 2; while d * d <= m { while m % d == 0 { best = d; m /= d; } d += 1; } if m > 1 { best = best.max(m); } best };
    for l in 2..=n { if is_prime(l) { if 2 * l <= n { pr.vars.push(l); } else { pr.nlarge += 1; } } }
    for &l in &pr.vars.clone() {
        let mut gr = vec![];
        for a in 2..=n { if lpf(a) == l { let m = a / l; gr.push((a, if m == 1 { 0 } else { m })); } }
        pr.groups.push(gr);
    }
    let pr = Arc::new(pr);
    // tasks
    let mut tasks: Vec<(usize, usize)> = vec![];
    {
        let mut st = State::new(&pr);
        let reps: Vec<usize> = if sym {
            let mut set = HashSet::new();
            for g in 0..gsz { let (a, b, c) = pr.dec(g);
                set.insert(pr.enc(gcd(a, mp) % mp, gcd(b, mq) % mq, gcd(c, r) % r)); }
            let mut v: Vec<usize> = set.into_iter().collect(); v.sort(); v
        } else { (0..gsz).collect() };
        for &g2 in &reps {
            let (ok, pl) = st.assign(&pr, 0, g2);
            if ok {
                if pr.vars.len() == 1 { tasks.push((g2, usize::MAX)); }
                else { for g3 in 0..gsz { let (ok3, pl3) = st.assign(&pr, 1, g3); if ok3 { tasks.push((g2, g3)); } st.unassign(&pr, 1, pl3); } }
            }
            st.unassign(&pr, 0, pl);
        }
    }
    let mut done: HashSet<usize> = HashSet::new();
    if let Some(rf) = &resume {
        if let Ok(s) = std::fs::read_to_string(rf) {
            for line in s.lines() { let w: Vec<&str> = line.split_whitespace().collect();
                if w.len() >= 3 && w[0] == "TASK" && w[2] == "done" { done.insert(w[1].parse().unwrap()); }
                if w.len() >= 1 && w[0] == "FOUND" { println!("resume log already contains FOUND"); }
            }
        }
    }
    let logfile = logf.map(|f| OpenOptions::new().create(true).append(true).open(f).unwrap());
    let sh = Arc::new(Shared { stop: AtomicBool::new(false), nodes: AtomicUsize::new(0), found: Mutex::new(None),
        log: Mutex::new(logfile), start: Instant::now(), tlimit, timed_out: AtomicBool::new(false) });
    let header = format!("# c22 n={} p={} x={} q={} y={} r={} cap={} |G|={} vars={} large={} sym={} genuine={} count={} tasks={} already_done={}",
        n, p, x, q, y, r, cap, gsz, pr.vars.len(), pr.nlarge, sym, genuine, count_mode, tasks.len(), done.len());
    println!("{}", header);
    if let Some(f) = sh.log.lock().unwrap().as_mut() { writeln!(f, "{}", header).unwrap(); }
    let tasks = Arc::new(tasks);
    let done = Arc::new(done);
    let next = Arc::new(AtomicUsize::new(0));
    let total_sols = Arc::new(Mutex::new(0u128));
    let ndone = Arc::new(AtomicUsize::new(0));
    let mut hs = vec![];
    for _ in 0..threads {
        let (pr, sh, tasks, done, next, total_sols, ndone) = (pr.clone(), sh.clone(), tasks.clone(), done.clone(), next.clone(), total_sols.clone(), ndone.clone());
        hs.push(std::thread::spawn(move || {
            let mut st = State::new(&pr);
            loop {
                let t = next.fetch_add(1, Ordering::SeqCst);
                if t >= tasks.len() || sh.stop.load(Ordering::Relaxed) { break; }
                if done.contains(&t) { continue; }
                if sh.start.elapsed().as_secs_f64() > sh.tlimit { sh.timed_out.store(true, Ordering::SeqCst); sh.stop.store(true, Ordering::SeqCst); break; }
                let (g2, g3) = tasks[t];
                let (ok, pl) = st.assign(&pr, 0, g2); assert!(ok);
                let mut nodes = 0usize; let mut sols = 0u128;
                if g3 == usize::MAX {
                    dfs(&pr, &mut st, 1, &sh, count_mode, &mut nodes, &mut sols);
                } else {
                    let (ok3, pl3) = st.assign(&pr, 1, g3); assert!(ok3);
                    dfs(&pr, &mut st, 2, &sh, count_mode, &mut nodes, &mut sols);
                    st.unassign(&pr, 1, pl3);
                }
                st.unassign(&pr, 0, pl);
                sh.nodes.fetch_add(nodes & 0xFFFFF, Ordering::Relaxed);
                // a task is complete iff the search was not stopped (timeout or a FOUND elsewhere)
                // while it ran, or it produced the FOUND itself.
                let stopped = sh.stop.load(Ordering::SeqCst);
                *total_sols.lock().unwrap() += sols;
                if !stopped || (sols > 0 && !count_mode) {
                    ndone.fetch_add(1, Ordering::SeqCst);
                    let line = format!("TASK {} done g2={} g3={} nodes={} sols={} t={:.1}", t, g2, g3, nodes, sols, sh.start.elapsed().as_secs_f64());
                    if let Some(f) = sh.log.lock().unwrap().as_mut() { writeln!(f, "{}", line).unwrap(); f.flush().unwrap(); }
                }
            }
        }));
    }
    for h in hs { h.join().unwrap(); }
    let found = sh.found.lock().unwrap().clone();
    let el = sh.start.elapsed().as_secs_f64();
    let nd = ndone.load(Ordering::SeqCst) + done.len();
    let res = if let Some(w) = &found {
        format!("FOUND n={} p={} x={} q={} y={} r={} cap={} psi:{}", n, p, x, q, y, r, cap, w)
    } else if sh.timed_out.load(Ordering::Relaxed) {
        format!("TIMEOUT tasks_done={}/{} (resume with --resume LOG)", nd, tasks.len())
    } else if count_mode {
        format!("COUNT {} tasks_done={}/{}", total_sols.lock().unwrap(), nd, tasks.len())
    } else {
        format!("NONE tasks_done={}/{} complete={}", nd, tasks.len(), nd == tasks.len())
    };
    let tail = format!("{} nodes~{} time={:.1}s", res, sh.nodes.load(Ordering::Relaxed), el);
    println!("{}", tail);
    if let Some(f) = sh.log.lock().unwrap().as_mut() { writeln!(f, "{}", tail).unwrap(); }
    if let (Some(wf), Some(w)) = (witf, found) {
        std::fs::write(wf, format!("{} {} {} {} {} {} {}\n{}\n", n, p, x, q, y, r, cap, w.trim())).unwrap();
    }
}
