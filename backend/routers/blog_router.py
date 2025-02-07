from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas.blogs_schema import BlogCreate, Blog, BlogUpdate
from schemas import users_schema  

from services.blog_service import BlogServicesClass
from services.user_service import UserServicesClass  
from services.get_db_service import get_db

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
    spesific_blog = await BlogServicesClass.get_one_blog_from_current_user(blog_id=blog_id, user=user, db=db)
    return Blog.from_orm(spesific_blog)

@router.post("/blogs", response_model=Blog, status_code=status.HTTP_201_CREATED)
async def create_blog(
    blog: BlogCreate, 
    user: users_schema.User = Depends(UserServicesClass.get_current_user), 
    db: Session = Depends(get_db)
):
    new_blog = await BlogServicesClass.create_blog(blog=blog, user=user, db=db)
    return Blog.from_orm(new_blog)

@router.put("/blogs/{blog_id}", response_model=Blog, status_code=status.HTTP_200_OK)
async def update_blog(
    blog: BlogUpdate, 
    blog_id: int, 
    user: users_schema.User = Depends(UserServicesClass.get_current_user), 
    db: Session = Depends(get_db)
):
    updated_blog =  BlogServicesClass.update_blog(blog=blog, blog_id=blog_id, user=user, db=db)
    return Blog.from_orm(updated_blog)

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