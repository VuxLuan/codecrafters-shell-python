import sys
import os
import subprocess

# --- Centralized Configuration ---
# A set provides faster lookups than a list (O(1) vs O(n))
BUILTIN_COMMANDS = {"echo", "exit", "type"}


# --- Reusable Helper Function ---
def find_executable(command_name: str) -> str | None:
    """Searches for an executable in the directories listed in PATH."""
    if not command_name:
        return None

    path_env = os.getenv("PATH", "")
    for directory in path_env.split(os.pathsep):
        full_path = os.path.join(directory, command_name)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None


# --- Command Handler Functions ---
def handle_exit(cmd_parts: list[str]) -> None:
    """Exits the shell. For now, exits with code 0."""
    sys.exit(0)


def handle_echo(cmd_parts: list[str]) -> None:
    """Prints the arguments back to the user."""
    print(" ".join(cmd_parts[1:]))


def handle_type(cmd_parts: list[str]) -> None:
    """Determines the type of a command."""
    if len(cmd_parts) < 2:
        return  # Do nothing if no command is provided

    cmd_to_find = cmd_parts[1]
    if cmd_to_find in BUILTIN_COMMANDS:
        print(f"{cmd_to_find} is a shell builtin")
    else:
        # Reuse the helper function
        full_path = find_executable(cmd_to_find)
        if full_path:
            print(f"{cmd_to_find} is {full_path}")
        else:
            print(f"{cmd_to_find}: not found")


# --- Dictionary Dispatcher ---
COMMAND_HANDLERS = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
}


def main() -> None:
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command_line = sys.stdin.readline().strip()
        if not command_line:
            continue

        cmd_parts = command_line.split()
        command = cmd_parts[0]

        if command in COMMAND_HANDLERS:
            # Look up the function in the dictionary and call it
            handler = COMMAND_HANDLERS[command]
            handler(cmd_parts)
        else:
            # --- Logic for External Commands ---
            executable_path = find_executable(command)
            if executable_path:
                try:
                    # Run the command and pass all parts (including command) as arguments
                    subprocess.run(cmd_parts)
                except Exception as e:
                    print(f"Error executing command: {e}")
            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
