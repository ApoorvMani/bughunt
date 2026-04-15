# bughunt

An offline-first, agentic AI red-team system built from scratch.

> Built for learning. Every line understood. No LangChain, no magic.

## Status

🚧 Work in progress — Phase 0

## Stack

- Python 3.11+
- Ollama (local LLM backend)
- ChromaDB (vector store, Phase 3+)
- SQLite (structured memory)
- Textual (TUI, Phase 8+)

## Setup

\```bash
git clone https://github.com/YOUR_USERNAME/bughunt
cd bughunt
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
# edit .env with your Ollama URL
\```

## Roadmap

See `docs/` for the full build roadmap and architecture notes.
