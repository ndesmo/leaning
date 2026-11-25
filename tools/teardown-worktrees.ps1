# Remove the loop worktrees, refusing whenever work could be lost. Never forces anything.
# Stop the loop terminals first.
#   .\tools\teardown-worktrees.ps1                   # C:\w\author and C:\w\reviewer
#   .\tools\teardown-worktrees.ps1 -Names reviewer   # just one
param(
  [string]$Root = 'C:\w',
  [string[]]$Names = @('author', 'reviewer')
)
$ErrorActionPreference = 'Stop'
$main = (git rev-parse --show-toplevel).Trim()
git -C $main fetch -q origin

$refused = @()
foreach ($n in $Names) {
  $wt = Join-Path $Root $n
  if (-not (Test-Path (Join-Path $wt '.git'))) { Write-Output "== ${wt}: not a worktree, skipping"; continue }
  Write-Output "== $wt"

  $dirty = git -C $wt status --porcelain
  if ($dirty) {
    Write-Output 'REFUSED: uncommitted changes:'; $dirty | ForEach-Object { "  $_" }
    $refused += $wt; continue
  }
  $branch = "$(git -C $wt branch --show-current)".Trim()   # empty for a detached worktree
  if ($branch) {
    $unpushed = git -C $wt log --oneline "$branch" --not --remotes
    if ($unpushed) {
      Write-Output "REFUSED: branch $branch has commits on no remote:"; $unpushed | ForEach-Object { "  $_" }
      $refused += $wt; continue
    }
  }

  # Ignored files (the 7 GB .lake cache) are removed with the worktree; tracked work is safe above.
  git -C $main worktree remove $wt
  if ($LASTEXITCODE -ne 0) { Write-Output "REFUSED by git: see message above"; $refused += $wt; continue }
  Write-Output 'removed'
}

git -C $main worktree prune
# Local agent branches already merged into main are safe to delete; others are kept.
git -C $main branch --merged origin/main --list 'agent/*' | ForEach-Object {
  $b = $_.Trim(' ', '*', '+'); if ($b) { git -C $main branch -d $b }
}
$kept = git -C $main branch --no-merged origin/main --list 'agent/*'
if ($kept) { Write-Output 'Kept (not merged into main):'; $kept | ForEach-Object { "  $($_.Trim())" } }

git -C $main worktree list
if ($refused.Count -gt 0) { Write-Output "Refused: $($refused -join ', ')"; exit 1 }
exit 0
