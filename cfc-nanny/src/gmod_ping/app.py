from cfcrconinterface import RCONInterface
import json

def response(status=200, response=None, error=None):
    body = {}

    if response:
        body["status"] = response

    if error:
        body["error"] = error

    body = json.dumps(body)

    return {
        "statusCode": status,
        "body": body
    }

def up():
    return response(response="server-is-up")

def down():
    return response(response="server-is-down")

def lambda_handler(event, context):
    interface = RCONInterface()

    success, result = interface.issue_command("status")
    if success:
        return up()

    return down()
