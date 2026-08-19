# Running this course in a GitHub Codespace

This is the recommended (and default) way to run the labs — everything is
preconfigured, so you only need a browser and a GitHub account.

## Start a Codespace

1. On the repository's GitHub page, click the green **Code** button.
2. Choose the **Codespaces** tab.
3. Click **Create codespace on main**.

A VS Code editor opens in your browser. The first build takes **3–5 minutes**;
watch the terminal for progress. When it finishes you'll see the model pull
complete and a ready message.

## What the setup does

- Creates a Python virtual environment (`.venv`) and installs `requirements.txt`.
- Installs and starts **Ollama** and pulls `llama3.2:3b` (the default lab model).
- Disables Copilot inline suggestions so you work the labs hands-on.

## Daily use

- Open **labs.md** and follow it top to bottom.
- Each lab tells you which folder to `cd` into. New terminals open at the repo
  root, so re-`cd` if you open a fresh one.
- Diff-merge steps use `code -d ../extra/<file>_complete.txt <skeleton>.py` — merge
  the highlighted gaps from left (reference) into right (your skeleton), then save.

## If the Codespace restarts

Run `bash scripts/startup_ollama.sh` to bring the local model server back up
(this also runs automatically on reattach). Your files and merges are preserved.

## Optional: use a faster cloud model

```
export ANTHROPIC_API_KEY=...     # or OPENAI_API_KEY=...
```

Set this in the terminal before running a lab; the labs detect it automatically.
