from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from schemas.users_schema import UserCreate, User, UserUpdate
from schemas.blogs_schema import Blog

from services.user_service import UserServicesClass
from services.get_db_service import get_db

from exceptions.handlers import handle_exception

router = APIRouter()


# Endpoint to get all users
@router.get("/users", response_model=List[User])
async def get_all_users(db: Session = Depends(get_db)):
    return await UserServicesClass.get_all_users(db=db)


# Endpoint to create a new user
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    db_user = await UserServicesClass.get_user_by_email(email=user.email, db=db)

    if db_user:
        return handle_exception(400, "Email already registered")

    new_user = await UserServicesClass.create_user(user=user, db=db)

    return new_user


# Endpoint to get the currently authenticated user
@router.get("/users/me", response_model=User)
async def get_current_user(user: User = Depends(UserServicesClass.get_current_user)):
    return user

# Update user endpoint
@router.put("/users/me", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(
    user_update: UserUpdate,
    user=Depends(
        UserServicesClass.get_current_user
    ),  # Ensure the user is authenticated
    db: Session = Depends(get_db),
):
    updated_user = await UserServicesClass.update_user(
        user_update=user_update, db=db, user=user
    )
    # Return the updated user
    return updated_user


# Update user password endpoint
# @router.put("/users/me/password", response_model=User, status_code=status.HTTP_200_OK)
# async def update_user_password(
#     new_password: str,
#     user=Depends(UserServicesClass.get_current_user),
#     db: Session = Depends(get_db),
# ):
#     updated_user = await UserServicesClass.update_user_password(
#         user=user, new_password=new_password, db=db
#     )
#     return updated_user


# Endpoint to delete user
@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    # This dependency returns a SQLAlchemy User instance
    user=Depends(UserServicesClass.get_current_user),
    db: Session = Depends(get_db),
):
    return await UserServicesClass.delete_user(db=db, user=user)


# Get all blogs for current user
@router.get("/users/me/blogs", response_model=list[Blog])
async def get_all_blogs_for_current_user(
    user=Depends(UserServicesClass.get_current_user),
    db: Session = Depends(get_db),
):
    return await UserServicesClass.get_all_blogs_for_current_user(user=user, db=db)
