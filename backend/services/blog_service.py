from sqlalchemy.orm import Session

from schemas import users_schema, blogs_schema  
from models.blogs_models import Blog

import os
from dotenv import load_dotenv

from exceptions.handlers import handle_exception

from utils.services_utils import get_or_404, authorize_user, handle_exceptions

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET is not defined in the environment variables")



class BlogServicesClass:
    @staticmethod
    @handle_exceptions
    async def get_one_blog_from_current_user(blog_id: int, user: users_schema.User, db: Session) -> blogs_schema.Blog:
        blog = get_or_404(Blog, db, id=blog_id)
        authorize_user(user, blog.owner_id)
        return blog

    @staticmethod
    @handle_exceptions
    async def create_blog(user: users_schema.User, db: Session, blog: blogs_schema.BlogCreate) -> Blog:
        blog_obj = Blog(**blog.model_dump(), owner_id=user.id)
        db.add(blog_obj)
        db.commit()
        db.refresh(blog_obj)
        return blog_obj

    @staticmethod
    @handle_exceptions
    async def update_blog(blog: blogs_schema.BlogUpdate, blog_id: int, user: users_schema.User, db: Session) -> Blog: 
        blog_obj = get_or_404(Blog, db, id=blog_id)
        authorize_user(user, blog_obj.owner_id)
        for key, value in blog.model_dump().items():
            setattr(blog_obj, key, value)
        db.commit()
        db.refresh(blog_obj)
        return blog_obj

    @staticmethod
    @handle_exceptions
    async def delete_blog(blog_id: int, user: users_schema.User, db: Session) -> dict | None:
        blog_obj = get_or_404(Blog, db, id=blog_id)
        authorize_user(user, blog_obj.owner_id)
        db.delete(blog_obj)
        db.commit()
        return {}

    @staticmethod
    @handle_exceptions
    async def get_all_blogs(db: Session) -> list[blogs_schema.Blog]:
        blogs = db.query(Blog).all()
        if not blogs:
            handle_exception(404, "No blogs found")
        return [blogs_schema.Blog.model_validate(blog) for blog in blogs]