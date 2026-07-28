[CmdletBinding()]
param()

$ErrorActionPreference = 'Stop'
$Errors = New-Object 'System.Collections.Generic.List[string]'
$Utf8 = New-Object System.Text.UTF8Encoding($false)

$RepositoryRoot = Split-Path -Parent $PSScriptRoot
$RequiredFiles = @(
    'README.md',
    'AGENTS.md',
    'BOOTSTRAP.md',
    'WORKFLOW.md',
    'MAINTAINERS.md',
    'FEATURES.json',
    '.gitignore',
    'LICENSE',
    'templates/AGENTS.md',
    'templates/handoff.md',
    'templates/project.gitignore',
    'templates/policy.local.example.yaml',
    'scripts/install.ps1'
)

foreach ($RelativePath in $RequiredFiles) {
    $Path = Join-Path $RepositoryRoot $RelativePath
    if (-not (Test-Path -LiteralPath $Path -PathType Leaf)) {
        $Errors.Add("Missing required file: $RelativePath")
    }
}

$FeaturePath = Join-Path $RepositoryRoot 'FEATURES.json'
if (Test-Path -LiteralPath $FeaturePath -PathType Leaf) {
    try {
        $Catalog = [System.IO.File]::ReadAllText($FeaturePath, $Utf8) | ConvertFrom-Json
        $Allowed = @('IMPLEMENTED', 'PROMPT_ONLY', 'PLANNED')
        foreach ($Feature in $Catalog.features) {
            if ($Allowed -notcontains $Feature.status) {
                $Errors.Add("Invalid feature status '$($Feature.status)' for '$($Feature.id)'.")
            }
        }
    } catch {
        $Errors.Add("FEATURES.json is invalid: $($_.Exception.Message)")
    }
}

$SensitiveFilePatterns = @(
    '^\.env$',
    '\.(key|pem|p12|pfx)$',
    '^(credentials|secrets)\.',
    '^policy\.local\.yaml$'
)

$Files = Get-ChildItem -LiteralPath $RepositoryRoot -Recurse -File -Force |
    Where-Object { $_.FullName -notmatch '[\\/]\.git[\\/]' }

foreach ($File in $Files) {
    $RelativePath = $File.FullName.Substring($RepositoryRoot.Length).TrimStart('\', '/')
    foreach ($Pattern in $SensitiveFilePatterns) {
        if ($File.Name -match $Pattern) {
            $Errors.Add("Sensitive or local-only filename is present: $RelativePath")
        }
    }
}

$TextExtensions = @('.md', '.txt', '.json', '.yaml', '.yml', '.toml', '.ini', '.ps1', '.py', '.js', '.ts', '.tsx', '.sh', '.cmd', '.bat')
$ValidatorPath = Join-Path $RepositoryRoot 'scripts\validate.ps1'

foreach ($File in $Files) {
    if ($TextExtensions -notcontains $File.Extension.ToLowerInvariant()) {
        continue
    }
    if ($File.FullName -eq $ValidatorPath) {
        continue
    }

    $Text = [System.IO.File]::ReadAllText($File.FullName, $Utf8)
    $RelativePath = $File.FullName.Substring($RepositoryRoot.Length).TrimStart('\', '/')

    if ($Text -match '(?i)\b[A-Z]:\\|\\\\[A-Za-z0-9._-]+\\|/home/[^<\s]+|/Users/[^<\s]+') {
        $Errors.Add("Device-absolute user path found: $RelativePath")
    }
    if ($Text -match '(?i)DESKTOP-[A-Z0-9-]{4,}') {
        $Errors.Add("Concrete device identifier found: $RelativePath")
    }
    if ($Text -match '(?i)(api[_-]?key|access[_-]?token|client[_-]?secret|password)\s*[:=]\s*[''"][^<\s][^''"]{7,}[''"]') {
        $Errors.Add("Possible embedded secret assignment found: $RelativePath")
    }
}

$IgnoreText = [System.IO.File]::ReadAllText((Join-Path $RepositoryRoot '.gitignore'), $Utf8)
foreach ($RequiredPattern in @('.env', '*.key', 'policy.local.yaml')) {
    if ($IgnoreText -notmatch [regex]::Escape($RequiredPattern)) {
        $Errors.Add(".gitignore is missing required pattern: $RequiredPattern")
    }
}

if ($Errors.Count -gt 0) {
    $Errors | ForEach-Object { Write-Error $_ }
    exit 1
}

Write-Host "PASS: Cross-File AI Workflow Core is valid ($($Files.Count) files checked)."
