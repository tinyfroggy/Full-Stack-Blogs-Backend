from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from schemas import users_schema
from models.blogs_models import Blog
from schemas import blogs_schema
import os
from dotenv import load_dotenv

load_dotenv()
_JWT_SECRET = os.getenv("_JWT_SECRET")


class BlogServicesClass:
    async def get_all_blogs_from_current_user(user: users_schema.User, db: Session):
        try:
            blogs = db.query(Blog).filter(Blog.owner_id == user.id).all()
            if not blogs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No blogs found"
                )
            return list(map(blogs_schema.Blog.from_orm, blogs))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

    @staticmethod
    async def get_one_blog_from_current_user(
        blog_id: int, user: users_schema.User, db: Session
    ):
        try:
            blog = db.query(Blog).filter(Blog.id == blog_id).first()

            if not blog:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
                )

            if user.id != blog.owner_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )

            return blogs_schema.Blog.from_orm(blog)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )

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
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error creating blog: {str(e)}",
            )

    async def update_blog(
        blog: blogs_schema.BlogUpdate,
        blog_id: int,
        user: users_schema.User,
        db: Session,
    ):
        try:
            blog_obj = db.query(Blog).filter(Blog.id == blog_id).first()

            if not blog_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
                )

            if user.id != blog_obj.owner_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )

            for key, value in blog.model_dump().items():
                setattr(blog_obj, key, value)

            db.commit()
            db.refresh(blog_obj)

            return blogs_schema.Blog.from_orm(blog_obj)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error updating blog: {str(e)}",
            )

    async def delete_blog(blog_id: int, user: users_schema.User, db: Session):
        try:
            blog_obj = db.query(Blog).filter(Blog.id == blog_id).first()

            if not blog_obj:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found"
                )

            if user.id != blog_obj.owner_id:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized"
                )

            db.delete(blog_obj)
            db.commit()
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error deleting blog: {str(e)}",
            )

    @staticmethod
    async def get_all_blogs(db: Session):
        try:
            blogs = db.query(Blog).all()
            if not blogs:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND, detail="No blogs found"
                )

            return list(map(blogs_schema.Blog.from_orm, blogs))
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
            )
