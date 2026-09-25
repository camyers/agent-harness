![Agent Harness: a tool loop, guardrails, provider switching and a run viewer, built from scratch in Python. A terminal shows the harness fixing failing tests, with a blocked read of .env and an approval prompt before the edit.](docs/images/banner.png)

# agent-harness

A small agent harness built from scratch in Python, as a way to learn how the tool-calling loop and its guardrails actually work. It talks to models through Groq's free, OpenAI-compatible API, so you can follow along without paying for anything.

![The React run viewer replaying a build doctor run: the task, token and timing stats, each tool call, the approved fix to cart.py and the passing tests.](docs/images/run-viewer.jpg)

This is a learning project. It follows a phase-by-phase plan from an accompanying blog post, and each phase gets a git tag when it's finished so you can check out the code as it stood at that point.

## Status

Phase 0 is done: environment setup and a single completion call against Groq. The rest is planned but not written yet.

0. Environment and a bare completion call (done)
1. The tool loop
2. Guardrails and sandboxing
3. Provider abstraction
4. Observability UI, built in React
5. A real use case

## Getting started

You'll need Python 3.9 or newer, Git, and a free Groq account.

### 1. Clone the repo

```bash
git clone https://github.com/camyers/agent-harness.git
cd agent-harness
```

If you've forked it, use your own fork's URL instead.

### 2. Create a virtual environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install the packages

```bash
pip install openai python-dotenv
```

The `openai` client works against Groq because Groq's API is OpenAI-compatible. `python-dotenv` loads your API key from a file so it stays out of the code.

### 4. Add your Groq API key

Sign up at [console.groq.com](https://console.groq.com) (no card needed) and create a key on the [API Keys page](https://console.groq.com/keys). The key is only shown once, so copy it before closing the page.

Then copy the example env file and paste your key in:

```bash
cp .env.example .env
```

On Windows, use `copy .env.example .env`. Open `.env` and set:

```
GROQ_API_KEY=gsk_your_key_here
```

`.env` is listed in `.gitignore`. Keep it that way, and never commit a real key.

### 5. Run it

```bash
python test_groq.py
python backend.py
```

Each one should print a short greeting from the model. If it does, the connection works and you're ready for the next phase.

## What's in the repo

`backend.py` has a `complete(prompt, backend="groq")` function. It only supports Groq for now, but taking a `backend` argument means phase 3 can add providers without a rewrite.

`test_groq.py` is a standalone script that makes one request, useful for checking your key and connection before touching anything else.

`.env.example` is the template for your local `.env` file.

## Troubleshooting

A 401 error, or a `KeyError: 'GROQ_API_KEY'`, usually means the `.env` file wasn't found or the key was copied with a stray space. Check that `.env` sits in the project root next to `backend.py` and is named exactly that.

A `model_not_found` 404 means Groq has retired the model, not that your setup is broken. Free-tier models change without much warning. Check [Groq's model list](https://console.groq.com/docs/models) and swap the new name into `backend.py` and `test_groq.py`. The default is `openai/gpt-oss-120b`, and `openai/gpt-oss-20b` is a faster option.

## Contributing

Issues and pull requests are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for how this project works and what kinds of changes fit best.

## License

[MIT](LICENSE)
