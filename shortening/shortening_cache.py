from cachetools import LRUCache

CACHE_SIZE = 2048

class ShorteningCache:
    def __init__(self):
        self.clear()
    def clear(self):  # Used pretty much only for setup and for tests
        self.cache = LRUCache(CACHE_SIZE)
    def put(self, url):
        self.cache[url.shortname] = url
    def get(self, shortname):
        return self.cache.get(shortname)
