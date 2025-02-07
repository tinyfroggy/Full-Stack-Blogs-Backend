from datetime import datetime

from sqlalchemy import Integer, Column, String, DateTime, Boolean
from sqlalchemy.orm import relationship 

from passlib.hash import bcrypt

from dependencies.database import Base


def get_blog():
    from .blogs_models import Blog

    return Blog


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=False)
    date_created = Column(DateTime, default=datetime.utcnow)

    blogs = relationship("Blog", back_populates="owner", cascade="all, delete-orphan")

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)  

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)

# every time you chang anything from models run this command
# alembic revision --autogenerate -m "your message"
# alembic upgrade head
# then go to the new version file and add the necessary changes