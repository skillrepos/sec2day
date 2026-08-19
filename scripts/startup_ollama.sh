#!/usr/bin/env bash
# Make sure Ollama is installed, running, and has the default lab model pulled.
# Called from BOTH postCreateCommand (first build) and postAttachCommand (every
# reattach) in .devcontainer/devcontainer.json -- safe to run repeatedly, since
# every step below is a fast no-op once it's already done (in particular,
# `ollama pull` on a model that's already cached is just a manifest check, not
# a re-download).
#
# Set OPENAI_API_KEY or ANTHROPIC_API_KEY to use a faster cloud model instead
# of this local one; common/llm.py auto-detects either.
set -e
MODEL="${OLLAMA_MODEL:-llama3.2:3b}"

# Ollama's installer needs zstd to unpack its archive; the bookworm base image
# doesn't ship it. Without this step the curl|sh install below fails with
# "ERROR: This version requires zstd for extraction" and nothing after it runs.
if ! command -v zstd >/dev/null 2>&1; then
    sudo apt-get update -qq && sudo apt-get install -y -qq zstd
fi

if ! command -v ollama >/dev/null 2>&1; then
    curl -fsSL https://ollama.com/install.sh | sh
fi

# Start the server if it isn't already up -- it doesn't survive a container
# stop/restart even though the binary and any pulled models stay on disk.
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
fi

# Don't just assume the start above worked -- check, and fail loudly if not.
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "Ollama server did NOT start. See /tmp/ollama.log for details."
    exit 1
fi

echo "Pulling ${MODEL} (fast no-op if already cached; ~2 GB on first run)..."
ollama pull "${MODEL}"
echo "Ollama ready with ${MODEL}."
