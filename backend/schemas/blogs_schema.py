from datetime import datetime
from pydantic import BaseModel


class BlogBase(BaseModel):
    title: str
    content: str


class BlogCreate(BlogBase):
    pass

class BlogUpdate(BlogBase):
    BlogUpdate: datetime

class BlogResponse(BlogBase):
    id: int

class Blog(BlogBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes  = True
