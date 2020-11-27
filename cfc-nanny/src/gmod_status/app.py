from os import getenv
from cfc_rcon_interface import RCONInterface
from response_caching import ResponseCache
from lambda_responses import Response
from rcon_status_parser import StatusParser

CACHE_SECONDS = 30
status_cache = ResponseCache(shelf_life=CACHE_SECONDS)
status_parser = StatusParser()

def scrub_status(status):
    for i, player in enumerate(status["players"]):
        del status["players"][i]["ip"]

    return status

def lambda_handler(event, context):
    interface = RCONInterface()
    full_status = getenv("FULL_STATUS") == "True"
    cache_lifetime = 0 if full_status else CACHE_SECONDS
    fingerprint = f"{interface.address}:{interface.port}:{full_status}"

    cached_response = status_cache.get(fingerprint)
    if cached_response:
        return cached_response

    success, response = interface.issue_command("status")
    if success != True:
        return Response(status=500, errors=response)

    parsed_status = status_parser.parse(response)
    if not full_status:
        parsed_status = scrub_status(parsed_status)

    formatted_response = Response(
        parsed_status,
        cache_lifetime=cache_lifetime
    )

    status_cache.set(
        fingerprint,
        formatted_response,
        shelf_life=cache_lifetime
    )

    return formatted_response

