# Contributing

Thanks for taking a look. This repo is mainly a learning project: the code is written phase by phase alongside a blog post, and the goal is that every line is something the author can explain. Contributions are welcome with that in mind.

## What fits well

- Fixing typos, unclear wording, or wrong steps in the README and setup instructions
- Setup notes for platforms that aren't covered yet, such as macOS, Linux, or WSL
- Bug reports and fixes for code that's already in the repo
- Updating a model name when Groq retires one
- Questions and ideas, opened as issues

Large features that jump ahead of the current phase, new dependencies, and rewrites that change the structure of the walkthrough are less likely to be merged, since they pull the repo away from the plan it's teaching. If you're unsure, open an issue first and ask.

## Before you open a pull request

1. For anything bigger than a small fix, open an issue to talk it through first.
2. Fork the repo and create a branch from `main`, for example `git checkout -b fix/model-name`.
3. Keep the change small and focused. One topic per pull request is easier to review.
4. Run the code you touched. `python test_groq.py` and `python backend.py` need a Groq API key in a local `.env` file, and your pull request should say what you ran.
5. Never commit `.env`, API keys, or the `.venv` folder. Check `git status` before you commit.
6. Write commit messages in the imperative, for example "Update model name in test_groq.py".

## Pull requests

Say what changed and why. If an AI assistant helped, that's fine, but read every line and be able to explain it. That's the same bar the project holds itself to.

## Style

Python follows PEP 8. Prefer code that's easy to read over code that's clever. There's no formatter or linter enforced yet. Docs are plain prose with sentence case headings.

## Reporting bugs

Include what you ran, your OS and Python version, and the full error output. Remove your API key from anything you paste. If you accidentally publish a key, revoke it in the Groq console right away.

For a security problem, use GitHub's private vulnerability reporting on the Security tab if it's enabled. Otherwise open an issue without exploit details and ask for a private way to share them.

## License

By contributing, you agree that your contributions will be licensed under the [MIT License](LICENSE).

Please be kind and constructive in issues and reviews.
