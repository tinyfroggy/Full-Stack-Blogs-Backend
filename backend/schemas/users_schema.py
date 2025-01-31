from datetime import datetime
from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    username: str


class UserCreate(UserBase):
    password: str  


class User(UserBase):
    id: int
    date_created: datetime

    class Config:
        from_attributes  = True 
