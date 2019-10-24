import schema

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from contextlib import contextmanager


class Url:
    def __init__(self, schema_object):
        self.id = schema_object.id
        self.shortname = schema_object.shortname
        self.url = schema_object.url

class Transacter:
    def __init__(self):
        self.engine = create_engine('mysql://root@localhost/urlshortener')
        self.sessionmaker = sessionmaker(bind = self.engine)

    # Adapted from https://docs.sqlalchemy.org/en/13/orm/session_basics.html#session-faq-whentocreate
    # This is a reasonable approach to having sessions scoped to individual parts of the code
    @contextmanager
    def session(self):
        session = self.sessionmaker()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

class UrlOperator:
    def create_url(self, session, shortname, url):
        url_object = schema.Url(shortname = shortname, url = url)
        session.add(url_object)

    def find_url(self, session, shortname):
        url_object = session.query(schema.Url).filter(
            schema.Url.shortname == shortname).first()

        if url_object == None:
            return None

        return Url(url_object)
