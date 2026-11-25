# Create (or repair) the worktrees the author and reviewer loops run in. Safe to rerun: each step
# is skipped when already done. Run from anywhere inside the main checkout.
#   .\tools\setup-worktrees.ps1                      # C:\w\author and C:\w\reviewer
#   .\tools\setup-worktrees.ps1 -Names author        # just one
param(
  [string]$Root = 'C:\w',                  # keep short: long paths are disabled on this machine
  [string[]]$Names = @('author', 'reviewer')
)
$ErrorActionPreference = 'Stop'
$elanBin = Join-Path (Join-Path $HOME '.elan') 'bin'
if (Test-Path $elanBin) { $env:PATH = $elanBin + [IO.Path]::PathSeparator + $env:PATH }

$main = (git rev-parse --show-toplevel).Trim()
$mainPackages = Join-Path $main 'halfline_lt\.lake\packages'
git -C $main fetch -q origin
New-Item -ItemType Directory -Force $Root | Out-Null

foreach ($n in $Names) {
  $wt = Join-Path $Root $n
  Write-Output "== $wt"
  if (-not (Test-Path (Join-Path $wt '.git'))) {
    git -C $main worktree add --detach $wt origin/main
  } else {
    Write-Output 'worktree exists'
  }

  $pkgs = Join-Path $wt 'halfline_lt\.lake\packages'
  if (-not (Test-Path (Join-Path $pkgs 'mathlib'))) {
    if (Test-Path (Join-Path $mainPackages 'mathlib')) {
      Write-Output 'copying the Lean package cache from the main checkout (about 7 GB)'
      robocopy $mainPackages $pkgs /E /MT:16 /NFL /NDL /NJH /NJS /NP | Out-Null
      if ($LASTEXITCODE -ge 8) { throw "robocopy failed with exit code $LASTEXITCODE" }
    } else {
      Write-Output 'downloading the Mathlib cache'
      Push-Location (Join-Path $wt 'halfline_lt'); try { lake exe cache get } finally { Pop-Location }
    }
  } else {
    Write-Output 'package cache present'
  }

  Push-Location (Join-Path $wt 'halfline_lt')
  try {
    lake build 2>&1 | Select-String 'Build completed|error' | Select-Object -Last 1 | ForEach-Object { $_.Line }
    if ($LASTEXITCODE -ne 0) { throw "lake build failed in $wt" }
  } finally { Pop-Location }
}
git -C $main worktree list
