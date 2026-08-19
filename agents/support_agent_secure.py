"""
Lab 6 -- Hardened OmniTech support agent. SKELETON.

Same agent, wrapped in a policy engine (policy.yaml):
  * Deny by default -- unlisted tools are refused (the shell disappears).
  * Refund cap -- amounts over the limit require human approval.
  * Path allow-list -- read_file only under approved prefixes.
Every decision is logged, so you get an audit trail for free.

Merge the gaps from extra/support_agent_secure_complete.txt, then:
  python support_agent_secure.py
"""
import os
import sys
import yaml
sys.path.insert(0, "..")
from common.llm import tool_call_loop, backend_banner

ORDERS = {"A1001": {"item": "Wireless Mouse", "total": 29.99, "status": "delivered"},
          "A1002": {"item": "USB-C Hub", "total": 45.00, "status": "shipped"}}
POLICY = yaml.safe_load(open(os.path.join(os.path.dirname(__file__), "policy.yaml")))["tools"]
AUDIT = []


def lookup_order(order_id=""):
    return ORDERS.get(order_id, "no such order")


def issue_refund(order_id="", amount=0):
    return f"REFUND ISSUED: ${amount} for {order_id}"


def read_file(path=""):
    try:
        return open(path).read()[:400]
    except Exception as e:
        return f"error: {e}"


# Note: run_shell is intentionally NOT defined -- policy denies it, so even if the
# model asks for it, authorize() refuses before anything runs.
TOOLS = {
    "lookup_order": ("Look up an order by order_id.", lookup_order),
    "issue_refund": ("Issue a refund: args order_id, amount.", issue_refund),
    "read_file": ("Read a public file: arg path.", read_file),
}


def authorize(tool, args):
    """Return (ok, reason) using POLICY. Deny by default."""
    rule = POLICY.get(tool)
    # TODO (gap 1): if there is no rule, or rule["allow"] is False, deny.
    #   For issue_refund, deny when amount > require_human_above (needs a human).
    #   For read_file, deny when the path doesn't start with an allowed prefix.
    #   Otherwise allow. Record every decision in AUDIT as (tool, args, ok, reason).
    raise NotImplementedError("merge gap 1")


SYSTEM = "You are the OmniTech support agent. Help the customer using your tools."


def trace(step, tool, args, result):
    print(f"  [step {step}] {tool}({args}) -> {str(result)[:80]}")


def handle(user_text):
    print(f"\ncustomer> {user_text}")
    final = tool_call_loop(SYSTEM, user_text, TOOLS, on_step=trace, authorize=authorize)
    print("agent>", final)


def main():
    print(backend_banner())
    print("OmniTech Support Agent (secure). Ctrl+C to quit.")
    while True:
        try:
            user = input("\ncustomer> ").strip()
        except (EOFError, KeyboardInterrupt):
            break
        if not user:
            continue
        print("agent>", tool_call_loop(SYSTEM, user, TOOLS, on_step=trace, authorize=authorize))
        print("  --- audit trail ---")
        for t, a, ok, r in AUDIT[-5:]:
            print(f"    {'ALLOW' if ok else 'DENY '} {t}({a}) {r}")


if __name__ == "__main__":
    main()
