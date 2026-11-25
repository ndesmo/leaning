# Check that every Lean name a proof page cites exists as a theorem, lemma or def in the Lean
# sources. A cited name is any <code>…</code> on a page under docs/ that looks like a Lean
# identifier with an underscore (e.g. fact_b, L1_lt_Lcl). Exit code 0 only if all exist.
$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent
$proj = Join-Path $root 'halfline_lt'

$declared = @{}
foreach ($lib in 'HalflineLt', 'Proofs') {
  $dir = Join-Path $proj $lib
  if (-not (Test-Path $dir)) { continue }
  foreach ($f in Get-ChildItem $dir -Recurse -Filter *.lean) {
    $text = [IO.File]::ReadAllText($f.FullName)
    foreach ($m in [regex]::Matches($text, '(?m)^(?:private\s+|noncomputable\s+)*(?:theorem|lemma|def|abbrev)\s+([^\s(:{\[]+)')) {
      $declared[$m.Groups[1].Value] = $true
    }
  }
}

$missing = @()
$checked = 0
foreach ($page in Get-ChildItem (Join-Path $root 'docs') -Recurse -Filter *.html) {
  $html = [IO.File]::ReadAllText($page.FullName)
  $rel = $page.FullName.Substring($root.Length + 1) -replace '\\', '/'
  $names = [regex]::Matches($html, '<code>([A-Za-z][A-Za-z0-9_'']*_[A-Za-z0-9_'']*)</code>') |
    ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique
  foreach ($n in $names) {
    $checked++
    if (-not $declared.ContainsKey($n)) { $missing += "${rel}: $n" }
  }
}
$missing | ForEach-Object { Write-Output "MISSING $_" }
Write-Output ("{0}: {1} cited names checked, {2} missing, {3} Lean declarations known" -f `
  $(if ($missing.Count -eq 0) { 'CLEAN' } else { 'PROBLEMS' }), $checked, $missing.Count, $declared.Count)
if ($missing.Count -eq 0) { exit 0 } else { exit 1 }
