import json
import os

def get_expected_auth(route):
    route = route.replace("/", "")
    route = route.replace("-", "_")
    route = route.upper()
    
    return os.environ.get("{}_AUTH".format(route), None)

def is_authorized(authorized):
    return { "isAuthorized": authorized }

def deny():
    return is_authorized(False)

def accept():
    return is_authorized(True)

def lambda_handler(event, context):
    auth = event.get("headers", {}).get("authorization", None)
    
    if auth is None:
        print("Auth is none, returning False")
        return deny()
        
    route = event.get("rawPath", None)
    
    if route is None:
        print("Route is none, returning False")
        return deny()

    expected = get_expected_auth(route)
    
    if expected is None:
        print("Route not present in AUTH, returning False")
        return deny()
        
    print("{} == {} = {}".format(auth, expected, auth == expected))

    is_authorized = auth == expected
    
    if is_authorized:
        return accept()
    
    return deny()

