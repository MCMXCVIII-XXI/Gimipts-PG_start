# !/usr/bin/env python

from gimipts_project.data import data_organization
import subprocess
import os
import sys
import re

def run_ansible() -> None:
    try:
        current_path = os.path.dirname(os.path.abspath(__file__))
        current_path = re.match(r'(.*?/pg_install)', current_path).group(1)
        
        data_organization()

        agent_output = subprocess.run('ssh-agent', shell=True, capture_output=True, text=True, check=True)

        for line in agent_output.stdout.splitlines():
            if line.startswith('SSH_AUTH_SOCK') or line.startswith('SSH_AGENT_PID'):
                key, value = line.split(';')[0].split('=')
                os.environ[key] = value

        subprocess.run('ssh-add ~/.ssh/id_ed25519', shell=True, check=True)

        subprocess.run('ansible-playbook '
                       f'{current_path}/ansible_run/playbook.yml '
                       f'-i {current_path}/ansible_run/inventory.ini --ask-become-pass',
                       shell=True, check=True)

        subprocess.run('ssh-agent -k', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        with open(f'{current_path}/ansible_run/inventory.ini', 'w') as f:
            f.truncate(0)

        print("The inventory file has been cleared.")

    except subprocess.CalledProcessError as e:
        print(f"Command '{e.cmd}' returned non-zero exit status {e.returncode}.", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)


if __name__ == "__main__":
    run_ansible()




