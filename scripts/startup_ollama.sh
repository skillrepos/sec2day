#!/usr/bin/env bash
# Make sure Ollama is installed, running, and has the default lab model pulled.
#
# Called from BOTH hooks in .devcontainer/devcontainer.json:
#   postCreateCommand  - once, when the container is first built
#   postAttachCommand  - every time VS Code attaches (including after a
#                        Codespace stop/resume, which is what kills the server)
#
# One script for both is deliberate: the server does NOT survive a container
# stop even though the installed binary and pulled models persist on disk, so
# the reattach path has to be able to do everything the create path does.
# Every step below is a no-op once it's already done, and the model check on
# the last step means a normal reattach touches the network zero times.
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

# Start the server if it isn't already up. This is the step that matters on
# reattach -- the container runs no systemd, so nothing else restarts it.
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
fi

# Don't just assume the start above worked -- check, and fail loudly if not.
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    echo "Ollama server did NOT start. See /tmp/ollama.log for details."
    exit 1
fi

# Only pull if the model isn't already on disk. `ollama pull` on a cached model
# still contacts the registry to check the manifest, which would make every
# reattach depend on the network and (with set -e) fail the whole hook on a
# transient hiccup, even though the model is sitting right there.
if ollama list 2>/dev/null | awk '{print $1}' | grep -qxF "${MODEL}"; then
    echo "Ollama ready with ${MODEL} (already present)."
else
    echo "Pulling ${MODEL} (~2 GB, first run only)..."
    ollama pull "${MODEL}"
    echo "Ollama ready with ${MODEL}."
fi
