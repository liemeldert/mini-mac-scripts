# Wrapper script for force elevated permissions
import os
import sys

def run_as_sudo():
    # Get the path to the original script
    script_path = os.path.join(os.path.dirname(sys.argv[0]), 'main.py')

    # Build the command to run the script as sudo
    cmd = f'sudo python3 {script_path}'

    # Run the command as a subprocess
    os.system(cmd)

if __name__ == '__main__':
    run_as_sudo()