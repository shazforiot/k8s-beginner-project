# SonarQube Cloud Onboarding Guide

This guide explains how to onboard the `k8s-beginner-project` repository to SonarQube Cloud (sonarcloud.io) for continuous code quality and security analysis.

---

## 📋 Repository Details

| Field | Value |
|-------|-------|
| Repository | `Thetips4you/k8s-beginner-project` |
| Language | JavaScript, Dockerfile |
| Branch | `main` |

---

## 🚀 Step 1: Sign Up / Login to SonarQube Cloud

1. Go to **https://sonarcloud.io**
2. Click **"Log in"** → Select **"GitHub"**
3. Authorize SonarQube Cloud to access your GitHub account
4. Grant access to your repositories (select `Thetips4you/k8s-beginner-project`)

---

## 🏢 Step 2: Create Organization

1. After login, click **"+"** (top-right) → **"Analyze new project"**
2. If prompted, create an **Organization**:
   - Choose **"Import from GitHub"**
   - Organization name: `Thetips4you` (or your GitHub username)
   - Plan: **Free** (for public repos)
3. Click **"Create"**

---

## 📦 Step 3: Import Repository

1. Select **"Analyze new project"**
2. Find `k8s-beginner-project` from the list
3. Click **"Set Up"**
4. Choose analysis method:

| Method | Best For |
|--------|----------|
| **Automatic Analysis** | Simple projects, quick setup |
| **CI-based Analysis** | Full control, GitHub Actions/Jenkins |

> **Recommended:** CI-based with GitHub Actions for more control

---

## ⚙️ Step 4: Set Up GitHub Actions (CI-based)

### 4.1 Generate SonarCloud Token

1. Go to **My Account** → **Security**
   - URL: https://sonarcloud.io/account/security
2. Generate a new token:
   - Name: `k8s-beginner-project`
   - Click **"Generate"**
