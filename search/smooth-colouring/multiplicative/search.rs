// Exhaustive search for multiplicative colourings (homomorphisms phi from the
// multiplicative monoid of positive integers to a finite abelian group G that
// are injective on {1..M}).
//
// Build:  rustc -O search.rs -o search.exe
//
// Modes
//   search scan N1 N2
//       for each n in N1..=N2 and every abelian group G of order n (as a
//       product of prime-power cyclic groups), decide whether a homomorphism
//       exists that is a bijection {1..n} -> G.  Prints one line per n.
//   search one key=value ...
//       dims=3,5,13     group Z_3 x Z_5 x Z_13   (dims=195 means Z_195)
//       m=195           injectivity required on {1..m}
//       budget=0        number of allowed "defects" (values repeated) among
//                       the P-smooth numbers <= m
//       primes=2,3,5    branching primes in this order (default: all primes
//                       p <= m/2 in increasing order).  Only numbers <= m
//                       all of whose prime factors are in the list are tested.
//       symdepth=99     use symmetry breaking for the first symdepth primes
//       cert=FILE       write a refutation certificate (budget must be 0,
//                       requires cyclic dims=n and symdepth<=1)
//       cap=1           each group element may be the image of at most cap
//                       numbers (cap>1: equidistribution test for quotients)
//       all=1           do not stop at the first solution; count them all
//
// Symmetry breaking (sound): let H be the group of automorphisms of
// G = Z_{d1} x ... x Z_{dk} acting by componentwise multiplication by units
// (u1,...,uk).  If phi is a solution then so is h o phi for every h in H.
// We keep a stabiliser chain: S_0 = H, and at depth j (prime p_j) we only try
// values g that are the minimum of their S_j-orbit, and set
// S_{j+1} = {h in S_j : h(g) = g}.  Every solution is H-equivalent to one
// visited: choose h_0 in S_0 moving phi(p_0) to its orbit minimum, then
// h_1 in S_1 (which fixes the new phi(p_0)) moving phi(p_1) to its S_1-orbit
// minimum, and so on.  For G cyclic (all d_i coprime) H is all of Aut(G).

use std::env;
use std::fs::File;
use std::io::{BufWriter, Write};
use std::time::Instant;

struct Ctx {
    n: usize,
    #[allow(dead_code)]
    dims: Vec<usize>,
    add: Vec<u16>,
    primes: Vec<usize>,
    items: Vec<Vec<(usize, usize)>>, // per prime index: (m, m/p)
    h: Vec<Vec<u16>>,
    phi: Vec<u16>,
    used: Vec<u16>,  // count of numbers with this value
    owner: Vec<u16>, // first number with this value
    nodes: u64,
    leaves: u64,
    nodes_at: Vec<u64>,
    budget: usize,
    cap: u16,
    symdepth: usize,
    all: bool,
    nsol: u64,
    sol: Option<Vec<u16>>,
    cert: Option<BufWriter<File>>,
    coll: std::collections::HashMap<(usize, usize), u64>,
    stats: bool,
}

fn primes_upto(n: usize) -> Vec<usize> {
    let mut v = vec![];
    for p in 2..=n {
        if (2..p).take_while(|d| d * d <= p).all(|d| p % d != 0) {
            v.push(p);
        }
    }
    v
}

fn gcd(a: usize, b: usize) -> usize {
    if b == 0 { a } else { gcd(b, a % b) }
}

fn decode(mut x: usize, dims: &[usize]) -> Vec<usize> {
    let mut t = vec![];
    for &d in dims {
        t.push(x % d);
        x /= d;
    }
    t
}
fn encode(t: &[usize], dims: &[usize]) -> usize {
    let mut x = 0;
    let mut mul = 1;
    for (i, &d) in dims.iter().enumerate() {
        x += t[i] * mul;
        mul *= d;
    }
    x
}

impl Ctx {
    fn new(dims: Vec<usize>, m: usize, primes: Vec<usize>) -> Ctx {
        let n: usize = dims.iter().product();
        let mut add = vec![0u16; n * n];
        for a in 0..n {
            let ta = decode(a, &dims);
            for b in 0..n {
                let tb = decode(b, &dims);
                let tc: Vec<usize> = (0..dims.len()).map(|i| (ta[i] + tb[i]) % dims[i]).collect();
                add[a * n + b] = encode(&tc, &dims) as u16;
            }
        }
        // items
        let mut items = vec![vec![]; primes.len()];
        for x in 2..=m {
            let mut r = x;
            let mut last: Option<usize> = None;
            for (k, &p) in primes.iter().enumerate() {
                if r % p == 0 {
                    last = Some(k);
                    while r % p == 0 {
                        r /= p;
                    }
                }
            }
            if r == 1 {
                let k = last.unwrap();
                items[k].push((x, x / primes[k]));
            }
        }
        // H: componentwise unit multiplications
        let mut units: Vec<Vec<usize>> = vec![vec![]];
        for &d in &dims {
            let us: Vec<usize> = (0..d.max(1)).filter(|&u| gcd(u, d) == 1).collect();
            let mut nu = vec![];
            for t in &units {
                for &u in &us {
                    let mut t2 = t.clone();
                    t2.push(u);
                    nu.push(t2);
                }
            }
            units = nu;
        }
        let mut h = vec![];
        for u in &units {
            let perm: Vec<u16> = (0..n)
                .map(|a| {
                    let ta = decode(a, &dims);
                    let tb: Vec<usize> = (0..dims.len()).map(|i| (ta[i] * u[i]) % dims[i]).collect();
                    encode(&tb, &dims) as u16
                })
                .collect();
            h.push(perm);
        }
        let np = primes.len();
        Ctx {
            n,
            dims,
            add,
            primes,
            items,
            h,
            phi: vec![0u16; m + 1],
            used: vec![0u16; n],
            owner: vec![0u16; n],
            nodes: 0,
            leaves: 0,
            nodes_at: vec![0; np + 1],
            budget: 0,
            cap: 1,
            symdepth: 99,
            all: false,
            nsol: 0,
            sol: None,
            cert: None,
            coll: std::collections::HashMap::new(),
            stats: false,
        }
    }

