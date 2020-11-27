from os import getenv
from json import loads
from cfc_rcon_interface import RCONInterface
from response_caching import ResponseCache
from lambda_responses import Response
from rcon_status_parser import StatusParser

CACHE_SECONDS = 30
status_cache = ResponseCache(shelf_life=CACHE_SECONDS)
status_parser = StatusParser()

command = "status"
command_with_pvp = f"{command};pvpstatusjson"

def scrub_status(status):
    for i, player in enumerate(status["players"]):
        del status["players"][i]["ip"]

    return status

def parse_response(response, full=False, pvp=False):
    pvp_status = None
    parsed_status = None

    if pvp:
        spl = response.split("\n")
        pvp_status = loads(spl[-1])
        response = "\n".join(spl[:-1])

    parsed_status = status_parser.parse(response)

    if not full:
        parsed_status = scrub_status(parsed_status)

    return parsed_status, pvp_status

def lambda_handler(event, context):
    interface = RCONInterface()
    include_pvp = getenv("INCLUDE_PVP") == "True"
    full_status = getenv("FULL_STATUS") == "True"
    cache_lifetime = 0 if full_status else CACHE_SECONDS
    fingerprint = f"{interface.address}:{interface.port}:{full_status}"

    cached_response = status_cache.get(fingerprint)
    if cached_response: return cached_response

    command = command_with_pvp if include_pvp else command

    success, response = interface.issue_command(command)
    if success != True: return Response(status=500, errors=response)

    parsed_status, pvp_status = parse_response(
        response,
        full=full_status,
        pvp=include_pvp
    )

    output = { "status": parsed_status }
    if include_pvp: output["pvpstatus"] = pvp_status

    formatted_response = Response(
        output,
        cache_lifetime=cache_lifetime
    )

    status_cache.set(
        fingerprint,
        formatted_response,
        shelf_life=cache_lifetime
    )

    return formatted_response

