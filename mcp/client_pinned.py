"""
Lab 7 -- Pinned MCP client. SKELETON.

Defenses at the integration boundary:
  1. Pin trusted tools by a hash of their description (pinned_manifest.json).
     A description that changed (rug pull) or a tool we never approved is quarantined.
  2. Sanitize descriptions before they reach the model: strip hidden-instruction
     markers so tool poisoning can't ride in on the metadata.

Merge the gaps from extra/client_pinned_complete.txt, then:
  python client_pinned.py
"""
import asyncio
import hashlib
import json
import os
import re
from fastmcp import Client
from evil_server import server

MANIFEST = json.load(open(os.path.join(os.path.dirname(__file__), "pinned_manifest.json")))
INJECTION_MARKERS = [r"<important>", r"ignore .*instructions", r"do not mention",
                     r"read the file", r"api_keys", r"exfiltrat"]


def desc_hash(description):
    return hashlib.sha256((description or "").strip().encode()).hexdigest()


def is_pinned(name, description):
    """True only if this tool name is pinned AND its description hash matches."""
    # TODO (gap 1): return True iff name is in MANIFEST and desc_hash(description)
    #   equals the pinned value.
    raise NotImplementedError("merge gap 1")


def sanitize(description):
    """Strip hidden-instruction markers from a description."""
    # TODO (gap 2): for each INJECTION_MARKERS pattern, remove matches
    #   (case-insensitive, DOTALL) and return the cleaned, stripped text.
    raise NotImplementedError("merge gap 2")


async def main():
    async with Client(server) as c:
        tools = await c.list_tools()
        print(f"{len(tools)} tools advertised. Applying pin + sanitize:\n")
        approved = []
        for t in tools:
            if is_pinned(t.name, t.description):
                approved.append(t.name)
                print(f"[TRUST]      {t.name}")
            else:
                clean = sanitize(t.description)
                print(f"[QUARANTINE] {t.name}: not pinned or description changed")
                if clean != (t.description or "").strip():
                    print(f"             (sanitizer stripped injected text from its description)")
        print(f"\nOnly these tools reach the model: {approved}")
        print("get_weather and apply_discount are quarantined; the payload never lands.")


if __name__ == "__main__":
    asyncio.run(main())
