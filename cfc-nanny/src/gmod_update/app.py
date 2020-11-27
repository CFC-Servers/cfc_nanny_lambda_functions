import os
from sshrunner import run_command
from lambda_responses import Response

directory = os.environ["SCRIPTS_DIRECTORY"]
host = os.environ["SSH_HOST"]
port = os.environ["SSH_PORT"]
username = os.environ["SSH_USERNAME"]
private_key = os.environ["SSH_PRIVATE_KEY"]
private_key = "-----BEGIN RSA PRIVATE KEY-----\n" + private_key + "\n-----END RSA PRIVATE KEY-----"

command = (
   f'cd {directory}; '
    './update_gmod_resources'
)

def lambda_handler(event, context):
    output = run_command(
        command=command,
        host=host,
        port=port,
        username=username,
        private_key=private_key
    )

    print("Update command output:")
    print(output.stdout)

    return Response(status=204)
