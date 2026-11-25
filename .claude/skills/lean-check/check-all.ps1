# Run check.ps1 on every Lean file that holds proofs (halfline_lt/HalflineLt and halfline_lt/Proofs).
# Exit code 0 only if every file is clean.
$ErrorActionPreference = 'Stop'
$root = Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent
$proj = Join-Path $root 'halfline_lt'
$check = Join-Path $PSScriptRoot 'check.ps1'

$files = foreach ($lib in 'HalflineLt', 'Proofs') {
  $dir = Join-Path $proj $lib
  if (Test-Path $dir) { Get-ChildItem $dir -Recurse -Filter *.lean | Sort-Object FullName }
}
if (-not $files) { Write-Output 'No proof files found.'; exit 1 }

$failed = @()
foreach ($f in $files) {
  $rel = $f.FullName.Substring($proj.Length + 1) -replace '\\', '/'
  Write-Output "== $rel"
  & $check -File $rel
  if ($LASTEXITCODE -ne 0) { $failed += $rel }
}
if ($failed.Count -gt 0) { Write-Output "FAILED: $($failed -join ', ')"; exit 1 }
Write-Output "ALL CLEAN: $(@($files).Count) files"
exit 0
