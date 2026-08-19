"""
Lab 8 -- Client that exercises the secured gateway. (Provided complete.)

It calls three tools: a permitted read, a permitted small refund, and a refund
over the limit. Watch the middleware allow the first two and deny the third,
then print the audit trail.

  python secure_client.py
"""
import asyncio
from fastmcp import Client
from secure_server import server, AUDIT


async def try_call(c, name, args):
    try:
        r = await c.call_tool(name, args)
        print(f"[OK]    {name}({args}) -> {r.data}")
    except Exception as e:
        print(f"[DENY]  {name}({args}) -> {e}")


async def main():
    async with Client(server) as c:
        await try_call(c, "lookup_order", {"order_id": "A1001"})
        await try_call(c, "issue_refund", {"order_id": "A1001", "amount": 20})
        await try_call(c, "issue_refund", {"order_id": "A1001", "amount": 999})
    print("\n--- audit trail ---")
    for row in AUDIT:
        mark = "ALLOW" if row["allowed"] else "DENY "
        print(f"  {mark} {row['tool']}({row['args']}) :: {row['reason']}")


if __name__ == "__main__":
    asyncio.run(main())
