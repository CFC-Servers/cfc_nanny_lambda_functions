import socket
import mcrcon
from os import getenv
from lambda_responses import Response
from json import loads

HOST = getenv("RCON_IP")
PORT = int(getenv("RCON_PORT"))
PASSWORD = getenv("RCON_PASSWORD")


def lambda_handler(event, context):
    body = event.get("body", None)
    if body is None:
        return Response(status=400, errors="Received empty body")

    body = loads(body)
    command = body.get("command", None)

    if command is None:
        return Response(status=400, errors="Did not receive a command")

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, PORT))

    try:
        # Log in
        result = mcrcon.login(sock, PASSWORD)
        if not result:
            Response(status=500, errors="Incorrect password")

        result = mcrcon.command(sock, command)
        return Response(content=result)
    finally:
        sock.close()

