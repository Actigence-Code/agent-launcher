#!/usr/bin/env python3
"""
Agent Launcher - Bilingual launcher for AI coding agents

English:
    Agent launcher that guides you through choosing either Codex or Claude,
    and whether to activate the dangerous sandbox/approval bypass switches.
    NEW: Review mode for transparent cross-agent validation and loop mode for iterative improvements.
    Ideal for ensuring consistent workflows from any shell session.

Français :
    Lanceur d'agent qui vous aide à choisir Codex ou Claude et à décider
    d'activer ou non les options dangereuses de contournement des sandbox
    et validations. NOUVEAU : Mode relecture pour validation transparente entre agents
    et mode boucle pour améliorations itératives.
    Parfait pour garantir un flux de travail cohérent depuis n'importe quel terminal.

Made with ❤️ in Tervuren, Belgium
Copyright (c) 2025 Actigence Management Consulting
Website: https://actigence.eu
Contact: hello@actigence.eu
"""

__version__ = "3.0.0"
__author__ = "Actigence Management Consulting"
__email__ = "hello@actigence.eu"
__url__ = "https://actigence.eu"

from __future__ import annotations

import argparse
import datetime
import json
import os
import signal
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from functools import lru_cache
from pathlib import Path
from typing import Dict, List, Optional, Tuple

def resolve_sudo_user_home() -> Optional[Path]:
    """Return the home directory of the sudo invoker, if any."""
    sudo_user = os.environ.get("SUDO_USER")
    if not sudo_user:
        return None
    try:
        import pwd  # type: ignore

        return Path(pwd.getpwnam(sudo_user).pw_dir)
    except (ImportError, KeyError):
        expanded = Path(f"~{sudo_user}").expanduser()
        if str(expanded) != f"~{sudo_user}":
            return expanded
    return None

SUDO_USER_HOME = resolve_sudo_user_home()
EFFECTIVE_HOME = SUDO_USER_HOME or Path.home()
SCRIPT_DIR = Path(__file__).resolve().parent

@lru_cache(maxsize=1)
def compute_search_path() -> str:
    """Build a search PATH that also covers the invoking user's binaries."""
    path_parts = os.environ.get("PATH", "").split(os.pathsep)
    extra_dirs: List[str] = [str(SCRIPT_DIR)]
    for directory in (EFFECTIVE_HOME / ".local/bin", EFFECTIVE_HOME / "bin"):
        extra_dirs.append(str(directory))
    if SUDO_USER_HOME and SUDO_USER_HOME != EFFECTIVE_HOME:
        for directory in (SUDO_USER_HOME / ".local/bin", SUDO_USER_HOME / "bin"):
            extra_dirs.append(str(directory))

    combined: List[str] = []
    for entry in path_parts + extra_dirs:
        if entry and entry not in combined:
            combined.append(entry)
    return os.pathsep.join(combined)

AGENT_METADATA = {
    "codex": {
        "label": "Codex",
        "binary": "codex",
        "danger_flag": "--dangerously-bypass-approvals-and-sandbox",
        "npm_package": "@openai/codex",
        "docs_url": "https://github.com/openai/codex#readme",
    },
    "claude": {
        "label": "Claude",
        "binary": "claude",
        "danger_flag": "--dangerously-skip-permissions",
        "npm_package": "@anthropic-ai/claude-code",
        "docs_url": "https://github.com/anthropics/claude-code",
    },
}

AGENT_CHOICES = tuple(AGENT_METADATA.keys())

STYLE_ACCENT = "\033[95m"
STYLE_SUCCESS = "\033[92m"
STYLE_WARNING = "\033[93m"
STYLE_RESET = "\033[0m"
STYLE_DIM = "\033[2m"
STYLE_CYAN = "\033[96m"

NODE_DOC_URL = "https://nodejs.org/en/download/package-manager"
CONFIG_DIR = EFFECTIVE_HOME / ".config" / "agent"
CONFIG_FILE = CONFIG_DIR / "config.json"
HISTORY_FILE = CONFIG_DIR / "history.log"

# Timeout for prompts (in seconds)
PROMPT_TIMEOUT = 300


