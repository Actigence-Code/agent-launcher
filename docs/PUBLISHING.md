# Publishing Guide

This guide explains how to publish Agent Launcher to GitHub and PyPI.

## Prerequisites

1. **GitHub Account**: You'll need a GitHub account
2. **PyPI Account**: Create an account at https://pypi.org
3. **Python Tools**: Install build tools

```bash
pip install build twine
```

## Step 1: Create GitHub Repository

### 1.1 Create Repository on GitHub

1. Go to https://github.com/new
2. Repository name: `agent-launcher`
3. Description: "Bilingual launcher for AI coding agents"
4. Make it Public
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### 1.2 Push Code to GitHub

```bash
cd /home/debian/agent-launcher

# Initialize git if not already done
git init

# Add all files
git add .

# Create initial commit
git commit -m "feat: initial release v3.0.0"

# Add GitHub remote (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/agent-launcher.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 1.3 Create Release on GitHub

1. Go to your repository on GitHub
2. Click "Releases" → "Create a new release"
3. Tag version: `v3.0.0`
4. Release title: `Agent Launcher v3.0.0`
5. Description: Copy from CHANGELOG.md
6. Click "Publish release"

## Step 2: Publish to PyPI

### 2.1 Build Distribution

```bash
cd /home/debian/agent-launcher

# Clean previous builds
rm -rf build/ dist/ *.egg-info/

# Build distribution packages
python -m build
```

This creates:
- `dist/agent-launcher-3.0.0.tar.gz` (source distribution)
- `dist/agent_launcher-3.0.0-py3-none-any.whl` (wheel)

### 2.2 Test on TestPyPI (Optional but Recommended)

```bash
# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test installation
pip install --index-url https://test.pypi.org/simple/ agent-launcher
```

### 2.3 Upload to PyPI

```bash
# Upload to PyPI
twine upload dist/*
```

You'll be prompted for:
- Username: `__token__`
- Password: Your PyPI API token (get from https://pypi.org/manage/account/token/)

### 2.4 Verify Installation

```bash
# Install from PyPI
pip install agent-launcher

# Test it works
agent --version
```

## Step 3: Configure GitHub Actions (Automated Publishing)

### 3.1 Create PyPI API Token

1. Go to https://pypi.org/manage/account/token/
2. Create a new token with scope "Entire account"
3. Copy the token (starts with `pypi-`)

### 3.2 Add Token to GitHub Secrets

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

### 3.3 Test Automated Publishing

Now when you create a new release on GitHub, it will automatically publish to PyPI!

## Step 4: Update README Links

Update the README.md with your actual GitHub username:

```bash
# Replace in README.md
sed -i 's/yourusername/YOUR_GITHUB_USERNAME/g' README.md

# Commit and push
git add README.md
git commit -m "docs: update GitHub username in README"
git push
```

## Publishing Checklist

Before each release:

- [ ] Update version in `pyproject.toml`
- [ ] Update version in `agent.py` (line with `version="agent 3.0.0"`)
- [ ] Update `CHANGELOG.md` with changes
- [ ] Run tests: `pytest`
- [ ] Check code style: `black agent.py && flake8 agent.py`
- [ ] Test locally: `python agent.py --help`
- [ ] Build package: `python -m build`
- [ ] Test on TestPyPI (optional)
- [ ] Create Git tag: `git tag v3.0.0`
- [ ] Push tag: `git push origin v3.0.0`
- [ ] Create GitHub Release
- [ ] Upload to PyPI (manual or wait for GitHub Actions)
- [ ] Test installation: `pip install agent-launcher`
- [ ] Announce on relevant communities

## Manual Publishing Commands Quick Reference

```bash
# 1. Prepare release
git add .
git commit -m "chore: bump version to 3.1.0"
git tag v3.1.0
git push origin main
git push origin v3.1.0

# 2. Build
python -m build

# 3. Upload to PyPI
twine upload dist/*

# 4. Clean up
rm -rf build/ dist/ *.egg-info/
```

## Versioning Strategy

We follow Semantic Versioning (semver.org):

- **MAJOR** (3.x.x): Breaking changes
- **MINOR** (x.1.x): New features, backward compatible
- **PATCH** (x.x.1): Bug fixes, backward compatible

Examples:
- `3.0.0` → `3.0.1`: Bug fix
- `3.0.1` → `3.1.0`: New feature (loop mode)
- `3.1.0` → `4.0.0`: Breaking change (API redesign)

## Troubleshooting

### "File already exists" error on PyPI

You can't re-upload the same version. Either:
1. Increment version number
2. Delete files from PyPI (but old users won't be able to reinstall)

### Build fails

```bash
# Ensure build tools are up to date
pip install --upgrade build setuptools wheel

# Check pyproject.toml syntax
python -c "import tomli; tomli.load(open('pyproject.toml', 'rb'))"
```

### Upload fails with 403 error

Check your PyPI token:
- Username must be `__token__`
- Password is your full token including `pypi-` prefix
- Token must have appropriate scope

## Distribution Channels

Once published, your package will be available:

1. **PyPI**: https://pypi.org/project/agent-launcher/
2. **GitHub**: https://github.com/yourusername/agent-launcher
3. **Installation**: `pip install agent-launcher`

## Marketing Your Package

- Add topics/tags on GitHub
- Share on Reddit (r/Python, r/programming)
- Tweet about it
- Write a blog post
- Submit to Python Weekly newsletter
- Add to Awesome Lists

## Support

- Documentation: Keep README.md updated
- Issues: Enable GitHub Issues
- Discussions: Enable GitHub Discussions
- Wiki: Add advanced usage guides
