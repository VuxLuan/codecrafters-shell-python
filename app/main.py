import sys


def main():
    # Uncomment this block to pass the first stage
    

    # Wait for user input
    while(True):
        sys.stdout.write("$ ")
        command = input()
        parts: list[str] = command.split()
        if command == "exit 0":
            break
        elif parts[0] == "echo":
            print(" ".join(parts[1:]))
        else:
            print(f"{command}: command not found")
        


if __name__ == "__main__":
    main()
