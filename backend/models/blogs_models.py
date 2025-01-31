# Importing datetime for handling date and time
import datetime as _dt
# Importing SQLAlchemy ORM for defining database models
import sqlalchemy.orm as _orm
# Importing necessary SQLAlchemy components for defining columns and relationships
from sqlalchemy import Integer, Column, String, DateTime, ForeignKey
# Importing the Base class from the database module (likely a SQLAlchemy Base for model inheritance)
from dependencies.database import Base

# Import User model only when needed (inside a function or method)
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
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = _orm.relationship("User", back_populates="blogs")