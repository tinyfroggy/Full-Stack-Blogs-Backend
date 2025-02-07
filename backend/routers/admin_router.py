from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from models.admins_models import Admin
from schemas.admin_schema import AdminMaineSchema, AdminUpdate, AdminCreate
from services.admin_service import AdminServicesClass
from schemas.users_schema import User, UserUpdate
from services.user_service import UserServicesClass
from services.get_db_service import get_db
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv
from exceptions.handlers import handle_exception
from typing import List

load_dotenv()
_JWT_SECRET = os.getenv("_JWT_SECRET")
oauth2_scheme = OAuth2PasswordBearer("/admins/token")

router = APIRouter()


@router.post("/admins", status_code=status.HTTP_201_CREATED, response_model=AdminMaineSchema)
async def create_admin(
    admin: AdminCreate,
    db: Session = Depends(get_db),
):
    db_admin = await AdminServicesClass.get_admin_by_email(email=admin.email, db=db)

    if db_admin:
        return handle_exception(400, "Admin already registered")

    new_admin = await AdminServicesClass.create_admin(admin=admin, db=db)

    return new_admin


@router.get("/admins", response_model=List[AdminMaineSchema])
async def get_all_admins(db: Session = Depends(get_db)):
    return await AdminServicesClass.get_all_admins(db=db)


# Get current admin (no extra dependency required for this route)
@router.get("/admins/me", response_model=AdminMaineSchema)
async def get_current_admin(admin: Admin = Depends(AdminServicesClass.get_current_admin)):
    return admin


@router.put("/admins/me", response_model=AdminMaineSchema, status_code=status.HTTP_200_OK)
async def update_admin(
    admin_update: AdminUpdate,
    admin=Depends(AdminServicesClass.get_current_admin),
    db: Session = Depends(get_db)
):
    updated_admin = await AdminServicesClass.update_admin(
        admin_update=admin_update, db=db, admin=admin
    )
    return updated_admin

# Update admin password endpoint
# @router.put("/users/me/password", response_model=AdminMaineSchema, status_code=status.HTTP_200_OK)
# async def update_admin_password(
#     new_password: str,
#     user=Depends(AdminServicesClass.get_current_admin),
#     db: Session = Depends(get_db),
# ):
#     updated_admin = await AdminServicesClass.update_user_password(
#         user=user, new_password=new_password, db=db
#     )
#     return updated_admin


@router.delete("/admins/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_admin(
    admin=Depends(AdminServicesClass.get_current_admin),
    db: Session = Depends(get_db),
):
    return await AdminServicesClass.delete_admin(db=db, admin=admin)


@router.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(AdminServicesClass.get_current_admin),
):
    if not admin:
        handle_exception(401, "You are not Admin")

    return await AdminServicesClass.get_user_by_id(user_id=user_id, db=db)


@router.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user_by_id(
    user_id: int,
    user_update: UserUpdate,
    db: Session = Depends(get_db),
    admin=Depends(AdminServicesClass.get_current_admin),
):
    user = await AdminServicesClass.get_user_by_id(user_id=user_id, db=db)
    updated_user = await UserServicesClass.update_user(user_update=user_update, db=db, user=user)
    return updated_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(
    user_id: int,
    db: Session = Depends(get_db),
    admin=Depends(AdminServicesClass.get_current_admin),
):
    user = await AdminServicesClass.get_user_by_id(user_id=user_id, db=db)
    return await UserServicesClass.delete_user(db=db, user=user)


