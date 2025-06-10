import sys
import os


def echo(cmd_parts: list[str]) -> None:
    print(" ".join(cmd_parts[1:]))


def type(cmd_parts: list[str]) -> None:
    builtins: list[str] = ["echo", "exit", "type"]
    if cmd_parts[1] in builtins:
        print(f"{cmd_parts[1]} is a shell builtin")
    else:
        paths = os.getenv("PATH", "")
        found_in_path = False
        cmd_to_find = cmd_parts[1]
        for dir in paths.split(os.pathsep):
            full_path = os.path.join(dir, cmd_to_find)
            if os.path.isfile(full_path) and os.access(full_path, os.X_OK):
                print(f"{cmd_to_find} is {full_path}")
                found_in_path = True
                break

        if not found_in_path:
            print(f"{cmd_to_find}: not found")


def main() -> None:
    # Wait for user input
    while True:
        sys.stdout.write("$ ")
        command: str = input()
        cmd_parts: list[str] = command.split()
        if command == "exit 0":
            break
        elif cmd_parts[0] == "echo":
            echo(cmd_parts)
        elif cmd_parts[0] == "type":
            type(cmd_parts)
        else:
            print(f"{command}: command not found")


if __name__ == "__main__":
    main()
