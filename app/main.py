import sys
import os
import subprocess
from pathlib import Path
import shlex
from typing import Callable

# --- Centralized Configuration ---
# A set provides faster lookups than a list (O(1) vs O(n))
BUILTIN_COMMANDS = {
    "echo",
    "exit",
    "type",
    "pwd",
    "cd",
}


# --- Reusable Helper Function ---
def find_executable(args: str) -> str | None:
    """Searches for an executable in the directories listed in PATH."""
    if not args:
        return None

    path_env = os.getenv("PATH", "")
    for directory in path_env.split(os.pathsep):
        full_path = os.path.join(directory, args)
        if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
            return full_path
    return None


# --- Command Handler Functions ---
def handle_exit(args: list[str]) -> None:
    """Exits the shell. For now, exits with code 0."""
    sys.exit(0)


def handle_echo(args: list[str]) -> None:
    """Prints the arguments back to the user."""
    print(" ".join(args[1:]))


def handle_type(args: list[str]) -> None:
    """Determines the type of a command."""
    if len(args) < 2:
        return  # Do nothing if no command is provided

    cmd_to_find = args[1]
    if cmd_to_find in BUILTIN_COMMANDS:
        print(f"{cmd_to_find} is a shell builtin")
    else:
        # Reuse the helper function
        full_path = find_executable(cmd_to_find)
        if full_path:
            print(f"{cmd_to_find} is {full_path}")
        else:
            print(f"{cmd_to_find}: not found")


def handle_pwd(args: list[str]) -> None:
    current_directory = os.getcwd()
    print(current_directory)


def handle_cd(args: list[str]) -> None:
    cmd_to_find = args[1]
    if len(cmd_to_find) == 1:
        home_directory = Path.home()
        os.chdir(home_directory)
    else:
        try:
            os.chdir(cmd_to_find)
        except FileNotFoundError:
            print(f"cd: {cmd_to_find}: No such file or directory")
        except PermissionError:
            print(f"Error: You do not have permission to access '{cmd_to_find}'.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# def handle_cat(args: list[str]) -> None:
#     filenames = args[1:]
#     if not filenames:
#         # If the list of filenames is empty, read from standard input
#         try:
#             for line in sys.stdin:
#                 print(line, end="")
#         except KeyboardInterrupt:
#             # Handle Ctrl+C by just printing a newline for a clean exit
#             print()
#     else:
#         # If filenames are provided, loop through them
#         for filename in filenames:
#             try:
#                 with open(filename, "r") as f:
#                     print(f.read(), end="")
#             except FileNotFoundError:
#                 sys.stderr.write(f"Error: Cannot find file '{filename}'\n")
#             except IsADirectoryError:
#                 sys.stderr.write(f"Error: '{filename}' is a directory, not a file\n")


# --- Dictionary Dispatcher ---
COMMAND_HANDLERS: dict[str, Callable[[list[str]], None]] = {
    "exit": handle_exit,
    "echo": handle_echo,
    "type": handle_type,
    "pwd": handle_pwd,
    "cd": handle_cd,
}


def main() -> None:
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command_line = sys.stdin.readline().strip()
        if not command_line:
            continue

        try:
            # Use shlex.split() to correctly parse the command line
            args = shlex.split(command_line, posix=True)
        except ValueError as e:
            # shlex raises ValueError for syntax errors, like an open quote
            print(f"Syntax Error: {e}", file=sys.stderr)
            continue  # Skip to the next prompt

        command = args[0]

        if command in COMMAND_HANDLERS:
            # Look up the function in the dictionary and call it
            handler = COMMAND_HANDLERS[command]
            handler(args)
        else:
            # --- Logic for External Commands ---
            executable_path = find_executable(command)
            if executable_path:
                try:
                    # Run the command and pass all parts (including command) as arguments
                    subprocess.run(args)
                except Exception as e:
                    print(f"Error executing command: {e}")
            else:
                print(f"{command}: command not found")


if __name__ == "__main__":
    main()
