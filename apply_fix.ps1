$ErrorActionPreference = "Stop"

if (-not (Test-Path ".\mkdocs.yml")) {
    throw "Ejecuta este script desde la raíz de SportsLabResearch_WEB."
}

New-Item -ItemType Directory -Force ".\.github\workflows" | Out-Null

Remove-Item ".\.github\workflows\deploy.yml" -Force -ErrorAction SilentlyContinue
Remove-Item ".\.github\workflows\update-site.yml" -Force -ErrorAction SilentlyContinue

Copy-Item "$PSScriptRoot\.github\workflows\pages.yml" ".\.github\workflows\pages.yml" -Force
Copy-Item "$PSScriptRoot\requirements.txt" ".\requirements.txt" -Force
Copy-Item "$PSScriptRoot\README_AUTOMATION.md" ".\README_AUTOMATION.md" -Force

Write-Host "Workflow único instalado correctamente." -ForegroundColor Green
Write-Host "Solo debe existir: .github\workflows\pages.yml" -ForegroundColor Cyan
