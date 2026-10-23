# GitHub Integration & CI/CD Pipeline

This guide outlines remote GitHub repository integration, branch governance, secret management, and automated continuous integration for the **RAG Technology Lab**.

---

## 1. Remote Repository Setup

```bash
# Link local repository to remote GitHub repository
git remote add origin https://github.com/<your-org>/rag-technology-lab.git

# Set default upstream branch to main
git branch -M main
git push -u origin main
```

---

## 2. GitHub Actions CI/CD Workflow

To automatically validate Python code, Pydantic schemas, and TypeScript frontend types on every pull request, create `.github/workflows/rag-ci.yml`:

```yaml
name: RAG Technology Lab CI

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  backend-tests:
    name: Python 3.12+ Backend Tests
    runs-on: ubuntu-latest

    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: rag_lab_db
          POSTGRES_PASSWORD: postgres
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: "pip"

      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Run Pytest Suite
        run: |
          pytest 10-testing/test_pytest.py -v

      - name: Run Standalone Technology Tests
        run: |
          python 01-programming/test_python.py
          python 02-backend/test_pydantic.py
          python 02-backend/test_fastapi.py

  frontend-tests:
    name: Frontend TypeScript Verification
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 20
      - name: Type Check TypeScript Interfaces
        run: |
          cd 09-frontend/typescript
          npx --yes typescript --noEmit
```

---

## 3. GitHub Secrets Management

Configure the following secrets under **Settings > Secrets and variables > Actions**:

| Secret Name | Purpose | Example Value |
| :--- | :--- | :--- |
| `HF_TOKEN` | Hugging Face token for downloading private/rate-limited models | `hf_...` |
| `POSTGRES_PASSWORD` | Production database password | `SuperSecretPassword!` |
| `OLLAMA_BASE_URL` | Remote GPU server running Ollama | `https://llm.internal.domain:11434` |
