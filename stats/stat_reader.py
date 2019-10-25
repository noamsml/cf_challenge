from datetime import datetime
from stats.timeutil import datetime_to_hour, SECONDS_PER_DAY, SECONDS_PER_WEEK

class StatResult:
    def __init__(self, all_time, last_day, last_week):
        self.all_time = all_time
        self.last_day = last_day
        self.last_week = last_week

class StatReader:
    def __init__(self, transacter, access_all_time_operator, access_hourly_operator, url_operator, clock = datetime):
        self.transacter = transacter
        self.access_all_time_operator = access_all_time_operator
        self.access_hourly_operator = access_hourly_operator
        self.url_operator = url_operator
        self.clock = clock

    def get_stats(self, shortname):
        with self.transacter.session() as session:
            url_object = self.url_operator.find_url_by_shortname(session, shortname)

            if url_object == None:
                return None

            all_time_accesses = self.access_all_time_operator.get_access_count(session, url_object.id)
            current_hour = datetime_to_hour(self.clock.now())

            day_accesses = self.access_hourly_operator.get_total_access_count(
                session,
                url_object.id,
                current_hour - SECONDS_PER_DAY,
                current_hour)

            week_accesses = self.access_hourly_operator.get_total_access_count(
                session,
                url_object.id,
                current_hour - SECONDS_PER_WEEK,
                current_hour)

            return StatResult(all_time = all_time_accesses,
                last_day = day_accesses,
                last_week = week_accesses)
