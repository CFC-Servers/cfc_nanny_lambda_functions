from cfcrconinterface import RCONInterface
import json

def response(status=200, response=None, error=None):
    body = {}

    if response:
        body["result"] = response

    if error:
        body["error"] = error

    body = json.dumps(body)

    return {
        "statusCode": status,
        "body": body
    }

def lambda_handler(event, context):
    interface = RCONInterface()

    body = event.get("body", None)

    if body is None:
        return response(status=400, error="Received empty body")

    body = json.loads(body)
    command = body.get("command", None)

    if command is None:
        return response(status=400, error="Did not receive a command")

    success, result = interface.issue_command(command)
    if success:
        return response(response=result)

    return response(status=500, error=result)
