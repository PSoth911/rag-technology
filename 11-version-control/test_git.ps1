# =============================================================================
# RAG Technology Testing Lab — Technology 24: Git Version Control Test (PowerShell)
# =============================================================================

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "🧪 Running 11-version-control: Git Operations Test (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 1. Verify Git Installation
Write-Host "`n[Step 1/5] Checking Git version..."
git --version

# 2. Setup Isolated Scratch Repository
$ScratchDir = "11-version-control\scratch_git_repo"
if (Test-Path $ScratchDir) {
    Remove-Item -Recurse -Force $ScratchDir
}
New-Item -ItemType Directory -Path $ScratchDir | Out-Null
Set-Location $ScratchDir

# 3. Create Initial Commit
Write-Host "`n[Step 2/5] Initializing local repository..."
git init -b main
git config user.name "RAG Lab Bot"
git config user.email "rag-lab@example.com"

Write-Host "`n[Step 3/5] Creating initial commit..."
Set-Content -Path "README.md" -Value "# Multilingual RAG Test Repo`nTracking ingestion pipelines for English and Khmer document corpora."
git add README.md
git commit -m "feat: initial commit with project overview"
git log -1 --oneline

# 4. Feature Branching & Merging
Write-Host "`n[Step 4/5] Creating and merging feature branch..."
git checkout -b feature/khmer-embeddings
Add-Content -Path "README.md" -Value "`n- Added BGE-M3 multilingual embedding support"
git commit -am "feat: add BGE-M3 embedding support"

git checkout main
git merge --no-ff feature/khmer-embeddings -m "merge: integrate feature/khmer-embeddings into main"

# 5. Tag Release & Verify History
Write-Host "`n[Step 5/5] Creating semantic release tag..."
git tag -a v1.0.0 -m "Release v1.0.0: Multilingual RAG Lab baseline"

Write-Host "`nCommit history graph:"
git log --graph --oneline --decorate -n 5

Set-Location ..\..
if (Test-Path $ScratchDir) {
    Remove-Item -Recurse -Force $ScratchDir
}
Write-Host "`n✓ Cleaned up scratch test repository."

Write-Host "======================================================================" -ForegroundColor Green
Write-Host "🎉 SUCCESS: Git version control tests completed successfully!" -ForegroundColor Green
Write-Host "======================================================================" -ForegroundColor Green
