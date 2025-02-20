# Prompt-History-Builder

A Python tool to distill raw chat logs into abridged `prompt_history.txt` files—unpacking how LLM-driven projects come to life at the edge of tech and purpose.

## What It Does
- Turns chaotic chats into structured summaries (e.g., `[User] 'prompt...' - summary`) using local parsing or Venice.ai’s API.
- Tracks LLM-driven tool development—born from a pro-life card game built with Grok 3.
- Supports chunking for big logs—processes files exceeding model context sizes.

## Why It’s Useful
- **Debugging**: Reveals how LLM projects (like this one) unfold and stumble.
- **Learning**: Teaches others (and future LLMs) to build with AI, step by step.
- **Roots**: Tied to [stronghold-quest](https://github.com/EricTylerZ/stronghold-quest)—pro-life tech at its peak (LLMs, Web3).

## Setup
1. Clone: `git clone https://github.com/EricTylerZ/prompt-history-builder.git`
2. Install deps: `pip install openai python-dotenv`
3. Copy configs:
   - `copy .env.example .env`—add your Venice API key (from https://venice.ai/settings/api).
   - `copy prompts.example.json prompts.json`—edit prompts as needed.
   - `copy models.example.json models.json`—run `python src/list_models.py` to refresh.
4. Run:
   - Local: `python src/main.py projects/your_chat.txt`
   - Test with Venice: `python src/test_main.py projects/your_chat.txt --models llama-3.2-3b --prompts p1`

## Structure
- `src/`:
  - `main.py`: Core tool with Venice API integration.
  - `test_main.py`: Testing arena—runs multiple models/prompts, handles chunking.
  - `list_models.py`: Fetches Venice model info to `models.json`.
  - `manage_dirs.py`: Sets up project dirs (`output/`, `logs/`).
  - `prompt_history_builder.py`: Original local parsing logic.
- `projects/`: Your workspace—empty in repo via `.gitignore`.
- `output/test/`: Test outputs—ignored.

## Chunking
- For logs > model context (e.g., 131k tokens for `llama-3.2-3b`):
  - Splits into chunks (80% of context size).
  - Adds “Note: The below was chunked...” only when chunked—avoids clutter on small files.
- Run: `python src/test_main.py projects/big_chat.txt --models llama-3.2-3b --prompts p3`.

## The Story
Started with a pro-life card game, built with Grok 3, and grew into a meta-tool for LLM projects. It’s about harnessing AI to track prompt history—think Git-managed logs for pro-life tech, with Web3 on the horizon—all to defend life through innovation.

## Next Steps
- Test chunking on big logs: `python src/test_main.py projects/full_chat.txt --models llama-3.3-70b --prompts p1`.
- Contribute: Fork it, refine prompts in `prompts.json`, or tweak models—build with it!