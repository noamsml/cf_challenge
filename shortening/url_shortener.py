class URLShortener:
    def __init__(self, transacter, url_operator, shortname_generator, cache):
        self.transacter = transacter
        self.url_operator = url_operator
        self.shortname_generator = shortname_generator
        self.cache = cache
    def shorten_url(self, url):
        with self.transacter.session() as session:
            try_num = 0
            while True:
                proposed_shortname = self.shortname_generator.generate_shortname(url, try_num)
                persisted_url = self.url_operator.find_url_by_shortname(session, proposed_shortname)

                if not persisted_url:
                    self.url_operator.create_url(session, proposed_shortname, url)
                    persisted_url = self.url_operator.find_url_by_shortname(session, proposed_shortname)
                    self.cache.put(persisted_url)
                    return persisted_url

                if persisted_url.url == url:
                    self.cache.put(persisted_url)
                    return persisted_url

                try_num += 1
