import sys


def main():
    # Uncomment this block to pass the first stage
    while True:
        sys.stdout.write("$ ")
        sys.stdout.flush()

        command = input().strip()

        if not command:
            continue
        
        print(f"{command}: command not found")


if __name__ == "__main__":
    main()
