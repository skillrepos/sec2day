#!/usr/bin/env bash
# Re-attach on container restart: make sure the Ollama server is running.
if ! curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
    nohup ollama serve >/tmp/ollama.log 2>&1 &
    sleep 3
fi
echo "Ollama server is up."
