[CmdletBinding()]
param(
    [ValidateSet('Recommend', 'Lite', 'Full')]
    [string]$Mode = 'Recommend',

    [switch]$Apply,

    [string]$ProjectRoot = (Get-Location).Path,

    [string]$AgentRoot = ''
)

$ErrorActionPreference = 'Stop'

function Test-CommandAvailable {
    param([Parameter(Mandatory = $true)][string]$Name)
    return [bool](Get-Command $Name -ErrorAction SilentlyContinue)
}

function Test-Skill {
    param(
        [Parameter(Mandatory = $true)][string]$SkillsRoot,
        [Parameter(Mandatory = $true)][string]$Name
    )
    return Test-Path -LiteralPath (Join-Path $SkillsRoot "$Name\SKILL.md") -PathType Leaf
}

$UserProfilePath = [Environment]::GetFolderPath('UserProfile')
if ([string]::IsNullOrWhiteSpace($AgentRoot)) {
    $SharedAgentRoot = Join-Path $UserProfilePath '.agents'
} else {
    $SharedAgentRoot = $AgentRoot
}
$SharedSkillsRoot = Join-Path $SharedAgentRoot 'skills'

$Tools = [ordered]@{
    powershell = $true
    git        = Test-CommandAvailable -Name 'git'
    gh         = Test-CommandAvailable -Name 'gh'
    chezmoi    = Test-CommandAvailable -Name 'chezmoi'
}

$GitHubAuthenticated = $false
if ($Tools.gh) {
    & gh auth status *> $null
    $GitHubAuthenticated = $LASTEXITCODE -eq 0
}

$Skills = [ordered]@{
    initial   = Test-Skill -SkillsRoot $SharedSkillsRoot -Name 'initial'
    startup   = Test-Skill -SkillsRoot $SharedSkillsRoot -Name 'startup'
    shutdown  = Test-Skill -SkillsRoot $SharedSkillsRoot -Name 'shutdown'
    readygate = Test-Skill -SkillsRoot $SharedSkillsRoot -Name 'readygate'
}

$GlobalExists = Test-Path -LiteralPath (Join-Path $SharedAgentRoot 'GLOBAL.md') -PathType Leaf
$LiteCount = @($Skills.initial, $Skills.startup, $Skills.shutdown | Where-Object { $_ }).Count

if ($LiteCount -eq 0 -and -not $GlobalExists) {
    $Classification = 'NONE'
} elseif ($LiteCount -eq 3 -and $GlobalExists -and $Skills.readygate) {
    $Classification = 'FULL'
} elseif ($LiteCount -eq 3) {
    $Classification = 'LITE'
} else {
    $Classification = 'DRIFT'
}

if ($Mode -eq 'Recommend') {
    switch ($Classification) {
        'NONE' {
            $RecommendedMode = 'Lite'
            $Reason = 'No shared lifecycle skills were detected; begin with the smallest safe profile.'
        }
        'LITE' {
            $RecommendedMode = 'Lite'
            $Reason = 'Lite is already available; add Full only when governed workflows are needed.'
        }
        'FULL' {
            $RecommendedMode = 'Lite'
            $Reason = 'Full capabilities are installed; daily project work should still use the Lite read surface.'
        }
        default {
            $RecommendedMode = 'None'
            $Reason = 'Sources are incomplete or divergent; produce a comparison before installing.'
        }
    }
} else {
    $RecommendedMode = $Mode
    $Reason = 'The caller selected an explicit mode; writes still require a separate confirmed Apply implementation.'
}

$Project = [ordered]@{
    root          = '<runtime-path-redacted>'
    exists        = Test-Path -LiteralPath $ProjectRoot -PathType Container
    agents        = Test-Path -LiteralPath (Join-Path $ProjectRoot 'AGENTS.md') -PathType Leaf
    handoff       = Test-Path -LiteralPath (Join-Path $ProjectRoot 'handoff.md') -PathType Leaf
    git_repository = Test-Path -LiteralPath (Join-Path $ProjectRoot '.git')
}

$Result = [ordered]@{
    bootstrap_version     = '0.2.0-local'
    classification        = $Classification
    requested_mode        = $Mode
    recommended_mode      = $RecommendedMode
    reason                = $Reason
    tools                 = $Tools
    github_authenticated  = $GitHubAuthenticated
    global_exists         = $GlobalExists
    skills                = $Skills
    project               = $Project
    writes_performed      = $false
    next_action           = 'Review BOOTSTRAP.md and confirm exact sources, targets, rollback, and external actions.'
}

$Result | ConvertTo-Json -Depth 5

if ($Apply) {
    throw 'Apply is PLANNED and intentionally disabled in 0.2.0-local. No files were changed.'
}
