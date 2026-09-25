import subprocess
import time

from guardrails import ROOT, log
from harness import run

TEST_COMMAND = "python -m unittest discover -s examples/shop"
MAX_LOG_CHARS = 3000
TASK = (
    "The test suite for examples/shop is failing. Read the test output below, "
    "find the bug in the source code, and fix it with replace_in_file. "
    "Then explain the cause and the fix in two or three sentences."
)


def run_tests() -> tuple[bool, str]:
    result = subprocess.run(
        TEST_COMMAND, shell=True, capture_output=True, text=True, errors="replace", cwd=ROOT
    )
    return result.returncode == 0, (result.stdout + result.stderr)[-MAX_LOG_CHARS:]


def main() -> None:
    passed, output = run_tests()
    if passed:
        print("The tests already pass. Nothing to fix.")
        return

    run_id = time.strftime("%Y%m%d-%H%M%S")
    context = f"Command: {TEST_COMMAND}\n\nOutput:\n{output}"
    print(run(TASK, context=context, run_id=run_id))

    passed, output = run_tests()
    log({"run_id": run_id, "event": "verify", "passed": passed, "output": output})
    print("\nTests pass now." if passed else f"\nTests still fail:\n{output}")


if __name__ == "__main__":
    main()