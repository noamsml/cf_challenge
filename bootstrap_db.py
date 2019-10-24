from storage import schema

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

engine = create_engine('mysql://root@localhost/urlshortener')

# Because this is a local development script, drop old data so the DB can be
# re-migrated. Obviously for a productionized app you'd have to use separate
# DB migrations for each schema change.
if database_exists(engine.url):
    drop_database(engine.url)

create_database(engine.url)

with engine.connect() as conn:
    schema.metadata.create_all(conn, checkfirst = True)
