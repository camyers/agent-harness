import json
import sys
import time

from backend import chat
from guardrails import NEEDS_APPROVAL, check, log
from tools import REGISTRY, TOOLS

MAX_STEPS = 10
SYSTEM_PROMPT = "You are a coding assistant. When a task needs a tool, call the tool right away. Do not announce what you are about to do, and never ask the user for permission in your reply. The harness asks for approval by itself."

def approve(name: str, args: dict) -> bool:
    print(f"\nThe model wants to use {name}:")
    for key, value in args.items():
        print(f"  {key}: {value}")
    return input("Allow? [y/N] ").strip().lower() == "y"


def execute(name: str, args: dict) -> tuple[str, str]:
    problem = check(name, args)
    if problem:
        return "blocked", f"blocked: {problem}"
    if name in NEEDS_APPROVAL and not approve(name, args):
        return "denied", "denied: the user said no"
    try:
        return "ok", REGISTRY[name](**args)
    except Exception as error:
        return "error", f"error: {error}"


def run(task: str) -> str:
    run_id = time.strftime("%Y%m%d-%H%M%S")
    log({"run_id": run_id, "event": "task", "task": task})
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": task},
    ]

    for step in range(MAX_STEPS):
        message = chat(messages, tools=TOOLS)

        if not message.tool_calls:
            log({"run_id": run_id, "event": "answer", "content": message.content})
            return message.content

        messages.append(
            {
                "role": "assistant",
                "content": message.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in message.tool_calls
                ],
            }
        )

        for call in message.tool_calls:
            name = call.function.name
            try:
                args = json.loads(call.function.arguments)
                outcome, result = execute(name, args)
            except Exception as error:
                args, outcome, result = call.function.arguments, "error", f"error: {error}"
            print(f"[{step + 1}] {name} {call.function.arguments} -> {outcome}")
            log(
                {
                    "run_id": run_id,
                    "event": "tool_call",
                    "step": step + 1,
                    "tool": name,
                    "args": args,
                    "outcome": outcome,
                    "result": result[:500],
                }
            )
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )

    log({"run_id": run_id, "event": "stopped", "reason": "step limit"})
    return "stopped: hit the step limit"


if __name__ == "__main__":
    print(run(sys.argv[1]))