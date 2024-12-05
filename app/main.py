import os
import sys
import subprocess
import shlex

# List of shell builtins
BUILTINS = {"echo", "exit", "type", "pwd", "cd"}

def find_executable(command):
    paths = os.getenv("PATH", "").split(":")
    for path in paths:
        potential_path = os.path.join(path, command)
        if os.path.isfile(potential_path) and os.access(potential_path, os.X_OK):
            return potential_path
    return None

def parse_command(command):
    try:
        return shlex.split(command, posix=True)
    except ValueError as e:
        print(f"Error parsing command: {e}")
        return []

def process_argument(arg):
    """
    Handles variable expansion and escaped characters in double quotes.
    """
    if arg.startswith('"') and arg.endswith('"'):
        # Remove the enclosing double quotes
        arg = arg[1:-1]
        result = []
        i = 0
        while i < len(arg):
            if arg[i] == "\\":
                # Handle escaped characters
                if i + 1 < len(arg) and arg[i + 1] in ['\\', '$', '"', '\n']:
                    result.append(arg[i + 1])
                    i += 1
                else:
                    result.append(arg[i])  # Keep the backslash as-is
            elif arg[i] == "$":
                # Variable expansion
                var_name = []
                i += 1
                while i < len(arg) and (arg[i].isalnum() or arg[i] == "_"):
                    var_name.append(arg[i])
                    i += 1
                i -= 1  # Compensate for the extra increment
                env_value = os.getenv("".join(var_name), "")
                result.append(env_value)
            else:
                result.append(arg[i])
            i += 1
        return "".join(result)
    return arg

def main():
    while True:
        # Display the prompt
        sys.stdout.write("$ ")
        sys.stdout.flush()

        # Wait for user input
        command = input().strip()

        if not command:
            continue

        # Parse the command
        parts = parse_command(command)
        if not parts:
            continue

        # Process double-quoted arguments
        parts = [process_argument(arg) for arg in parts]

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
