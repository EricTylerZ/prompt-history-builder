# Prompt-History-Builder

A Python tool to distill raw chat logs into abridged `prompt_history.txt` files—unpacking how LLM-driven projects come to life at the edge of tech and purpose.

## What It Does
- Turns chaotic chats (e.g., "hey so im trying to...") into structured summaries:  
  `[User] 'prompt...' - summary`
- Designed for projects built with LLMs—tracks their evolution, spots fixes, and shares the playbook.
- Lives locally at `C:\Users\Luke\Documents\SoftProjects\prompt-history-builder\` with `src/`, `projects/`, and a root `prompt_history.txt` in the repo. Raw logs stay off GitHub.

## Why It’s Useful
- **Debugging**: Reveals how LLM projects—like its own origin—unfold and where they stumble.  
- **Learning**: Teaches others (and future LLMs) to build with AI, one prompt at a time.  
- **Roots**: Born from a pro-life card game crafted with Grok 3, it’s tied to [stronghold-quest](https://github.com/EricTylerZ/stronghold-quest)—a push for life using LLMs, Web3, and beyond.

## Setup
1. Clone: `git clone https://github.com/EricTylerZ/prompt-history-builder.git`
2. Deps: `pip install -r requirements.txt` (none yet, but ready to grow)
3. Run: `python src/main.py projects/your_chat.txt`

## Structure
- `src/`: Core scripts (`manage_dirs.py` handles dirs)  
- `projects/`: Your sandbox, kept empty in repo via `.gitignore`  
- `output/`: Parsed histories land here (e.g., `prompt_history-*.txt`)  

## The Story
This kicked off with a pro-life card game, built alongside Grok 3, starting from "hey so im trying to learn cmd tools...". Chats piled up, and this tool emerged to make sense of them—abridging prompts to fuel projects like [stronghold-quest](https://github.com/EricTylerZ/stronghold-quest). It’s pro-life tech at its peak—LLMs shaping tools, Web3 on the horizon—all to defend life through innovation.

## Next Steps
- Refine `parse_chat()` for sharper summaries (see issues).  
- Open to forks—build on it, make it yours.