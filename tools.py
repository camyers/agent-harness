import subprocess
from pathlib import Path

MAX_CHARS = 4000


def read_file(path: str) -> str:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    return text[:MAX_CHARS]


def list_dir(path: str = ".") -> str:
    entries = sorted(Path(path).iterdir())
    return "\n".join(p.name + ("/" if p.is_dir() else "") for p in entries)


def run_shell(command: str) -> str:
    result = subprocess.run(
        command, shell=True, capture_output=True, text=True, errors="replace"
    )
    return (result.stdout + result.stderr)[:MAX_CHARS]


REGISTRY = {
    "read_file": read_file,
    "list_dir": list_dir,
    "run_shell": run_shell,
}

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read a text file and return its contents.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "File path, relative to the project folder."}
                },
                "required": ["path"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_dir",
            "description": "List the files and folders in a directory. Folders end with a slash.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "Directory path. Defaults to the project folder."}
                },
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Run a shell command and return its output.",
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {"type": "string", "description": "The command to run."}
                },
                "required": ["command"],
            },
        },
    },
]