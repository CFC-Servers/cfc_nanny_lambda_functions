from cfc_rcon_interface import RCONInterface
from lambda_responses import Response
from json import loads

interface = RCONInterface()

def lambda_handler(event, context):

    body = event.get("body", None)

    if body is None:
        return Response(status=400, errors="Received empty body")

    body = loads(body)
    command = body.get("command", None)

    if command is None:
        return Response(status=400, errors="Did not receive a command")

    success, result = interface.issue_command(command)
    if success:
        return Response(content=result)

    return Response(status=500, errors=result)
