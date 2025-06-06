import sys


def main():
    # Uncomment this block to pass the first stage
    builtins: list[str] = ["echo", "exit", "type"]

    # Wait for user input
    while(True):
        sys.stdout.write("$ ")
        command = input()
        parts: list[str] = command.split()
        if command == "exit 0":
            break
        elif parts[0] == "echo":
            print(" ".join(parts[1:]))
        elif parts[0] == "type":
            if parts[1] in builtins:
                print(f"{parts[1]} is a shell builtin")
            else:
                print(f"{parts[1]}: not found")
        else:
            print(f"{command}: command not found")
        


if __name__ == "__main__":
    main()