@dataclass(frozen=True)
class AgentSelection:
    """Represents the final user choices."""

    agent: str
    bypass: bool
    model: Optional[str]
    add_dirs: Tuple[str, ...]
    dry_run: bool = False
    review_mode: bool = False
    loop_duration: Optional[int] = None


@dataclass
class AgentConfig:
    """Persistent configuration."""

    default_agent: Optional[str] = None
    default_bypass: Optional[bool] = None
    default_model: Optional[str] = None


@lru_cache(maxsize=32)
def which_cached(binary: str) -> Optional[str]:
    """Cached version of shutil.which() to avoid repeated lookups."""
    import shutil
    return shutil.which(binary, path=compute_search_path())


def supports_color() -> bool:
    """Detect if the terminal supports color output."""
    if not sys.stdout.isatty():
        return False
    term = os.environ.get("TERM", "")
    if term == "dumb":
        return False
    if "color" in term or term in ("xterm", "xterm-256color", "screen", "linux"):
        return True
    return os.environ.get("COLORTERM") is not None


def is_interactive() -> bool:
    """Check if running in an interactive terminal."""
    return sys.stdin.isatty() and sys.stdout.isatty()


def load_config() -> AgentConfig:
    """Load persistent configuration from disk."""
    if not CONFIG_FILE.exists():
        return AgentConfig()
    try:
        with open(CONFIG_FILE, "r") as f:
            data = json.load(f)
            return AgentConfig(**data)
    except (json.JSONDecodeError, OSError, TypeError):
        return AgentConfig()


