from pydantic import BaseModel, EmailStr
from datetime import datetime


class AdminBase(BaseModel):
    email: EmailStr
    username: str


class AdminCreate(AdminBase):
    password: str


class AdminUpdate(BaseModel):
    email: EmailStr | None = None
    username: str | None = None


class AdminMaineSchema(AdminBase):
    id: int
    date_created: datetime

    class Config:
        from_attributes = True
