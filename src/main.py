import sys
import os
from openai import OpenAI
from dotenv import load_dotenv
from manage_dirs import setup_project_dirs, suggest_move, select_project
from prompt_history_builder import read_chat_file, write_logs

load_dotenv()
client = OpenAI(api_key=os.getenv("VENICE_API_KEY"), base_url="https://api.venice.ai/api/v1")
TOOL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def parse_with_venice(chat_text, project_name):
    print(f"Starting Venice parse for {project_name} with {len(chat_text)} chars")
    prompt = (
        "Parse this chat log into an abridged prompt history for a pro-life tech project. "
        "For each user prompt, output: [User] 'prompt excerpt...' - summary of what the user "
        "was doing with the LLM (e.g., designing a tool, brainstorming Web3). If the LLM "
        "failed or misunderstood, append: (LLM Failure: description). Return each entry on a new line."
    )
    print("Calling Venice API with model llama-3.2-3b")
    response = client.chat.completions.create(
        model="llama-3.2-3b",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": chat_text}
        ],
        temperature=0.3
    )
    print("API call succeeded")
    return f"(Abridged) Prompt History for {project_name} (Feb 2025)\n\n" + response.choices[0].message.content

def main():
    if len(sys.argv) != 2:
        print("Usage: python src/main.py <chat_file_path>")
        sys.exit(1)

    chat_file = sys.argv[1]
    chat_text = read_chat_file(chat_file)
    if not chat_text:
        sys.exit(1)

    project_name = select_project(chat_file, TOOL_ROOT)
    output_dir, logs_dir = setup_project_dirs(project_name, TOOL_ROOT)

    result = parse_with_venice(chat_text, project_name)
    timestamp = os.path.splitext(os.path.basename(chat_file))[0] + "-venice"
    prompt_history_file = os.path.join(output_dir, f"prompt_history-{timestamp}.txt")

    with open(prompt_history_file, "w", encoding="utf-8") as f:
        f.write(result)

    print(f"Abridged history saved to {prompt_history_file}")
    suggest_move(chat_file, logs_dir)

if __name__ == "__main__":
    main()