import os
from sshrunner import run_command
from lambda_responses import Response

directory = os.environ["SCRIPTS_DIRECTORY"]
host = os.environ["SSH_HOST"]
port = os.environ["SSH_PORT"]
username = os.environ["SSH_USERNAME"]
private_key = os.environ["SSH_PRIVATE_KEY"].replace("\\n", "\n")

command = (
   f'cd {directory}; '
    'nohup ./update-gmod-resources < /dev/null > /dev/null 2>&1 &'
)

def update_resources():
    output = run_command(
        command=command,
        host=host,
        port=int(port),
        username=username,
        private_key=private_key
    )

def lambda_handler(event, context):
    update_resources()

    return Response(status=204)
