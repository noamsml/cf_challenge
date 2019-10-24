from storage import schema

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from contextlib import contextmanager


class Url:
    def __init__(self, schema_object):
        self.id = schema_object.id
        self.shortname = schema_object.shortname
        self.url = schema_object.url

class Transacter:
    def __init__(self, url):
        self.engine = create_engine(url)
        self.sessionmaker = sessionmaker(bind = self.engine)

    def raw_connection(self):
        return self.engine.connect()

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

class URLOperator:
    def create_url(self, session, shortname, url):
        url_object = schema.Url(shortname = shortname, url = url)
        session.add(url_object)

    def find_url_by_shortname(self, session, shortname):
        url_object = session.query(schema.Url).filter(
            schema.Url.shortname == shortname).first()

        if url_object == None:
            return None

        return Url(url_object)

    def find_url_by_url_value(self, session, url):
        url_object = session.query(schema.Url).filter(
            schema.Url.url == url).first()

        if url_object == None:
            return None

        return Url(url_object)
