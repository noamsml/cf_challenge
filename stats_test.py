import datetime

from integration_common import IntegrationTestCase

from stats.stat_processor import StatProcessor
from stats.stat_reader import StatReader
from stats.stat_processor import StatDatapoint
from shortening.url_shortener import URLShortener
from shortening.shortname_generator import ShortnameGenerator
from storage.adapter import URLOperator, AccessAllTimeOperator

BASE_TIME = datetime.datetime(2019, 10, 24, 17, 8)

class StatsTest(IntegrationTestCase):
    def integrationSetUp(self):
        self.shortname_generator = ShortnameGenerator()
        self.url_operator = URLOperator()
        self.access_all_time_operator = AccessAllTimeOperator()
        self.stat_processor = StatProcessor(self.transacter,
            self.access_all_time_operator)
        self.stat_reader = StatReader(self.transacter,
            self.access_all_time_operator,
            self.url_operator)
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
