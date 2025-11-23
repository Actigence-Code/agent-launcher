# Agent Launcher 🤖

**Bilingual (English/Français)** launcher for AI coding agents (Codex & Claude Code).

A powerful, user-friendly command-line tool that simplifies launching and managing AI coding agents with advanced features like review mode, loop mode, and configuration persistence.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

## ✨ Features

- 🎯 **Guided Selection**: Interactive prompts to choose between Codex and Claude
- 🔒 **Safety Controls**: Configurable sandbox and approval bypass settings
- 🔄 **Review Mode**: Automatic cross-agent validation and debugging
- 🔁 **Loop Mode**: Iterative improvements with time-based iterations
- 💾 **Persistent Configuration**: Save your preferences for future use
- 🌍 **Bilingual**: Full English and French support
- 📝 **Command History**: Track all your agent invocations
- 🎨 **Smart Terminal Detection**: Automatic color support based on your terminal
- 🔧 **Environment Variables**: Configure via environment for automation
- 📦 **Easy Installation**: Self-installing with `--install` flag

## 📦 Installation

### Option 1: pip install (Recommended)

```bash
pip install agent-launcher
```

### Option 2: Direct Download

```bash
# Download the script
curl -o agent.py https://raw.githubusercontent.com/Actigence-Code/agent-launcher/main/agent.py

# Make it executable
chmod +x agent.py

# Install globally
./agent.py --install
```

### Option 3: From Source

```bash
git clone https://github.com/Actigence-Code/agent-launcher.git
cd agent-launcher
pip install -e .
```

## 🚀 Quick Start

### Basic Usage

```bash
# Interactive mode - will prompt for choices
agent

# Specify agent directly
agent --agent claude

# With bypass mode (be careful!)
agent --agent codex --bypass

# Dry run to see what would be executed
agent --dry-run --agent claude
```

### Advanced Features

```bash
# Review mode: Second agent reviews the first agent's work
agent --agent claude --review

# Loop mode: Iterate improvements for 30 minutes
agent --agent claude --loop 30

# Combined: Loop with review
agent --agent claude --loop 60 --review

# Specify model and additional directories
agent --agent claude --model sonnet --add-dir /path/to/project

# Save your preferences as defaults
agent --agent claude --bypass --save-defaults
```

### Environment Variables

```bash
# Configure via environment
export AGENT_TYPE=claude
export AGENT_BYPASS=true
export AGENT_MODEL=opus

# Now just run
agent
```

## 📖 Usage Examples

### Example 1: Quick Interactive Session

```bash
$ agent
Agent ? (1) Codex | (2) Claude - tapez le numéro ou le nom: 2
Dangerously bypass approvals & sandbox ? [y/N | o/N] : n

Agent Ready / Agent Prêt
- Agent: Claude | Agent choisi : Claude
- Bypass: DISABLED | Bypass : DÉSACTIVÉ
WARNING: Read the official docs before enabling bypass.
Bon travail / Happy coding!

Launching Claude...
```

### Example 2: Code Review Workflow

```bash
# Have Claude write the code, then Codex reviews it
agent --agent claude --review "Implement a binary search tree in Python"

# Or vice versa
agent --agent codex --review "Create a REST API with authentication"
```

### Example 3: Iterative Improvement

```bash
# Work on optimizing code for 45 minutes
agent --agent claude --loop 45 --bypass "Optimize the database queries in src/models"
```

### Example 4: Non-Interactive Automation

```bash
# Use in scripts or CI/CD
AGENT_TYPE=claude AGENT_BYPASS=false agent --quiet "Run tests and fix any failures"
```

## 🎛️ Command-Line Options

### Agent Selection

- `-a, --agent {codex,claude}`: Choose the agent (Codex or Claude)
- `--check-version`: Check installed agent version

### Safety Options

- `--bypass`: Enable dangerous sandbox/approval bypass ⚠️
- `--no-bypass`: Explicitly disable bypass
- `-q, --quiet`: Suppress styling (for scripts)

### Advanced Modes

- `--review`: Enable review mode (other agent reviews output)
- `--loop MINUTES`: Enable loop mode for N minutes (default: 60)
- `-m, --model MODEL`: Specify model to use
- `--add-dir DIR`: Add additional working directory (repeatable)

### Configuration

- `--save-defaults`: Save current options as defaults
- `--dry-run`: Show command without executing
- `--install`: Install launcher globally

