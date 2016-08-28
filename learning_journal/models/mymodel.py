from sqlalchemy import (
    Column,
    Index,
    Integer,
    UnicodeText,
    Unicode,
    Date
)

from .meta import Base
import datetime


def _now():
    return datetime.datetime.now()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    creation_date = Column(Date, default=_now)
    body = Column(UnicodeText)


Index('my_index', Entry.title, unique=True, mysql_length=255)
