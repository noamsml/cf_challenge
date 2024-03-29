from storage.transacters import ProductionTransacter
from shortening.shortening_cache import ShorteningCache
from shortening.url_resolver import URLResolver
from shortening.url_shortener import URLShortener
from shortening.shortname_generator import ShortnameGenerator
from storage.adapter import URLOperator, AccessAllTimeOperator, AccessHourlyOperator
from stats.stat_processor import StatProcessor
from stats.stat_reader import StatReader

# Hack: Initialize all of our classes a module globals so we can put the manual
# dependency injection we do into one place. Obviously if I had more time,
# getting a real DI framework is preferred.
transacter = ProductionTransacter()
shortname_generator = ShortnameGenerator()
shortening_cache = ShorteningCache()
url_operator = URLOperator()
access_all_time_operator = AccessAllTimeOperator()
access_hourly_operator = AccessHourlyOperator()
url_shortener = URLShortener(transacter, url_operator, shortname_generator,shortening_cache)
url_resolver = URLResolver(transacter, url_operator, shortening_cache)
stat_processor = StatProcessor(transacter, access_all_time_operator, access_hourly_operator)
stat_reader = StatReader(transacter, access_all_time_operator, access_hourly_operator, url_operator)
