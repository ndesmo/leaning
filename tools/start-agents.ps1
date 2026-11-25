# Start the author and reviewer loops in one Windows Terminal window, one tab each. A loop that is
# already running (found by its --name) is not started twice. Safe to run at login or any time.
#   .\tools\start-agents.ps1            # start whatever isn't running
#   .\tools\start-agents.ps1 -DryRun    # only report what it would do
param(
  [string[]]$Roles = @('author', 'reviewer'),
  [string]$Model = 'claude-opus-5-5',
  [switch]$DryRun
)
$runner = Join-Path $PSScriptRoot 'run-agent.ps1'
$running = @(Get-CimInstance Win32_Process -Filter "Name='claude.exe'" | ForEach-Object { $_.CommandLine })

$tabs = @()
foreach ($r in $Roles) {
  if ($running | Where-Object { $_ -match "--name $r\b" }) {
    Write-Output "$r is already running; not starting another."
    continue
  }
  Write-Output "starting $r"
  $tabs += , @('new-tab', '--title', $r, 'powershell.exe', '-NoExit', '-NoProfile', '-File', $runner,
    '-Role', $r, '-Model', $Model)
}
if (-not $tabs -or $DryRun) { return }

# Windows Terminal separates tab commands with a ';' argument.
$wtArgs = @('-w', 'proofs-agents')
for ($i = 0; $i -lt $tabs.Count; $i++) {
  if ($i -gt 0) { $wtArgs += ';' }
  $wtArgs += $tabs[$i]
}
$quoted = $wtArgs | ForEach-Object { if ($_ -match '\s') { '"' + $_ + '"' } else { $_ } }
Start-Process wt.exe -ArgumentList ($quoted -join ' ')
