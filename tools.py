import subprocess

from guardrails import ALLOWED_COMMANDS, ROOT

MAX_CHARS = 4000
TIMEOUT_SECONDS = 10


def read_file(path: str) -> str:
    text = (ROOT / path).read_text(encoding="utf-8", errors="replace")
    return text[:MAX_CHARS]


def list_dir(path: str = ".") -> str:
    entries = sorted((ROOT / path).iterdir())
    return "\n".join(p.name + ("/" if p.is_dir() else "") for p in entries)


def write_file(path: str, content: str) -> str:
    target = ROOT / path
    if target.exists():
        raise FileExistsError("that file already exists, and write_file only creates new files")
    target.write_text(content, encoding="utf-8")
    return f"wrote {len(content)} characters to {path}"


def run_shell(command: str) -> str:
    result = subprocess.run(
        command,
        shell=True,
        capture_output=True,
        text=True,
        errors="replace",
        cwd=ROOT,
        timeout=TIMEOUT_SECONDS,
    )
    return (result.stdout + result.stderr)[:MAX_CHARS]


REGISTRY = {
    "read_file": read_file,
    "list_dir": list_dir,
    "write_file": write_file,
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
            "name": "write_file",
            "description": "Create a new text file. It cannot overwrite an existing file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {"type": "string", "description": "New file path, relative to the project folder."},
                    "content": {"type": "string", "description": "The text to write."},
                },
                "required": ["path", "content"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_shell",
            "description": "Run a shell command and return its output. Only these exact commands are allowed: " + ", ".join(sorted(ALLOWED_COMMANDS)),
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