def main : IO Unit := do
  let ts ← (List.range 4).mapM fun i => IO.asTask (pure (i * i))
  let rs ← ts.mapM fun t => IO.ofExcept t.get
  IO.println s!"search target ok; parallel tasks returned {rs}"
