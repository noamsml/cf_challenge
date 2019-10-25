from storage.transacters import ProductionTransacter
from shortening.url_resolver import URLResolver
from shortening.url_shortener import URLShortener
from shortening.shortname_generator import ShortnameGenerator
from storage.adapter import URLOperator, AccessAllTimeOperator
from stats.stat_processor import StatProcessor
from stats.stat_reader import StatReader

# Hack: Initialize all of our classes a module globals so we can put the manual
# dependency injection we do into one place. Obviously if I had more time,
# getting a real DI framework is preferred.
transacter = ProductionTransacter()
shortname_generator = ShortnameGenerator()
url_operator = URLOperator()
access_all_time_operator = AccessAllTimeOperator()
url_shortener = URLShortener(transacter, url_operator, shortname_generator)
url_resolver = URLResolver(transacter, url_operator)
stat_processor = StatProcessor(transacter, access_all_time_operator)
stat_reader = StatReader(transacter, access_all_time_operator, url_operator)
