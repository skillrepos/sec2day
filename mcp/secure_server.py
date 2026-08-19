"""
Lab 8 -- A secured MCP gateway. SKELETON.

Defenses at the boundary, enforced by middleware (so every tool is covered):
  1. Scope check -- each tool requires a scope; the caller only holds some.
  2. Per-action authorization -- refunds over a limit are denied even with scope.
  3. Audit trail -- every call (allowed or denied) is recorded.

Merge the gaps from extra/secure_server_complete.txt, then run the client:
  python secure_client.py
"""
from fastmcp import FastMCP
from fastmcp.server.middleware import Middleware
from fastmcp.exceptions import ToolError

# What scope each tool needs, and the ceiling for refunds.
REQUIRED_SCOPE = {
    "lookup_order": "orders:read",
    "track_package": "orders:read",
    "issue_refund": "orders:refund",
}
REFUND_LIMIT = 50.0

# The authenticated caller (in production this comes from a verified token).
# The support agent is granted read + refund, but NOT admin.
CALLER_SCOPES = {"orders:read", "orders:refund"}

AUDIT = []


class SecurityMiddleware(Middleware):
    async def on_call_tool(self, context, call_next):
        name = context.message.name
        args = dict(context.message.arguments or {})
        ok, reason = self.authorize(name, args)
        AUDIT.append({"tool": name, "args": args, "allowed": ok, "reason": reason})
        if not ok:
            raise ToolError(f"denied: {reason}")
        return await call_next(context)

    def authorize(self, name, args):
        """Return (ok, reason)."""
        need = REQUIRED_SCOPE.get(name)
        # TODO (gap 1): deny if the tool has no required scope on file
        #   ("unknown tool"), or if that scope is not in CALLER_SCOPES
        #   ("missing scope: <scope>"). Then, for issue_refund, deny when
        #   amount > REFUND_LIMIT ("over refund limit"). Otherwise allow ("ok").
        raise NotImplementedError("merge gap 1")


server = FastMCP("omnitech-secure-gateway")
server.add_middleware(SecurityMiddleware())


@server.tool
def lookup_order(order_id: str) -> str:
    """Look up an OmniTech order by its ID."""
    return f"Order {order_id}: shipped"


@server.tool
def track_package(order_id: str) -> str:
    """Return the tracking status for an order."""
    return f"Order {order_id}: out for delivery"


@server.tool
def issue_refund(order_id: str, amount: float) -> str:
    """Issue a refund for an order."""
    return f"REFUND ISSUED: ${amount} for {order_id}"


if __name__ == "__main__":
    server.run()
