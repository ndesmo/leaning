/-!
# Floating-point helpers

Core Lean only. Everything computed with `Float` is numerical evidence, not proof.
-/

namespace HalflineNum

def pi : Float := 3.141592653589793

/-! The compiler rebuilds a float literal with `Float.ofScientific` at every use, which is slow
inside loops (about 3 µs for `1e-300`). Hot code uses these top-level constants instead. -/

def c0 : Float := 0.0
def cHalf : Float := 0.5
def c1 : Float := 1.0
def c2 : Float := 2.0
def c3 : Float := 3.0
def cTiny : Float := 1e-300

/-- `log Γ(x)` for `x ≥ 1/2` (Lanczos, g = 7, nine terms; relative error about 1e-15). -/
def lgamma (x : Float) : Float := Id.run do
  let coef : Array Float := #[0.99999999999980993, 676.5203681218851, -1259.1392167224028,
    771.32342877765313, -176.61502916214059, 12.507343278686905,
    -0.13857109526572012, 9.9843695780195716e-6, 1.5056327351493116e-7]
  let z := x - 1.0
  let t := z + 7.5
  let mut a := coef[0]!
  for i in [1:9] do
    a := a + coef[i]! / (z + i.toFloat)
  return 0.5 * Float.log (2.0 * pi) + (z + 0.5) * Float.log t - t + Float.log a

/-- One-bound-state constant `L1(γ)`. -/
def L1 (γ : Float) : Float :=
  Float.exp (lgamma (γ + 1.0) - lgamma (γ + 0.5)) / (Float.sqrt pi * (γ + 0.5)) *
    Float.pow ((γ - 0.5) / (γ + 0.5)) (γ - 0.5)

/-- Semiclassical constant `Lcl(γ)`. -/
def Lcl (γ : Float) : Float :=
  Float.exp (lgamma (γ + 1.0) - lgamma (γ + 1.5)) / (2.0 * Float.sqrt pi)

/-- `r(γ) = L1(γ) / Lcl(γ)`. -/
def rOf (γ : Float) : Float := 2.0 * Float.pow ((γ - 0.5) / (γ + 0.5)) (γ - 0.5)

/-- SplitMix64 generator, so every run is reproducible from its seed. -/
structure Rng where
  state : UInt64

def Rng.next (g : Rng) : UInt64 × Rng :=
  let s := g.state + 0x9E3779B97F4A7C15
  let z := (s ^^^ (s >>> 30)) * 0xBF58476D1CE4E5B9
  let z := (z ^^^ (z >>> 27)) * 0x94D049BB133111EB
  (z ^^^ (z >>> 31), ⟨s⟩)

/-- Uniform on `[a, b)`. -/
def Rng.range (g : Rng) (a b : Float) : Float × Rng :=
  let (z, g') := g.next
  (a + (b - a) * ((z >>> 11).toFloat / 9007199254740992.0), g')

/-- `a + s (b - a)`, componentwise. -/
def lin (a b : Array Float) (s : Float) : Array Float := Id.run do
  let mut out := a
  for i in [0:a.size] do
    out := out.set! i (a[i]! + s * (b[i]! - a[i]!))
  return out

/-- Fixed-point decimal with `d` digits after the point (for `|x| < 1e6`). -/
def fmtFixed (x : Float) (d : Nat) : String := Id.run do
  let n := (Float.abs x * Float.pow 10.0 d.toFloat + 0.5).floor.toUInt64.toNat
  let p := 10 ^ d
  let fs := toString (n % p)
  let fs := String.ofList (List.replicate (d - fs.length) '0') ++ fs
  let sign := if x < 0.0 && n != 0 then "-" else ""
  return sign ++ toString (n / p) ++ (if d == 0 then "" else "." ++ fs)

/-- Scientific notation with `d` digits after the point. -/
def fmtSci (x : Float) (d : Nat) : String := Id.run do
  if x == 0.0 then return "0"
  let a := Float.abs x
  let mut e := (Float.log10 a).floor
  let mut m := a / Float.pow 10.0 e
  if m ≥ 10.0 then
    m := m / 10.0
    e := e + 1.0
  if m < 1.0 then
    m := m * 10.0
    e := e - 1.0
  let es := if e < 0.0 then "-" ++ toString (-e).toUInt64 else toString e.toUInt64
  return (if x < 0.0 then "-" else "") ++ fmtFixed m d ++ "e" ++ es

/-- Parameters as a `;`-separated list (one CSV field). -/
def fmtParams (p : Array Float) : String :=
  String.intercalate ";" (p.toList.map (fmtFixed · 6))

end HalflineNum
