import time

class ResponseCache:
    def __init__(self, shelf_life=5):
        self.shelf_life = shelf_life
        self.cache = {}

    def set(self, key, value, shelf_life=None):
        print(f"Setting '{key}' to '{value}' in ResponseCache")
        lifetime = shelf_life or self.shelf_life
        now = time.time()

        struct = {
            "value": value,
            "expiration": now + lifetime
        }

        self.cache[key] = struct

    def get(self, key):
        print(f"Getting '{key}' from ResponseCache")
        cached = self.cache.get(key)

        if cached is None:
            print(f"'{key}' didn't exist in ResponseCache")
            return None

        now = time.time()
        expiration = cached.get("expiration", 0)
        is_stale = now > expiration

        if is_stale:
            print(f"Expiration on '{key}' in ResponseCache")
            return None

        value = cached["value"]

        print(f"Returning cached value for '{key}': '{value}'")

        return value
