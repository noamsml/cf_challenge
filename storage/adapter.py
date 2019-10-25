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

class AccessAllTimeOperator:
    def increment_access_count(self, session, url_id, amount = 1):
        access_object = session.query(schema.AccessAllTime)\
            .filter(schema.AccessAllTime.url_id == url_id)\
            .with_for_update()\
            .first()

        if access_object == None:
            session.add(schema.AccessAllTime(url_id = url_id, counter = amount))
        else:
            access_object.counter += amount

    def get_access_count(self, session, url_id):
        access_object = session.query(schema.AccessAllTime)\
            .filter(schema.AccessAllTime.url_id == url_id)\
            .first()

        if access_object == None:
            return 0

        return access_object.counter


class AccessHourlyOperator:
    def increment_access_count(self, session, url_id, hour, amount = 1):
        access_object = session.query(schema.AccessHourly)\
            .filter(schema.AccessHourly.url_id == url_id)\
            .filter(schema.AccessHourly.hour == hour)\
            .with_for_update()\
            .first()

        if access_object == None:
            session.add(schema.AccessHourly(url_id = url_id, hour = hour, counter = amount))
        else:
            access_object.counter += amount

    def get_total_access_count(self, session, url_id, hour_min, hour_max):
        access_objects = session.query(schema.AccessHourly)\
            .filter(schema.AccessHourly.url_id == url_id)\
            .filter(schema.AccessHourly.hour > hour_min)\
            .filter(schema.AccessHourly.hour <= hour_max)\
            .all()

        return sum(map(lambda access: access.counter, access_objects))
