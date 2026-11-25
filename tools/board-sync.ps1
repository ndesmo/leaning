# Sync the "Proofs by Claude" project board with GitHub: add open issues and PRs that are missing,
# and set each item's Status from its real state. Idempotent; safe to run any time.
#   closed / merged          -> Done
#   open pull request        -> In Review
#   issue labelled in-progress -> In Progress
#   anything else open       -> Todo
param([string]$Owner = 'ndesmo', [string]$Repo = 'leaning', [int]$Project = 1)
$ErrorActionPreference = 'Stop'

$fields = gh project field-list $Project --owner $Owner --format json | ConvertFrom-Json
$status = $fields.fields | Where-Object { $_.name -eq 'Status' }
$opt = @{}; foreach ($o in $status.options) { $opt[$o.name] = $o.id }
$projectId = (gh project view $Project --owner $Owner --format json | ConvertFrom-Json).id

$items = (gh project item-list $Project --owner $Owner --limit 500 --format json | ConvertFrom-Json).items
$onBoard = @{}; foreach ($i in $items) { if ($i.content.url) { $onBoard[$i.content.url] = $i } }

# Add open issues and PRs that are not on the board yet.
$open = @()
$open += gh issue list --repo "$Owner/$Repo" --state open --limit 500 --json url | ConvertFrom-Json
$open += gh pr list --repo "$Owner/$Repo" --state open --limit 200 --json url | ConvertFrom-Json
$added = 0
foreach ($o in $open) {
  if (-not $onBoard.ContainsKey($o.url)) {
    $new = gh project item-add $Project --owner $Owner --url $o.url --format json | ConvertFrom-Json
    $onBoard[$o.url] = [pscustomobject]@{ id = $new.id; status = $null; content = [pscustomobject]@{ url = $o.url } }
    $added++
  }
}

# Desired status for every item on the board.
$changed = 0
foreach ($url in @($onBoard.Keys)) {
  $item = $onBoard[$url]
  if ($url -match '/pull/(\d+)$') {
    $s = (gh pr view $Matches[1] --repo "$Owner/$Repo" --json state | ConvertFrom-Json).state
    $want = if ($s -eq 'OPEN') { 'In Review' } else { 'Done' }
  } elseif ($url -match '/issues/(\d+)$') {
    $iss = gh issue view $Matches[1] --repo "$Owner/$Repo" --json state,labels | ConvertFrom-Json
    $want = if ($iss.state -ne 'OPEN') { 'Done' }
            elseif ($iss.labels.name -contains 'in-progress') { 'In Progress' }
            else { 'Todo' }
  } else { continue }
  if ($item.status -ne $want) {
    gh project item-edit --id $item.id --project-id $projectId --field-id $status.id --single-select-option-id $opt[$want] | Out-Null
    $changed++
  }
}
Write-Output "board synced: $added added, $changed status changes, $($onBoard.Count) items"
