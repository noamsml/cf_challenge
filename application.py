from storage.transacters import ProductionTransacter
from shortening.url_resolver import URLResolver
from shortening.url_shortener import URLShortener
from shortening.shortname_generator import ShortnameGenerator
from storage.adapter import URLOperator

# Hack: Initialize all of our classes a module globals so we can put the manual
# dependency injection we do into one place. Obviously if I had more time,
# getting a real DI framework is preferred.
transacter = ProductionTransacter()
shortname_generator = ShortnameGenerator()
url_operator = URLOperator()
url_shortener = URLShortener(transacter, url_operator, shortname_generator)
url_resolver = URLResolver(transacter, url_operator)
