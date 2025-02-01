# Importing datetime for handling date and time
import datetime as _dt

# Importing SQLAlchemy ORM for defining database models
import sqlalchemy.orm as _orm

# Importing passlib for password hashing
import passlib.hash as _hash

# Importing necessary SQLAlchemy components for defining columns and relationships
from sqlalchemy import Integer, Column, String, DateTime

# Importing the Base class from the database module (likely a SQLAlchemy Base for model inheritance)
from dependencies.database import Base


# Import Blog model only when needed (inside a function or method)
def get_blog():
    from .blogs_models import Blog

    return Blog


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    date_created = Column(DateTime, default=_dt.datetime.utcnow)

    blogs = _orm.relationship("Blog", back_populates="owner")

    def verify_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.hashed_password)

    @classmethod
    def hash_password(cls, password: str) -> str:
        return _hash.bcrypt.hash(password)
