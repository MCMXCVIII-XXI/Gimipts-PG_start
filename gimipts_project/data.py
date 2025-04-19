import argparse
import sys
import os
import re

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Connect to a remote server via SSH.')
    parser.add_argument(
        '-H', '--hostname', required=True, type=str,
        help='Enter the IP address or the server name.'
    )
    args = parser.parse_args()
    return args

def add_inventory(args: argparse.Namespace) -> None:
    try:
        current_path = os.path.dirname(os.path.abspath(__file__))
        current_path = re.match(r'(.*?/pg_install)', current_path).group(1)
        
        new_servers = args.hostname.split()
        if len(new_servers) < 2:
            raise ValueError("At least two server IPs or names are required.")

        second_server = new_servers[1]

        with open(f'{current_path}/ansible_run/inventory.ini', 'a') as f:
            f.write("[myhosts]\n")
            server_number = 0
            for new_server_ip in new_servers:
                server_number += 1
                new_server_name = f"server{server_number}"
                f.write(f"{new_server_name} ansible_host={new_server_ip}\n")
                print(f"Successfully added {new_server_name} to inventory file.")

        return second_server
    except FileNotFoundError:
        print("Error: inventory.ini file not found.", file=sys.stderr)
    except PermissionError:
        print("Error: Permission denied when writing to inventory.ini.", file=sys.stderr)
    except ValueError as ve:
        print(f"Value error: {ve}", file=sys.stderr)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)

def data_organization() -> None:
    args = parse_arguments()
    return add_inventory(args)
