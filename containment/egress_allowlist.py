"""
Lab 10 -- Egress allow-list. (Imported by the sandbox.)

An agent tool that fetches URLs should only reach approved hosts. Everything
else is denied, so a hijacked agent can't phone home or exfiltrate to an
attacker domain.
"""
from urllib.parse import urlparse

ALLOWED_HOSTS = {"api.omnitech.example", "docs.omnitech.example"}


def check_url(url):
    """Return (ok, reason)."""
    host = (urlparse(url).hostname or "").lower()
    if not host:
        return False, "no host in URL"
    if host in ALLOWED_HOSTS:
        return True, "ok"
    return False, f"egress to '{host}' not on allow-list"
