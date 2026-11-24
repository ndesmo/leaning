import HalflineNum.Basic

/-!
# Nelder–Mead maximisation
-/

namespace HalflineNum

/-- Maximise `f` from `x0` (initial simplex step `step`) with at most about `maxEval`
evaluations. Returns the best point and its value. -/
def nelderMead (f : Array Float → Float) (x0 : Array Float) (step : Float)
    (maxEval : Nat) : Array Float × Float := Id.run do
  let n := x0.size
  let g := fun x => -(f x)
  let mut pts : Array (Array Float) := #[x0]
  for i in [0:n] do
    pts := pts.push (x0.set! i (x0[i]! + step))
  let mut vals : Array Float := pts.map g
  let mut evals := n + 1
  while evals < maxEval do
    let order := (Array.range (n + 1)).qsort (fun a b => vals[a]! < vals[b]!)
    pts := order.map (pts[·]!)
    vals := order.map (vals[·]!)
    if vals[n]! - vals[0]! ≤ 1e-13 * (Float.abs vals[0]! + 1e-13) then break
    let mut c := Array.replicate n 0.0
    for j in [0:n] do
      for i in [0:n] do
        c := c.set! i (c[i]! + pts[j]![i]! / n.toFloat)
    let worst := pts[n]!
    let refl := lin c worst (-1.0)
    let fr := g refl
    evals := evals + 1
    if fr < vals[0]! then
      let ex := lin c worst (-2.0)
      let fe := g ex
      evals := evals + 1
      if fe < fr then
        pts := pts.set! n ex
        vals := vals.set! n fe
      else
        pts := pts.set! n refl
        vals := vals.set! n fr
    else if fr < vals[n - 1]! then
      pts := pts.set! n refl
      vals := vals.set! n fr
    else
      let outside := fr < vals[n]!
      let cp := if outside then lin c refl 0.5 else lin c worst 0.5
      let fc := g cp
      evals := evals + 1
      if fc < (if outside then fr else vals[n]!) then
        pts := pts.set! n cp
        vals := vals.set! n fc
      else
        let best := pts[0]!
        for j in [1:n + 1] do
          let p := lin best pts[j]! 0.5
          pts := pts.set! j p
          vals := vals.set! j (g p)
        evals := evals + n
  let mut bi := 0
  for j in [1:n + 1] do
    if vals[j]! < vals[bi]! then bi := j
  return (pts[bi]!, -vals[bi]!)

end HalflineNum
