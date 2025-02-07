import datetime as _dt
import sqlalchemy.orm as _orm
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
from dependencies.database import Base

def get_user():
    from .users_models import User
    return User


class Blog(Base):
    __tablename__ = 'blogs'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    content = Column(String, index=True)
    created_at = Column(DateTime, default=_dt.datetime.utcnow)
    updated_at = Column(DateTime, default=_dt.datetime.utcnow, onupdate=_dt.datetime.utcnow)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    owner = _orm.relationship("User", back_populates="blogs")