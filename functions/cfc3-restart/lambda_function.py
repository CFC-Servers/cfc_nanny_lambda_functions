import os
from sshrunner import run_command


def lambda_handler(event, context):
    return run_command(
        command="cd /var/steam/gmod/cfc3/ && ./cfc3 restart",
        host="172.245.14.234", 
        port=22, 
        username="steam",
        private_key="-----BEGIN RSA PRIVATE KEY-----\n" + os.environ["private_key"] + "\n-----END RSA PRIVATE KEY-----"
    )