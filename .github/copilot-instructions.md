# Working with this course code

This repo is a hands-on security training course. Code files are intentionally
split into **skeletons** (in topic folders, with `# TODO` gaps) and **completed
references** (in `extra/*.txt`). Students merge the gaps themselves via `code -d`.

Some files are **deliberately vulnerable** (e.g. `support_bot.py`, `evil_server.py`,
`runaway_agent.py`, `omnitech_agent.py`). That is by design — they are the "attack"
half of each attack-then-defend lab. Do not "fix" them.

## Explain-this-app template

When a student asks you to explain a file, answer in this structure:

1. **What it does** — one sentence.
2. **High-level flow** — the 3–5 steps the code takes when run.
3. **Key building blocks** — the important functions/classes and their jobs.
4. **Data flow** — what goes in, what comes out, and where untrusted input enters.
5. **Safe experiments** — small changes the student can try to learn.
6. **Debug checklist** — the first things to check if it errors (did you complete
   the `code -d` merge? are you in the right folder? is the model server up?).

## House rules

- Explain concepts; do not complete the `# TODO` gaps for the student.
- Keep security framing present-tense and practical.
- If asked to run a shell command, prefer the allow-listed lab commands.
