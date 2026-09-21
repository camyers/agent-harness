from dotenv import load_dotenv
from openai import OpenAI
import os

load_dotenv()

def complete(prompt: str, backend: str = "groq") -> str:
    if backend == "groq":
        client = OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1",
        )
        response = client.chat.completions.create(
            model="openai/gpt-oss-120b",
            messages=[{"role": "user", "content": prompt}],
        )
        return response.choices[0].message.content

    raise ValueError(f"unknown backend: {backend}")

def chat(messages: list, tools: list | None = None, backend: str = "groq"):
    if backend == "groq":
        client = OpenAI(
            api_key=os.environ["GROQ_API_KEY"],
            base_url="https://api.groq.com/openai/v1",
        )
        kwargs = {"model": "openai/gpt-oss-120b", "messages": messages}
        if tools:
            kwargs["tools"] = tools
        return client.chat.completions.create(**kwargs).choices[0].message

    raise ValueError(f"unknown backend: {backend}")


if __name__ == "__main__":
    print(complete("Say hello in one sentence."))