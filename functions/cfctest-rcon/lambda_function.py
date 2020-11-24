from cfcrconinterface import RCONInterface()

def lambda_handler(event, context):
    interface = RCONInterface()

    command = event.get("body", None)
    if command is None:
        print("Command is none, returning empty response")
        return {}

    success, response = interface.issue_command(command)
    if success:
        return {"response": response}

    return {"error": str(response)}
