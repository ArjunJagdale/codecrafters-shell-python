import sys
import os


Builtins = {"echo", "exit", "type"}

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
        

        # Handle type command
        elif command.startswith("type"):
            parts = command.split()
            if len(parts)>1:
                target = parts[1]
                if target in Builtins:
                    print(f"{target} is a shell builtin")
                else:
                    print(f"{target}: not found")
            
            else:
                print("type: missing operand")

        else:
            print(f"{command}: command not found")
        





if __name__ == "__main__":
    main()
