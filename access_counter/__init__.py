import datetime
import os

from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv("DATABASE_URL").replace("postgres://", "postgresql://", 1)
ENGINE = create_engine(DB_URL)
Base = declarative_base()


class Db(Base):
    __tablename__ = "access_counter"
    id = Column(Integer, primary_key=True)
    ipaddr = Column(Text)
    date = Column(Text)


Session = sessionmaker(bind=ENGINE)
session = Session()


def main(ipaddr):
    dt_today = datetime.datetime.today()
    today = '{}-{}-{}'.format(dt_today.year, dt_today.month, dt_today.day)
    if list(session.query(Db).filter(Db.ipaddr == ipaddr, Db.date == today)):
        new = False
    else:
        new = True
        session.add(Db(ipaddr=ipaddr, date=today))
        session.commit()
    count = session.query(Db).count()
    return count, new


def reset():
    try:
        Base.metadata.tables['access_counter'].create(bind=ENGINE)
    except Exception:
        pass
    session.query(Db).delete()
    session.commit()
    session.close()
    return 0
