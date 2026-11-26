// gtile7 = gtile6 with mode=coset generalised to H = Z_{p^{a+1}}, fibres cosets of p^a Z (q = |H|/p).
// gtile6: generalisation of gtile5 (|B|=3) to |B|=p, after the reduction B -> tB inside the p-Sylow H,
// |H| = p^2, G = H x Z_m, m = n/p (t = m coprime to p; Tijdeman: A(+)B=G, gcd(t,|B|)=1 => A(+)tB=G).
// With B inside H: A(+)B=G <=> for every w in Z_m, the fibre A_w is a complement of B in H (|A_w|=p).
// phi = (h, f): h: S -> H, f: S -> Z_m.  Primes <= n/2 are branched; fibre contents must stay inside
// some complement of B.  Primes > n/2 occur once each in [n] and fill the remaining fibre slots freely,
// so every surviving leaf is a tiling.
// mode=ext   : any H with |H|<=25 (hd=25 | hd=5,5 | hd=9 | hd=3,3), any B; complements enumerated,
//              subsets of complements stored in a 2^|H| bitset.
// mode=coset : H = Z_{p^2} (hd=p*p), each fibre must be one coset of pZ_{p^2} (= the complement set of
//              every non-subgroup tile B of Z_{p^2}; see notes).  Works for p=13.
// Symmetry: units of Z_m on f(2) (orbit-minimal); on h(2), automorphisms of H preserving the complement set.
// Parallel split: split=i/N keeps the depth-1 nodes (choice for prime 3) with counter % N == i.
// Build: rustc -O gtile6.rs -o gtile6.exe
// Run:   gtile6 n=195 p=5 hd=25 mode=coset split=0/20 limit=..   |  gtile6 n=.. p=5 hd=5,5 B=0/0,0/1,0/2,1/0,4/2
use std::env;
struct S { m: usize, hg: usize, p: usize, q: usize, coset: bool, hadd: Vec<usize>, ext: Vec<u64>, primes: Vec<usize>,
  items: Vec<Vec<(usize,usize)>>, f: Vec<usize>, h: Vec<usize>, mask: Vec<u32>, res: Vec<usize>, cnt: Vec<usize>,
  nodes: u64, limit: u64, hsym: Vec<usize>, fsym: Vec<usize>, depth: Vec<u64>, si: u64, sn: u64, c1: u64 }
