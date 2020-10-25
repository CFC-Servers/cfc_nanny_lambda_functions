import asyncio
import asyncssh
import sys
import os

HOST = "172.245.14.234"
PORT = 22
USERNAME = 'steam'
PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----\n" + os.environ["private_key"] + "\n-----END RSA PRIVATE KEY-----"


class SSHRunner:
    def __init__(self, host, port=22, username="steam", private_key=None):
        self.host = host
        self.port = port
        self.username = username
        self.private_key = private_key

    async def run_command(self, command):
        result = None
        async with asyncssh.connect(self.host, username=self.username, client_keys=[self.private_key], known_hosts=None) as conn:
            result = await conn.run(command, check=True)

        return result


async def main():
    ssh = SSHRunner(HOST, port=PORT, username=USERNAME, private_key=bytes(PRIVATE_KEY, "utf-8"))
    result = await ssh.run_command("ls")

    return { "stdout": result.stdout }


def lambda_handler(event, context):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(main())

