from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Boolean

from passlib.hash import bcrypt

from dependencies.database import Base

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        return bcrypt.verify(password, self.hashed_password)  

    @classmethod
    def hash_password(cls, password: str) -> str:
        return bcrypt.hash(password)
