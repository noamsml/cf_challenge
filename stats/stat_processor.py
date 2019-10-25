class StatDatapoint:
    def __init__(self, url_id, time_accessed):
        self.url_id = url_id
        self.time_accessed = time_accessed

class StatProcessor:
    def __init__(self, transacter, access_all_time_operator):
        self.transacter = transacter
        self.access_all_time_operator = access_all_time_operator

    def process_datapoint(self, stat_datapoint):
        with self.transacter.session() as session:
            self.access_all_time_operator.increment_access_count(session, stat_datapoint.url_id)
