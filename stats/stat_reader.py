class StatResult:
    def __init__(self, all_time):
        self.all_time = all_time

class StatReader:
    def __init__(self, transacter, access_all_time_operator, url_operator):
        self.transacter = transacter
        self.access_all_time_operator = access_all_time_operator
        self.url_operator = url_operator

    def get_stats(self, shortname):
        with self.transacter.session() as session:
            url_object = self.url_operator.find_url_by_shortname(session, shortname)

            if url_object == None:
                return None

            all_time_accesses = self.access_all_time_operator.get_access_count(session, url_object.id)

            return StatResult(all_time = all_time_accesses)
