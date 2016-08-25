from sqlalchemy import (
    Column,
    Index,
    Integer,
    Text,
    UnicodeText,
    Date
)

from .meta import Base
import datetime


def _now():
    return datetime.datetime.now()


class Journal(Base):
    __tablename__ = 'journals'
    id = Column(Integer, primary_key=True)
    title = Column(Text)
    creation_date = Column(Date, default=_now)
    body = Column(UnicodeText)


Index('my_index', Journal.title, unique=True, mysql_length=255)