### Info Commands

- `-V, --version`: Show version information
- `-h, --help`: Show help message

## 🔧 Configuration Files

### Config Location

- Linux/macOS: `~/.config/agent/config.json`
- Configuration is automatically created on first use

### Config Structure

```json
{
  "default_agent": "claude",
  "default_bypass": false,
  "default_model": "opus"
}
```

### Command History

All commands are logged to `~/.config/agent/history.log`:

```json
{
  "timestamp": "2025-11-23T12:34:56",
  "agent": "claude",
  "bypass": false,
  "model": "sonnet",
  "command": "claude --model sonnet 'Fix the bug'",
  "review_mode": false,
  "loop_duration": null
}
```

## 🎨 Review Mode

Review mode adds a quality assurance step by having the alternate agent review and improve the output:

1. **Primary Agent Executes**: Your chosen agent completes the task
2. **Review Prompt**: You're asked if you want to review
3. **Secondary Agent Reviews**: The other agent checks for bugs and improvements
4. **Interactive**: You can skip review or cancel at any time

```bash
# Example workflow
agent --agent claude --review "Implement user authentication"

# Output:
# [REVIEW MODE] Running primary agent: Claude
# [REVIEW MODE] The agent will execute your request first...
# (Claude implements authentication)
# [REVIEW MODE] Primary agent completed with exit code 0
# [REVIEW MODE] Launch review agent (Codex)? [Y/n | O/n] : y
# (Codex reviews and suggests improvements)
```

## 🔁 Loop Mode

Loop mode enables iterative improvements over a specified time period:

- Runs multiple iterations until time expires
- Optional review after each iteration
- Minimum 5 minutes required for next iteration
- User can cancel at any time

```bash
# Optimize code for 30 minutes
agent --agent claude --loop 30 "Optimize performance in src/api"

# With review after each iteration
agent --agent claude --loop 60 --review "Refactor legacy codebase"
```

## 🔐 Safety Notes

### ⚠️ Bypass Mode Warning

The `--bypass` flag disables safety sandboxes and approval prompts. Use with extreme caution:

- **Codex**: `--dangerously-bypass-approvals-and-sandbox`
- **Claude**: `--dangerously-skip-permissions`

**Only use bypass mode when:**
- You fully trust the code being executed
- You're working in a sandboxed/disposable environment
- You understand the security implications

## 🌍 Bilingual Support

All prompts and messages are displayed in both English and French:

```
Agent ? (1) Codex | (2) Claude - tapez le numéro ou le nom:
Dangerously bypass approvals & sandbox ? [y/N | o/N] :
Agent Ready / Agent Prêt
Bon travail / Happy coding!
```

## 🐛 Troubleshooting

### Agent Not Found

```bash
# Check if agent is installed
agent --check-version --agent claude

# Install missing agent (requires npm)
# The launcher will offer to install if npm is available
```

### Permission Errors

```bash
# For global installation
sudo agent --install

# Or install to user directory
AGENT_INSTALL_DIR=~/.local/bin agent --install
```

### Clear Configuration

```bash
# Remove config to start fresh
rm -rf ~/.config/agent/
```

## 📚 Requirements

- **Python**: 3.8 or higher
- **Operating System**: Linux, macOS, or Windows (with WSL)
- **Dependencies**: None (pure Python, stdlib only)
- **Optional**: Node.js + npm (for agent installation)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### Development Setup

```bash
git clone https://github.com/Actigence-Code/agent-launcher.git
cd agent-launcher
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e ".[dev]"
```

### Running Tests

```bash
pytest
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [OpenAI Codex](https://github.com/openai/codex) for the amazing AI coding assistant
- [Anthropic Claude Code](https://github.com/anthropics/claude-code) for powerful code understanding
- All contributors who help improve this tool

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/Actigence-Code/agent-launcher/issues)
- **Discussions**: [GitHub Discussions](https://github.com/Actigence-Code/agent-launcher/discussions)
- **Documentation**: [Wiki](https://github.com/Actigence-Code/agent-launcher/wiki)

## 🗺️ Roadmap

- [ ] Support for additional AI coding agents
- [ ] Plugin system for custom workflows
- [ ] Web UI for configuration
- [ ] Team collaboration features
- [ ] Cloud sync for configuration
- [ ] Integration with popular IDEs

---

Made with ❤️ by the AI coding community
