# Securing AI Agents, MCP & RAG in Production
### A 2-Day Attack-Then-Defend Intensive — Tech Skills Transformations

**Revision 1.0 — December 2026**

A hands-on workshop where you break and then harden a realistic AI support agent —
its RAG pipeline, its tools, its MCP gateway, and a coding agent — across the six
layers of a practical security blueprint. Every lab is an attack followed by a
defense, run in a GitHub Codespace. No security background required; Python literacy
is assumed.

## Getting started

1. Click the green **Code** button → **Codespaces** → **Create codespace on main**.
2. Wait 3–5 minutes for the environment to build. It creates a Python virtualenv,
   installs dependencies, and pulls the local model `llama3.2:3b`.
3. When setup finishes, open **labs.md** (it opens in preview by default) and start
   at Lab 1.

## The lab model / API keys

Labs use a small **local model (Ollama `llama3.2:3b`)** by default — no account or
key needed. Replies take 30s–2 min on a 4-core Codespace; that's expected.

To use a faster cloud model instead, set one of these in the terminal before
running a lab (the labs auto-detect it):

```
export ANTHROPIC_API_KEY=...      # uses Claude
# or
export OPENAI_API_KEY=...         # uses GPT
```

## System requirements

- A GitHub account (Codespaces free tier is sufficient for this course).
- A modern browser (Chrome recommended).
- **Bonus lab only:** a paid Claude account with Claude Code installed.

## Merge steps and hover notes

Labs use a diff-and-merge workflow: `code -d ../extra/<file>_complete.txt <skeleton>.py`
opens the completed reference on the left and your skeleton on the right. Merge the
highlighted blocks left-to-right, then save.

`merge-info.json` at the repo root carries a short explanation for every block you
will merge (28 of them across 15 files). With the **Merge Info** VS Code extension
installed, hovering a block in the left pane shows that note. The labs work without
the extension — the notes are optional depth.

## Repository layout

```
foundations/  Lab 1  threat modeling
injection/    Lab 2  direct prompt injection
rag/          Lab 3  RAG poisoning + provenance filtering
data/         Lab 4  PII tokenization
guardrails/   Lab 5  guard pipeline + red-team harness
agents/       Lab 6  tool authorization policy
mcp/          Labs 7-8  MCP tool poisoning, scoped gateway
codingagent/  Lab 9  coding-agent injection
containment/  Lab 10 blast-radius containment
ops/          Lab 11 observability + CI security gate
capstone/     Labs 12-13 AI Act Article 50 controls, end-to-end hardening + scorecard
bonus-claudecode/  optional Claude Code hardening lab
extra/        completed reference code for diff-merge steps
merge-info.json  hover notes for every merge block
common/       shared model client used by all labs
```

## Troubleshooting

- **A lab fails with `NotImplementedError: merge gap N`** — you ran a skeleton
  before completing its `code -d` merge step. Re-open the diff and merge the gap.
- **Model replies are very slow** — that's the local model. Set a cloud API key
  (above) for near-instant replies.
- **`ollama: connection refused`** — run `bash scripts/startup_ollama.sh` to
  restart the local model server.
- **`address already in use`** — a previous lab's process is still running; the
  labs use in-memory transport, so just start a fresh terminal.

## License & attribution

For educational use only by the attendees of our workshops.
© 2026 Tech Skills Transformations LLC and Brent C. Laster. All rights reserved.
techskillstransformations.com
