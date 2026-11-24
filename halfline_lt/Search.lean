import HalflineNum

/-!
# `search`: numerics for the Neumann half-line Lieb–Thirring ratio

Run from the folder that should receive `results/`:
* `search validate` checks the solver against exact Pöschl–Teller levels and soliton ratios;
* `search sech2` finds the best centred `ν(ν+1) sech²` for each γ (closed form, FD check);
* `search run <bump|twoWell|expansion|dressed> <starts> <seed> [minBound]` runs Nelder–Mead from
  random starts in parallel, then refines the best candidate for each γ; `minBound = 2`
  restricts the search to potentials with at least two Neumann bound states;
* `search check <family> <gamma> <p1;p2;...>` refines one parameter vector and appends it to
  `results/checks.csv`;
* `search bench` times the solver.

All numbers here are `Float` computations: evidence, not proof.
-/

open HalflineNum

/-- The exponents of Task 2, with sanity checks at γ = 1 and γ = 3/2. -/
def gammas : Array Float := #[1.0, 1.5, 1.75, 2.0, 2.25, 2.4, 2.5, 2.6, 3.0]

def sech (x : Float) : Float := c1 / Float.cosh x

def clamp (x lo hi : Float) : Float := if x < lo then lo else if x > hi then hi else x

/-- Pöschl–Teller potential `ν(ν+1) sech²(x)`. -/
def pt (ν : Float) : Float → Float :=
  let a := ν * (ν + 1.0)
  fun x => let s := sech x; a * s * s

/-- Exact Neumann levels of `pt ν`: `-(ν-k)²` for even `k < ν`. -/
def ptNeumannLevels (ν : Float) : Array Float := Id.run do
  let mut out : Array Float := #[]
  let mut k := 0.0
  while k < ν do
    out := out.push (-((ν - k) * (ν - k)))
    k := k + 2.0
  return out

/-- `R / (2 L1)` for `ν(ν+1) sech²` in closed form (the sech integral cancels). -/
def sech2Ratio (γ ν : Float) : Float := Id.run do
  let mut s := 0.0
  for e in ptNeumannLevels ν do
    s := s + Float.pow (-e) γ
  let num := s / Float.pow (ν * (ν + 1.0)) (γ + 0.5)
  let den := Float.pow (γ - 0.5) (γ - 0.5) / Float.pow (γ + 0.5) (γ + 0.5)
  return num / den

/-- Best `ν` for `sech2Ratio γ`: scan `(0, 12]` in steps of 1e-3, then golden section. -/
def bestSech2 (γ : Float) : Float × Float := Id.run do
  let mut bestν := 0.001
  let mut bestR := sech2Ratio γ 0.001
  for i in [2:12001] do
    let ν := i.toFloat * 0.001
    let v := sech2Ratio γ ν
    if v > bestR then
      bestR := v
      bestν := ν
  let mut a := bestν - 0.001
  let mut b := bestν + 0.001
  for _ in [0:80] do
    let c := b - 0.6180339887498949 * (b - a)
    let d := a + 0.6180339887498949 * (b - a)
    if sech2Ratio γ c > sech2Ratio γ d then b := d else a := c
  let ν := 0.5 * (a + b)
  return (ν, sech2Ratio γ ν)

/-! Each family decodes its parameters once and returns a closure over the decoded values. -/

/-- `e^a sech²(x - c)`: one bump, possibly off-centre. -/
def bump (p : Array Float) : Float → Float :=
  let A := Float.exp (clamp p[0]! (-6.0) 5.0)
  let c := clamp p[1]! (-6.0) 12.0
  fun x => let s := sech (x - c); A * s * s

/-- `e^{a₁} sech²(x) + e^{a₂} sech²((x - c) / e^w)`: a well at the wall plus a second well. -/
def twoWell (p : Array Float) : Float → Float :=
  let A1 := Float.exp (clamp p[0]! (-6.0) 5.0)
  let A2 := Float.exp (clamp p[1]! (-6.0) 5.0)
  let w := Float.exp (clamp p[2]! (-1.5) 1.5)
  let c := clamp p[3]! 0.0 15.0
  fun x =>
    let s1 := sech x
    let s2 := sech ((x - c) / w)
    A1 * s1 * s1 + A2 * s2 * s2

/-- `(Σ_k c_k exp(-(x - 0.75 k)² / 0.72))²`: a smooth expansion in Gaussians of width 0.6. -/
def expansion (p : Array Float) : Float → Float :=
  let cs := p.map (clamp · (-15.0) 15.0)
  let centres := (Array.range p.size).map (0.75 * ·.toFloat)
  let inv := 1.0 / 0.72
  fun x => Id.run do
    let mut s := c0
    for k in [0:cs.size] do
      let d := x - centres[k]!
      s := s + cs[k]! * Float.exp (-(d * d) * inv)
    return s * s

