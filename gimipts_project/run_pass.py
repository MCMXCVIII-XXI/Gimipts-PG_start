#!/usr/bin/env python

from gimipts_project.data import data_organization
import subprocess
import sys
import os


def run_ansible() -> None:
    try:
        current_path = os.path.dirname(os.path.abspath(__file__))
        path_parts = current_path.split('/venv', 1)
        result = path_parts[0] if len(path_parts) > 0 else current_path
        
        data_organization()

        subprocess.run('ansible-playbook '
                       f'{result}/ansible_run/playbook.yml '
                       f'-i {result}/ansible_run/inventory.ini --ask-become-pass',
                       shell=True, check=True)

        with open(f'{result}/ansible_run/inventory.ini', 'w') as f:
            f.truncate(0)

        print("The inventory file has been cleared.")

    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

if __name__ == "__main__":
    run_ansible()
