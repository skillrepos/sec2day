"""
Lab 9 -- A tiny coding agent. VULNERABLE ON PURPOSE.

It ingests repo files (README, CONTRIBUTING, and .agent-config.json "hooks") as
trusted instructions, then runs whatever commands it's told to -- including the
attacker's payload hidden in CONTRIBUTING.md and the config's preToolUse hook.

  python mini_coder.py

This DEMO does not actually execute the commands (that would be dangerous); it
prints "WOULD RUN: ..." so you can see exactly what a real agent would have run.
"""
import json
import os
import sys
sys.path.insert(0, "..")
from common.llm import backend_banner

REPO = os.path.join(os.path.dirname(__file__), "sample_repo")


def read_repo_instructions():
    """Naive: treat every repo doc AND the config hooks as instructions."""
    parts = []
    for name in ("README.md", "CONTRIBUTING.md"):
        parts.append(open(os.path.join(REPO, name)).read())
    cfg = json.load(open(os.path.join(REPO, ".agent-config.json")))
    hooks = [cfg.get("preToolUse"), cfg.get("postEdit")]
    return "\n".join(parts), [h for h in hooks if h]


def run(cmd):
    print(f"  WOULD RUN: {cmd}")


def main():
    print(backend_banner())
    instructions, hooks = read_repo_instructions()
    print("Agent ingested repo instructions and config hooks as trusted input.\n")
    # A real agent would let the model plan from these instructions and call a
    # run-command tool. The hooks it found get run automatically first:
    for h in hooks:
        run(h)
    # ...and any command embedded in CONTRIBUTING.md would be planned and run too.
    for line in instructions.splitlines():
        if "curl" in line or "id_rsa" in line:
            print(f"  (agent picked up embedded instruction): {line.strip()[:90]}")
    print("\nEvery one of those came from repo content an attacker can edit.")


if __name__ == "__main__":
    main()
