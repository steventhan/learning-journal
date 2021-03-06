from sqlalchemy import (
    Column,
    Index,
    Integer,
    UnicodeText,
    Unicode,
    Date
)

from .meta import Base
from datetime import datetime


def _now():
    return datetime.now()


class Entry(Base):
    __tablename__ = 'entries'
    id = Column(Integer, primary_key=True)
    title = Column(Unicode)
    creation_date = Column(Date, default=_now)
    body = Column(UnicodeText)
