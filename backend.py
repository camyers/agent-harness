import os
import time
from typing import Protocol

from dotenv import load_dotenv
from openai import BadRequestError, OpenAI

load_dotenv()

class ToolCallRejected(Exception):
    """The provider refused a malformed tool call before the harness saw it."""

class Completion:
    """One reply from a provider, with what it cost to get it."""

    def __init__(self, message, model: str, prompt_tokens: int, completion_tokens: int, latency_ms: int):
        self.message = message
        self.model = model
        self.prompt_tokens = prompt_tokens
        self.completion_tokens = completion_tokens
        self.latency_ms = latency_ms


class Provider(Protocol):
    def complete(self, messages: list, tools: list | None = None) -> Completion: ...


class GroqProvider:
    def __init__(self, model: str | None = None):
        self.model = model or os.environ.get("MODEL", "openai/gpt-oss-120b")
        self.client = OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1",
        )

    def complete(self, messages: list, tools: list | None = None) -> Completion:
        kwargs = {"model": self.model, "messages": messages}
        if tools:
            kwargs["tools"] = tools

        start = time.perf_counter()
        try:
            response = self.client.chat.completions.create(**kwargs)
        except BadRequestError as error:
            if error.code != "tool_use_failed":
                raise
            body = error.body if isinstance(error.body, dict) else {}
            raise ToolCallRejected(body.get("failed_generation", str(error))) from error
        latency_ms = round((time.perf_counter() - start) * 1000)

        return Completion(
            message=response.choices[0].message,
            model=self.model,
            prompt_tokens=response.usage.prompt_tokens,
            completion_tokens=response.usage.completion_tokens,
            latency_ms=latency_ms,
        )


PROVIDERS = {"groq": GroqProvider}


def get_provider(name: str | None = None) -> Provider:
    name = name or os.environ.get("BACKEND", "groq")
    if name not in PROVIDERS:
        raise ValueError(f"unknown backend: {name}")
    return PROVIDERS[name]()


if __name__ == "__main__":
    provider = get_provider()
    result = provider.complete([{"role": "user", "content": "Say hello in one sentence."}])
    print(result.message.content)