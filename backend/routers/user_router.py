# Importing necessary modules and classes from FastAPI
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

# Importing SQLAlchemy's Session class for database interaction
from sqlalchemy.orm import Session

# Importing custom services for database session and user services
from services.get_db_service import get_db  # For database connection
# For user-related business logic
from services.user_service import UserServicesClass

# Importing schemas for user data validation and response format
from schemas.users_schema import UserCreate, User, UserUpdate
from typing import List  # For list response typing

# Initializing FastAPI router
router = APIRouter()


# Endpoint to create a new user
@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    db_user = await UserServicesClass.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered"
        )

    # Create the user
    new_user = await UserServicesClass.create_user(user=user, db=db)

    # Return the created user
    return new_user


# Endpoint to generate JWT token for authentication
@router.post("/token", status_code=status.HTTP_200_OK)
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    user = await UserServicesClass.authenticate_user(
        email=form_data.username, password=form_data.password, db=db
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    return await UserServicesClass.create_token(user=user)


# Endpoint to get the currently authenticated user
@router.get("/users/me", response_model=User)
async def get_current_user(user: User = Depends(UserServicesClass.get_current_user)):
    return user


# Endpoint to get all users
@router.get("/users", response_model=List[User])
async def get_all_users(db: Session = Depends(get_db)):
    return await UserServicesClass.get_all_users(db=db)


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


# Endpoint to delete user
@router.delete("/users/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    # This dependency returns a SQLAlchemy User instance
    user=Depends(UserServicesClass.get_current_user),
    db: Session = Depends(get_db),
):
    return await UserServicesClass.delete_user(db=db, user=user)


# get one user
@router.get("/users/{user_id}", response_model=User)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    return await UserServicesClass.get_user_by_id(user_id=user_id, db=db)


# Update user by ID
@router.put("/users/{user_id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user_by_id(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = await UserServicesClass.get_user_by_id(user_id=user_id, db=db)
    updated_user = await UserServicesClass.update_user(user_update=user_update, db=db, user=user)
    return updated_user


# Delete user by ID
@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = await UserServicesClass.get_user_by_id(user_id=user_id, db=db)
    return await UserServicesClass.delete_user(db=db, user=user)
