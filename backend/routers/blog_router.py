from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from services.get_db_service import get_db
from services.blog_service import BlogServicesClass
from schemas.blogs_schema import BlogCreate, Blog, BlogUpdate, BlogResponse
from schemas import users_schema
from services.user_service import UserServicesClass

router = APIRouter()

@router.get("/blogs", response_model=List[Blog], status_code=status.HTTP_200_OK)
async def get_all_blogs_from_current_user(
    user: users_schema.User = Depends(UserServicesClass.get_current_user), 
    db: Session = Depends(get_db)
):
    return await BlogServicesClass.get_all_blogs_from_current_user(user=user, db=db)

@router.get("/blogs/{blog_id}", response_model=Blog, status_code=status.HTTP_200_OK)
async def get_one_blog_from_current_user(
    blog_id: int,
    user: users_schema.User = Depends(UserServicesClass.get_current_user),
    db: Session = Depends(get_db)
):
    return await BlogServicesClass.get_one_blog_from_current_user(blog_id=blog_id, user=user, db=db)

@router.post("/blogs", response_model=Blog, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogCreate, 
    user: users_schema.User = Depends(UserServicesClass.get_current_user), 
    db: Session = Depends(get_db)
):
    return await BlogServicesClass.create_blog(blog=blog, user=user, db=db)

@router.put("/blogs/{blog_id}", response_model=Blog, status_code=status.HTTP_200_OK)
async def update_blog(
    blog: BlogUpdate, 
    blog_id: int, 
    user: users_schema.User = Depends(UserServicesClass.get_current_user), 
    db: Session = Depends(get_db)
):
    return await BlogServicesClass.update_blog(blog=blog, blog_id=blog_id, user=user, db=db)

@router.delete("/blogs/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(
    blog_id: int, 
    user: users_schema.User = Depends(UserServicesClass.get_current_user), 
    db: Session = Depends(get_db)
):
    await BlogServicesClass.delete_blog(blog_id=blog_id, user=user, db=db)

@router.get("/all/blogs", response_model=List[Blog], status_code=status.HTTP_200_OK)
async def get_all_blogs(db: Session = Depends(get_db)):
    return await BlogServicesClass.get_all_blogs(db=db)