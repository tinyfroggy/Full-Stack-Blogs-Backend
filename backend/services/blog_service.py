# Importing necessary modules and libraries
# FastAPI utilities for dependency injection and handling exceptions
from fastapi import Depends, HTTPException
# SQLAlchemy's Session to interact with the database
from sqlalchemy.orm import Session

# Importing custom services and models
# A function to get the database session (dependency injection)
from .get_db_service import get_db
from schemas import users_schema  # Schemas for user data validation
from models.blogs_models import Blog  # Model for blog data

# Importing libraries for hashing passwords and creating JWT tokens
import passlib.hash as _hash  # Passlib for password hashing
import jwt as _jwt  # JWT library for encoding and decoding tokens

from schemas import users_schema  # Importing user schemas for data validation

# Importing email validation library
# To validate email format
from email_validator import validate_email, EmailNotValidError

from fastapi.security import OAuth2PasswordBearer
from schemas import blogs_schema


_JWT_SECRET = "secret"
oauth2_scheme = OAuth2PasswordBearer("/api/1/token")


class BlogServicesClass:
    async def create_blog(user: users_schema.User, db: Session, blog: blogs_schema.BlogCreate):
        blog_obj = Blog(**blog.dict(), owner_id=user.id)
        db.add(blog_obj)
        db.commit()
        db.refresh(blog_obj)
        return blogs_schema.Blog.from_orm(blog_obj)

    async def get_user_blogs(user: users_schema.User, db: Session):
        blogs = db.query(Blog).filter(Blog.owner_id == user.id).all()
        return list(map(blogs_schema.Blog.from_orm, blogs))