    fn run(&mut self) -> bool {
        // number 1 has value 0
        self.phi[1] = 0;
        self.used[0] = 1;
        self.owner[0] = 1;
        let stab: Vec<usize> = (0..self.h.len()).collect();
        self.dfs(0, &stab, 0)
    }

    fn dfs(&mut self, k: usize, stab: &Vec<usize>, defects: usize) -> bool {
        self.nodes += 1;
        self.nodes_at[k] += 1;
        if k == self.primes.len() {
            self.nsol += 1;
            if self.sol.is_none() {
                self.sol = Some(self.phi.clone());
            }
            return !self.all;
        }
        let n = self.n;
        let p = self.primes[k];
        let nit = self.items[k].len();
        let usesym = k < self.symdepth && stab.len() > 1;
        for g in 0..n {
            if usesym {
                let mut minimal = true;
                for &hi in stab {
                    if (self.h[hi][g] as usize) < g {
                        minimal = false;
                        break;
                    }
                }
                if !minimal {
                    continue;
                }
            }
            self.phi[p] = g as u16;
            let mut done = 0;
            let mut d = defects;
            let mut ok = true;
            let mut cpair = (0usize, 0usize);
            for idx in 0..nit {
                let (m, q) = self.items[k][idx];
                let v = self.add[g * n + self.phi[q] as usize] as usize;
                self.phi[m] = v as u16;
                done = idx + 1;
                if self.used[v] >= self.cap {
                    d += 1;
                    if d > self.budget {
                        cpair = (self.owner[v] as usize, m);
                        // not inserted
                        done = idx;
                        ok = false;
                        break;
                    }
                } else if self.used[v] == 0 {
                    self.owner[v] = m as u16;
                }
                self.used[v] += 1;
            }
            let mut found = false;
            if ok {
                if let Some(w) = self.cert.as_mut() {
                    writeln!(w, "D").unwrap();
                }
                if usesym {
                    let ns: Vec<usize> = stab.iter().cloned().filter(|&hi| self.h[hi][g] as usize == g).collect();
                    found = self.dfs(k + 1, &ns, d);
                } else if k < self.symdepth {
                    found = self.dfs(k + 1, stab, d);
                } else {
                    let ns = vec![0usize];
                    found = self.dfs(k + 1, &ns, d);
                }
            } else {
                self.leaves += 1;
                if self.stats {
                    *self.coll.entry(cpair).or_insert(0) += 1;
                }
                if let Some(w) = self.cert.as_mut() {
                    writeln!(w, "{} {}", cpair.0, cpair.1).unwrap();
                }
            }
            for idx in 0..done {
                let (m, _) = self.items[k][idx];
                let v = self.phi[m] as usize;
                self.used[v] -= 1;
            }
            if found {
                return true;
            }
        }
        false
    }
}

fn partitions(e: usize, maxpart: usize) -> Vec<Vec<usize>> {
    if e == 0 {
        return vec![vec![]];
    }
    let mut out = vec![];
    let mut a = e.min(maxpart);
    while a >= 1 {
        for mut rest in partitions(e - a, a) {
            let mut v = vec![a];
            v.append(&mut rest);
            out.push(v);
        }
        a -= 1;
    }
    out
}

