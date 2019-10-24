from storage import schema
from storage.transacters import ProductionTransacter, TestTransacter

from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database, drop_database

def dropAndRecreate(engine):
    # Because this is a local development script, drop old data so the DB can be
    # re-migrated. Obviously for a productionized app you'd have to use separate
    # DB migrations for each schema change.
    if database_exists(engine.url):
        drop_database(engine.url)

    create_database(engine.url)

    with engine.connect() as conn:
        schema.metadata.create_all(conn, checkfirst = True)

dropAndRecreate(ProductionTransacter().engine)
dropAndRecreate(TestTransacter().engine)
