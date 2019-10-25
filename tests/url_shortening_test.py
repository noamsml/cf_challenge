import unittest

from tests.integration_common import IntegrationTestCase

from shortening.url_resolver import URLResolver
from shortening.url_shortener import URLShortener
from shortening.shortname_generator import ShortnameGenerator
from storage.adapter import URLOperator
from shortening.shortening_cache import ShorteningCache

TEST_URL = "http://noam.horse/"
TEST_URL2 = "http://noam.horse/resume.html"

class URLIntegrationTest(IntegrationTestCase):
    def integrationSetUp(self):
        self.shortname_generator = ShortnameGenerator()
        self.url_operator = URLOperator()
        self.shortening_cache = ShorteningCache()
        self.url_shortener = URLShortener(self.transacter,
            self.url_operator,
            self.shortname_generator,
            self.shortening_cache)
        self.url_resolver = URLResolver(self.transacter,
            self.url_operator,
            self.shortening_cache)

    def test_shorten(self):
        short = self.url_shortener.shorten_url(TEST_URL)

        unshort = self.url_resolver.resolve_url(short.shortname)

        self.assertEqual(unshort.url, TEST_URL)

    def test_shorten_cold(self): # Test behavior when cache is cold
        short = self.url_shortener.shorten_url(TEST_URL)

        self.shortening_cache.clear()

        unshort = self.url_resolver.resolve_url(short.shortname)

        self.assertEqual(unshort.url, TEST_URL)

    def test_shorten_idempotence(self):
        short = self.url_shortener.shorten_url(TEST_URL)

        reshort = self.url_shortener.shorten_url(TEST_URL)

        self.assertEqual(short.shortname, reshort.shortname)

    def test_shorten_different_urls(self):
        short = self.url_shortener.shorten_url(TEST_URL)

        othershort = self.url_shortener.shorten_url(TEST_URL2)

        self.assertNotEqual(short.shortname, othershort.shortname)

        unshort_other = self.url_resolver.resolve_url(othershort.shortname)

        self.assertEqual(unshort_other.url, TEST_URL2)

    def test_multiple_url_idempotence(self):
        short = self.url_shortener.shorten_url(TEST_URL)

        othershort = self.url_shortener.shorten_url(TEST_URL2)

        self.assertNotEqual(short.shortname, othershort.shortname)

        othershort_second = self.url_shortener.shorten_url(TEST_URL2)

        self.assertEqual(othershort_second.shortname, othershort.shortname)

class TryOnlyShortnameGenerator:
    def generate_shortname(self, url, try_number = 0):
        return str(try_number)

# Test probing behavior to make sure we handle hash collisions gracefully
# Run the URL integration test with an intentionally broken shortname
# generator to make sure probing and idempotence work as expected
class URLProbingTest(URLIntegrationTest):
    def integrationSetUp(self):
        self.shortname_generator = TryOnlyShortnameGenerator()
        self.url_operator = URLOperator()
        self.shortening_cache = ShorteningCache()
        self.url_shortener = URLShortener(self.transacter,
            self.url_operator,
            self.shortname_generator,
            self.shortening_cache)
        self.url_resolver = URLResolver(self.transacter,
            self.url_operator,
            self.shortening_cache)
