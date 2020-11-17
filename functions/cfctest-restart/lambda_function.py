import os
from sshrunner import run_command
import re

name = "cfctest"
directory = "/var/steam/gmod/cfc-test/"
timeout_seconds = 30
command = f'cd {directory}; ' \
        f'timeout {timeout_seconds} ./{name} restart || ' \
        f'(echo "{name} could not restart within {timeout_seconds} killing process" && ' \
        f'pkill -fe "{name}.cfg" && ' \
        f'./{name} start)'

def clean_output(out):
    lines = out.split("\n")
    cleaned_lines = []
    
    for line in lines:
        line = line.split("\r").pop()
        line = re.sub(r"(\x9B|\x1B\[)[0-?]*[ -\/]*[@-~]", "", line) # remove ANSI formatting codes
        line = re.sub(r"/var/[^\s]*", "****", line)
        cleaned_lines.append( line )
    
    return "\n".join(cleaned_lines)

def lambda_handler(event, context):
    output = run_command(
        command=command,
        host="172.245.14.234",
        port=22,
        username="steam",
        private_key="-----BEGIN RSA PRIVATE KEY-----\n" + os.environ["private_key"] + "\n-----END RSA PRIVATE KEY-----"
    )
    
    print("Command outputed: \n", output)
    
    output["stdout"] = clean_output(output["stdout"])
    
    return output
