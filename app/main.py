import sys
import os
import subprocess

# List of shell builtins
BUILTINS = {"echo", "exit", "type", "pwd", "cd"}

def find_executable(command):
    # Get the PATH environment variable
    paths = os.getenv("PATH", "").split(":")
    
    # Search for the command in each directory listed in PATH
    for path in paths:
        potential_path = os.path.join(path, command)
        # Check if it's an executable file
        if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
            return potential_path
    return None

def main():
    while True:
        # Display the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input().strip()

        # If the command is empty, continue to the next loop
        if not command:
            continue

        # Split the command into parts
        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        # Handle the `exit` command
        if cmd == "exit":
            exit_code = int(args[0]) if args and args[0].isdigit() else 0
            sys.exit(exit_code)

        # Handle the `echo` command
        elif cmd == "echo":
            print(" ".join(args))

        # Handle the `pwd` command
        elif cmd == "pwd":
            print(os.getcwd())

        # Handle the `cd` command
        elif cmd == "cd":
            if not args:
                print("cd: missing operand")
            else:
                path = args[0]
                try:
                    os.chdir(path)
                except FileNotFoundError:
                    print(f"cd: {path}: No such file or directory")
                except NotADirectoryError:
                    print(f"cd: {path}: Not a directory")
                except PermissionError:
                    print(f"cd: {path}: Permission denied")

        # Handle the `type` command
        elif cmd == "type":
            if not args:
                print("type: missing operand")
            else:
                target = args[0]
                if target in BUILTINS:
                    print(f"{target} is a shell builtin")
                else:
                    executable_path = find_executable(target)
                    if executable_path:
                        print(f"{target} is {executable_path}")
                    else:
                        print(f"{target}: not found")

        # Handle running external commands
        else:
            executable_path = find_executable(cmd)
            if executable_path:
                try:
                    result = subprocess.run([executable_path] + args, capture_output=True, text=True)
                    print(result.stdout, end="")
                except Exception as e:
                    print(f"Error executing {cmd}: {e}")
            else:
                print(f"{cmd}: command not found")


if __name__ == "__main__":
    main()
