import datetime as _dt
import sqlalchemy.orm as _orm
import passlib.hash as _hash
from sqlalchemy import Integer, Column, String, DateTime, Boolean
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
    date_created = Column(DateTime, default=_dt.datetime.utcnow)

    blogs = _orm.relationship("Blog", back_populates="owner", cascade="all, delete-orphan")

    def verify_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.hashed_password)  

    @classmethod
    def hash_password(cls, password: str) -> str:
        return _hash.bcrypt.hash(password)

# every time you chang anything from models run this command
# alembic revision --autogenerate -m "your message"
# alembic upgrade head
# then go to the new version file and add the necessary changes