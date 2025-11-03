# Cleanup unnecessary files for DevOps project

Write-Host "🗑️ Cleaning up unnecessary files..." -ForegroundColor Yellow

# Remove unnecessary markdown files
$filesToRemove = @(
    "COMPLETE_PROJECT_GUIDE.md",
    "FIXES_APPLIED.md",
    "NEXT_STEPS.md",
    "README_DEVOPS.md",
    "TEST_LOCALLY_FIRST.md",
    "Dockerfile.lightweight"
)

foreach ($file in $filesToRemove) {
    if (Test-Path $file) {
        Remove-Item $file -Force
        Write-Host "✅ Removed: $file" -ForegroundColor Green
    }
}

Write-Host "`n✅ Cleanup complete!" -ForegroundColor Green
Write-Host "`n📁 Essential files kept:" -ForegroundColor Cyan
Write-Host "  - README.md (Main documentation)" -ForegroundColor White
Write-Host "  - DEVOPS_GUIDE.md (Complete DevOps guide)" -ForegroundColor White
Write-Host "  - SETUP_INSTRUCTIONS.md (Quick setup)" -ForegroundColor White
Write-Host "  - PROJECT_ARCHITECTURE.md (System architecture)" -ForegroundColor White
Write-Host "  - RESULTS_GUIDE.md (Results documentation)" -ForegroundColor White
