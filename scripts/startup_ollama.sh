#!/usr/bin/env bash
# Install Ollama (if needed), start the server, and pull the default lab model.
# The labs run against this by default; set OPENAI_API_KEY or ANTHROPIC_API_KEY
# to use a faster cloud model instead (common/llm.py auto-detects).
set -e
MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

if ! command -v ollama >/dev/null 2>&1; then
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Start the server in the background if it isn't already up.
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
fi

echo "Pulling ${MODEL} (first run only, ~2 GB)..."
ollama pull "${MODEL}"
echo "Ollama ready with ${MODEL}."
