from cfc_rcon_interface import RCONInterface
from lambda_responses import lambda_response
from json import loads

def lambda_handler(event, context):
    interface = RCONInterface()

    body = event.get("body", None)

    if body is None:
        return lambda_response(status=400, errors="Received empty body")

    body = loads(body)
    command = body.get("command", None)

    if command is None:
        return lambda_response(status=400, errors="Did not receive a command")

    success, result = interface.issue_command(command)
    if success:
        return lambda_response(response=result)

    return lambda_response(status=500, errors=result)
