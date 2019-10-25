from datetime import datetime, timedelta

from integration_common import IntegrationTestCase

from stats.stat_processor import StatProcessor
from stats.stat_reader import StatReader
from stats.stat_processor import StatDatapoint
from shortening.url_shortener import URLShortener
from shortening.shortname_generator import ShortnameGenerator
from storage.adapter import URLOperator, AccessAllTimeOperator, AccessHourlyOperator

BASE_TIME = datetime(2019, 10, 24, 17, 8)

class FakeClock:
    def __init__(self):
        self.now_value = BASE_TIME
    def now(self):
        return self.now_value

class StatsTest(IntegrationTestCase):
    def integrationSetUp(self):
        self.clock = FakeClock()
        self.shortname_generator = ShortnameGenerator()
        self.url_operator = URLOperator()
        self.access_all_time_operator = AccessAllTimeOperator()
        self.access_hourly_operator = AccessHourlyOperator()
        self.stat_processor = StatProcessor(self.transacter,
            self.access_all_time_operator,
            self.access_hourly_operator)
        self.stat_reader = StatReader(self.transacter,
            self.access_all_time_operator,
            self.access_hourly_operator,
            self.url_operator,
            self.clock)
        self.url_shortener = URLShortener(self.transacter,
            self.url_operator,
            self.shortname_generator)

    def test_all_time_access(self):
        url1 = self.url_shortener.shorten_url("http://noam.horse/resume.html")
        url2 = self.url_shortener.shorten_url("http://noam.horse/")

        access1 = StatDatapoint(url_id = url1.id, time_accessed = BASE_TIME)
        access2 = StatDatapoint(url_id = url1.id, time_accessed = BASE_TIME)
        access3 = StatDatapoint(url_id = url2.id, time_accessed = BASE_TIME)

        self.stat_processor.process_datapoint(access1)
        self.stat_processor.process_datapoint(access2)
        self.stat_processor.process_datapoint(access3)

        stats1 = self.stat_reader.get_stats(url1.shortname)
        stats2 = self.stat_reader.get_stats(url2.shortname)

        self.assertEqual(stats1.all_time, 2)
        self.assertEqual(stats2.all_time, 1)

    def test_daily_accesses(self):
        url1 = self.url_shortener.shorten_url("http://noam.horse/resume.html")

        access1 = StatDatapoint(url_id = url1.id,
            time_accessed = BASE_TIME)
        access2 = StatDatapoint(url_id = url1.id,
            time_accessed = BASE_TIME - timedelta(hours = 27))
        access3 = StatDatapoint(url_id = url1.id,
            time_accessed = BASE_TIME - timedelta(hours = 2))
        access4 = StatDatapoint(url_id = url1.id,
            time_accessed = BASE_TIME - timedelta(seconds = 2))

        self.stat_processor.process_datapoint(access1)
        self.stat_processor.process_datapoint(access2)
        self.stat_processor.process_datapoint(access3)
        self.stat_processor.process_datapoint(access4)

        self.clock.now_value = BASE_TIME + timedelta(hours = 3)

        stats1 = self.stat_reader.get_stats(url1.shortname)

        self.clock.now_value = BASE_TIME - timedelta(hours = 5)

        stats2 = self.stat_reader.get_stats(url1.shortname)

        self.assertEqual(stats1.last_day, 3)
        self.assertEqual(stats2.last_day, 1)
    def test_weekly_accesses(self):
        url1 = self.url_shortener.shorten_url("http://noam.horse/resume.html")

        access1 = StatDatapoint(url_id = url1.id,
            time_accessed = BASE_TIME)
        access2 = StatDatapoint(url_id = url1.id,
            time_accessed = BASE_TIME - timedelta(days = 8))
        access3 = StatDatapoint(url_id = url1.id,
            time_accessed = BASE_TIME - timedelta(days = 2))
        access4 = StatDatapoint(url_id = url1.id,
            time_accessed = BASE_TIME - timedelta(seconds = 2))

        self.stat_processor.process_datapoint(access1)
        self.stat_processor.process_datapoint(access2)
        self.stat_processor.process_datapoint(access3)
        self.stat_processor.process_datapoint(access4)

        self.clock.now_value = BASE_TIME

        stats1 = self.stat_reader.get_stats(url1.shortname)

        self.clock.now_value = BASE_TIME - timedelta(days = 7)

        stats2 = self.stat_reader.get_stats(url1.shortname)

        self.assertEqual(stats1.last_week, 3)
        self.assertEqual(stats2.last_week, 1)
