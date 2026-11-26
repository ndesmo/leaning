// Exact search for |B|=3 periodic tilings in |G|=585, after the reduction B -> 65B inside the
// 3-Sylow H (Tijdeman: A(+)B=G, gcd(t,|B|)=1 => A(+)tB=G; t=65 is a unit on H and kills Z65).
// With B inside H: A(+)B=G  <=>  for every coset w of H (w in G/H = Z65), A_w (+) B = H, |A_w|=3.
// phi = (h, f): h: S -> H, f: S -> Z65.  Search primes <= n/2; fibre masks of h-values must stay
// subsets of some complement C of B in H (C(+)B=H).  Primes > n/2 occur once each and then fill
// the 19 missing fibre slots freely, so every surviving leaf is a tiling.
// Symmetry: units of Z65 permute fibres -> f(2) in {0,1,5,13}.  (No H-symmetry used.)
// Build: rustc -O gtile5.rs -o gtile5.exe
// Run:   gtile5 hd=9 B=0,1,2       |  gtile5 hd=3,3 B=0/0,1/0,0/1   [limit=..]
use std::env;
struct S { m: usize, hg: usize, hadd: Vec<usize>, ext: Vec<bool>, primes: Vec<usize>, items: Vec<Vec<(usize,usize)>>,
  f: Vec<usize>, h: Vec<usize>, mask: Vec<u16>, nodes: u64, limit: u64, sol: bool, hsym: Vec<usize>, depth: Vec<u64>, top: i64, topc: i64, fsym: Vec<usize> }
