# Read-only status of the author and reviewer loops: worktrees, open PRs and recent session activity.
#   .\tools\agent-status.ps1              # last 8 actions per agent
#   .\tools\agent-status.ps1 -Actions 20
param(
  [string]$Root = 'C:\w',
  [string[]]$Names = @('author', 'reviewer'),
  [int]$Actions = 8,
  [int]$StallGraceMinutes = 15
)
$ErrorActionPreference = 'Continue'
$now = Get-Date

function Short([string]$s, [int]$n) {
  $s = ($s -replace '\s+', ' ').Trim()
  if ($s.Length -gt $n) { $s.Substring(0, $n) + '...' } else { $s }
}

# Last N actions and the latest scheduled wakeup from a Claude Code session log (.jsonl).
function Read-Session([string]$path, [int]$n) {
  $acts = New-Object System.Collections.Generic.List[string]
  $wake = $null
  foreach ($line in [IO.File]::ReadLines($path)) {
    if ($line -notmatch '"type":"assistant"') { continue }
    try { $o = $line | ConvertFrom-Json } catch { continue }
    if (-not $o.message.content) { continue }
    $t = ([datetime]$o.timestamp).ToLocalTime()
    foreach ($c in $o.message.content) {
      if ($c.type -eq 'tool_use') {
        $i = $c.input
        if ($c.name -eq 'ScheduleWakeup' -and $i.delaySeconds) { $wake = $t.AddSeconds([double]$i.delaySeconds) }
        $d = foreach ($k in 'command', 'url', 'file_path', 'skill', 'description', 'prompt', 'query', 'reason') {
          if ($i.$k) { $i.$k; break }
        }
        $acts.Add(('{0:HH:mm}  [{1}] {2}' -f $t, $c.name, (Short "$d" 150)))
      } elseif ($c.type -eq 'text' -and $c.text.Trim()) {
        $acts.Add(('{0:HH:mm}  (says) {1}' -f $t, (Short $c.text 150)))
      }
    }
  }
  [pscustomobject]@{ Actions = @($acts | Select-Object -Last $n); Wake = $wake }
}

foreach ($n in $Names) {
  $wt = Join-Path $Root $n
  Write-Output "=== $n ($wt)"
  if (-not (Test-Path (Join-Path $wt '.git'))) { Write-Output 'no worktree'; continue }

  $branch = "$(git -C $wt branch --show-current)".Trim()
  if (-not $branch) { $branch = "detached at $("$(git -C $wt rev-parse --short HEAD)".Trim())" }
  $ahead = @(git -C $wt log --oneline origin/main..HEAD 2>$null)
  $dirty = @(git -C $wt status --porcelain)
  Write-Output "branch: $branch | commits not on main: $($ahead.Count) | uncommitted files: $($dirty.Count)"

  $logDir = Join-Path $HOME ('.claude\projects\' + (($wt -replace '[:\\/]', '-')))
  $log = Get-ChildItem $logDir -Filter *.jsonl -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  if (-not $log) { Write-Output 'no session log found'; continue }
  $idle = [int]($now - $log.LastWriteTime).TotalMinutes
  $s = Read-Session $log.FullName $Actions
  $state = "last activity $($log.LastWriteTime.ToString('HH:mm')) ($idle min ago)"
  if ($s.Wake) {
    $state += "; next wake $($s.Wake.ToString('HH:mm'))"
    if ($now -gt $s.Wake.AddMinutes($StallGraceMinutes) -and $log.LastWriteTime -lt $s.Wake) {
      $state += "  ** POSSIBLY STUCK: past its wake time with no activity (permission prompt? terminal closed?) **"
    }
  } elseif ($idle -gt 70) {
    $state += '  ** no wakeup scheduled and idle over an hour: loop may have stopped **'
  }
  Write-Output $state
  $s.Actions | ForEach-Object { "  $_" }
}

Write-Output '=== open pull requests'
$prs = gh pr list --state open --json number,title,headRefName,headRefOid 2>$null | ConvertFrom-Json
if (-not $prs) { Write-Output 'none' }
foreach ($p in $prs) {
  $checks = gh pr checks $p.number 2>$null | ForEach-Object { ($_ -split "`t")[1] }
  $ci = if ($checks -contains 'fail') { 'CI failing' } elseif ($checks -contains 'pending') { 'CI running' } elseif ($checks -contains 'pass') { 'CI passed' } else { 'CI not reported' }
  $comments = (gh pr view $p.number --json comments 2>$null | ConvertFrom-Json).comments
  $marker = "reviewer-loop sha=$($p.headRefOid)"
  $reviewed = @($comments | Where-Object { $_.body -match [regex]::Escape($marker) })
  $rev = if ($reviewed) {
    $v = ($reviewed[-1].body -split "`n" | Where-Object { $_ -match 'blocking findings' } | Select-Object -First 1)
    'reviewed: ' + (Short "$v" 60)
  } else { 'not yet reviewed at latest commit' }
  Write-Output ("#{0} {1} [{2}] | {3} | {4}" -f $p.number, (Short $p.title 60), $p.headRefName, $ci, $rev)
}
