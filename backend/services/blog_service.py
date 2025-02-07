from fastapi import HTTPException
from sqlalchemy.orm import Session

from schemas import users_schema, blogs_schema  # Group schemas
from models.blogs_models import Blog

import os
from dotenv import load_dotenv

from exceptions.handlers import handle_exception

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")


class BlogServicesClass:
    @staticmethod
    async def get_all_blogs_from_current_user(user: users_schema.User, db: Session):
        try:
            blogs = db.query(Blog).filter(Blog.owner_id == user.id).all()
            if not blogs:
                raise handle_exception(404, "No blogs found")
            return list(map(blogs_schema.Blog.from_orm, blogs))

        except HTTPException as he:
            raise he
        except Exception as e:
            raise handle_exception(500, str(e))

    @staticmethod
    async def get_one_blog_from_current_user(
        blog_id: int, user: users_schema.User, db: Session
    ):
        try:
            blog = db.query(Blog).filter(Blog.id == blog_id).first()

            if not blog:
                handle_exception(404, "Blog not found")

            if user.id != blog.owner_id:
                handle_exception(401, "Unauthorized")

            return blogs_schema.Blog.from_orm(blog)

        except HTTPException as he:
            raise he
        except Exception as e:
            handle_exception(500, str(e))

    @staticmethod
    async def create_blog(
        user: users_schema.User, db: Session, blog: blogs_schema.BlogCreate
    ):
        try:
            blog_obj = Blog(**blog.model_dump(), owner_id=user.id)

            db.add(blog_obj)
            db.commit()
            db.refresh(blog_obj)

            return blogs_schema.Blog.from_orm(blog_obj)

        except Exception as e:
            db.rollback()
            handle_exception(500, str(e))

    @staticmethod
    async def update_blog(
        blog: blogs_schema.BlogUpdate,
        blog_id: int,
        user: users_schema.User,
        db: Session,
    ):
        try:
            blog_obj = db.query(Blog).filter(Blog.id == blog_id).first()

            if not blog_obj:
                handle_exception(404, "Blog not found")

            if user.id != blog_obj.owner_id:
                handle_exception(401, "Unauthorized")

            for key, value in blog.model_dump().items():
                setattr(blog_obj, key, value)

            db.commit()
            db.refresh(blog_obj)

            return blogs_schema.Blog.from_orm(blog_obj)

        except HTTPException as he:
            db.rollback()
            raise he
        except Exception as e:
            db.rollback()
            handle_exception(500, str(e))

    @staticmethod
    async def delete_blog(blog_id: int, user: users_schema.User, db: Session):
        try:
            blog_obj = db.query(Blog).filter(Blog.id == blog_id).first()

            if not blog_obj:
                handle_exception(404, "Blog not found")

            if user.id != blog_obj.owner_id:
                handle_exception(401, "Unauthorized")

            db.delete(blog_obj)
            db.commit()

        except HTTPException as he:
            db.rollback()
            raise he
        except Exception as e:
            db.rollback()
            handle_exception(500, str(e))

    @staticmethod
    async def get_all_blogs(db: Session):
        try:
            blogs = db.query(Blog).all()
            if not blogs:
                handle_exception(404, "No blogs found")

            return list(map(blogs_schema.Blog.from_orm, blogs))

        except HTTPException as he:
            raise he
        except Exception as e:
            handle_exception(500, str(e))
