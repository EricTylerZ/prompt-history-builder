# prompt-history-builder/src/prompt_history_builder.py
import os
from datetime import datetime
from manage_dirs import setup_project_dirs, suggest_move, select_project

TOOL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Fixed: up two levels

def read_chat_file(file_path):
    """Read the unabridged chat file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return None

def parse_chat(chat_text):
    """Parse raw chat into user prompts and LLM responses."""
    lines = chat_text.splitlines()
    user_prompts = []
    llm_responses = []
    current_block = []
    is_user = True

    for line in lines:
        line = line.strip()
        if not line:  # Blank line separates blocks
            if current_block:
                if is_user:
                    user_prompts.append("\n".join(current_block))
                else:
                    llm_responses.append("\n".join(current_block))
                current_block = []
                is_user = not is_user
        elif any(keyword in line.lower() for keyword in ["hey so", "but i", "actually", "well we", "is there"]):  # User prompts
            if current_block and not is_user:
                llm_responses.append("\n".join(current_block))
                current_block = []
            current_block.append(line)
            is_user = True
        elif any(keyword in line.lower() for keyword in ["let’s walk", "thanks for", "great news", "you’re right", "i see"]):  # Grok responses
            if current_block and is_user:
                user_prompts.append("\n".join(current_block))
                current_block = []
            current_block.append(line)
            is_user = False
        elif line and not any(x in line.lower() for x in ["posts", "web pages", "def ", "import ", "# ", "notepad ", "cd ", "dir "]):  # Skip meta/code/cmd
            current_block.append(line)

    if current_block:  # Last block
        if is_user:
            user_prompts.append("\n".join(current_block))
        else:
            llm_responses.append("\n".join(current_block))

    return user_prompts, llm_responses

def write_logs(user_prompts, llm_responses, project_name, input_file, output_dir):
    """Write logs to project-specific output folder."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    user_prompts_file = os.path.join(output_dir, f"{base_name}-user-prompts-{timestamp}.txt")
    full_log_file = os.path.join(output_dir, f"{base_name}-full-log-{timestamp}.txt")
    prompt_history_file = os.path.join(output_dir, f"prompt_history-{timestamp}.txt")

    metadata = f"date: {datetime.now()}\nsource: {input_file}\nproject: {project_name}\n\n"

    with open(user_prompts_file, "w", encoding="utf-8") as f:
        f.write(metadata + "=== user prompts ===\n")
        for i, prompt in enumerate(user_prompts, 1):
            f.write(f"prompt-{i}:\n{prompt}\n\n")

    with open(full_log_file, "w", encoding="utf-8") as f:
        f.write(metadata + "=== full log ===\n")
        for i, (prompt, response) in enumerate(zip(user_prompts, llm_responses), 1):
            f.write(f"user-prompt-{i}:\n{prompt}\n\nllm-response-{i}:\n{response}\n\n")

    with open(prompt_history_file, "w", encoding="utf-8") as f:
        f.write(f"(Abridged) Prompt History for {project_name} ({datetime.now().strftime('%b %Y')})\n\n")
        for i, (prompt, response) in enumerate(zip(user_prompts, llm_responses), 1):
            prompt_line = prompt.split("\n")[0].strip()
            response_summary = response.split("\n")[0].strip() if response else "No response"
            f.write(f"[User] \"{prompt_line}\"\n- {response_summary}\n\n")

    return user_prompts_file, full_log_file, prompt_history_file

def main():
    print("prompt-history-builder")
    input_file = input("enter path to chat file (e.g., C:\\path\\to\\file.txt): ").strip()
    chat_text = read_chat_file(input_file)
    if chat_text:
        project_name = select_project(input_file, TOOL_ROOT)
        output_dir, logs_dir = setup_project_dirs(project_name, TOOL_ROOT)
        user_prompts, llm_responses = parse_chat(chat_text)
        user_file, full_file, prompt_history_file = write_logs(user_prompts, llm_responses, project_name, input_file, output_dir)
        print(f"logs saved:\n- {user_file}\n- {full_file}\n- {prompt_history_file}")
        suggest_move(input_file, logs_dir)

if __name__ == "__main__":
    main()