class URLResolver:
    def __init__(self, transacter, url_operator):
        self.transacter = transacter
        self.url_operator = url_operator
    def resolve_url(self, shortname):
        with self.transacter.session() as session:
            return self.url_operator.find_url_by_shortname(session, shortname)
