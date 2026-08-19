"""
Lab 9 -- Command policy for a coding agent. (Imported by the secure coder.)

A coding agent runs shell commands. This policy decides which commands are safe
to run automatically. It combines an allow-list (only these binaries) with a
deny-scan (block obviously dangerous patterns even if the binary is allowed).
"""
import re
import shlex

ALLOWED_BINARIES = {"python", "python3", "pytest", "pip", "ls", "cat", "echo", "git"}

DANGEROUS_PATTERNS = [
    r"\bcurl\b", r"\bwget\b", r"\|\s*(sh|bash)\b",   # download-and-run
    r"\brm\s+-rf\b", r"\bssh\b", r"id_rsa", r"\.env\b",
    r"/etc/passwd", r"nc\b", r"base64\b.*\|\s*(sh|bash)",
]


def evaluate(command):
    """Return (ok, reason). Deny by default outside the allow-list."""
    for pat in DANGEROUS_PATTERNS:
        if re.search(pat, command, re.IGNORECASE):
            return False, f"blocked dangerous pattern: {pat}"
    try:
        binary = shlex.split(command)[0]
    except (ValueError, IndexError):
        return False, "unparseable command"
    binary = binary.rsplit("/", 1)[-1]
    if binary not in ALLOWED_BINARIES:
        return False, f"binary '{binary}' not on allow-list"
    return True, "ok"
