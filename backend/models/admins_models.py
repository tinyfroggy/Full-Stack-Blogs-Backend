from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from dependencies.database import Base
import passlib.hash as _hash

class Admin(Base):
    __tablename__ = "admins"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_admin = Column(Boolean, default=True)
    date_created = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        return _hash.bcrypt.verify(password, self.hashed_password)  

    @classmethod
    def hash_password(cls, password: str) -> str:
        return _hash.bcrypt.hash(password)
