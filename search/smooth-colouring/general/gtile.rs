// General periodic-tiling search for n-satisfactory colourings.
// Decides: is there phi: Z^+ -> G = Z_d1 x ... x Z_dr (multiplicative -> additive)
// with A = phi({1..n}) of size n and A (+) B = G, for a GIVEN complement B (0 in B)?
// Constraint used: for distinct a,b <= n, phi(a)-phi(b) not in D0 = (B-B) (incl. 0).
// Primes <= n/2 are branched (increasing); primes in (n/2,n] are then placed by an
// exact cover of the holes G \ (A_smooth + B) by translates of B.
// Symmetry: componentwise unit automorphisms u with u*D0 = D0; phi(2) taken orbit-minimal.
// Build: rustc -O gtile.rs -o gtile.exe
// Run:   gtile n=195 dims=9,5,13 B=0/0/0,1/0/0,2/3/7   (elements as '/'-separated coords)
use std::env;
struct S { n: usize, g: usize, add: Vec<u16>, neg: Vec<u16>, d0: Vec<usize>, b: Vec<usize>,
  primes: Vec<usize>, items: Vec<Vec<(usize,usize)>>, bigp: Vec<usize>, phi: Vec<usize>,
  blk: Vec<u32>, nodes: u64, sol: Option<Vec<usize>>, stab: Vec<Vec<usize>>, limit: u64, timeout: bool, leaves: u64, bvars: Vec<Vec<usize>> }
