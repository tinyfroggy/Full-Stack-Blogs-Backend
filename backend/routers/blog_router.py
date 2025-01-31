# Importing necessary modules and classes from FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
# Importing SQLAlchemy's Session class for database interaction
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

# Importing custom services for database session and user services
from services.get_db_service import get_db  # For database connection
# Importing user services for user creation and authentication
from services.blog_service import BlogServicesClass

# Importing schemas for data validation
from schemas.blogs_schema import BlogCreate, Blog
from schemas import users_schema
from services.user_service import UserServicesClass
from typing import List


router = APIRouter()


@router.post("/blogs", response_model=Blog, status_code=status.HTTP_201_CREATED)
async def create_blog(blog: BlogCreate, user: users_schema.User = Depends(UserServicesClass.get_current_user), db: Session = Depends(get_db)):
    return await BlogServicesClass.create_blog(blog=blog, user=user, db=db)


@router.get("/blogs", response_model=List[Blog], status_code=status.HTTP_200_OK)
async def get_all_blogs(user: users_schema.User = Depends(UserServicesClass.get_current_user), db: Session = Depends(get_db)):
    return await BlogServicesClass.get_user_blogs(user=user, db=db)
