# Compile a Lean file from halfline_lt/ with `#print axioms` for every theorem and lemma, then
# report errors, sorry warnings and non-standard axioms. Exit code 0 means clean.
# Runs on Windows PowerShell 5.1 and on pwsh (Linux CI).
param(
  [Parameter(Mandatory = $true)][string]$File,   # path relative to halfline_lt/, e.g. HalflineLt/Spec.lean
  [int]$TimeoutSec = 1500
)
$ErrorActionPreference = 'Stop'
$elanBin = Join-Path (Join-Path $HOME '.elan') 'bin'
if (Test-Path $elanBin) { $env:PATH = $elanBin + [IO.Path]::PathSeparator + $env:PATH }

$root = Split-Path (Split-Path (Split-Path $PSScriptRoot -Parent) -Parent) -Parent
$proj = Join-Path $root 'halfline_lt'
$src = Join-Path $proj ($File -replace '\\', '/')
if (-not (Test-Path $src)) { Write-Output "No such file: $src"; exit 1 }

$text = [System.IO.File]::ReadAllText($src)
$ns = [regex]::Match($text, '(?m)^namespace\s+(\S+)').Groups[1].Value
$prefix = if ($ns) { "$ns." } else { '' }
$names = @([regex]::Matches($text, '(?m)^(?:theorem|lemma)\s+(\S+)') | ForEach-Object { $_.Groups[1].Value })

$tmp = Join-Path ([IO.Path]::GetTempPath()) 'lean-check'
New-Item -ItemType Directory -Force $tmp | Out-Null
$check = Join-Path $tmp 'AxiomCheck.lean'
$tail = ($names | ForEach-Object { "#print axioms $prefix$_" }) -join "`n"
[System.IO.File]::WriteAllText($check, $text + "`n" + $tail + "`n", (New-Object System.Text.UTF8Encoding $false))

$out = Join-Path $tmp 'out.txt'
$err = Join-Path $tmp 'err.txt'
$sw = [Diagnostics.Stopwatch]::StartNew()
Push-Location $proj
try {
  $p = Start-Process -FilePath 'lake' -ArgumentList @('env', 'lean', $check) -NoNewWindow -PassThru `
    -RedirectStandardOutput $out -RedirectStandardError $err
  if (-not $p.WaitForExit($TimeoutSec * 1000)) {
    Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue
    Get-Process lean -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
    Write-Output "Timed out after $TimeoutSec s. If Lean sat at low CPU, see the antivirus note in reference.md."
    exit 1
  }
} finally { Pop-Location }

$lines = @(Get-Content $out, $err -ErrorAction SilentlyContinue)
$standard = 'depends on axioms: \[propext, Classical\.choice, Quot\.sound\]$|does not depend on any axioms'
$errors = @($lines | Where-Object { $_ -match ': error' })
$sorries = @($lines | Where-Object { $_ -match "declaration uses 'sorry'" })
$axiomLines = @($lines | Where-Object { $_ -match 'depends on axioms|does not depend on any axioms' })
$bad = @($axiomLines | Where-Object { $_ -notmatch $standard })

$errors + $sorries + $bad | ForEach-Object { Write-Output $_ }
$ok = ($errors.Count -eq 0) -and ($sorries.Count -eq 0) -and ($bad.Count -eq 0) -and ($axiomLines.Count -eq $names.Count)
Write-Output ("{0}: {1} theorems, {2} with standard axioms only, {3} errors, {4} sorry warnings, {5} s" -f `
  $(if ($ok) { 'CLEAN' } else { 'PROBLEMS' }), $names.Count, ($axiomLines.Count - $bad.Count), $errors.Count,
  $sorries.Count, [int]$sw.Elapsed.TotalSeconds)
if ($ok) { exit 0 } else { exit 1 }
