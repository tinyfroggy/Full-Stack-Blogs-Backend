from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class BlogBase(BaseModel):
    title: str
    content: str


class BlogCreate(BlogBase):
    pass
class BlogUpdate(BlogBase):
    pass

class BlogResponse(BlogBase):
    id: int

class Blog(BlogBase):
    id: int
    owner_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes  = True