fn groups_of_order(n: usize) -> Vec<Vec<usize>> {
    // list of dims (prime-power cyclic factors); cyclic group first
    let mut res: Vec<Vec<usize>> = vec![vec![]];
    let mut r = n;
    let mut p = 2;
    while r > 1 {
        if r % p == 0 {
            let mut e = 0;
            while r % p == 0 {
                r /= p;
                e += 1;
            }
            let parts = partitions(e, e);
            let mut nr = vec![];
            for base in &res {
                for part in &parts {
                    let mut b = base.clone();
                    for &a in part {
                        b.push(p.pow(a as u32));
                    }
                    nr.push(b);
                }
            }
            res = nr;
        }
        p += 1;
    }
    res
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("usage: search scan N1 N2 | search one key=value...");
        return;
    }
    if args[1] == "scan" {
        let n1: usize = args[2].parse().unwrap();
        let n2: usize = args[3].parse().unwrap();
        for n in n1..=n2 {
            let t0 = Instant::now();
            let primes: Vec<usize> = primes_upto(n / 2);
            let mut total_nodes = 0u64;
            let mut found = false;
            let groups = if n == 1 { vec![vec![1usize]] } else { groups_of_order(n) };
            let ng = groups.len();
            for dims in groups {
                let mut c = Ctx::new(dims.clone(), n, primes.clone());
                let r = c.run();
                total_nodes += c.nodes;
                if r {
                    let phi = c.sol.unwrap();
                    let ds: Vec<String> = dims.iter().map(|d| d.to_string()).collect();
                    let mut s = format!("{} YES dims={} primes=", n, ds.join(","));
                    let mut first = true;
                    for &p in &primes {
                        if !first {
                            s.push(';');
                        }
                        first = false;
                        let t = decode(phi[p] as usize, &dims);
                        let ts: Vec<String> = t.iter().map(|d| d.to_string()).collect();
                        s.push_str(&format!("{}:{}", p, ts.join(",")));
                    }
                    println!("{} nodes={} secs={:.2}", s, total_nodes, t0.elapsed().as_secs_f64());
                    found = true;
                    break;
                }
            }
            if !found {
                println!("{} NO groups={} nodes={} secs={:.2}", n, ng, total_nodes, t0.elapsed().as_secs_f64());
            }
            std::io::stdout().flush().unwrap();
        }
        return;
    }
    // mode one
    let mut dims: Vec<usize> = vec![];
    let mut m = 0usize;
    let mut budget = 0usize;
    let mut primes: Option<Vec<usize>> = None;
    let mut symdepth = 99usize;
    let mut cert: Option<String> = None;
    let mut all = false;
    let mut cap = 1u16;
    let mut stats = false;
    for a in &args[2..] {
        let kv: Vec<&str> = a.splitn(2, '=').collect();
        let (k, v) = (kv[0], kv[1]);
        match k {
            "dims" => dims = v.split(',').map(|x| x.parse().unwrap()).collect(),
            "m" => m = v.parse().unwrap(),
            "budget" => budget = v.parse().unwrap(),
            "primes" => primes = Some(v.split(',').map(|x| x.parse().unwrap()).collect()),
            "symdepth" => symdepth = v.parse().unwrap(),
            "cert" => cert = Some(v.to_string()),
            "all" => all = v == "1",
            "cap" => cap = v.parse().unwrap(),
            "stats" => stats = v == "1",
            _ => panic!("unknown key {}", k),
        }
    }
    let n: usize = dims.iter().product();
    if m == 0 {
        m = n;
    }
    let primes = primes.unwrap_or_else(|| primes_upto(m / 2));
    let t0 = Instant::now();
    let mut c = Ctx::new(dims.clone(), m, primes.clone());
    c.budget = budget;
    c.cap = cap;
    c.symdepth = symdepth;
    c.all = all;
    c.stats = stats;
    if let Some(f) = &cert {
        assert!(budget == 0 && dims.len() == 1 && symdepth <= 1);
        let mut w = BufWriter::new(File::create(f).unwrap());
        let ps: Vec<String> = primes.iter().map(|d| d.to_string()).collect();
        writeln!(w, "n {}", n).unwrap();
        writeln!(w, "m {}", m).unwrap();
        writeln!(w, "primes {}", ps.join(" ")).unwrap();
        writeln!(w, "rootsym {}", if symdepth == 1 { 1 } else { 0 }).unwrap();
        c.cert = Some(w);
    }
    let r = c.run();
    if let Some(w) = c.cert.as_mut() {
        w.flush().unwrap();
    }
    let nsmooth: usize = 1 + c.items.iter().map(|v| v.len()).sum::<usize>();
    println!(
        "dims={:?} m={} budget={} primes={:?} smooth_numbers={} symdepth={}",
        dims, m, budget, primes, nsmooth, symdepth
    );
    println!(
        "result={} solutions_seen={} nodes={} leaves={} secs={:.2}",
        if c.nsol > 0 { "EXISTS" } else { "NONE" },
        c.nsol,
        c.nodes,
        c.leaves,
        t0.elapsed().as_secs_f64()
    );
    let _ = r;
    println!("nodes_at_depth={:?}", c.nodes_at);
    if let Some(phi) = &c.sol {
        let mut s = String::from("solution ");
        for &p in &primes {
            let t = decode(phi[p] as usize, &dims);
            let ts: Vec<String> = t.iter().map(|d| d.to_string()).collect();
            s.push_str(&format!("{}:{};", p, ts.join(",")));
        }
        println!("{}", s);
    }
    if stats {
        let mut v: Vec<((usize, usize), u64)> = c.coll.iter().map(|(a, b)| (*a, *b)).collect();
        v.sort_by(|a, b| b.1.cmp(&a.1));
        println!("distinct_collision_pairs={}", v.len());
        for (pair, cnt) in v.iter().take(40) {
            println!("collision {} {} count {}", pair.0, pair.1, cnt);
        }
    }
}
