import os
from sshrunner import run_command
from restart_utils import clean_output
import re
import json

name = "cfc3"
directory = "/var/steam/gmod/cfc3/"
timeout_seconds = 30

name = f"[{name[0]}]" + name[1:] # prevents command from killing itsself

command = f'cd {directory}; ' \
        f'timeout {timeout_seconds} ./{name} restart || ' \
        f'( printf "\n{name} could not restart within {timeout_seconds} killing process" && ' \
        f'pkill -fe "{name}.cfg"; ' \
        f'./{name} start )'

def lambda_handler(event, context):
    print("Running: ", command)
    output = run_command(
        command=command,
        host="172.245.14.234",
        port=22,
        username="steam",
        private_key="-----BEGIN RSA PRIVATE KEY-----\n" + os.environ["private_key"] + "\n-----END RSA PRIVATE KEY-----"
    )

    print("Command outputed: \n", output.stdout)

    output.stdout = clean_output(output.stdout)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "stdout": output.stdout
        })
    }
