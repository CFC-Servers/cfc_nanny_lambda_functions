from cfc_rcon_interface import RCONInterface
from response_caching import ResponseCache
from lambda_responses import Response

status_cache = ResponseCache(shelf_life=1)
up = Response({"status": "server-is-up"}, cache_lifetime=1)
down = Response({"status": "server-is-down"}, cache_lifetime=1)

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