/-- `e^a sech²(x) · exp(Σ_k c_k exp(-(x - 0.75 k)² / 0.72))`: the half-soliton times a smooth
positive perturbation; `c = 0` is exactly the soliton. -/
def dressed (p : Array Float) : Float → Float :=
  let A := Float.exp (clamp p[0]! (-6.0) 5.0)
  let cs := (p.extract 1 p.size).map (clamp · (-4.0) 4.0)
  let centres := (Array.range cs.size).map (0.75 * ·.toFloat)
  let inv := 1.0 / 0.72
  fun x => Id.run do
    let mut s := c0
    for k in [0:cs.size] do
      let d := x - centres[k]!
      s := s + cs[k]! * Float.exp (-(d * d) * inv)
    let sh := sech x
    return A * sh * sh * Float.exp s

def potFor (fam : String) (p : Array Float) : Float → Float :=
  match fam with
  | "bump" => bump p
  | "twoWell" => twoWell p
  | "dressed" => dressed p
  | _ => expansion p

/-- Random starting point for a family, determined by the seed. `dressed` starts near the
half-soliton for this γ. -/
def initFor (fam : String) (γ : Float) (seed : Nat) : Array Float := Id.run do
  let a0 := Float.log (γ * γ - 0.25)
  let ranges : Array (Float × Float) := match fam with
    | "bump" => #[(-1.0, 3.0), (-2.0, 6.0)]
    | "twoWell" => #[(-1.0, 3.0), (-2.0, 3.0), (-1.0, 1.0), (0.0, 8.0)]
    | "dressed" => #[(a0 - 0.5, a0 + 0.5)] ++ Array.replicate 8 (-1.0, 1.0)
    | _ => Array.replicate 8 (-3.0, 3.0)
  let mut g : Rng := ⟨seed.toUInt64⟩
  let mut x : Array Float := #[]
  for (lo, hi) in ranges do
    let (u, g') := g.range lo hi
    x := x.push u
    g := g'
  return x

def maxEvalFor (fam : String) : Nat :=
  match fam with
  | "bump" => 300
  | "twoWell" => 1200
  | "dressed" => 4000
  | _ => 3000

/-- Search objective: the Richardson value from grids `h = 0.03` and `h = 0.015`, minus a penalty
on their difference. A single coarse grid was exploited: the optimiser drifted to narrow,
under-resolved potentials whose grid error inflated the ratio by up to 3e-3. -/
def objective (fam : String) (γ : Float) (minBound : Nat) (p : Array Float) : Float :=
  let V := potFor fam p
  let e1 := evalPot γ ⟨30.0, 1000⟩ V 1e-9
  let e2 := evalPot γ ⟨30.0, 2000⟩ V 1e-9
  let r := e2.ratio + (e2.ratio - e1.ratio) / 3.0 - 5.0 * Float.abs (e2.ratio - e1.ratio)
  -- With one Neumann bound state, R ≤ 2 L1 holds by the one-bound-state bound, so a
  -- counterexample needs at least two; `minBound = 2` restricts the search to those.
  if e2.nBound < minBound then r - 1.0 else r

def runStart (fam : String) (γ : Float) (minBound seed : Nat) : Array Float × Float :=
  nelderMead (objective fam γ minBound) (initFor fam γ seed) 0.5 (maxEvalFor fam)

/-- A candidate refined on two boxes; `err` adds the Richardson and box differences. -/
structure Verified where
  value : Float
  err : Float
  order : Float
  boxDiff : Float
  sameCount : Bool
  nBound : Nat
  eff : Float

def verify (γ : Float) (V : Float → Float) : Verified :=
  let a := refine γ 30.0 1500 V
  let b := refine γ 45.0 2250 V
  let boxDiff := Float.abs (b.value - a.value)
  { value := b.value, err := a.hErr + b.hErr + boxDiff, order := b.order, boxDiff := boxDiff
    sameCount := a.sameCount && b.sameCount && a.fine.nBound == b.fine.nBound
    nBound := b.fine.nBound, eff := b.eff }

/-- Upper bound on `R / (2 L1)` that must hold: `(Lcl + L1)/(2 L1)` for γ ≥ 3/2 (ELU (1.6) plus
the one-bound-state bound) and `L_1 = L1(1)` at γ = 1 (Read–Schulz); no check otherwise. -/
def knownBound (γ : Float) : Float :=
  if γ ≥ 1.5 then (1.0 + 1.0 / rOf γ) / 2.0 else if γ == 1.0 then 1.0 else 1.0 / 0.0

def writeCsv (path : String) (lines : Array String) : IO Unit :=
  IO.FS.writeFile path (String.intercalate "\n" lines.toList ++ "\n")

def checkHeader : String :=
  "ratio,err,observed_order,box_diff,same_count,n_bound,eff,eff_threshold,known_bound," ++
    "bound_ok,beats,params"

/-- Refine a candidate and format the checks as the CSV fields of `checkHeader`. -/
def checkFields (fam : String) (γ : Float) (p : Array Float) : String :=
  let vf := verify γ (potFor fam p)
  let thr := if γ ≥ 1.5 then 2.0 - 1.0 / rOf γ else 0.0
  let kb := knownBound γ
  let boundOk := decide (vf.value ≤ kb + vf.err)
  let beats := vf.sameCount && vf.value - 1.0 > 10.0 * vf.err
  s!"{fmtFixed vf.value 9},{fmtSci vf.err 2},{fmtFixed vf.order 3},{fmtSci vf.boxDiff 2}," ++
    s!"{vf.sameCount},{vf.nBound},{fmtFixed vf.eff 6},{fmtFixed thr 6},{fmtFixed kb 6}," ++
    s!"{boundOk},{beats},{fmtParams p}"

/-- Parse a decimal such as `-5.786609` (no exponent). -/
def parseDecimal (s : String) : Option Float :=
  let (sign, body) := if s.startsWith "-" then (-1.0, String.ofList (s.toList.drop 1))
    else (1.0, s)
  match body.splitOn "." with
  | [i] => do
    let n ← i.toNat?
    pure (sign * n.toFloat)
  | [i, f] => do
    let n ← i.toNat?
    let m ← f.toNat?
    pure (sign * (n.toFloat + m.toFloat / Float.pow 10.0 f.length.toFloat))
  | _ => none

def validate (out : String) : IO Unit := do
  let mut lines : Array String :=
    #["test,param,index,exact,computed,rel_err,observed_order,L,n_finest"]
  let consts : Array (String × Float × Float) := #[
    ("lgamma(1/2)", lgamma 0.5, Float.log (Float.sqrt pi)),
    ("lgamma(5)", lgamma 5.0, Float.log 24.0),
    ("2L1(1)", 2.0 * L1 1.0, 8.0 / (3.0 * Float.sqrt 3.0 * pi)),
    ("2L1(2)", 2.0 * L1 2.0, 32.0 / (15.0 * pi) * Float.pow 0.6 1.5),
    ("L1(3/2)", L1 1.5, 3.0 / 16.0),
    ("Lcl(3/2)", Lcl 1.5, 3.0 / 16.0),
    ("r(5/2)", rOf 2.5, 8.0 / 9.0)]
  for (name, got, exact) in consts do
    let rel := Float.abs ((got - exact) / exact)
    lines := lines.push s!"constant,{name},0,{fmtSci exact 12},{fmtSci got 12},{fmtSci rel 2},,,"
  for ν in #[0.75, 1.5, 2.5, 4.5] do
    let exact := ptNeumannLevels ν
    let ev := fun (n : Nat) => (evalPot 1.0 ⟨40.0, n⟩ (pt ν) 1e-14).eigs
    let e1 := ev 4000
    let e2 := ev 8000
    let e4 := ev 16000
    if e1.size != exact.size || e2.size != exact.size || e4.size != exact.size then
      IO.println s!"level count mismatch at nu = {ν}: {e1.size}, {e2.size}, {e4.size}"
      continue
    for k in [0:exact.size] do
      let x := e4[k]! + (e4[k]! - e2[k]!) / 3.0
      let rel := Float.abs ((x - exact[k]!) / exact[k]!)
      let p := Float.log ((e1[k]! - e2[k]!) / (e2[k]! - e4[k]!)) / Float.log 2.0
      lines := lines.push (s!"pt_level,{fmtFixed ν 2},{2 * k},{fmtSci exact[k]! 12}," ++
        s!"{fmtSci x 12},{fmtSci rel 2},{fmtFixed p 3},40,16000")
  for γ in #[0.75, 1.0, 1.5, 2.0, 2.5, 3.0] do
    let rf := refine γ 40.0 4000 (pt (γ - 0.5))
    let exact := sech2Ratio γ (γ - 0.5)
    let rel := Float.abs ((rf.value - exact) / exact)
    lines := lines.push (s!"soliton_ratio,{fmtFixed γ 2},0,{fmtSci exact 12}," ++
      s!"{fmtSci rf.value 12},{fmtSci rel 2},{fmtFixed rf.order 3},40,16000")
  writeCsv s!"{out}/validation.csv" lines
  for l in lines do IO.println l

