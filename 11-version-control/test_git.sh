#!/usr/bin/env bash
# =============================================================================
# RAG Technology Testing Lab — Technology 24: Git Version Control Test
# =============================================================================

set -e

echo "======================================================================"
echo "🧪 Running 11-version-control: Git Operations Test"
echo "======================================================================"

# 1. Verify Git Installation
echo -e "\n[Step 1/5] Checking Git version..."
git --version

# 2. Setup Isolated Scratch Repository
SCRATCH_DIR="./11-version-control/scratch_git_repo"
rm -rf "$SCRATCH_DIR"
mkdir -p "$SCRATCH_DIR"
cd "$SCRATCH_DIR"

echo -e "\n[Step 2/5] Initializing local repository..."
git init -b main
git config user.name "RAG Lab Bot"
git config user.email "rag-lab@example.com"

# 3. Create Initial Commit
echo -e "\n[Step 3/5] Creating initial commit..."
cat << 'EOF' > README.md
# Multilingual RAG Test Repo
Tracking ingestion pipelines for English and Khmer document corpora.
EOF

git add README.md
git commit -m "feat: initial commit with project overview"
git log -1 --oneline

# 4. Feature Branching & Merging
echo -e "\n[Step 4/5] Creating and merging feature branch..."
git checkout -b feature/khmer-embeddings

cat << 'EOF' >> README.md
- Added BGE-M3 multilingual embedding support
EOF

git commit -am "feat: add BGE-M3 embedding support"
git checkout main
git merge --no-ff feature/khmer-embeddings -m "merge: integrate feature/khmer-embeddings into main"

# 5. Tag Release & Verify History
echo -e "\n[Step 5/5] Creating semantic release tag..."
git tag -a v1.0.0 -m "Release v1.0.0 — Multilingual RAG Lab baseline"

echo "Commit history graph:"
git log --graph --oneline --decorate -n 5

# Cleanup scratch repository
cd ../..
rm -rf "$SCRATCH_DIR"
echo -e "\n✓ Cleaned up scratch test repository."

echo "======================================================================"
echo "🎉 SUCCESS: Git version control tests completed successfully!"
echo "======================================================================"
