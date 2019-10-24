import unittest
from shortname_generator import ShortnameGenerator, SHORTNAME_LENGTH

class ShortnameGeneratorTest(unittest.TestCase):
    def setUp(self):
        self.generator = ShortnameGenerator()
    def test_basic(self):
        shortname = self.generator.generate_shortname("http://noam.horse")
        self.assertEqual(type(shortname), str)
        self.assertEqual(len(shortname), SHORTNAME_LENGTH)
    def test_variety_by_url(self):
        shortname1 = self.generator.generate_shortname("http://noam.horse")
        shortname2 = self.generator.generate_shortname("https://cloudflare.com")
        self.assertNotEqual(shortname1, shortname2)
    def test_variety_by_url(self):
        shortname1 = self.generator.generate_shortname("http://noam.horse", 0)
        shortname2 = self.generator.generate_shortname("http://noam.horse", 1)
        self.assertNotEqual(shortname1, shortname2)
