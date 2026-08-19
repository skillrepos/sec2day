"""
Lab 5 -- A reusable guardrails pipeline. SKELETON.

Input guards run before the model; output guards run after. Each guard returns
(ok, reason, maybe_fixed_text). The pipeline short-circuits on the first input
guard that fails, and always runs output guards so redaction still happens.

Merge the gaps from extra/guards_complete.txt, then run the red-team harness:
  python redteam.py guarded
"""
import re

STAFF_CODE = "SPRING-STAFF-42"
ALLOWED_TOPICS = ["order", "return", "refund", "shipping", "ship", "product",
                  "account", "password", "delivery", "tracking", "omnitech", "item"]
JAILBREAK_PATTERNS = [
    r"ignore (all |your |previous )?(instructions|rules)",
    r"you are now|no rules|no restrictions|devbot",
    r"system (update|override|prompt)",
    r"reveal|print your (system )?prompt|discount code",
]
MAX_INPUT_CHARS = 600


def guard_jailbreak(text):
    """Reject text that matches a known jailbreak/override pattern."""
    # TODO (gap 1): if any JAILBREAK_PATTERNS matches (case-insensitive), return
    #   (False, "jailbreak pattern", text). Otherwise (True, "ok", text).
    raise NotImplementedError("merge gap 1")


def guard_length(text):
    """Reject oversized input (cheap defense against prompt stuffing)."""
    if len(text) > MAX_INPUT_CHARS:
        return False, f"input too long ({len(text)} chars)", text
    return True, "ok", text


def guard_output_secret(text):
    """Redact the staff code and its de-dashed variant from any output."""
    # TODO (gap 2): replace STAFF_CODE and a dash-separated variant with [REDACTED];
    #   return (True, "redacted" if changed else "ok", cleaned_text).
    raise NotImplementedError("merge gap 2")


INPUT_GUARDS = [guard_length, guard_jailbreak]
OUTPUT_GUARDS = [guard_output_secret]


def check_input(text):
    """Run all input guards. Return (ok, reason)."""
    for g in INPUT_GUARDS:
        ok, reason, _ = g(text)
        if not ok:
            return False, reason
    return True, "ok"


def apply_output_guards(text):
    """Run all output guards, chaining any text fixes. Return fixed text."""
    for g in OUTPUT_GUARDS:
        _ok, _reason, text = g(text)
    return text