def save_config(config: AgentConfig) -> None:
    """Save configuration to disk."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(asdict(config), f, indent=2)
    except OSError as exc:
        print(f"Warning: Could not save config: {exc}", file=sys.stderr)


def log_command_history(selection: AgentSelection, extras: List[str]) -> None:
    """Log command execution to history file."""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    try:
        with open(HISTORY_FILE, "a") as f:
            timestamp = datetime.datetime.now().isoformat()
            command_parts = [AGENT_METADATA[selection.agent]["binary"]]
            if selection.bypass:
                command_parts.append(AGENT_METADATA[selection.agent]["danger_flag"])
            if selection.model:
                command_parts.extend(["--model", selection.model])
            for directory in selection.add_dirs:
                command_parts.extend(["--add-dir", directory])
            command_parts.extend(extras)
            log_entry = {
                "timestamp": timestamp,
                "agent": selection.agent,
                "bypass": selection.bypass,
                "model": selection.model,
                "add_dirs": list(selection.add_dirs),
                "extras": extras,
                "command": " ".join(command_parts),
                "review_mode": selection.review_mode,
                "loop_duration": selection.loop_duration,
            }
            f.write(json.dumps(log_entry) + "\n")
    except OSError:
        pass  # Don't fail if we can't log


def load_env_config() -> Dict[str, any]:
    """Load configuration from environment variables."""
    env_config = {}
    if agent := os.environ.get("AGENT_TYPE"):
        if agent.lower() in AGENT_CHOICES:
            env_config["agent"] = agent.lower()
    if bypass := os.environ.get("AGENT_BYPASS"):
        env_config["bypass"] = bypass.lower() in ("1", "true", "yes", "y")
    if model := os.environ.get("AGENT_MODEL"):
        env_config["model"] = model
    return env_config


def build_parser() -> argparse.ArgumentParser:
    """Create and configure the bilingual command-line parser."""
    description = (
        "Guided selector for Codex or Claude agents.\n"
        "Sélecteur guidé pour les agents Codex ou Claude."
    )
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "-a",
        "--agent",
        choices=AGENT_CHOICES,
        help="Choose the agent (Codex/Claude). | Choisir l'agent (Codex/Claude).",
    )
    bypass_group = parser.add_mutually_exclusive_group()
    bypass_group.add_argument(
        "--bypass",
        dest="bypass",
        action="store_true",
        help=(
            "Enable dangerous sandbox/approval bypass.\n"
            "Activer le contournement dangereux des sandbox/approbations."
        ),
    )
    bypass_group.add_argument(
        "--no-bypass",
        dest="bypass",
        action="store_false",
        help=(
            "Disable dangerous sandbox/approval bypass.\n"
            "Désactiver le contournement dangereux des sandbox/approbations."
        ),
    )
    parser.set_defaults(bypass=None)
    parser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Suppress styling for scripts. | Supprimer le style pour les scripts.",
    )
    parser.add_argument(
        "-m",
        "--model",
        help="Select the target model. | Choisir le modèle.",
    )
    parser.add_argument(
        "--add-dir",
        dest="add_dir",
        metavar="DIR",
        action="append",
        help=(
            "Allow an additional directory for the agent. (repeatable)\n"
            "Autoriser un répertoire supplémentaire pour l'agent. "
            "(option répétable)"
        ),
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help=(
            "Show the command that would be executed without running it.\n"
            "Afficher la commande qui serait exécutée sans la lancer."
        ),
    )
    parser.add_argument(
        "--save-defaults",
        action="store_true",
        help=(
            "Save current options as defaults for future invocations.\n"
            "Sauvegarder les options actuelles comme défauts pour les prochaines fois."
        ),
    )
    parser.add_argument(
        "--check-version",
        action="store_true",
        help=(
            "Check the version of the selected agent.\n"
            "Vérifier la version de l'agent sélectionné."
        ),
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version="agent 3.0.0",
        help="Show version information. | Afficher la version.",
    )
    parser.add_argument(
        "--install",
        action="store_true",
        help=(
            "Install this launcher into a directory from PATH for global usage.\n"
            "Installer ce lanceur dans un répertoire du PATH pour l'utiliser partout."
        ),
    )
    parser.add_argument(
        "--review",
        action="store_true",
        help=(
            "Enable review mode: the other agent will transparently review and debug the output.\n"
            "Activer le mode relecture : l'autre agent relira et débuggera le résultat de manière transparente."
        ),
    )
    parser.add_argument(
        "--loop",
        type=int,
        metavar="MINUTES",
        help=(
            "Enable loop mode: iterate improvements for N minutes (default: 60).\n"
            "Activer le mode boucle : itérer les améliorations pendant N minutes (par défaut : 60)."
        ),
    )
    return parser


def timeout_handler(signum, frame):
    """Handle timeout signal."""
    print("\nTimeout: No input received. Annulation / Cancelled.", file=sys.stderr)
    sys.exit(1)


def prompt_with_timeout(prompt_text: str) -> str:
    """Prompt with a timeout for non-interactive environments."""
    if not is_interactive():
        print("Error: Interactive input required but not in an interactive terminal.", file=sys.stderr)
        sys.exit(1)

    # Set up signal handler for timeout
    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(PROMPT_TIMEOUT)

    try:
        result = input(prompt_text)
        signal.alarm(0)  # Cancel the alarm
        return result
    except KeyboardInterrupt:
        signal.alarm(0)
        print("\nInterruption reçue. Annulation.", file=sys.stderr)
        sys.exit(1)


def prompt_agent(config: AgentConfig, use_style: bool) -> str:
    """Prompt until a valid agent name is obtained."""
    default_hint = ""
    if config.default_agent:
        default_hint = f" (default: {config.default_agent})"

    accent = STYLE_ACCENT if use_style else ""
    reset = STYLE_RESET if use_style else ""

    prompt = (
        f"{accent}Agent ?{reset}{default_hint} "
        "(1) Codex | (2) Claude - tapez le numéro ou le nom: "
    )
    mapping = {
        "1": "codex",
        "2": "claude",
        "codex": "codex",
        "claude": "claude",
    }
    while True:
        choice = prompt_with_timeout(prompt).strip().lower()
        if not choice and config.default_agent:
            return config.default_agent
        agent = mapping.get(choice)
        if agent:
            return agent
        print(
            "Réponse invalide. Merci de choisir 1/Codex ou 2/Claude.\n"
            "Invalid answer. Please choose 1/Codex or 2/Claude."
        )


def prompt_bypass(config: AgentConfig, use_style: bool) -> bool:
    """Prompt for bypass confirmation."""
    accent = STYLE_ACCENT if use_style else ""
    reset = STYLE_RESET if use_style else ""

    question = (
        f"{accent}Dangerously bypass approvals & sandbox ?{reset} "
    )
    default = config.default_bypass if config.default_bypass is not None else False
    return ask_yes_no(question, default=default)


def validate_directories(directories: Tuple[str, ...]) -> Tuple[str, ...]:
    """Validate that all directories exist and return valid ones."""
    valid_dirs = []
    for directory in directories:
        path = Path(directory).expanduser().resolve()
        if not path.exists():
            print(
                f"Warning: Directory '{directory}' does not exist. Skipping.\n"
                f"Attention : Le répertoire '{directory}' n'existe pas. Ignoré.",
                file=sys.stderr,
            )
        elif not path.is_dir():
            print(
                f"Warning: '{directory}' is not a directory. Skipping.\n"
                f"Attention : '{directory}' n'est pas un répertoire. Ignoré.",
                file=sys.stderr,
            )
        else:
            valid_dirs.append(str(path))
    return tuple(valid_dirs)


def resolve_selection(namespace: argparse.Namespace, config: AgentConfig, env_config: Dict, use_style: bool) -> AgentSelection:
    """Determine selection using arguments, environment, then interactive prompts."""
    # Priority: CLI args > Environment vars > Interactive prompts > Config fallback (non-interactive only)

    # Determine agent
    agent = namespace.agent or env_config.get("agent")
    if not agent:
        if is_interactive():
            agent = prompt_agent(config, use_style)
        elif config.default_agent:
            agent = config.default_agent
        else:
            print("Error: No agent specified and not in interactive mode.", file=sys.stderr)
            sys.exit(1)

    # Determine bypass
    if namespace.bypass is not None:
        bypass = namespace.bypass
    elif "bypass" in env_config:
        bypass = env_config["bypass"]
    elif is_interactive():
        bypass = prompt_bypass(config, use_style)
    elif config.default_bypass is not None:
        bypass = config.default_bypass
    else:
        bypass = False

    # Determine model
    model = namespace.model or env_config.get("model") or config.default_model

    # Validate and collect directories
    add_dirs = validate_directories(tuple(namespace.add_dir or ()))

    # Handle loop duration
    loop_duration = None
    if namespace.loop is not None:
        loop_duration = namespace.loop if namespace.loop > 0 else 60

    return AgentSelection(
        agent=agent,
        bypass=bypass,
        model=model,
        add_dirs=add_dirs,
        dry_run=namespace.dry_run,
        review_mode=namespace.review,
        loop_duration=loop_duration,
    )


def build_command(selection: AgentSelection, extras: List[str]) -> List[str]:
    """Construct the subprocess command for the chosen agent."""
    try:
        details = AGENT_METADATA[selection.agent]
    except KeyError as exc:
        raise ValueError(f"Unsupported agent selection: {selection.agent}") from exc
    command = [details["binary"]]
    if selection.bypass:
        command.append(details["danger_flag"])
    if selection.model:
        command.extend(["--model", selection.model])
    for directory in selection.add_dirs:
        command.extend(["--add-dir", directory])
    command.extend(extras)
    return command


def get_other_agent(current_agent: str) -> str:
    """Get the other agent (for review mode)."""
    return "claude" if current_agent == "codex" else "codex"


def run_review_cycle(selection: AgentSelection, extras: List[str], use_style: bool) -> int:
    """Run the primary agent, then have the other agent review the output transparently."""
    accent = STYLE_CYAN if use_style else ""
    reset = STYLE_RESET if use_style else ""

    print(f"\n{accent}[REVIEW MODE] Running primary agent: {AGENT_METADATA[selection.agent]['label']}{reset}")
    print(f"{accent}[REVIEW MODE] The agent will execute your request first...{reset}\n")

    # Run primary agent interactively (allow full terminal interaction)
    command = build_command(selection, extras)
    try:
        primary_result = subprocess.run(command)
        primary_exit_code = primary_result.returncode
    except KeyboardInterrupt:
        print(f"\n{accent}[REVIEW MODE] Primary agent interrupted by user{reset}")
        return 130
    except Exception as e:
        print(f"\n{accent}[REVIEW MODE] Primary agent failed: {e}{reset}", file=sys.stderr)
        return 1

    print(f"\n{accent}[REVIEW MODE] Primary agent completed with exit code {primary_exit_code}{reset}")

    # Ask if user wants to proceed with review
    if is_interactive():
        try:
            proceed = ask_yes_no(
                f"\n{accent}[REVIEW MODE] Launch review agent ({AGENT_METADATA[get_other_agent(selection.agent)]['label']})?{reset} ",
                default=True
            )
            if not proceed:
                print(f"{accent}[REVIEW MODE] Review skipped by user{reset}")
                return primary_exit_code
        except KeyboardInterrupt:
            print(f"\n{accent}[REVIEW MODE] Review cancelled by user{reset}")
            return primary_exit_code

    # Now run review with the other agent interactively
    other_agent = get_other_agent(selection.agent)
    print(f"\n{accent}[REVIEW MODE] Running review agent: {AGENT_METADATA[other_agent]['label']}{reset}")
    print(f"{accent}[REVIEW MODE] The review agent will now check and improve the work...{reset}\n")

    review_prompt = "Review the previous agent's work. Check for bugs, errors, and improvements. Fix any issues found and ensure production-ready quality."

    # Create review selection
    review_selection = AgentSelection(
        agent=other_agent,
        bypass=selection.bypass,
        model=selection.model,
        add_dirs=selection.add_dirs,
        dry_run=False,
        review_mode=False,
        loop_duration=None,
    )

    # Build review command with the prompt
    review_command = build_command(review_selection, [review_prompt])

    # Run review agent interactively
    try:
        review_result = subprocess.run(review_command)
        return review_result.returncode
    except KeyboardInterrupt:
        print(f"\n{accent}[REVIEW MODE] Review agent interrupted by user{reset}")
        return 130
    except Exception as e:
        print(f"\n{accent}[REVIEW MODE] Review agent failed: {e}{reset}", file=sys.stderr)
        return primary_exit_code


def run_loop_mode(selection: AgentSelection, extras: List[str], use_style: bool) -> None:
    """Run iterative improvement loop for specified duration."""
    accent = STYLE_CYAN if use_style else ""
    reset = STYLE_RESET if use_style else ""

    duration_minutes = selection.loop_duration or 60
    end_time = time.time() + (duration_minutes * 60)

    print(f"\n{accent}[LOOP MODE] Starting iterative improvements for {duration_minutes} minutes{reset}")
    print(f"{accent}[LOOP MODE] Agent: {AGENT_METADATA[selection.agent]['label']}{reset}")
    if selection.review_mode:
        print(f"{accent}[LOOP MODE] Review mode enabled with {AGENT_METADATA[get_other_agent(selection.agent)]['label']}{reset}")
    print()

    iteration = 1
    while time.time() < end_time:
        remaining = int((end_time - time.time()) / 60)
        print(f"\n{accent}{'='*60}{reset}")
        print(f"{accent}[LOOP MODE] Iteration {iteration} - {remaining} minutes remaining{reset}")
        print(f"{accent}{'='*60}{reset}\n")

        # Run primary agent interactively
        command = build_command(selection, extras)
        try:
            result = subprocess.run(command)
            exit_code = result.returncode
        except KeyboardInterrupt:
            print(f"\n{accent}[LOOP MODE] Interrupted by user. Exiting loop.{reset}")
            break
        except Exception as e:
            print(f"\n{accent}[LOOP MODE] Iteration {iteration} failed: {e}{reset}", file=sys.stderr)
            exit_code = 1

        print(f"\n{accent}[LOOP MODE] Iteration {iteration} completed with exit code {exit_code}{reset}")

        # Use review mode if enabled
        if selection.review_mode:
            if is_interactive():
                try:
                    proceed = ask_yes_no(
                        f"\n{accent}[LOOP MODE] Run review agent for this iteration?{reset} ",
                        default=True
                    )
                    if not proceed:
                        print(f"{accent}[LOOP MODE] Review skipped{reset}")
                    else:
                        other_agent = get_other_agent(selection.agent)
                        print(f"\n{accent}[LOOP MODE] Running review agent: {AGENT_METADATA[other_agent]['label']}{reset}\n")

                        review_selection = AgentSelection(
                            agent=other_agent,
                            bypass=selection.bypass,
                            model=selection.model,
                            add_dirs=selection.add_dirs,
                            dry_run=False,
                            review_mode=False,
                            loop_duration=None,
                        )
                        review_prompt = f"Review iteration {iteration}. Check for bugs and improvements. Fix any issues found."
                        review_command = build_command(review_selection, [review_prompt])

                        try:
                            subprocess.run(review_command)
                        except KeyboardInterrupt:
                            print(f"\n{accent}[LOOP MODE] Review interrupted{reset}")
                        except Exception as e:
                            print(f"\n{accent}[LOOP MODE] Review failed: {e}{reset}", file=sys.stderr)
                except KeyboardInterrupt:
                    print(f"\n{accent}[LOOP MODE] Interrupted by user. Exiting loop.{reset}")
                    break

        iteration += 1

        # Check if we have enough time for another iteration (minimum 5 minutes)
        remaining_time = end_time - time.time()
        if remaining_time < 300:
            print(f"\n{accent}[LOOP MODE] Less than 5 minutes remaining. Ending loop.{reset}")
            break

        # Ask if user wants to continue
        if is_interactive() and remaining_time > 0:
            try:
                continue_loop = ask_yes_no(
                    f"\n{accent}[LOOP MODE] Continue to next iteration?{reset} ",
                    default=True
                )
                if not continue_loop:
                    print(f"{accent}[LOOP MODE] User requested to stop loop{reset}")
                    break
            except KeyboardInterrupt:
                print(f"\n{accent}[LOOP MODE] Interrupted by user. Exiting loop.{reset}")
                break

    print(f"\n{accent}{'='*60}{reset}")
    print(f"{accent}[LOOP MODE] Completed {iteration - 1} iterations{reset}")
    print(f"{accent}{'='*60}{reset}")


def check_agent_version(agent_key: str) -> None:
    """Check and display the version of the agent binary."""
    try:
        details = AGENT_METADATA[agent_key]
    except KeyError:
        print(f"Agent inconnu: {agent_key}", file=sys.stderr)
        sys.exit(1)

    binary = details["binary"]
    binary_path = which_cached(binary)

    if not binary_path:
        print(f"{details['label']} is not installed.", file=sys.stderr)
        sys.exit(1)

    try:
        result = subprocess.run(
            [binary, "--version"],
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
        print(f"{details['label']} version:")
        print(result.stdout or result.stderr or "Version information not available")
    except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
        print(f"Could not check version: {exc}", file=sys.stderr)
        sys.exit(1)


def launch_agent(selection: AgentSelection, extras: List[str], use_style: bool) -> None:
    """Execute the chosen agent and exit with its return code."""
    # Handle special modes first
    if selection.loop_duration:
        run_loop_mode(selection, extras, use_style)
        return

    if selection.review_mode:
        exit_code = run_review_cycle(selection, extras, use_style)
        sys.exit(exit_code)
        return

    # Normal execution
    command = build_command(selection, extras)
    binary = command[0]

    binary_path = which_cached(binary)
    if not binary_path:
        print(
            f"Impossible de trouver la commande '{binary}'. Vérifiez l'installation.",
            file=sys.stderr,
        )
        sys.exit(1)

    if selection.dry_run:
        print("Dry-run mode: Would execute the following command:")
        print(" ".join(command))
        sys.exit(0)

    # Log the command before execution
    log_command_history(selection, extras)

    # Show progress message
    accent = STYLE_ACCENT if use_style else ""
    reset = STYLE_RESET if use_style else ""
    label = AGENT_METADATA[selection.agent]["label"]
    print(f"{accent}Launching {label}...{reset}")
    print(f"{accent}Lancement de {label}...{reset}")
    sys.stdout.flush()

    # Use os.execvp for direct execution (replaces current process)
    try:
        os.execvp(binary_path, command)
    except OSError as exc:
        print(
            f"Impossible de lancer {selection.agent}: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)


def styled(text: str, style: str, use_style: bool) -> str:
    """Apply ANSI styling conditionally."""
    if not use_style:
        return text
    return f"{style}{text}{STYLE_RESET}"


def display_summary(selection: AgentSelection, use_style: bool) -> None:
    """Show bilingual summary of choices."""
    header = styled("Agent Ready / Agent Prêt", STYLE_ACCENT, use_style)
    label = AGENT_METADATA.get(selection.agent, {}).get(
        "label", selection.agent.title()
    )
    agent_line = (
        f"- Agent: {label} | Agent choisi : {label}"
    )
    bypass_state_en = "ENABLED" if selection.bypass else "DISABLED"
    bypass_state_fr = "ACTIVÉ" if selection.bypass else "DÉSACTIVÉ"
    bypass_line = (
        f"- Bypass: {bypass_state_en} | Bypass : {bypass_state_fr}"
    )
    remark = (
        "WARNING: Read the official docs before enabling bypass.\n"
        "ATTENTION : relisez la documentation officielle avant d'activer le bypass."
    )
    if selection.bypass:
        bypass_line = styled(bypass_line, STYLE_WARNING, use_style)
        remark = styled(remark, STYLE_WARNING, use_style)
    else:
        bypass_line = styled(bypass_line, STYLE_DIM, use_style)
    footer = styled("Bon travail / Happy coding!", STYLE_SUCCESS, use_style)
    print(header)
    print(agent_line)
    print(bypass_line)
    if selection.model:
        print(f"- Model: {selection.model} | Modèle : {selection.model}")
    if selection.add_dirs:
        joined_dirs = ", ".join(selection.add_dirs)
        print(
            f"- Extra dirs: {joined_dirs} | Répertoires ajoutés : {joined_dirs}"
        )
    if selection.review_mode:
        review_msg = styled("REVIEW MODE ENABLED", STYLE_CYAN, use_style)
        print(f"- {review_msg}")
    if selection.loop_duration:
        loop_msg = styled(f"LOOP MODE: {selection.loop_duration} minutes", STYLE_CYAN, use_style)
        print(f"- {loop_msg}")
    if selection.dry_run:
        dry_run_msg = styled("DRY-RUN MODE", STYLE_WARNING, use_style)
        print(f"- {dry_run_msg}")
    print(remark)
    print(footer)
    sys.stdout.flush()


def ask_yes_no(question: str, default: bool) -> bool:
    """Prompt the user with a bilingual yes/no question."""
    yes_values = {"y", "yes", "o", "oui"}
    no_values = {"n", "no", "non"}
    default_choice = "y" if default else "n"
    prompt_suffix = f"[{'Y' if default else 'y'}/{'n' if default else 'N'} | {'O' if default else 'o'}/N] : "
    while True:
        choice = prompt_with_timeout(f"{question}{prompt_suffix}").strip().lower()
        if not choice:
            choice = default_choice
        if choice in yes_values:
            return True
        if choice in no_values:
            return False
        print(
            "Merci de répondre par y/o pour Oui ou n pour Non.\n"
            "Please answer y for Yes or n for No."
        )


def determine_install_directory() -> Path:
    """Pick an installation directory, preferring PATH-aware locations."""
    env_dir = os.environ.get("AGENT_INSTALL_DIR")
    if env_dir:
        return Path(env_dir).expanduser()
    xdg_dir = os.environ.get("XDG_BIN_HOME")
    if xdg_dir:
        return Path(xdg_dir).expanduser()
    try:
        is_root = os.geteuid() == 0
    except AttributeError:
        is_root = False
    if is_root:
        return Path("/usr/local/bin")
    return Path.home() / ".local/bin"


def perform_install() -> None:
    """Install the current script into a PATH directory."""
    import shutil

    script_path = Path(__file__).resolve()
    target_dir = determine_install_directory()
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / "agent"
    try:
        if target_path.exists() or target_path.is_symlink():
            try:
                if target_path.resolve() == script_path:
                    print(
                        f"Agent déjà disponible via {target_path}. "
                        "Rien à faire."
                    )
                    return
            except OSError:
                # Unable to resolve (dangling symlink), will replace it.
                pass
            target_path.unlink()
    except PermissionError as exc:
        print(
            f"Impossible de remplacer {target_path}: {exc}",
            file=sys.stderr,
        )
        sys.exit(1)

    installed_via = "symlink"
    try:
        target_path.symlink_to(script_path)
    except OSError:
        installed_via = "copy"
        try:
            shutil.copy2(script_path, target_path)
            os.chmod(target_path, 0o755)
        except OSError as exc:
            print(
                f"Impossible de copier le script vers {target_path}: {exc}",
                file=sys.stderr,
            )
            sys.exit(1)

    print(
        f"Agent installé dans {target_path} "
        f"({'lien symbolique' if installed_via == 'symlink' else 'copie'})."
    )
    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    if str(target_dir) not in path_entries:
        print(
            "⚠️ Ajoutez ce dossier à votre PATH si besoin :\n"
            f"   export PATH=\"{target_dir}:$PATH\"",
            file=sys.stderr,
        )
    sys.exit(0)


def ensure_agent_ready(agent_key: str) -> None:
    """Ensure required binaries exist, offering npm installs when feasible."""
    try:
        details = AGENT_METADATA[agent_key]
    except KeyError:
        print(f"Agent inconnu: {agent_key}", file=sys.stderr)
        sys.exit(1)
    binary = details["binary"]
    if which_cached(binary):
        return
    label = details["label"]
    npm_path = which_cached("npm")
    print(
        f"{label} CLI n'est pas installée (commande '{binary}' introuvable).",
        file=sys.stderr,
    )
    if npm_path is None:
        print(
            "npm n'est pas disponible, impossible d'installer automatiquement.\n"
            "Installez Node.js (qui inclut npm) en suivant la documentation officielle :\n"
            f"- Node.js package manager guide : {NODE_DOC_URL}\n"
            f"- Documentation {label} : {details['docs_url']}",
            file=sys.stderr,
        )
        sys.exit(1)
    question = (
        f"Installer {label} via npm (`npm install -g {details['npm_package']}`) maintenant ? "
    )
    if not ask_yes_no(question, default=False):
        print(
            "Installation annulée. Consultez la documentation pour les étapes détaillées :\n"
            f"- {details['docs_url']}",
            file=sys.stderr,
        )
        sys.exit(1)
    print(f"Installation de {label} en cours…")
    result = subprocess.run(
        [
            npm_path,
            "install",
            "-g",
            details["npm_package"],
        ],
        check=False,
    )
    if result.returncode != 0:
        print(
            "L'installation npm a échoué. Vérifiez vos permissions ou consultez la documentation :\n"
            f"- {details['docs_url']}",
            file=sys.stderr,
        )
        sys.exit(result.returncode or 1)

    # Clear cache after installation
    compute_search_path.cache_clear()
    which_cached.cache_clear()

    if which_cached(binary):
        print(f"{label} installé avec succès.")
        return
    npm_bin_dir = os.popen(f"{npm_path} bin -g").read().strip()
    print(
        f"L'installation semble terminée mais '{binary}' reste introuvable.\n"
        "Assurez-vous que le dossier global npm est dans votre PATH :\n"
        f"- npm bin -g -> {npm_bin_dir or '(non déterminé)'}",
        file=sys.stderr,
    )
    sys.exit(1)


def main(argv: Optional[List[str]] = None) -> None:
    """Entrypoint for CLI or module usage."""
    parser = build_parser()
    namespace, extras = parser.parse_known_args(argv)
    if extras and extras[0] == "--":
        extras = extras[1:]

    if namespace.install:
        perform_install()
        return

    # Load configurations
    config = load_config()
    env_config = load_env_config()

    # Determine if we should use styling
    use_style = not namespace.quiet and supports_color()

    # Handle version check
    if namespace.check_version:
        # Need to determine which agent first
        agent = namespace.agent or env_config.get("agent") or config.default_agent
        if not agent:
            if is_interactive():
                agent = prompt_agent(config, use_style)
            else:
                print("Error: No agent specified for version check.", file=sys.stderr)
                sys.exit(1)
        check_agent_version(agent)
        return

    # Resolve selection
    selection = resolve_selection(namespace, config, env_config, use_style)

    # Save defaults if requested
    if namespace.save_defaults:
        new_config = AgentConfig(
            default_agent=selection.agent,
            default_bypass=selection.bypass,
            default_model=selection.model,
        )
        save_config(new_config)
        print(f"Configuration saved to {CONFIG_FILE}")
        print(f"Configuration sauvegardée dans {CONFIG_FILE}")
        if selection.dry_run:
            return

    # Ensure agent is ready
    ensure_agent_ready(selection.agent)

    # For review mode, also ensure the other agent is ready
    if selection.review_mode:
        ensure_agent_ready(get_other_agent(selection.agent))

    # Display summary
    display_summary(selection, use_style)

    # Launch agent
    launch_agent(selection, extras, use_style)


if __name__ == "__main__":
    main()
