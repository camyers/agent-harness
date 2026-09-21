from backend import chat
from tools import TOOLS

message = chat(
    [{"role": "user", "content": "What files are in the current directory?"}],
    tools=TOOLS,
)

print("content:", message.content)
print("tool_calls:", message.tool_calls)