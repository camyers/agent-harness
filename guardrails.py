import json
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LOG_FILE = ROOT / "runs.jsonl"

NEEDS_APPROVAL = {"run_shell", "write_file", "replace_in_file"}
OFF_LIMITS = {".env", ".git"}
ALLOWED_COMMANDS = {
    "dir",
    "ls",
    "pwd",
    "git status",
    "git log --oneline",
    "git diff",
    "git branch",
    "python -m unittest discover -s examples/shop",
}

def check_edit(args: dict) -> str | None:
    path = args.get("path", "")
    problem = check_path(path)
    if problem:
        return problem
    if Path(path).name.startswith("test_"):
        return "test files are read-only. Fix the source code, not the test"
    text = (ROOT / path).read_text(encoding="utf-8")
    count = text.count(args.get("old", ""))
    if count == 0:
        return "old text not found. Read the file again and copy the lines exactly"
    if count > 1:
        return f"old text appears {count} times. Include more surrounding lines so it matches once"
    return None

def check(name: str, args: dict) -> str | None:
    """Return the reason a call is refused, or None if it can go ahead."""
    if name in ("read_file", "list_dir", "write_file"):
        return check_path(args.get("path", "."))
    if name == "replace_in_file":
        return check_edit(args)
    if name in ("read_file", "list_dir", "write_file"):
        return check_path(args.get("path", "."))
    if name == "run_shell":
        return check_command(args.get("command", ""))
    return f"unknown tool: {name}"


def check_path(path: str) -> str | None:
    full = (ROOT / path).resolve()
    if full != ROOT and ROOT not in full.parents:
        return "that path is outside the project folder"
    if any(part.lower() in OFF_LIMITS for part in full.relative_to(ROOT).parts):
        return "that file or folder is off limits"
    return None


def check_command(command: str) -> str | None:
    if " ".join(command.split()).lower() in ALLOWED_COMMANDS:
        return None
    allowed = ", ".join(sorted(ALLOWED_COMMANDS))
    return f"that command is not on the allowlist. Allowed: {allowed}"


def log(event: dict) -> None:
    line = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"), **event}
    with LOG_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(line) + "\n")