"""
Lab 7 -- Naive MCP client. (Provided complete -- run it to SEE the poisoning.)

It connects to the gateway, lists the tools, and prints each description exactly
as the model would receive it. Notice the hidden <IMPORTANT> instruction inside
get_weather's description -- that text goes straight into the model's context.

  python client_inspect.py
"""
import asyncio
from fastmcp import Client
from evil_server import server


async def main():
    async with Client(server) as c:
        tools = await c.list_tools()
        print(f"Connected. {len(tools)} tools advertised:\n")
        for t in tools:
            print(f"== {t.name} ==")
            print((t.description or "").strip())
            print()
        print("A naive client hands ALL of these descriptions to the model verbatim.")
        print("The get_weather description alone is a working prompt-injection payload.")


if __name__ == "__main__":
    asyncio.run(main())
