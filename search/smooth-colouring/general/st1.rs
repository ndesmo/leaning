// Stage-1 necessary condition: completely additive f: {1..n} -> Z_m with every fibre of size exactly c.
// (|B|=3 tilings in |G|=585 reduce to B inside the 3-Sylow H; then f = phi mod H, m=65, c=3.)
// Big primes p > n/2 occur once and fill deficits freely, so only smooth part is searched with count<=c.
use std::env;
struct S { m: usize, c: usize, primes: Vec<usize>, items: Vec<Vec<(usize,usize)>>, f: Vec<usize>, cnt: Vec<usize>, nodes: u64, sols: u64, limit: u64, maxsol: u64, first: Option<Vec<usize>> }
impl S {
  fn dfs(&mut self, k: usize) {
    if self.nodes > self.limit || self.sols >= self.maxsol { return; }
    if k == self.primes.len() { self.sols += 1; if self.first.is_none() { self.first = Some(self.f.clone()); } return; }
    let p = self.primes[k];
    for v in 0..self.m {
      if k == 0 && ![0,1,5,13].contains(&v) && self.m == 65 { continue; }
      self.nodes += 1;
      let mut done = 0; let mut ok = true;
      for idx in 0..self.items[k].len() { let (x, y) = self.items[k][idx];
        let w = (v + self.f[y]) % self.m; if self.cnt[w] >= self.c { ok = false; break; }
        self.f[x] = w; self.cnt[w] += 1; done += 1; }
      let _ = p;
      if ok { self.dfs(k+1); }
      for idx in (0..done).rev() { let x = self.items[k][idx].0; self.cnt[self.f[x]] -= 1; }
      if self.nodes > self.limit || self.sols >= self.maxsol { return; }
    }
  }
}
fn main() {
  let (mut n, mut m, mut c, mut limit, mut maxsol) = (195usize, 65usize, 3usize, 1_000_000_000u64, 1u64);
  for a in env::args().skip(1) { let kv: Vec<&str> = a.splitn(2,'=').collect(); match kv[0] {
    "n" => n = kv[1].parse().unwrap(), "m" => m = kv[1].parse().unwrap(), "c" => c = kv[1].parse().unwrap(),
    "limit" => limit = kv[1].parse().unwrap(), "maxsol" => maxsol = kv[1].parse().unwrap(), _ => panic!() } }
  let isp = |x: usize| x > 1 && (2..x).take_while(|d| d*d <= x).all(|d| x % d != 0);
  let primes: Vec<usize> = (2..=n/2).filter(|&x| isp(x)).collect();
  let mut items = vec![vec![]; primes.len()];
  for x in 2..=n { let mut r = x; let mut last = None; for (k,&p) in primes.iter().enumerate() { if r % p == 0 { last = Some(k); while r % p == 0 { r /= p; } } }
    if r == 1 { let k = last.unwrap(); items[k].push((x, x / primes[k])); } }
  let mut s = S { m, c, primes, items, f: vec![0; n+1], cnt: vec![0; m], nodes: 0, sols: 0, limit, maxsol, first: None };
  s.cnt[0] = 1;
  let t = std::time::Instant::now(); s.dfs(0);
  println!("n={} m={} c={} sols={} nodes={} complete={} secs={:.1}", n, m, c, s.sols, s.nodes, s.nodes <= limit && s.sols < maxsol, t.elapsed().as_secs_f64());
  if let Some(f) = s.first { println!("first: {:?}", &f[..]); }
}
