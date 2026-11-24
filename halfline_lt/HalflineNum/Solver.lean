import HalflineNum.Basic

/-!
# Neumann half-line eigenvalues by finite differences

`-u'' - V u = E u` on `(0, L)` with `u'(0) = 0` and `u(L) = 0`. Cell-centred grid
`x_i = (i + 1/2) h`, `h = L / n`; ghost values `u_{-1} = u_0` (Neumann) and `u_n = -u_{n-1}`
(Dirichlet at the face `x = L`), both second order. The matrix is symmetric tridiagonal with
off-diagonal `-1/h²`; its negative eigenvalues come from Sturm counts and bisection.
-/

namespace HalflineNum

structure Grid where
  L : Float
  n : Nat

def Grid.h (g : Grid) : Float := g.L / g.n.toFloat

/-- Number of eigenvalues below `lam`: the negative pivots of `LDLᵀ` for `T - lam`.
Written as a tail-recursive loop so the compiled code keeps `q` unboxed. -/
def sturmCount (diag : FloatArray) (off2 lam : Float) : Nat :=
  if 0 < diag.size then
    let q := diag[0]! - lam
    go 1 q (if q < c0 then 1 else 0)
  else 0
where
  go (i : Nat) (q : Float) (cnt : Nat) : Nat :=
    if h : i < diag.size then
      let q' := (diag[i] - lam) - off2 / (if Float.abs q < cTiny then -cTiny else q)
      go (i + 1) q' (if q' < c0 then cnt + 1 else cnt)
    else cnt
  termination_by diag.size - i

/-- All negative eigenvalues in increasing order, to relative tolerance `tol`.
`lo` must lie below the spectrum. -/
def negEigs (diag : FloatArray) (off2 lo tol : Float) : Array Float := Id.run do
  let n := sturmCount diag off2 c0
  let mut out : Array Float := #[]
  for k in [0:n] do
    let mut a := if k == 0 then lo else out[k - 1]!
    let mut b := c0
    for _ in [0:200] do
      if b - a ≤ tol * (c1 + Float.abs a) then break
      let m := cHalf * (a + b)
      if m == a || m == b then break
      if sturmCount diag off2 m > k then b := m else a := m
    out := out.push (cHalf * (a + b))
  return out

/-- One potential, evaluated on one grid. Ratios are in units of `2 L1(γ)`. -/
structure Eval where
  ratio : Float
  eff : Float
  eigs : Array Float
  mass : Float

def Eval.nBound (e : Eval) : Nat := e.eigs.size

def sample (g : Grid) (V : Float → Float) : FloatArray := Id.run do
  let h := g.h
  let mut vs := FloatArray.emptyWithCapacity g.n
  for i in [0:g.n] do
    vs := vs.push (V ((i.toFloat + cHalf) * h))
  return vs

/-- `R / (2 L1(γ))` with `R = Σ |E_j|^γ / ∫₀^L V^{γ+1/2}` (midpoint rule), and the
ground-state efficiency `|E₀|^γ / (2 L1(γ) M)`. -/
def evalPot (γ : Float) (g : Grid) (V : Float → Float) (tol : Float) : Eval := Id.run do
  let vs := sample g V
  let h := g.h
  let h2 := c1 / (h * h)
  let p := γ + cHalf
  let mut diag := FloatArray.emptyWithCapacity g.n
  let mut vmax := c0
  let mut mass := c0
  for i in [0:g.n] do
    let v := vs[i]!
    if v > vmax then vmax := v
    mass := mass + Float.pow v p
    let base := if i == 0 then h2 else if i + 1 == g.n then c3 * h2 else c2 * h2
    diag := diag.push (base - v)
  mass := mass * h
  let es := negEigs diag (h2 * h2) (-vmax - c1) tol
  let twoL1 := c2 * L1 γ
  if mass ≤ c0 || es.size == 0 then
    return { ratio := c0, eff := c0, eigs := es, mass := mass }
  let mut s := c0
  for e in es do
    s := s + Float.pow (-e) γ
  return { ratio := s / (mass * twoL1), eff := Float.pow (-es[0]!) γ / (mass * twoL1),
           eigs := es, mass := mass }

/-- Richardson extrapolation over the grids `n`, `2n`, `4n` on `[0, L]`. -/
structure Refined where
  value : Float
  hErr : Float
  order : Float
  sameCount : Bool
  /-- Richardson-extrapolated ground-state efficiency. -/
  eff : Float
  fine : Eval

def refine (γ L : Float) (n : Nat) (V : Float → Float) : Refined :=
  let e1 := evalPot γ ⟨L, n⟩ V 1e-14
  let e2 := evalPot γ ⟨L, 2 * n⟩ V 1e-14
  let e4 := evalPot γ ⟨L, 4 * n⟩ V 1e-14
  let r12 := e2.ratio + (e2.ratio - e1.ratio) / 3.0
  let r24 := e4.ratio + (e4.ratio - e2.ratio) / 3.0
  { value := r24
    hErr := Float.abs (r24 - r12)
    order := Float.log ((e1.ratio - e2.ratio) / (e2.ratio - e4.ratio)) / Float.log 2.0
    sameCount := e1.nBound == e2.nBound && e2.nBound == e4.nBound
    eff := e4.eff + (e4.eff - e2.eff) / 3.0
    fine := e4 }

end HalflineNum