impl S {
  fn put(&mut self, v: usize, s: i32) { for i in 0..self.d0.len() { let w = self.add[v*self.g+self.d0[i]] as usize; self.blk[w] = (self.blk[w] as i32 + s) as u32; } }
  fn cover(&mut self, holes: &mut Vec<bool>, left: usize, out: &mut Vec<usize>) -> bool {
    if left == 0 { return true; }
    self.nodes += 1; if self.nodes > self.limit { self.timeout = true; return false; }
    let h = holes.iter().position(|&x| x).unwrap();
    for j in 0..self.b.len() { // translate t with t + b_j = h
      let t = self.add[h*self.g + self.neg[self.b[j]] as usize] as usize;
      if (0..self.b.len()).all(|i| holes[self.add[t*self.g+self.b[i]] as usize]) {
        for i in 0..self.b.len() { holes[self.add[t*self.g+self.b[i]] as usize] = false; }
        out.push(t);
        if self.cover(holes, left - 1, out) { return true; }
        out.pop();
        for i in 0..self.b.len() { holes[self.add[t*self.g+self.b[i]] as usize] = true; }
      }
    }
    false
  }
  fn dfs(&mut self, k: usize) -> bool {
    if k == self.primes.len() {
      let mut holes = vec![true; self.g];
      for x in 1..=self.n { if self.phi[x] != usize::MAX { for i in 0..self.b.len() { holes[self.add[self.phi[x]*self.g+self.b[i]] as usize] = false; } } }
      self.leaves += 1;
      // symmetry-sound leaf: a pruned solution u*phi tiles with u*B, so try every u^{-1}B
      let holes0 = holes.clone(); let saveb = self.b.clone();
      let mut out = vec![]; let mut okc = false;
      for bv in self.bvars.clone() {
        self.b = bv.clone(); holes = vec![true; self.g];
        for x in 1..=self.n { if self.phi[x] != usize::MAX { for i in 0..self.b.len() { holes[self.add[self.phi[x]*self.g+self.b[i]] as usize] = false; } } }
        out.clear();
        if holes.iter().filter(|&&h| h).count() == self.bigp.len() * self.b.len() && self.cover(&mut holes, self.bigp.len(), &mut out) { okc = true; break; }
      }
      let _ = holes0; if !okc { self.b = saveb.clone(); }
      if okc {
        for (i,&p) in self.bigp.clone().iter().enumerate() { self.phi[p] = out[i]; }
        self.sol = Some(self.phi.clone()); return true; }
      return false;
    }
    for g in 0..self.g {
      if k == 0 && self.stab.iter().any(|u| u[g] < g) { continue; }
      if self.nodes > self.limit { self.timeout = true; return false; }
      self.nodes += 1;
      let p = self.primes[k]; self.phi[p] = g;
      let mut done = 0; let mut ok = true;
      for idx in 0..self.items[k].len() {
        let (x, y) = self.items[k][idx];
        let v = self.add[g*self.g + self.phi[y]] as usize;
        if self.blk[v] != 0 { ok = false; break; }
        self.phi[x] = v; self.put(v, 1); done += 1;
      }
      if ok && self.dfs(k+1) { return true; }
      for idx in (0..done).rev() { let x = self.items[k][idx].0; let v = self.phi[x]; self.put(v, -1); self.phi[x] = usize::MAX; }
    }
    self.phi[self.primes[k]] = usize::MAX;
    false
  }
}
fn gcd(a: usize, b: usize) -> usize { if b == 0 { a } else { gcd(b, a % b) } }
fn main() {
  let (mut n, mut dims, mut bs, mut limit, mut dil, mut sl, mut nsl) = (195usize, vec![585usize], String::new(), 200_000_000u64, false, 0usize, 1usize);
  for a in env::args().skip(1) { let kv: Vec<&str> = a.splitn(2,'=').collect(); match kv[0] {
    "n" => n = kv[1].parse().unwrap(), "dims" => dims = kv[1].split(',').map(|x| x.parse().unwrap()).collect(),
    "B" => bs = kv[1].to_string(), "limit" => limit = kv[1].parse().unwrap(), "dil" => dil = kv[1] == "1", "slice" => { let v: Vec<usize> = kv[1].split('/').map(|x| x.parse().unwrap()).collect(); sl = v[0]; nsl = v[1]; }, _ => panic!("key") } }
  let g: usize = dims.iter().product();
  let enc = |c: &Vec<usize>| c.iter().zip(&dims).fold(0, |acc, (x, d)| acc * d + x % d);
  let dec = |mut e: usize| { let mut c = vec![0; dims.len()]; for i in (0..dims.len()).rev() { c[i] = e % dims[i]; e /= dims[i]; } c };
  let mut add = vec![0u16; g*g]; let mut neg = vec![0u16; g];
  for x in 0..g { let cx = dec(x); neg[x] = enc(&cx.iter().zip(&dims).map(|(a,d)| (d - a) % d).collect()) as u16;
    for y in 0..g { let cy = dec(y); add[x*g+y] = enc(&cx.iter().zip(&cy).map(|(a,b)| a+b).collect()) as u16; } }
  let mut units = vec![vec![]]; for &d in &dims { let mut nu = vec![]; for u in &units { for k in 1..d { if gcd(k,d)==1 { let mut v: Vec<usize> = u.clone(); v.push(k); nu.push(v); } } } units = nu; }
  let umaps: Vec<Vec<usize>> = units.iter().map(|u| (0..g).map(|x| enc(&dec(x).iter().zip(u).map(|(a,k)| a*k).collect())).collect()).collect();
  let isp = |x: usize| x > 1 && (2..x).take_while(|d| d*d <= x).all(|d| x % d != 0);
  let primes: Vec<usize> = (2..=n/2).filter(|&x| isp(x)).collect();
  let bigp: Vec<usize> = (n/2+1..=n).filter(|&x| isp(x)).collect();
  let mut items = vec![vec![]; primes.len()];
  for x in 2..=n { let mut r = x; let mut last = None; for (k,&p) in primes.iter().enumerate() { if r % p == 0 { last = Some(k); while r % p == 0 { r /= p; } } }
    if r == 1 { let k = last.unwrap(); items[k].push((x, x / primes[k])); } }
  let blist: Vec<Vec<usize>> = if bs == "all3" {
    // all B={0,b1,b2} up to translation and componentwise units
    let mut reps: Vec<usize> = (1..g).filter(|&x| umaps.iter().all(|m| m[x] >= x)).collect(); reps.sort();
    let mut seen = std::collections::BTreeSet::new();
    for &b1 in &reps { for b2 in 1..g { if b2 == b1 { continue; }
      let bb = [0usize, b1, b2]; let mut best: Option<Vec<usize>> = None;
      for &t in &bb { for m in &umaps { let mut c: Vec<usize> = bb.iter().map(|&x| m[add[x*g + neg[t] as usize] as usize]).collect(); c.sort();
        if best.as_ref().map_or(true, |b| c < *b) { best = Some(c); } } }
      seen.insert(best.unwrap()); } }
    seen.into_iter().collect()
  } else { vec![bs.split(',').map(|t| enc(&t.split('/').map(|x| x.parse().unwrap()).collect())).collect()] };
  eprintln!("{} complement classes", blist.len());
  let mut found = false;
  for (bi, b) in blist.into_iter().enumerate() {
  if bi % nsl != sl { continue; }
  let bs: String = b.iter().map(|&x| dec(x).iter().map(|c| c.to_string()).collect::<Vec<_>>().join("/")).collect::<Vec<_>>().join(",");
  assert!(b[0] == 0 && b.len() * n == g);
  let mut d0: Vec<usize> = vec![]; for &x in &b { for &y in &b { let d = add[x*g + neg[y] as usize] as usize; if !d0.contains(&d) { d0.push(d); } } }
  if dil { let base = d0.clone(); for t in 2..g { if gcd(t, b.len()) != 1 { continue; } for &d in &base { let mut x = 0usize; for _ in 0..t { x = add[x*g+d] as usize; } if !d0.contains(&x) { d0.push(x); } } } }
  d0.sort();
  let mut stab = vec![];
  for m in &umaps { let m = m.clone();
    let mut img: Vec<usize> = d0.iter().map(|&d| m[d]).collect(); img.sort(); if img == d0 { stab.push(m); } }
  let mut s = S { n, g, add: add.clone(), neg: neg.clone(), d0, b, primes: primes.clone(), items: items.clone(), bigp: bigp.clone(), phi: vec![usize::MAX; n+1], blk: vec![0; g], nodes: 0, sol: None, stab: stab.clone(), limit, timeout: false, leaves: 0, bvars: vec![] };
  { let mut bv: Vec<Vec<usize>> = vec![]; for m in &stab { let mut c: Vec<usize> = s.b.iter().map(|&x| m[x]).collect(); c.sort(); if !bv.contains(&c) { bv.push(c); } } s.bvars = bv; }
  s.phi[1] = 0; s.put(0, 1);
  let t = std::time::Instant::now();
  let r = s.dfs(0);
  println!("n={} dims={:?} dil={} B={} result={} leaves={} nodes={} stab={} secs={:.2}", n, dims, dil, bs, if r {"EXISTS"} else if s.timeout {"TIMEOUT"} else {"NONE"}, s.leaves, s.nodes, s.stab.len(), t.elapsed().as_secs_f64());
  if let Some(phi) = s.sol { let isq = |x: usize| x > 1 && (2..x).take_while(|d| d*d <= x).all(|d| x % d != 0);
    let v: Vec<String> = (2..=n).filter(|&x| isq(x)).map(|p| format!("{}:{}", p, dec(phi[p]).iter().map(|c| c.to_string()).collect::<Vec<_>>().join("/"))).collect();
    println!("solution Bused={} {}", s.b.iter().map(|&x| dec(x).iter().map(|c| c.to_string()).collect::<Vec<_>>().join("/")).collect::<Vec<_>>().join(","), v.join(" ")); found = true; }
  }
  println!("done found={}", found);
}
