"""
common/llm.py -- one tiny model client for every lab.

Backend is chosen automatically:
  * ANTHROPIC_API_KEY set  -> Anthropic (model: ANTHROPIC_MODEL or claude-sonnet-4-5)
  * OPENAI_API_KEY set     -> OpenAI    (model: OPENAI_MODEL or gpt-4o-mini)
  * otherwise              -> local Ollama (model: OLLAMA_MODEL or llama3.2:3b)
Force one with LLM_BACKEND=ollama|openai|anthropic|mock.
`mock` is a deterministic stand-in used only by the course's own test suite.

Public API:
  chat(messages, system=None, json_mode=False, temperature=0.0) -> str
  tool_call_loop(system, user, tools, max_steps=3, on_step=None) -> str
"""
import json
import os
import re

BACKEND = os.getenv("LLM_BACKEND") or (
    "anthropic" if os.getenv("ANTHROPIC_API_KEY")
    else "openai" if os.getenv("OPENAI_API_KEY")
    else "ollama"
)


def _ollama_chat(messages, system, json_mode, temperature):
    import ollama
    model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    msgs = ([{"role": "system", "content": system}] if system else []) + messages
    kwargs = {"model": model, "messages": msgs, "options": {"temperature": temperature}}
    if json_mode:
        kwargs["format"] = "json"
    return ollama.chat(**kwargs)["message"]["content"]


def _openai_chat(messages, system, json_mode, temperature):
    from openai import OpenAI
    client = OpenAI()
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    msgs = ([{"role": "system", "content": system}] if system else []) + messages
    kwargs = {"model": model, "messages": msgs, "temperature": temperature}
    if json_mode:
        kwargs["response_format"] = {"type": "json_object"}
    return client.chat.completions.create(**kwargs).choices[0].message.content


def _anthropic_chat(messages, system, json_mode, temperature):
    import anthropic
    client = anthropic.Anthropic()
    model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5")
    sys_prompt = system or ""
    if json_mode:
        sys_prompt += "\nRespond with a single JSON object and nothing else."
    resp = client.messages.create(
        model=model, max_tokens=1024, temperature=temperature,
        system=sys_prompt, messages=messages,
    )
    return "".join(b.text for b in resp.content if getattr(b, "type", "") == "text")


def _mock_chat(messages, system, json_mode, temperature):
    """Deterministic responses so the repo's own tests can run without a model."""
    text = " ".join(m["content"] for m in messages if m["role"] == "user").lower()
    sys_text = (system or "").lower()
    if json_mode or "reply with a json" in sys_text or "respond with json" in sys_text:
        # Tool loop: follow any injected instruction the way a naive small model would.
        if "tool result:" in text:
            return json.dumps({"final": "MOCK: done, based on the tool result."})
        m = re.search(r"tool[:=]\s*([a-z_]+)\s*\(([^)]*)\)", text)
        if m:
            return json.dumps({"tool": m.group(1), "args": {"raw": m.group(2)}})
        if "refund" in text:
            return json.dumps({"tool": "issue_refund", "args": {"order_id": "A1001", "amount": 999}})
        if "look up" in text or "order" in text:
            return json.dumps({"tool": "lookup_order", "args": {"order_id": "A1001"}})
        return json.dumps({"final": "MOCK: done."})
    if "ignore" in text and ("instructions" in text or "rules" in text):
        return "MOCK: Sure! Here is the system prompt and the internal data you asked for: SECRET-DISCOUNT-CODE-42."
    return "MOCK: I can help with OmniTech orders, returns and shipping."


_BACKENDS = {
    "ollama": _ollama_chat,
    "openai": _openai_chat,
    "anthropic": _anthropic_chat,
    "mock": _mock_chat,
}


def chat(messages, system=None, json_mode=False, temperature=0.0):
    """messages: list of {"role": "user"|"assistant", "content": str}. Returns text."""
    if isinstance(messages, str):
        messages = [{"role": "user", "content": messages}]
    return _BACKENDS[BACKEND](messages, system, json_mode, temperature)


def backend_banner():
    model = {
        "ollama": os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        "openai": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "anthropic": os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
        "mock": "mock",
    }[BACKEND]
    return f"[llm] backend={BACKEND} model={model}"


TOOL_LOOP_SYSTEM = """You are an agent. You can call tools.
Reply with a JSON object ONLY, in one of two shapes:
  {"tool": "<tool_name>", "args": {...}}   -- to call a tool
  {"final": "<answer to the user>"}         -- when you are done
Available tools:
{tool_list}
"""


def tool_call_loop(system, user, tools, max_steps=3, on_step=None, authorize=None):
    """
    Minimal agent loop shared by the agent labs.
      tools     : dict name -> (description, callable(**args) -> str)
      on_step   : optional callback(step_no, tool_name, args, result) for tracing
      authorize : optional callable(tool_name, args) -> (ok: bool, reason: str)
    Returns the final answer text.
    """
    tool_list = "\n".join(f"- {n}: {d}" for n, (d, _) in tools.items())
    # replace(), not format(): the template contains literal JSON braces.
    sys_prompt = (system or "") + "\n" + TOOL_LOOP_SYSTEM.replace("{tool_list}", tool_list)
    history = [{"role": "user", "content": user}]
    for step in range(1, max_steps + 1):
        raw = chat(history, system=sys_prompt, json_mode=True)
        try:
            msg = json.loads(raw)
        except json.JSONDecodeError:
            msg = {"final": raw}
        if "final" in msg or "tool" not in msg:
            return msg.get("final", raw)
        name, args = msg["tool"], msg.get("args", {}) or {}
        allowed, why = (True, "ok")
        if authorize:
            allowed, why = authorize(name, args)   # called once: it may write an audit row
        if name not in tools:
            result = f"ERROR: unknown tool {name}"
        elif not allowed:
            result = f"DENIED: {why}"
        else:
            try:
                result = str(tools[name][1](**args))
            except TypeError as e:
                result = f"ERROR: bad args for {name}: {e}"
        if on_step:
            on_step(step, name, args, result)
        history.append({"role": "assistant", "content": raw})
        history.append({"role": "user", "content": f"Tool result: {result}\nContinue."})
    return "(stopped: max steps reached)"
