import asyncssh
import asyncio

class SSHRunner:
    def __init__(self, host, port=22, username="steam", private_key=None):
        self.host = host
        self.port = port
        self.username = username
        self.private_key = private_key

    async def run_command(self, command):
        result = None
        async with asyncssh.connect(self.host, port=self.port, username=self.username, client_keys=[self.private_key], known_hosts=None) as conn:
            result = await conn.run(command, check=False)

        return result


def run_command(*args, **kwargs):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(run_command_async(*args, **kwargs))

async def run_command_async(command, host, port, username, private_key):
    ssh = SSHRunner(host, port=port, username=username, private_key=bytes(private_key, "utf-8"))

    return await ssh.run_command(command)

