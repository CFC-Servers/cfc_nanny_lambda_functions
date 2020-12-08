from json import dumps
from mcstatus import MinecraftServer
from threading import Thread
from lambda_responses import Response

SERVERS = [
    "lobby",
    "survival",
    "creative"
]

BASE_URL = "mc.cfcservers.org"
PORT = 25565

results = {}

def add_status_to_results(name):
    server = MinecraftServer(f"{name}.{BASE_URL}", PORT)
    status = server.status()

    results[name] = status.raw

def lambda_handler(event, context):
    threads = []
    for server in SERVERS:
        t = Thread(target=add_status_to_results, args=(server,))
        threads.append(t)
        t.start()

    for thread in threads:
        thread.join()

    return Response(content=results)

