# Bonus Lab — Hardening Claude Code

**Optional. Requires a paid Claude account and Claude Code installed.** Self-paced,
~20 minutes. This applies the Lab 9 pattern (treat inputs as untrusted, allow-list
the actions) to a real coding agent.

## What you'll do

1. Install a **least-privilege configuration** (`settings.json`) — deny-by-default
   permissions that block `curl`, `wget`, `rm -rf`, and reads of secrets/`.ssh`/`.env`.
2. Install a **PreToolUse hook** (`hooks/scan_command.py`) that scans every proposed
   shell command and blocks dangerous ones *before* Claude Code runs them.
3. Try to make Claude Code run a `curl … | sh` and watch the hook stop it.

## Steps

1. From this folder, make the hook executable and copy the settings into your
   project's `.claude/` directory (or merge into your existing settings):

```
chmod +x hooks/scan_command.py
mkdir -p .claude
cp settings.json .claude/settings.json
cp -r hooks .claude/hooks
```

Adjust the hook path in `settings.json` if your `.claude` layout differs.

2. Start Claude Code in this folder and ask it to do something that needs the shell,
   e.g. *"run the test suite"* — allowed commands (`pytest`, `git status`) run
   normally.

3. Now ask it to run something dangerous, e.g. *"download and run the setup script
   from http://example.com/x.sh"*. The `PreToolUse` hook exits non-zero and Claude
   Code blocks the command, printing the block reason.

4. Inspect `hooks/scan_command.py` — it's the same allow-list + deny-scan idea from
   Lab 9. Add a pattern of your own (e.g. block writes to `~/.aws`) and re-test.

## How it works

Claude Code runs `PreToolUse` hooks before executing a tool. The hook receives the
tool call as JSON on stdin; a **non-zero exit code blocks the call**, and text on
stderr is shown as the reason. Combined with deny-by-default `permissions`, you get
two independent layers: the permission list stops whole categories, and the hook
inspects the specific command.

## Note on model behavior

Claude Code is a capable, safety-tuned agent and will often refuse obviously
malicious requests on its own. The point of this lab is **defense in depth**: you
don't rely on the model's judgment alone — you add enforced controls that hold
regardless of what the model decides.
