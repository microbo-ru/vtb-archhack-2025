import os
import subprocess

def find_xsd_files(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.xsd'):
                yield os.path.join(root, file)

#  xsdata generate order.xsd --output plantuml --package samples/test
def cli_action(file):
    # Replace 'your_cli_command' with the actual CLI command you want to run
    subprocess.run(['your_cli_command', file])

if __name__ == '__main__':
    directory = '.'  # Replace with the directory you want to search
    for file in find_xsd_files(directory):
        cli_action(file)
