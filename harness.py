import json
import sys
import time
import difflib

from backend import ToolCallRejected, get_provider
from guardrails import NEEDS_APPROVAL, check, log
from tools import REGISTRY, TOOLS

MAX_STEPS = 10
SYSTEM_PROMPT = "You are a coding assistant. When a task needs a tool, call the tool right away. Only call the tools provided in this request. Do not announce what you are about to do, and never ask the user for permission in your reply. The harness asks for approval by itself."

DENIED_MESSAGE = "denied: the user said no. Do not retry this call or a variation of it. Carry on without it if you can, or stop and explain what you wanted to do and why."

provider = get_provider()


def approve(name: str, args: dict) -> bool:
    print(f"\nThe model wants to use {name}:")
    if name == "replace_in_file":
        print(show_diff(args))
    else:
        for key, value in args.items():
            print(f"  {key}: {value}")
    return input("Allow? [y/N] ").strip().lower() == "y"

def show_diff(args: dict) -> str:
    lines = difflib.unified_diff(
        args.get("old", "").splitlines(),
        args.get("new", "").splitlines(),
        fromfile=args.get("path", ""),
        tofile=args.get("path", ""),
        lineterm="",
    )
    return "\n".join(lines)

def execute(name: str, args: dict, denied: set) -> tuple[str, str]:
    problem = check(name, args)
    if problem:
        return "blocked", f"blocked: {problem}"
    key = name + json.dumps(args, sort_keys=True)
    if key in denied:
        return "blocked", "blocked: the user already said no to this exact call. Do not ask again."
    if name in NEEDS_APPROVAL and not approve(name, args):
        denied.add(key)
        return "denied", DENIED_MESSAGE
    try:
        return "ok", REGISTRY[name](**args)
    except Exception as error:
        return "error", f"error: {error}"


def run(task: str, context: str = "", run_id: str | None = None) -> str:
    run_id = run_id or time.strftime("%Y%m%d-%H%M%S")
    log({"run_id": run_id, "event": "task", "task": task})
    prompt = task
    if context:
        log({"run_id": run_id, "event": "context", "text": context})
        prompt = f"{task}\n\n{context}"
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]
    total_tokens = 0
    denied = set()
    total_latency_ms = 0

    for step in range(MAX_STEPS):
        try:
            result = provider.complete(messages, tools=TOOLS)
        except ToolCallRejected as error:
            print(f"[{step + 1}] rejected tool call: {error}")
            log({"run_id": run_id, "event": "rejected", "step": step + 1, "generation": str(error)})
            messages.append(
                {
                    "role": "user",
                    "content": f"Your last tool call was rejected because it named a tool that doesn't exist or had malformed arguments: {error}. Use only these tools: {', '.join(REGISTRY)}.",
                }
            )
            continue
        message = result.message
        total_tokens += result.prompt_tokens + result.completion_tokens
        total_latency_ms += result.latency_ms
        log(
            {
                "run_id": run_id,
                "event": "usage",
                "step": step + 1,
                "model": result.model,
                "prompt_tokens": result.prompt_tokens,
                "completion_tokens": result.completion_tokens,
                "latency_ms": result.latency_ms,
            }
        )

        if not message.tool_calls:
            log({"run_id": run_id, "event": "answer", "content": message.content})
            print(f"\n{result.model}: {total_tokens} tokens, {total_latency_ms}ms total")
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
                outcome, result_text = execute(name, args, denied)
            except Exception as error:
                args, outcome, result_text = call.function.arguments, "error", f"error: {error}"
            print(f"[{step + 1}] {name} {call.function.arguments} -> {outcome}")
            log(
                {
                    "run_id": run_id,
                    "event": "tool_call",
                    "step": step + 1,
                    "tool": name,
                    "args": args,
                    "outcome": outcome,
                    "result": result_text[:500],
                }
            )
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result_text}
            )

    log({"run_id": run_id, "event": "stopped", "reason": "step limit"})
    return "stopped: hit the step limit"


if __name__ == "__main__":
    print(run(sys.argv[1]))