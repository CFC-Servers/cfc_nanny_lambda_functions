from json import dumps

def lambda_response(self, status=200, response=None, flat_response=False, errors=None):
    body = {}

    if response:
        # Lets callers put their dictionary values directly on the body instead of nested under "response"
        if flat_response and type(response) is dict:
            for key, value in response.items():
                body[key] = value
        else:
            body["response"] = response

    if errors:
        if type(errors) is not list:
            errors = [errors]

        body["errors"] = errors

    body = dumps(body)

    return {
        "statusCode": status,
        "body": body
    }
