from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Index,
    Integer,
    Sequence,
    String,
    Text,
)

from geru.models.meta import Base


class PageView(Base):
    """
    The session identifier, the date, time and
    page requested within a given session for every request made.
    """
    __tablename__ = 'pageview'

    id = Column(Integer, Sequence('seq_pageview_id'), primary_key=True)
    session_id = Column(String(length=70))
    date = Column(DateTime, default=datetime.now())
    url = Column(Text)

    def to_dict(self, exclude=()):
        attrs = ['id', 'session_id', 'date', 'url']
        for i in exclude:
            attrs.remove(i)
        return {k: str(getattr(self, k)) for k in attrs}


Index('pageview_session_id', PageView.session_id, unique=False)
Index('pageview_url', PageView.url, unique=False)