impl S {
  #[inline] fn ins(&mut self, w: usize, hh: usize) -> bool {
    if self.coset {
      let (r, d) = (hh % self.q, hh / self.q); let bit = 1u32 << d;
      if self.mask[w] & bit != 0 { return false; }
      if self.cnt[w] > 0 && self.res[w] != r { return false; }
      self.res[w] = r; self.mask[w] |= bit; self.cnt[w] += 1; true
    } else {
      let bit = 1u32 << hh; let nm = self.mask[w] | bit;
      if self.mask[w] & bit != 0 || (self.ext[(nm >> 6) as usize] >> (nm & 63)) & 1 == 0 { return false; }
      self.mask[w] = nm; self.cnt[w] += 1; true
    }
  }
  #[inline] fn del(&mut self, w: usize, hh: usize) {
    let bit = if self.coset { 1u32 << (hh / self.q) } else { 1u32 << hh };
    self.mask[w] &= !bit; self.cnt[w] -= 1;
  }
  fn dfs(&mut self, k: usize) -> bool {
    self.depth[k] += 1;
    if k == self.primes.len() { return true; }
    for v in 0..self.m { if k == 0 && !self.fsym.contains(&v) { continue; }
     for hv in 0..self.hg { if k == 0 && !self.hsym.contains(&hv) { continue; }
      if k == 1 { self.c1 += 1; if (self.c1 - 1) % self.sn != self.si { continue; } }
      if self.nodes > self.limit { return false; }
      self.nodes += 1;
      let pr = self.primes[k]; self.f[pr] = v; self.h[pr] = hv;
      let mut done = 0; let mut ok = true;
      for idx in 0..self.items[k].len() { let (x, y) = self.items[k][idx];
        let w = (v + self.f[y]) % self.m; let hh = self.hadd[hv*self.hg + self.h[y]];
        if !self.ins(w, hh) { ok = false; break; }
        self.f[x] = w; self.h[x] = hh; done += 1; }
      if ok && self.dfs(k+1) { return true; }
      for idx in (0..done).rev() { let x = self.items[k][idx].0; let (w, hh) = (self.f[x], self.h[x]); self.del(w, hh); }
    } }
    false
  }
}
fn gcd(a: usize, b: usize) -> usize { if b == 0 { a } else { gcd(b, a % b) } }
fn rec(c: &mut Vec<usize>, start: usize, p: usize, hg: usize, b: &Vec<usize>, hadd: &Vec<usize>, out: &mut Vec<u32>) {
  if c.len() == p { let mut cov = 0u32; for &x in c.iter() { for &y in b { let s = hadd[x*hg+y]; if cov >> s & 1 == 1 { return; } cov |= 1 << s; } }
    out.push(c.iter().fold(0u32, |a, &x| a | 1 << x)); return; }
  for x in start..hg { c.push(x); rec(c, x+1, p, hg, b, hadd, out); c.pop(); }
}
fn main() {
  let (mut n, mut p, mut hd, mut bs, mut limit, mut coset, mut si, mut sn) = (195usize, 5usize, vec![25usize], String::new(), u64::MAX, false, 0u64, 1u64);
  for a in env::args().skip(1) { let kv: Vec<&str> = a.splitn(2,'=').collect(); match kv[0] {
    "n" => n = kv[1].parse().unwrap(), "p" => p = kv[1].parse().unwrap(),
    "hd" => hd = kv[1].split(',').map(|x| x.parse().unwrap()).collect(), "B" => bs = kv[1].to_string(),
    "limit" => limit = kv[1].parse().unwrap(), "mode" => coset = kv[1] == "coset",
    "split" => { let v: Vec<u64> = kv[1].split('/').map(|x| x.parse().unwrap()).collect(); si = v[0]; sn = v[1]; }, _ => panic!("key") } }
  let hg: usize = hd.iter().product(); assert!(n % p == 0); { let mut t = hg; while t % p == 0 { t /= p; } assert!(t == 1 && hg >= p*p); } if !coset { assert!(hg == p*p); } let q = hg / p; let m = n / p;
  if coset { assert!(hd.len() == 1 && p <= 31); } else { assert!(hg <= 25); }
  let fsym: Vec<usize> = (0..m).filter(|&x| (1..m.max(2)).filter(|&u| gcd(u, m) == 1).all(|u| (u * x) % m >= x)).collect();
  let enc = |c: &Vec<usize>| c.iter().zip(&hd).fold(0, |acc, (x, d)| acc * d + x % d);
  let dec = |mut e: usize| { let mut c = vec![0; hd.len()]; for i in (0..hd.len()).rev() { c[i] = e % hd[i]; e /= hd[i]; } c };
  let mut hadd = vec![0; hg*hg]; for x in 0..hg { for y in 0..hg { hadd[x*hg+y] = enc(&dec(x).iter().zip(&dec(y)).map(|(a,b)| a+b).collect()); } }
  let mut auts: Vec<Vec<usize>> = vec![];
  if hd.len() == 1 { for u in 1..hg { if gcd(u, hg) == 1 { auts.push((0..hg).map(|x| x*u % hg).collect()); } } }
  else { let q = hd[0]; assert!(hd.len() == 2 && hd[1] == q);
    for a in 0..q { for b in 0..q { for c in 0..q { for d in 0..q { if (a*d + q*q - (b*c)%q) % q == 0 { continue; }
      auts.push((0..hg).map(|x| { let (x1,x2) = (x/q, x%q); ((a*x1+b*x2)%q)*q + (c*x1+d*x2)%q }).collect()); } } } } }
  let mut ext = vec![0u64; if coset { 1 } else { ((1usize << hg) + 63) / 64 }];
  let mut comps: Vec<u32> = vec![]; let ncomp; let hsym: Vec<usize>;
  if coset { ncomp = p; let mut hs = vec![0usize]; let mut t = 1; while t < hg { hs.push(t); t *= p; } hsym = hs; bs = format!("coset-of-{}Z{}", q, hg); }
  else {
    let b: Vec<usize> = bs.split(',').map(|t| enc(&t.split('/').map(|x| x.parse().unwrap()).collect())).collect();
    assert!(b.len() == p && b[0] == 0);
    rec(&mut vec![], 0, p, hg, &b, &hadd, &mut comps); ncomp = comps.len();
    for &c in &comps { let mut s = c; loop { ext[(s >> 6) as usize] |= 1u64 << (s & 63); if s == 0 { break; } s = (s - 1) & c; } }
    let mut cs = comps.clone(); cs.sort();
    let stab: Vec<&Vec<usize>> = auts.iter().filter(|u| { let mut t: Vec<u32> = comps.iter().map(|&c| (0..hg).filter(|&x| c >> x & 1 == 1).fold(0u32, |a, x| a | 1 << u[x])).collect(); t.sort(); t == cs }).collect();
    hsym = (0..hg).filter(|&x| stab.iter().all(|u| u[x] >= x)).collect();
    eprintln!("H-stabiliser (of complement set) size {} of {}; h(2) reps {:?}", stab.len(), auts.len(), hsym);
  }
  let isp = |x: usize| x > 1 && (2..x).take_while(|d| d*d <= x).all(|d| x % d != 0);
  let primes: Vec<usize> = (2..=n/2).filter(|&x| isp(x)).collect();
  let mut items = vec![vec![]; primes.len()];
  for x in 2..=n { let mut r = x; let mut last = None; for (k,&q) in primes.iter().enumerate() { if r % q == 0 { last = Some(k); while r % q == 0 { r /= q; } } }
    if r == 1 { let k = last.unwrap(); items[k].push((x, x / primes[k])); } }
  let np = primes.len();
  let mut s = S { m, hg, p, q, coset, hadd, ext, primes, items, f: vec![0; n+1], h: vec![0; n+1], mask: vec![0; m], res: vec![0; m], cnt: vec![0; m],
    nodes: 0, limit, hsym, fsym, depth: vec![0; np+1], si, sn, c1: 0 };
  assert!(s.ins(0, 0)); // phi(1) = 0
  let t = std::time::Instant::now();
  let r = if ncomp == 0 { false } else { s.dfs(0) };
  println!("gtile7 split={}/{} n={} p={} H={:?} B={} mode={} complements={} result={} nodes={} secs={:.2} depth={:?}", si, sn, n, p, hd, bs,
    if coset {"coset"} else {"ext"}, ncomp, if r {"EXISTS"} else if s.nodes > limit {"TIMEOUT"} else {"NONE"}, s.nodes, t.elapsed().as_secs_f64(), &s.depth);
  if r { // fill each fibre with big primes; print phi on all primes as h-coords/f (G = H x Z_m)
    let bigp: Vec<usize> = (n/2+1..=n).filter(|&x| isp(x)).collect(); let mut bi = 0;
    for w in 0..m {
      let fill: Vec<usize> = if coset { let r0 = if s.cnt[w] > 0 { s.res[w] } else { 0 };
          (0..p).filter(|&d| s.mask[w] >> d & 1 == 0).map(|d| d*q + r0).collect() }
        else { let mk = s.mask[w]; let c = *comps.iter().find(|&&c| c & mk == mk).unwrap(); (0..hg).filter(|&e| c >> e & 1 == 1 && mk >> e & 1 == 0).collect() };
      for e in fill { let q = bigp[bi]; bi += 1; s.f[q] = w; s.h[q] = e; } }
    assert!(bi == bigp.len());
    let all: Vec<usize> = (2..=n).filter(|&x| isp(x)).collect();
    let v: Vec<String> = all.iter().map(|&q| format!("{}:{}/{}", q, dec(s.h[q]).iter().map(|c| c.to_string()).collect::<Vec<_>>().join("/"), s.f[q])).collect();
    println!("solution {}", v.join(" ")); }
}