3. **Copy the token** (you won't see it again!)

### 4.2 Add Token to GitHub Secrets

1. Go to your repo: https://github.com/Thetips4you/k8s-beginner-project
2. Navigate to **Settings** → **Secrets and variables** → **Actions**
3. Click **"New repository secret"**
4. Add:
   - **Name:** `SONAR_TOKEN`
   - **Value:** *(paste the token)*
5. Click **"Add secret"**

### 4.3 Workflow File (Already Created)

The GitHub Actions workflow is located at:
```
.github/workflows/sonarcloud.yml
```

**Workflow Contents:**
```yaml
name: SonarCloud Analysis

on:
  push:
    branches:
      - main
  pull_request:
    types: [opened, synchronize, reopened]

jobs:
  sonarcloud:
    name: SonarCloud Scan
    runs-on: ubuntu-latest

    steps:
      - name: Checkout code
        uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'

      - name: Install dependencies
        run: |
          cd app
          npm install --if-present

      - name: Run tests with coverage
        run: |
          cd app
          npm test --if-present || true

      - name: SonarCloud Scan
        uses: SonarSource/sonarcloud-github-action@master
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### 4.4 Configuration File (Already Created)

The SonarCloud configuration is located at:
```
sonar-project.properties
```

**Key Configuration:**
```properties
sonar.projectKey=Thetips4you_k8s-beginner-project
sonar.organization=Thetips4you
sonar.projectName=k8s-beginner-project
sonar.sources=app
sonar.exclusions=**/node_modules/**,**/coverage/**,**/k8s/**
```

---

## 🤖 Alternative: Automatic Analysis (No Pipeline)

If you prefer a simpler setup without maintaining a CI pipeline, SonarCloud offers **Automatic Analysis** that runs directly on their servers.

### When to Use Automatic Analysis

| Use Case | Recommended Method |
|----------|-------------------|
| Quick setup, minimal config | ✅ Automatic Analysis |
| Simple projects (JS, Python, etc.) | ✅ Automatic Analysis |
| Need test coverage reports | ❌ Use CI-based |
| Custom build steps required | ❌ Use CI-based |
| Monorepos or complex builds | ❌ Use CI-based |

### Setup Steps

1. **Import Project in SonarCloud**
   - Go to https://sonarcloud.io/projects/create
   - Select **"Import from GitHub"**
   - Choose organization: `Thetips4you`
   - Select repository: `k8s-beginner-project`

2. **Enable Automatic Analysis**
   - Go to **Project Settings** → **Analysis Method**
   - Toggle **"Automatic Analysis"** to **ON**

3. **Disable CI-based Workflow (Optional)**
   - If switching from CI-based, delete or disable:
     ```
     .github/workflows/sonarcloud.yml
     ```
   - You can keep `sonar-project.properties` for configuration

### How It Works

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Push Code     │ ──▶ │  SonarCloud     │ ──▶ │   Results in    │
│   to GitHub     │     │  Auto-Analyzes  │     │   Dashboard     │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

- SonarCloud detects pushes via GitHub webhook
- Analysis runs on SonarCloud's infrastructure
- No GitHub Actions minutes consumed
- Results appear in SonarCloud dashboard

### Limitations

| Feature | Automatic | CI-based |
|---------|-----------|----------|
| Zero config | ✅ | ❌ |
| Test coverage | ❌ | ✅ |
| Custom build steps | ❌ | ✅ |
| Private repos (free) | ❌ | ✅ |
| All languages | ❌ | ✅ |

### Supported Languages (Automatic Analysis)

- JavaScript / TypeScript
- Python
- Java
- Kotlin
- Ruby
- Go
- PHP
- C# / VB.NET
- HTML / CSS

> **Note:** For this project (JavaScript), Automatic Analysis works well. If you need coverage reports, use CI-based analysis.

---

## 🚀 Step 5: Trigger First Scan

### Option A: Push to GitHub

```bash
git add .
git commit -m "Add SonarCloud integration"
git push origin main
```

### Option B: Manual Trigger

1. Go to **Actions** tab in GitHub
2. Select **"SonarCloud Analysis"** workflow
3. Click **"Run workflow"**

### Verify Results

Once the workflow completes, check results at:
```
https://sonarcloud.io/project/overview?id=Thetips4you_k8s-beginner-project
```

---

## 🏷️ Step 6: Add Quality Gate Badges (Optional)

Add these badges to your `README.md`:

```markdown
[![Quality Gate Status](https://sonarcloud.io/api/project_badges/measure?project=Thetips4you_k8s-beginner-project&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=Thetips4you_k8s-beginner-project)

[![Bugs](https://sonarcloud.io/api/project_badges/measure?project=Thetips4you_k8s-beginner-project&metric=bugs)](https://sonarcloud.io/summary/new_code?id=Thetips4you_k8s-beginner-project)

[![Vulnerabilities](https://sonarcloud.io/api/project_badges/measure?project=Thetips4you_k8s-beginner-project&metric=vulnerabilities)](https://sonarcloud.io/summary/new_code?id=Thetips4you_k8s-beginner-project)

[![Code Smells](https://sonarcloud.io/api/project_badges/measure?project=Thetips4you_k8s-beginner-project&metric=code_smells)](https://sonarcloud.io/summary/new_code?id=Thetips4you_k8s-beginner-project)

[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=Thetips4you_k8s-beginner-project&metric=coverage)](https://sonarcloud.io/summary/new_code?id=Thetips4you_k8s-beginner-project)

[![Duplicated Lines (%)](https://sonarcloud.io/api/project_badges/measure?project=Thetips4you_k8s-beginner-project&metric=duplicated_lines_density)](https://sonarcloud.io/summary/new_code?id=Thetips4you_k8s-beginner-project)
```

---

## 📊 What SonarCloud Analyzes

| Metric | Description |
|--------|-------------|
| **Bugs** | Reliability issues that could cause failures |
| **Vulnerabilities** | Security weaknesses in the code |
| **Code Smells** | Maintainability issues |
| **Coverage** | Percentage of code covered by tests |
| **Duplications** | Repeated code blocks |
| **Security Hotspots** | Code requiring security review |

---

## 🔧 Troubleshooting

| Issue | Solution |
|-------|----------|
| "Project not found" | Verify `sonar.projectKey` matches exactly |
| "Invalid token" | Regenerate token and update GitHub secret |
| "No files analyzed" | Check `sonar.sources` path is correct |
| "Organization not found" | Verify org name in `sonar.organization` |
| "Permission denied" | Ensure SonarCloud has access to the repo |

---

## 📁 Project File Structure

```
k8s-beginner-project/
├── .github/
│   └── workflows/
│       ├── ci-cd.yaml          # Existing CI/CD workflow
│       └── sonarcloud.yml      # SonarCloud analysis workflow
├── app/                        # Application source code
├── k8s/                        # Kubernetes manifests
├── sonar-project.properties    # SonarCloud configuration
├── sonarCloud.md               # This documentation
├── Dockerfile
└── README.md
```

---

## 🔗 Useful Links

- **SonarCloud Dashboard:** https://sonarcloud.io
- **Project Overview:** https://sonarcloud.io/project/overview?id=Thetips4you_k8s-beginner-project
- **SonarCloud Documentation:** https://docs.sonarcloud.io
- **GitHub Actions for SonarCloud:** https://github.com/SonarSource/sonarcloud-github-action

---

## 📺 Video Tutorial

Watch the full tutorial on YouTube:
**Thetips4you** → https://youtube.com/@Thetips4you

---

*Generated for k8s-beginner-project | Thetips4you*
