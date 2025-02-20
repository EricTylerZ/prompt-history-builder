import sys
import os
import json
import argparse
from openai import OpenAI
from dotenv import load_dotenv
from manage_dirs import setup_project_dirs, select_project
from prompt_history_builder import read_chat_file
from datetime import datetime

load_dotenv()
client = OpenAI(api_key=os.getenv("VENICE_API_KEY"), base_url="https://api.venice.ai/api/v1")
TOOL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_prompts(file_path="prompts.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {k: v["text"] for k, v in data["prompts"].items()}
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Create it with prompt definitions.")
        sys.exit(1)

def load_models(file_path="models.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["models"]
    except FileNotFoundError:
        print(f"Error: {file_path} not found. Run list_models.py first.")
        sys.exit(1)

def get_model_context(model_id, models):
    for model in models:
        if model["id"] == model_id:
            return model["context_tokens"]
    return 65536  # Default

def parse_with_venice(chat_text, project_name, model, prompt_text, models):
    context_tokens = get_model_context(model, models)
    chunk_size = int(context_tokens * 0.8 * 0.75)
    approx_tokens = len(chat_text) / 0.75
    chunks = [chat_text[i:i+chunk_size] for i in range(0, len(chat_text), chunk_size)]
    result = ""
    print(f"Parsing with {model}, {len(chat_text)} chars, chunk size {chunk_size}")
    if approx_tokens > context_tokens:
        print(f"Warning: {model} has {context_tokens} tokens, file is ~{int(approx_tokens)} tokens—chunking required")
        result += "Note: The below was chunked with different API calls, so there may be some discrepancies between chunks and numbers.\n\n"
    for i, chunk in enumerate(chunks):
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt_text},
                {"role": "user", "content": chunk if len(chunks) == 1 else f"Chunk {i+1}/{len(chunks)}:\n{chunk}"}
            ],
            temperature=0.3
        )
        if len(chunks) > 1:
            result += f"Chunk {i+1}:\n" + response.choices[0].message.content + "\n\n"
        else:
            result += response.choices[0].message.content
        print(f"API call succeeded for {model}, chunk {i+1}")
    return f"(Abridged) Prompt History for {project_name} (Feb 2025)\n\n" + result

def main():
    parser = argparse.ArgumentParser(description="Test prompt history parsing.")
    parser.add_argument("chat_file", help="Path to chat log file")
    parser.add_argument("--models", nargs="+", help="Models to test (e.g., llama-3.2-3b llama-3.3-70b)")
    parser.add_argument("--prompts", nargs="+", default=["p1"], help="Prompt IDs from prompts.json")
    args = parser.parse_args()

    chat_file = args.chat_file
    chat_text = read_chat_file(chat_file)
    if not chat_text:
        sys.exit(1)

    project_name = select_project(chat_file, TOOL_ROOT)
    output_dir, _ = setup_project_dirs(project_name, TOOL_ROOT, test_mode=True)
    timestamp = os.path.splitext(os.path.basename(chat_file))[0] + f"-{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    prompts = load_prompts()
    models = load_models()

    model_list = args.models if args.models else [m["id"] for m in models[:2]]
    tests = []
    for model in model_list:
        for prompt_id in args.prompts:
            if prompt_id in prompts:
                tests.append((model, prompt_id))
                print(f"Added test: {model}, {prompt_id}")

    for model, prompt_id in tests[:4]:
        print(f"Running: {model}, {prompt_id}")
        result = parse_with_venice(chat_text, project_name, model, prompts[prompt_id], models)
        output_file = os.path.join(output_dir, f"prompt_history-{timestamp}-{model}-{prompt_id}.txt")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(result)
        print(f"Saved to {output_file}")

if __name__ == "__main__":
    main()