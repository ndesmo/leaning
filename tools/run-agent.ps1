# Run one agent loop in its worktree (one terminal tab). Called by start-agents.ps1.
#   .\tools\run-agent.ps1 -Role author
param(
  [Parameter(Mandatory = $true)][ValidateSet('author', 'reviewer')][string]$Role,
  [string]$Root = 'C:\w',
  [string]$Model = 'claude-opus-5-5'
)
$wt = Join-Path $Root $Role
if (-not (Test-Path (Join-Path $wt '.git'))) {
  Write-Output "No worktree at $wt. Run tools\setup-worktrees.ps1 first."
  return
}
Set-Location $wt
$Host.UI.RawUI.WindowTitle = $Role

# Start from the latest main, so the loop loads current instructions. Leave the worktree alone if
# it has local changes; the loop's preflight handles unfinished work from a previous run.
git fetch -q origin
if (-not (git status --porcelain)) {
  git checkout -q --detach origin/main
  Write-Output "$Role worktree at $(git log --oneline -1)"
} else {
  Write-Output "$Role worktree has local changes; not switching to main."
}

& claude --model $Model --name $Role "/loop /$Role-loop"
