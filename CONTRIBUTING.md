# Contributing to Agent Launcher

First off, thank you for considering contributing to Agent Launcher! It's people like you that make this tool better for everyone.

## Code of Conduct

This project and everyone participating in it is governed by respect and professionalism. Please be kind and courteous to others.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the existing issues as you might find that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps to reproduce the problem**
* **Provide specific examples**
* **Describe the behavior you observed and what behavior you expected**
* **Include your environment details** (OS, Python version, agent versions)

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a detailed description of the suggested enhancement**
* **Explain why this enhancement would be useful**
* **List some examples of how it would be used**

### Pull Requests

1. Fork the repo and create your branch from `main`
2. If you've added code, add tests
3. Ensure the test suite passes
4. Make sure your code follows the existing style
5. Write a clear commit message

## Development Setup

```bash
# Clone your fork
git clone https://github.com/yourusername/agent-launcher.git
cd agent-launcher

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode
pip install -e ".[dev]"
```

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=agent --cov-report=html

# Run specific test file
pytest tests/test_specific.py
```

## Code Style

We use:
- **Black** for code formatting (line length 100)
- **flake8** for linting
- **isort** for import sorting
- **mypy** for type checking

```bash
# Format code
black agent.py

# Sort imports
isort agent.py

# Check linting
flake8 agent.py

# Type check
mypy agent.py
```

## Commit Message Guidelines

We follow conventional commits:

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting, etc.)
- `refactor:` Code refactoring
- `test:` Adding or updating tests
- `chore:` Maintenance tasks

Examples:
```
feat: add support for GPT-4 agent
fix: resolve crash when config file is corrupted
docs: update installation instructions for Windows
```

## Adding New Agents

To add support for a new AI agent:

1. Update `AGENT_METADATA` in `agent.py`:
```python
AGENT_METADATA = {
    # ... existing agents ...
    "newagent": {
        "label": "New Agent",
        "binary": "newagent",
        "danger_flag": "--unsafe-mode",
        "npm_package": "@company/newagent",
        "docs_url": "https://docs.newagent.com",
    },
}
```

2. Update documentation
3. Add tests
4. Update README with examples

## Adding New Features

When adding new features:

1. Maintain backward compatibility when possible
2. Update relevant documentation
3. Add command-line arguments if needed
4. Consider bilingual support (English/French)
5. Add tests for the new feature
6. Update CHANGELOG.md

## Documentation

- Keep README.md up to date
- Document new features in docstrings
- Update CHANGELOG.md
- Add examples for new functionality

## Release Process

(For maintainers)

1. Update version in `pyproject.toml`
2. Update `CHANGELOG.md`
3. Create a new release on GitHub
4. GitHub Actions will automatically publish to PyPI

## Questions?

Feel free to open an issue with the question label or start a discussion.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
