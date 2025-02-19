# prompt-history-builder/src/prompt-history-builder.py
import os
from datetime import datetime

# Tool root is prompt-history-builder, projects are within it
TOOL_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECTS_DIR = os.path.join(TOOL_ROOT, "projects")

def read_chat_file(file_path):
    """Read the unabridged chat file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except (FileNotFoundError, PermissionError) as e:
        print(f"Error: {e}")
        return None

def parse_chat(chat_text):
    """Parse chat into user prompts and LLM responses."""
    lines = chat_text.splitlines()
    user_prompts = []
    llm_responses = []
    current_block = []
    is_user = False

    for line in lines:
        line = line.strip()
        if line.startswith("[User"):
            if current_block:
                if is_user:
                    user_prompts.append("\n".join(current_block))
                else:
                    llm_responses.append("\n".join(current_block))
            current_block = [line]
            is_user = True
        elif line.startswith("[Grok"):
            if current_block:
                if is_user:
                    user_prompts.append("\n".join(current_block))
                else:
                    llm_responses.append("\n".join(current_block))
            current_block = [line]
            is_user = False
        elif line and not line.startswith("[Note"):
            current_block.append(line)

    if current_block:
        if is_user:
            user_prompts.append("\n".join(current_block))
        else:
            llm_responses.append("\n".join(current_block))

    return user_prompts, llm_responses

def write_logs(user_prompts, llm_responses, project_name, input_file):
    """Write logs to project-specific output folder and suggest moving input."""
    output_dir = os.path.join(PROJECTS_DIR, project_name, "output")
    logs_dir = os.path.join(PROJECTS_DIR, project_name, "logs")
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base_name = os.path.splitext(os.path.basename(input_file))[0]

    user_prompts_file = os.path.join(output_dir, f"{base_name}-user-prompts-{timestamp}.txt")
    full_log_file = os.path.join(output_dir, f"{base_name}-full-log-{timestamp}.txt")
    abridged_file = os.path.join(output_dir, f"{base_name}-abridged-history-{timestamp}.txt")

    metadata = f"date: {datetime.now()}\nsource: {input_file}\nproject: {project_name}\n\n"

    with open(user_prompts_file, "w", encoding="utf-8") as f:
        f.write(metadata + "=== user prompts ===\n")
        for i, prompt in enumerate(user_prompts, 1):
            f.write(f"prompt-{i}:\n{prompt}\n\n")

    with open(full_log_file, "w", encoding="utf-8") as f:
        f.write(metadata + "=== full log ===\n")
        for i, (prompt, response) in enumerate(zip(user_prompts, llm_responses), 1):
            f.write(f"user-prompt-{i}:\n{prompt}\n\nllm-response-{i}:\n{response}\n\n")

    with open(abridged_file, "w", encoding="utf-8") as f:
        f.write(metadata + "=== abridged history ===\n")
        for i, prompt in enumerate(user_prompts, 1):
            short_prompt = prompt.split("\n")[0][:50] + ("..." if len(prompt) > 50 else "")
            f.write(f"{i}. {short_prompt}\n")

    return user_prompts_file, full_log_file, abridged_file, logs_dir

def select_project(input_file):
    """Let user pick or create a project within prompt-history-builder."""
    os.makedirs(PROJECTS_DIR, exist_ok=True)
    projects = [d for d in os.listdir(PROJECTS_DIR) if os.path.isdir(os.path.join(PROJECTS_DIR, d))]
    if not projects:
        print("No existing projects found.")
    else:
        print("Existing projects:")
        for i, proj in enumerate(projects, 1):
            print(f"{i}. {proj}")

    choice = input("Enter project number (or 'n' for new project): ").strip().lower()
    if choice == "n":
        project_name = input("Enter new project name: ").strip()
        if not project_name:
            project_name = "unnamed-project"
        os.makedirs(os.path.join(PROJECTS_DIR, project_name, "logs"), exist_ok=True)
        os.makedirs(os.path.join(PROJECTS_DIR, project_name, "output"), exist_ok=True)
        return project_name
    elif choice.isdigit() and 1 <= int(choice) <= len(projects):
        return projects[int(choice) - 1]
    else:
        print("Invalid choice, using 'unnamed-project'.")
        os.makedirs(os.path.join(PROJECTS_DIR, "unnamed-project", "logs"), exist_ok=True)
        os.makedirs(os.path.join(PROJECTS_DIR, "unnamed-project", "output"), exist_ok=True)
        return "unnamed-project"

def main():
    print("prompt-history-builder")
    input_file = input("enter path to chat file (e.g., C:\\path\\to\\file.txt): ").strip()
    chat_text = read_chat_file(input_file)
    if chat_text:
        user_prompts, llm_responses = parse_chat(chat_text)
        project_name = select_project(input_file)
        user_file, full_file, abridged_file, logs_dir = write_logs(user_prompts, llm_responses, project_name, input_file)
        print(f"logs saved:\n- {user_file}\n- {full_file}\n- {abridged_file}")
        input_dir = os.path.dirname(input_file)
        if input_dir != logs_dir:
            move_cmd = f"move \"{input_file}\" \"{logs_dir}\""
            print(f"Suggestion: Move your original log file to the project's logs folder:\n  {move_cmd}")

if __name__ == "__main__":
    main()