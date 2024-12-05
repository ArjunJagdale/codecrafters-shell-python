import os
import sys
import subprocess

# List of shell builtins
BUILTINS = {"echo", "exit", "type", "pwd", "cd"}

def find_executable(command):
    paths = os.getenv("PATH", "").split(":")
    for path in paths:
        potential_path = os.path.join(path, command)
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

        if not command:
            continue

        parts = command.split()
        cmd = parts[0]
        args = parts[1:]

        if cmd == "exit":
            exit_code = int(args[0]) if args and args[0].isdigit() else 0
            sys.exit(exit_code)

        elif cmd == "echo":
            print(" ".join(args))

        elif cmd == "pwd":
            print(os.getcwd())

        elif cmd == "cd":
            if not args:
                print("cd: missing operand")
            else:
                path = args[0]

                # Handle `~` for the home directory
                if path == "~" or path.startswith("~/"):
                    home_dir = os.getenv("HOME")
                    if not home_dir:
                        print("cd: HOME environment variable not set")
                        continue
                    # Replace `~` with the home directory
                    path = os.path.join(home_dir, path[2:] if path.startswith("~/") else "")

                try:
                    os.chdir(path)
                except FileNotFoundError:
                    print(f"cd: {path}: No such file or directory")
                except NotADirectoryError:
                    print(f"cd: {path}: Not a directory")
                except PermissionError:
                    print(f"cd: {path}: Permission denied")

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
