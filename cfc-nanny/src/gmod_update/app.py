import os
from sshrunner import run_command
from lambda_responses import Response
from threading import Thread

directory = os.environ["SCRIPTS_DIRECTORY"]
host = os.environ["SSH_HOST"]
port = os.environ["SSH_PORT"]
username = os.environ["SSH_USERNAME"]
private_key = os.environ["SSH_PRIVATE_KEY"]

command = (
   f'cd {directory}; '
    './update-gmod-resources'
)

def update_resources():
    output = run_command(
        command=command,
        host=host,
        port=port,
        username=username,
        private_key=private_key
    )

    print("Update command output:")
    print(output.stdout)

def lambda_handler(event, context):
    Thread(target=update_resources).start()

    return Response(status=204)
