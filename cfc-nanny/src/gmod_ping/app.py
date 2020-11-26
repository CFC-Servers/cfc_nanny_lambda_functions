from cfc_rcon_interface import RCONInterface
from response_caching import ResponseCache
from lambda_responses import lambda_response
import json

status_cache = ResponseCache(shelf_life=5)

up = lambda_response(response={"status": "server-is-up"}, flat_response=True)
down = lambda_response(response={"status": "server-is-down"}, flat_response=True)

def lambda_handler(event, context):
    interface = RCONInterface()

    destination = f"{interface.address}:{interface.port}"

    cached_response = status_cache.get(destination)
    if cached_response:
        return cached_response

    success = interface.issue_command("status")

    response = up if success else down

    status_cache.set(destination, response)

    return response
