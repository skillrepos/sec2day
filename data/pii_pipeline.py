"""
Lab 4 (part 2) -- Tokenize PII before the model or the logs ever see it. SKELETON.

The pattern: detect PII, replace each value with a stable token, keep a private
vault mapping token->value in the application, send only tokenized text to the
model, then de-tokenize the model's reply for the user. The model does its job
without ever holding a card number or SSN.

Merge the gaps from extra/pii_pipeline_complete.txt, then:
  python pii_pipeline.py
"""
import json
import os
import re

RECORDS = json.load(open(os.path.join(os.path.dirname(__file__), "customer_records.json")))

PII_PATTERNS = {
    "CARD":  r"\b(?:\d[ -]?){13,16}\b",
    "SSN":   r"\b\d{3}-\d{2}-\d{4}\b",
    "EMAIL": r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b",
    "PHONE": r"\b\d{3}-\d{3}-\d{4}\b",
}


class Vault:
    """Holds token<->value mappings. Lives in the app, never sent to the model."""

    def __init__(self):
        self._to_token = {}
        self._to_value = {}
        self._counter = {}

    def tokenize(self, kind, value):
        """Return a stable token like <CARD_1> for this value, creating one if new."""
        # TODO (gap 1): if value already tokenized, return its token; otherwise
        #   make a token f"<{kind}_{n}>" with an incrementing per-kind counter,
        #   store both directions, and return it.
        raise NotImplementedError("merge gap 1")

    def detokenize(self, text):
        """Replace any tokens in text with their original values."""
        for token, value in self._to_value.items():
            text = text.replace(token, value)
        return text


def redact(text, vault):
    """Replace every PII match in text with a vault token. Returns tokenized text."""
    # TODO (gap 2): for each (kind, pattern) in PII_PATTERNS, re.sub every match
    #   with vault.tokenize(kind, match). Return the fully tokenized text.
    raise NotImplementedError("merge gap 2")


def build_safe_prompt(order_id, vault):
    rec = next(r for r in RECORDS if r["order_id"] == order_id)
    return redact(json.dumps(rec), vault)


def main():
    vault = Vault()
    safe = build_safe_prompt("A1001", vault)
    print("TOKENIZED PROMPT (safe to log and to send to the model):")
    print("  ", safe)
    assert "1234" not in safe and "521-44-9087" not in safe, "PII leaked!"
    # Simulate a model reply that references a token, then restore for the user.
    model_reply = "I've looked up the card ending in <CARD_1>; your refund is on the way."
    print("\nMODEL REPLY (tokenized):", model_reply)
    print("USER-FACING REPLY (de-tokenized):", vault.detokenize(model_reply))
    print("\nThe model never saw a real card number or SSN.")


if __name__ == "__main__":
    main()
