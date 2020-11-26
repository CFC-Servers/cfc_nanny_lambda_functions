from cfcrconinterface import RCONInterface
import json
import time

CACHE_DURATION = 5
STATUS_CACHE = {}

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

def get_cached(destination):
    response = STATUS_CACHE.get(destination, None)

    if response is None:
        return None

    now = time.time()
    expiration = response.get("expires", 0)
    is_stale = now >= expiration

    if is_stale:
        return None

    return response.get("response", {})

def set_cached(destination, response):
    now = time.time()

    struct = {
        "response": response,
        "expires": now + CACHE_DURATION
    }

    STATUS_CACHE[destination] = struct

def lambda_handler(event, context):
    interface = RCONInterface()

    destination = f"{interface.address}:{interface.port}"

    cached_response = get_cached(destination)
    if cached_response:
        return cached_response

    success = interface.issue_command("status")

    response = up() if success else down()

    set_cached(destination, response)

    return response
