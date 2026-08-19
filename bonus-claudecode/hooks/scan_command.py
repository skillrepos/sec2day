#!/usr/bin/env python3
"""
Bonus lab -- Claude Code PreToolUse hook: scan a proposed shell command and block
dangerous ones before they run. Claude Code passes the tool call as JSON on stdin;
this hook exits non-zero (with a reason on stderr) to block, or zero to allow.

Wire it up in settings.json (see README-bonus.md). This is the same allow-list /
deny-scan idea as Lab 9, applied to a real coding agent.
"""
import json
import re
import sys

DANGEROUS = [
    r"\bcurl\b.*\|\s*(sh|bash)", r"\bwget\b.*\|\s*(sh|bash)",
    r"\brm\s+-rf\s+/", r"id_rsa", r"/etc/passwd", r"\bnc\b\s",
    r"base64\b.*\|\s*(sh|bash)", r">\s*~/\.ssh", r"\.env\b",
]


def main():
    try:
        event = json.load(sys.stdin)
    except json.JSONDecodeError:
        sys.exit(0)  # nothing to scan
    command = (event.get("tool_input", {}) or {}).get("command", "")
    for pat in DANGEROUS:
        if re.search(pat, command, re.IGNORECASE):
            print(f"BLOCKED by security hook: matched /{pat}/ in command:\n  {command}",
                  file=sys.stderr)
            sys.exit(2)  # non-zero -> Claude Code blocks the tool call
    sys.exit(0)


if __name__ == "__main__":
    main()
