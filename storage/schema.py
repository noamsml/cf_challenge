from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

metadata = MetaData()

urls = Table('urls', metadata,
    Column('id', Integer, primary_key=True),
    Column('shortname', String(32), index=True, unique=True),
    Column('url', String(1024)))

accesses_hourly = Table('accesses_hourly', metadata,
    Column('id', Integer, primary_key=True),
    Column('url_id', Integer),
    Column('hour', Integer), # Hour stat in the form of seconds since epoch
    Column('counter', Integer))

Index('hourly_url_hour', accesses_hourly.c.url_id, accesses_hourly.c.hour, unique = True)

accesses_alltime = Table('accesses_alltime', metadata,
    Column('id', Integer, primary_key=True),
    Column('url_id', Integer, index = True, unique = True),
    Column('counter', Integer))

class Url(Base):
    __tablename__ = "urls"

    id = Column(Integer, primary_key=True)
    shortname = Column(String)
    url = Column(String)

class AccessAllTime(Base):
    __tablename__ = "accesses_alltime"

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer)
    counter = Column(Integer)

class AccessHourly(Base):
    __tablename__ = "accesses_hourly"

    id = Column(Integer, primary_key=True)
    url_id = Column(Integer)
    hour = Column(Integer)
    counter = Column(Integer)
