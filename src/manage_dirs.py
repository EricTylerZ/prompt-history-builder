import os

def setup_project_dirs(project_name, tool_root, test_mode=False):
    """Set up project directories and return paths."""
    projects_dir = os.path.join(tool_root, "projects")
    project_dir = os.path.join(projects_dir, project_name)
    output_dir = os.path.join(project_dir, "output", "test" if test_mode else "")
    logs_dir = os.path.join(project_dir, "logs")
    
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    
    return output_dir, logs_dir

def suggest_move(input_file, logs_dir):
    """Suggest moving the input file if not in logs."""
    input_path = os.path.abspath(input_file)
    logs_path = os.path.abspath(logs_dir)
    if not input_path.startswith(logs_path):
        move_cmd = f"move \"{input_file}\" \"{logs_dir}\""
        print(f"Suggestion: Move your original log file to the project's logs folder:\n  {move_cmd}")

def select_project(input_file, tool_root):
    """Let user pick or create a project within prompt-history-builder."""
    projects_dir = os.path.join(tool_root, "projects")
    os.makedirs(projects_dir, exist_ok=True)
    projects = [d for d in os.listdir(projects_dir) if os.path.isdir(os.path.join(projects_dir, d))]
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
        return project_name
    elif choice.isdigit() and 1 <= int(choice) <= len(projects):
        return projects[int(choice) - 1]
    else:
        print("Invalid choice, using 'unnamed-project'.")
        return "unnamed-project"