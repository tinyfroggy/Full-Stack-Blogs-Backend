# Importing necessary modules and classes from FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
# Importing SQLAlchemy's Session class for database interaction
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm

# Importing custom services for database session and user services
from services.get_db_service import get_db  # For database connection
# For user-related business logic
from services.user_service import UserServicesClass

# Importing schemas for user data validation and response format
# User creation schema and User response schema
from schemas.users_schema import UserCreate, User

router = APIRouter()


@router.post("/users")
async def create_user(user: UserCreate = Depends(), db: Session = Depends(get_db)):
    db_user = await UserServicesClass.get_user_by_email(email=user.email, db=db)

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    #  create the user
    user = await UserServicesClass.create_user(user=user, db=db)
    # return token
    return await UserServicesClass.create_token(user=user)


@router.post("/token")
async def generate_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = await UserServicesClass.authenticate_user(email=form_data.username, password=form_data.password, db=db)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    return await UserServicesClass.create_token(user=user)


@router.get("/users/me", response_model=User)
async def get_current_user(user: User = Depends(UserServicesClass.get_current_user)):
    return user