impl S {
  fn dfs(&mut self, k: usize) -> bool {
    self.depth[k] += 1;
    if k == self.primes.len() { self.sol = true; return true; }
    for v in 0..self.m { if k == 0 && !self.fsym.contains(&v) { continue; }
     for hv in 0..self.hg { if k == 0 && !self.hsym.contains(&hv) { continue; }
      if k == 0 { self.topc += 1; if self.top >= 0 && self.topc - 1 != self.top { continue; } }
      if self.nodes > self.limit { return false; }
      self.nodes += 1;
      let p = self.primes[k]; self.f[p] = v; self.h[p] = hv;
      let mut done = 0; let mut ok = true;
      for idx in 0..self.items[k].len() { let (x, y) = self.items[k][idx];
        let w = (v + self.f[y]) % self.m; let hh = self.hadd[hv*self.hg + self.h[y]];
        let bit = 1u16 << hh; let nm = self.mask[w] | bit;
        if self.mask[w] & bit != 0 || !self.ext[nm as usize] { ok = false; break; }
        self.mask[w] = nm; self.f[x] = w; self.h[x] = hh; done += 1; }
      if ok && self.dfs(k+1) { return true; }
      for idx in (0..done).rev() { let x = self.items[k][idx].0; self.mask[self.f[x]] &= !(1u16 << self.h[x]); }
    } }
    false
  }
}
fn gcd(a: usize, b: usize) -> usize { if b == 0 { a } else { gcd(b, a % b) } }
fn main() {
  let (mut n, mut hd, mut bs, mut limit, mut top) = (195usize, vec![9usize], String::new(), 10_000_000_000u64, -1i64);
  for a in env::args().skip(1) { let kv: Vec<&str> = a.splitn(2,'=').collect(); match kv[0] {
    "n" => n = kv[1].parse().unwrap(), "hd" => hd = kv[1].split(',').map(|x| x.parse().unwrap()).collect(),
    "B" => bs = kv[1].to_string(), "limit" => limit = kv[1].parse().unwrap(), "top" => top = kv[1].parse().unwrap(), _ => panic!("key") } }
  let hg: usize = hd.iter().product(); assert!(hg == 9 && n % 3 == 0); let m = n / 3;
  let fsym: Vec<usize> = (0..m).filter(|&x| (1..m.max(2)).filter(|&u| gcd(u, m) == 1).all(|u| (u * x) % m >= x)).collect();
  let enc = |c: &Vec<usize>| c.iter().zip(&hd).fold(0, |acc, (x, d)| acc * d + x % d);
  let dec = |mut e: usize| { let mut c = vec![0; hd.len()]; for i in (0..hd.len()).rev() { c[i] = e % hd[i]; e /= hd[i]; } c };
  let mut hadd = vec![0; hg*hg]; for x in 0..hg { for y in 0..hg { hadd[x*hg+y] = enc(&dec(x).iter().zip(&dec(y)).map(|(a,b)| a+b).collect()); } }
  let b: Vec<usize> = bs.split(',').map(|t| enc(&t.split('/').map(|x| x.parse().unwrap()).collect())).collect();
  assert!(b.len() == 3 && b[0] == 0);
  // complements C of B in H, and all their subsets
  let mut ext = vec![false; 1 << hg]; let mut ncomp = 0; let mut comps: Vec<u32> = vec![];
  for c in 0u32..(1 << hg) { if c.count_ones() != 3 { continue; }
    let mut cov = 0u32; let mut good = true;
    for x in 0..hg { if c >> x & 1 == 1 { for &y in &b { let s = hadd[x*hg+y]; if cov >> s & 1 == 1 { good = false; } cov |= 1 << s; } } }
    if good && cov == (1 << hg) - 1 { ncomp += 1; comps.push(c); let mut s = c; loop { ext[s as usize] = true; if s == 0 { break; } s = (s - 1) & c; } } }
  let mut auts: Vec<Vec<usize>> = vec![];
  if hd.len() == 1 { for u in [1usize,2,4,5,7,8] { auts.push((0..9).map(|x| x*u % 9).collect()); } }
  else { for a in 0..3 { for bq in 0..3 { for c in 0..3 { for d in 0..3 { if (a*d + 9 - (bq*c)%3) % 3 == 0 { continue; }
    auts.push((0..9).map(|x| { let (x1,x2) = (x/3, x%3); ((a*x1+bq*x2)%3)*3 + (c*x1+d*x2)%3 }).collect()); } } } } }
  let mut bs_sorted = b.clone(); bs_sorted.sort();
  let stab: Vec<Vec<usize>> = auts.into_iter().filter(|u| { let ub: Vec<usize> = b.iter().map(|&x| u[x]).collect();
    ub.iter().any(|&c| { let mut t: Vec<usize> = ub.iter().map(|&x| (0..hg).find(|&y| hadd[y*hg+c] == x).unwrap()).collect(); t.sort(); t == bs_sorted }) }).collect();
  let hsym: Vec<usize> = (0..hg).filter(|&x| stab.iter().all(|u| u[x] >= x)).collect();
  eprintln!("H-stabiliser size {} h(2) reps {:?}", stab.len(), hsym);
  let isp = |x: usize| x > 1 && (2..x).take_while(|d| d*d <= x).all(|d| x % d != 0);
  let primes: Vec<usize> = (2..=n/2).filter(|&x| isp(x)).collect();
  let mut items = vec![vec![]; primes.len()];
  for x in 2..=n { let mut r = x; let mut last = None; for (k,&p) in primes.iter().enumerate() { if r % p == 0 { last = Some(k); while r % p == 0 { r /= p; } } }
    if r == 1 { let k = last.unwrap(); items[k].push((x, x / primes[k])); } }
  let mut s = S { m, hg, hadd, ext, primes, items, f: vec![0; n+1], h: vec![0; n+1], mask: vec![0; m], nodes: 0, limit, sol: false, hsym: hsym.clone(), depth: vec![0; 30], top, topc: 0, fsym: fsym.clone() };
  s.mask[0] = 1; // phi(1) = 0
  let t = std::time::Instant::now();
  let r = if ncomp == 0 { false } else { s.dfs(0) };
  println!("gtile5 top={} n={} H={:?} B={} complements={} result={} nodes={} secs={:.2} depth={:?}", top, n, hd, bs, ncomp,
    if r {"EXISTS"} else if s.nodes > limit {"TIMEOUT"} else {"NONE"}, s.nodes, t.elapsed().as_secs_f64(), &s.depth[..26]);
  if r { // complete each fibre with big primes; print phi on all primes as h-coords/f (G = H x Z_m)
    let bigp: Vec<usize> = (n/2+1..=n).filter(|&x| isp(x)).collect(); let mut bi = 0;
    for w in 0..m { let mk = s.mask[w] as u32; let c = *comps.iter().find(|&&c| c & mk == mk).unwrap();
      for e in 0..hg { if c >> e & 1 == 1 && mk >> e & 1 == 0 { let p = bigp[bi]; bi += 1; s.f[p] = w; s.h[p] = e; } } }
    assert!(bi == bigp.len());
    let all: Vec<usize> = (2..=n).filter(|&x| isp(x)).collect();
    let v: Vec<String> = all.iter().map(|&p| format!("{}:{}/{}", p, dec(s.h[p]).iter().map(|c| c.to_string()).collect::<Vec<_>>().join("/"), s.f[p])).collect();
    println!("solution {}", v.join(" ")); }
}