def sech2 (out : String) : IO Unit := do
  let mut lines : Array String :=
    #["gamma,best_nu,ratio_closed_form,ratio_fd,fd_err,n_bound,observed_order"]
  for γ in gammas do
    let (ν, rcf) := bestSech2 γ
    let rf := refine γ 40.0 4000 (pt ν)
    lines := lines.push (s!"{fmtFixed γ 2},{fmtFixed ν 6},{fmtFixed rcf 9}," ++
      s!"{fmtFixed rf.value 9},{fmtSci rf.hErr 2},{rf.fine.nBound},{fmtFixed rf.order 3}")
  writeCsv s!"{out}/sech2_family.csv" lines
  for l in lines do IO.println l

def run (out fam : String) (starts seed minBound : Nat) : IO Unit := do
  let t0 ← IO.monoMsNow
  let tag := if minBound > 1 then s!"{fam}_min{minBound}" else fam
  let mut tasks : Array (Array (Nat × Task (Array Float × Float))) := #[]
  for gi in [0:gammas.size] do
    let γ := gammas[gi]!
    let mut row := #[]
    for s in [0:starts] do
      let sd := seed + 1000 * gi + s
      row := row.push (sd, Task.spawn fun _ => runStart fam γ minBound sd)
    tasks := tasks.push row
  let mut all : Array String := #["gamma,seed,objective,params"]
  let mut ver : Array String := #["gamma,family,seed," ++ checkHeader]
  for gi in [0:gammas.size] do
    let γ := gammas[gi]!
    let mut best : Nat × Array Float × Float := (0, #[], -1.0)
    for (sd, t) in tasks[gi]! do
      let (p, v) := t.get
      all := all.push s!"{fmtFixed γ 2},{sd},{fmtFixed v 8},{fmtParams p}"
      if v > best.2.2 then best := (sd, p, v)
    let (sd, p, _) := best
    ver := ver.push (s!"{fmtFixed γ 2},{fam},{sd}," ++ checkFields fam γ p)
    IO.println ver.back!
  writeCsv s!"{out}/search_{tag}.csv" all
  writeCsv s!"{out}/verified_{tag}.csv" ver
  let t1 ← IO.monoMsNow
  IO.println s!"{tag}: {starts} starts x {gammas.size} gammas in {(t1 - t0) / 1000} s"

def main (args : List String) : IO UInt32 := do
  let out := "results"
  IO.FS.createDirAll out
  match args with
  | ["validate"] =>
    validate out
    return 0
  | ["sech2"] =>
    sech2 out
    return 0
  | ["bench"] =>
    let g : Grid := ⟨40.0, 16000⟩
    let t0 ← IO.monoNanosNow
    let vs := sample g (pt 4.5)
    let t1 ← IO.monoNanosNow
    let h2 := 1.0 / (g.h * g.h)
    let diag := vs.data.foldl (init := FloatArray.emptyWithCapacity g.n) fun d v => d.push (2.0 * h2 - v)
    let mut c := 0
    for i in [0:100] do
      c := c + sturmCount diag (h2 * h2) (-1.0 - i.toFloat * 0.1)
    let t2 ← IO.monoNanosNow
    let e := evalPot 1.0 g (pt 4.5) 1e-14
    let t3 ← IO.monoNanosNow
    IO.println s!"sample: {(t1 - t0) / 1000} us; 100 sturm counts: {(t2 - t1) / 1000} us (c={c})"
    IO.println s!"evalPot n=16000: {(t3 - t2) / 1000000} ms, {e.eigs.size} eigenvalues"
    return 0
  | ["check", fam, g, ps] =>
    match parseDecimal g, (ps.splitOn ";").mapM parseDecimal with
    | some γ, some p =>
      let line := s!"{fmtFixed γ 2},{fam}," ++ checkFields fam γ p.toArray
      let path := s!"{out}/checks.csv"
      let fresh := !(← System.FilePath.pathExists path)
      let h ← IO.FS.Handle.mk path .append
      if fresh then h.putStrLn ("gamma,family," ++ checkHeader)
      h.putStrLn line
      IO.println line
      return 0
    | _, _ =>
      IO.eprintln "check: could not parse gamma or parameters"
      return 1
  | "run" :: fam :: starts :: seed :: rest =>
    if !(fam == "bump" || fam == "twoWell" || fam == "expansion" || fam == "dressed") then
      IO.eprintln s!"unknown family {fam}"
      return 1
    let minBound := match rest with
      | [mb] => mb.toNat!
      | _ => 1
    run out fam starts.toNat! seed.toNat! minBound
    return 0
  | _ =>
    IO.eprintln ("usage: search validate | sech2 | bench | check <family> <gamma> <params> | " ++
      "run <bump|twoWell|expansion|dressed> <starts> <seed> [minBound]")
    return 1
