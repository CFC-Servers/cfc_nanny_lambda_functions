import json
import os

def is_authorized(authorized):
    return { "isAuthorized": authorized }

def deny():
    return is_authorized(False)

def accept():
    return is_authorized(True)

def get_allowed_keys(route):
    route = route.replace("/", "")
    route = route.replace("-", "_")
    route = route.upper()

    allowed_key_names = os.environ.get("{}_AUTH".format(route), None)

    if not allowed_key_names:
        return None

    allowed_keys = set()
    allowed_key_names = auth_keys.split(",")
    for key_name in allowed_key_names:
        key = os.environ.get(key_name, None)

        if not key:
            print("Erorr! Couldn't find key in environment: {}".format(key_name))
            continue

        allowed_keys.add(key)

    return allowed_keys

def lambda_handler(event, context):
    key = event.get("headers", {}).get("authorization", None)

    if key is None:
        print("Auth is none, returning False")
        return deny()

    route = event.get("rawPath", None)

    if route is None:
        print("Route is none, returning False")
        return deny()

    allowed_keys = get_allowed_keys(route)

    if allowed_keys is None:
        print("Couldn't find any allowed keys for given route, '{}'. Denying.".format(route))
        return deny()

    is_authorized = key in allowed_keys

    if is_authorized:
        return accept()

    return deny()

