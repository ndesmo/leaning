# Check that every Lean name a proof page cites exists as a theorem, lemma or def, either in the
# project's Lean sources or in Mathlib. A cited name is any <code>...</code> on a page under docs/
# that looks like a Lean identifier with an underscore (e.g. fact_b, L1_lt_Lcl). Mathlib names
# are looked up in halfline_lt/.lake/packages/mathlib, which exists after `lake build`; deprecated
# aliases do not count, so pages cite current names. Exit code 0 only if all exist.
# -DocsDir checks pages in another folder (for testing); the default is the repo's docs/.
param([string]$DocsDir)
$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent
if (-not $DocsDir) { $DocsDir = Join-Path $root 'docs' }
$proj = Join-Path $root 'halfline_lt'
$declRe = '(?m)^(?:@\[[^\]\r\n]*\]\s*)?(?:(?:private|protected|noncomputable|nonrec)\s+)*(?:theorem|lemma|def|abbrev)\s+([^\s(:{\[]+)'

function Get-Declared([string[]]$dirs) {
  $set = @{}
  foreach ($dir in $dirs) {
    if (-not (Test-Path $dir)) { continue }
    foreach ($f in Get-ChildItem $dir -Recurse -Filter *.lean) {
      $text = [IO.File]::ReadAllText($f.FullName)
      foreach ($m in [regex]::Matches($text, $declRe)) {
        $name = $m.Groups[1].Value
        $set[$name] = $true
        # Pages cite the last component of a dotted name (Nat.Prime.foo is cited as foo).
        $set[($name -split '\.')[-1]] = $true
      }
    }
  }
  return $set
}

$declared = Get-Declared @((Join-Path $proj 'HalflineLt'), (Join-Path $proj 'Proofs'))

$cited = @()
$docsFull = (Resolve-Path $DocsDir).Path.TrimEnd('\', '/')
foreach ($page in Get-ChildItem $docsFull -Recurse -Filter *.html) {
  $html = [IO.File]::ReadAllText($page.FullName)
  $rel = 'docs/' + ($page.FullName.Substring($docsFull.Length + 1) -replace '\\', '/')
  $names = [regex]::Matches($html, '<code>([A-Za-z][A-Za-z0-9_'']*_[A-Za-z0-9_'']*)</code>') |
    ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
  foreach ($n in $names) { $cited += [pscustomobject]@{ Page = $rel; Name = $n } }
}

$notLocal = @($cited | Where-Object { -not $declared.ContainsKey($_.Name) })
$mathlibDir = Join-Path $proj '.lake/packages/mathlib/Mathlib'
$mathlib = @{}
if ($notLocal.Count -gt 0) {
  if (Test-Path $mathlibDir) {
    $mathlib = Get-Declared @($mathlibDir)
  } else {
    Write-Output "NOTE Mathlib sources not found at $mathlibDir; run lake build first. Mathlib names count as missing."
  }
}

$missing = @()
foreach ($c in $notLocal) {
  if ($mathlib.ContainsKey($c.Name)) { Write-Output "MATHLIB $($c.Page): $($c.Name)" }
  else { $missing += "$($c.Page): $($c.Name)" }
}
$missing | ForEach-Object { Write-Output "MISSING $_" }
Write-Output ("{0}: {1} cited names checked, {2} from Mathlib, {3} missing, {4} project declarations known" -f `
  $(if ($missing.Count -eq 0) { 'CLEAN' } else { 'PROBLEMS' }), $cited.Count, ($notLocal.Count - $missing.Count),
  $missing.Count, $declared.Count)
if ($missing.Count -eq 0) { exit 0 } else { exit 1 }
