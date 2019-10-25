class URLResolver:
    def __init__(self, transacter, url_operator, cache):
        self.transacter = transacter
        self.cache = cache
        self.url_operator = url_operator
        
    def resolve_url(self, shortname):
        url_from_cache = self.cache.get(shortname)

        if url_from_cache:
            return url_from_cache

        url_from_db = self.resolve_url_from_db(shortname)
        self.cache.put(url_from_db)

        return url_from_db

    def resolve_url_from_db(self, shortname):
        with self.transacter.session() as session:
            return self.url_operator.find_url_by_shortname(session, shortname)
