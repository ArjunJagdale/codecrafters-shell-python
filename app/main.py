import sys


def main():

    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input().strip()

        if not command:
            continue

        # Handling the exit command
        if command.startswith("exit"):
            parts = command.split()
            if len(parts)>1 and parts[1].isdigit():
                exit_code = int(parts[1])
            else:
                exit_code = 0
            sys.exit(exit_code)
        
        # Handling the echo command
        elif command.startswith("echo"):
            print(" ".join(command.split()[1:]))
        
        else:
            print(f"{command}: command not found")
        



if __name__ == "__main__":
    main()
