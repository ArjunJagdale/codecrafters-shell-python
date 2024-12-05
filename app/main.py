import sys
import os
import subprocess

# List of shell builtins
BUILTINS = {"echo", "exit", "type", "pwd"}

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

        # Handle the `exit` command
        if command.startswith("exit"):
            parts = command.split()
            if len(parts) > 1 and parts[1].isdigit():
                exit_code = int(parts[1])
            else:
                exit_code = 0  # Default to exit code 0 if none is provided
            sys.exit(exit_code)

        # Handle the `echo` command
        elif command.startswith("echo"):
            print(" ".join(command.split()[1:]))

        # Handle the `pwd` command
        elif command == "pwd":
            print(os.getcwd())

        # Handle the `type` command
        elif command.startswith("type"):
            parts = command.split()
            if len(parts) > 1:
                target = parts[1]
                # Check if the command is a builtin
                if target in BUILTINS:
                    print(f"{target} is a shell builtin")
                else:
                    # Check if the command is an executable in the PATH
                    executable_path = find_executable(target)
                    if executable_path:
                        print(f"{target} is {executable_path}")
                    else:
                        print(f"{target}: not found")
            else:
                print("type: missing operand")

        # Handle running external commands
        else:
            parts = command.split()
            program_name = parts[0]
            arguments = parts[1:]

            # Find the program in PATH
            executable_path = find_executable(program_name)
            if executable_path:
                try:
                    # Run the external program with arguments
                    result = subprocess.run([executable_path] + arguments, capture_output=True, text=True)
                    # Print the output of the external program
                    print(result.stdout, end="")
                except Exception as e:
                    print(f"Error executing {program_name}: {e}")
            else:
                print(f"{program_name}: command not found")


if __name__ == "__main__":
    main()
