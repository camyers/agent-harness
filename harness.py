import json
import sys

from backend import chat
from tools import REGISTRY, TOOLS

MAX_STEPS = 10


def run(task: str) -> str:
    messages = [{"role": "user", "content": task}]

    for step in range(MAX_STEPS):
        message = chat(messages, tools=TOOLS)

        if not message.tool_calls:
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
            print(f"[{step + 1}] {name} {call.function.arguments}")
            try:
                args = json.loads(call.function.arguments)
                result = REGISTRY[name](**args)
            except Exception as error:
                result = f"error: {error}"
            messages.append(
                {"role": "tool", "tool_call_id": call.id, "content": result}
            )

    return "stopped: hit the step limit"


if __name__ == "__main__":
    print(run(sys.argv[1]))