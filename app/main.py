import sys


def main():
    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input().strip()

        if not command:
            continue

        if command.startswith("exit"):
            parts = command.split()
            if len(parts)>1 and parts[1].isdigit():
                exit_code = int(parts[1])
            else:
                exit_code = 0
            sys.exit(exit_code)
            

        
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
