from fastapi.security import OAuth2PasswordRequestForm
from services.admin_service import AdminServicesClass
from services.user_service import UserServicesClass
from exceptions.handlers import handle_exception
from fastapi import APIRouter, Depends, status
from services.get_db_service import get_db
from sqlalchemy.orm import Session
from auth.create_token import TokenServiceClass


router = APIRouter()


# Endpoint to generate JWT token for authentication
@router.post("/users/token", status_code=status.HTTP_200_OK)
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = await UserServicesClass.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        return handle_exception(401, "Invalid Credentials")

    # Create token with necessary data
    token = TokenServiceClass.create_access_token(
        data={"sub": user.email, "id": user.id, "is_user": user.is_admin}
    )

    return {"access_token": token, "token_type": "bearer"}

    # return await UserServicesClass.create_token(user=user)


@router.post("/admins/token", status_code=status.HTTP_200_OK)
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    admin = await AdminServicesClass.authenticate_admin(
        email=form_data.username, password=form_data.password, db=db
    )

    if not admin:
        handle_exception(401, "Incorrect email or password")

    # Create token with necessary data
    token = TokenServiceClass.create_access_token(
        data={"sub": admin.email, "id": admin.id, "is_admin": admin.is_admin}
    )

    return {"access_token": token, "token_type": "bearer"}
