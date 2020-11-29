import os
from cfc_rcon_interface import RCONInterface
from sshrunner import run_command
from restart_utils import clean_output
from lambda_responses import Response

timeout_seconds = 30

name = os.environ["SERVER_NAME"]
name = f"[{name[0]}]" + name[1:] # prevents command from killing itsself

directory = os.environ["SERVER_DIRECTORY"]
host = os.environ["SSH_HOST"],
port = os.environ["SSH_PORT"],
username = os.environ["SSH_USERNAME"],
private_key = os.environ["SSH_PRIVATE_KEY"]

pre_restart_command = "sv_cheats 1;net_fakeloss 10000"
pre_restart_command = "status"

command = (
    f'cd {directory}; '
    f'timeout {timeout_seconds} ./{name} restart || '
    f'( printf "\n{name} could not restart within {timeout_seconds} killing process" && '
    f'pkill -fe "{name}.cfg"; '
    f'./{name} start )'
)

rcon_interface = RCONInterface()

def lambda_handler(event, context):
    print("Running: ", command)

    success, rcon_output = rcon_interface.issue_command(pre_restart_command)
    print(f"Pre restart function: Success: {success} Output follows:")
    print(rcon_output)

    output = run_command(
        command=command,
        host=host,
        port=port,
        username=username,
        private_key=private_key
    )

    print("Command output: \n", output.stdout)

    output.stdout = clean_output(output.stdout)

    return Response({"stdout": output.stdout})
