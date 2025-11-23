# 🚀 Quick Start Guide

## Publishing to GitHub and PyPI

### Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `agent-launcher`
3. Description: "Bilingual launcher for AI coding agents (Codex & Claude)"
4. Make it **Public**
5. Don't initialize with README (we already have one)
6. Click "Create repository"

### Step 2: Push to GitHub

```bash
cd /home/debian/agent-launcher

# The repo is already initialized and committed
# Just add the remote and push (replace YOUR_USERNAME)

git remote add origin https://github.com/YOUR_USERNAME/agent-launcher.git
git push -u origin main
git push origin v3.0.0
```

### Step 3: Create PyPI Account

1. Go to https://pypi.org/account/register/
2. Create an account
3. Verify your email
4. Go to https://pypi.org/manage/account/token/
5. Create a new API token with scope "Entire account"
6. **Copy the token** (starts with `pypi-`)

### Step 4: Publish to PyPI

```bash
cd /home/debian/agent-launcher
source venv/bin/activate

# Upload to PyPI (it will ask for username and password)
twine upload dist/*

# Enter:
# - Username: __token__
# - Password: <paste your PyPI token>
```

### Step 5: Configure GitHub Actions (Optional but Recommended)

1. Go to your GitHub repository
2. Settings → Secrets and variables → Actions
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Paste your PyPI token
6. Click "Add secret"

Now every time you create a GitHub release, it will automatically publish to PyPI!

### Step 6: Test Installation

```bash
# In a new terminal or virtual environment
pip install agent-launcher

# Test it
agent --version
agent --help
```

## Success! 🎉

Your package is now:
- ✅ On GitHub: `https://github.com/YOUR_USERNAME/agent-launcher`
- ✅ On PyPI: `https://pypi.org/project/agent-launcher/`
- ✅ Installable worldwide: `pip install agent-launcher`

## Next Steps

### Share Your Project

- Add topics on GitHub: `ai`, `coding-assistant`, `claude`, `codex`
- Share on Twitter/X
- Post on Reddit (r/Python, r/programming)
- Add to your GitHub profile

### Future Releases

When you want to release a new version:

```bash
# 1. Update version in pyproject.toml and agent.py
# 2. Update CHANGELOG.md
# 3. Commit changes
git add .
git commit -m "chore: bump version to 3.1.0"
git tag v3.1.0
git push origin main
git push origin v3.1.0

# 4. Create GitHub Release (this triggers auto-publish if Actions configured)
# Or manually:
source venv/bin/activate
rm -rf dist/
python -m build
twine upload dist/*
```

## Troubleshooting

### "File already exists" on PyPI

You can't re-upload the same version. Increment the version number in `pyproject.toml`.

### Authentication failed

Make sure:
- Username is exactly `__token__`
- Password is your full PyPI token (including `pypi-` prefix)

### Build warnings about license

These are just warnings, the build succeeded. The package works fine.

## Current Status

✅ Git repository initialized
✅ Initial commit created
✅ Version tag v3.0.0 created
✅ Package built successfully
✅ Local installation tested
✅ Command works: `agent --version` → `agent 3.0.0`

**Ready to push to GitHub and publish to PyPI!**
