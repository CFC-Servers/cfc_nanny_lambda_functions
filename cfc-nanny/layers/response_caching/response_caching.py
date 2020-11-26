import time

class ResponseCache():
    def __init__(self, shelf_life=5):
        self.shelf_life = shelf_life
        self.cache = {}

    def set(key, value):
        now = time.time()

        struct = {
            "value": value,
            "expiration": now + self.shelf_life
        }

        self.cache[key] = struct

    def get(key):
        cached = self.cache.get(key)

        if cached is None:
            return None

        now = time.time()
        expiration = cached.get("expiration", 0)
        is_stale = now > expiration

        if is_stale:
            return None

        return cached["value"]
