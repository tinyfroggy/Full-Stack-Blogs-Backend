# Importing necessary modules and libraries
# FastAPI utilities for dependency injection and handling exceptions
from fastapi import Depends, HTTPException
# SQLAlchemy's Session to interact with the database
from sqlalchemy.orm import Session

# Importing custom services and models
# A function to get the database session (dependency injection)
from .get_db_service import get_db
from models.users_models import User  # The User model from the models directory
from schemas import users_schema  # Schemas for user data validation

# Importing libraries for hashing passwords and creating JWT tokens
import passlib.hash as _hash  # Passlib for password hashing
import jwt as _jwt  # JWT library for encoding and decoding tokens

from schemas import users_schema  # Importing user schemas for data validation

# Importing email validation library
# To validate email format
from email_validator import validate_email, EmailNotValidError

from fastapi.security import OAuth2PasswordBearer


_JWT_SECRET = "secret"

oauth2_scheme = OAuth2PasswordBearer("/api/1/token")


class UserServicesClass():

    async def get_user_by_email(email: str, db: Session = Depends(get_db)):
        return db.query(User).filter(User.email == email).first()

    async def create_user(user: users_schema.UserCreate, db: Session = Depends(get_db)):
        # check if user already exists
        existing_user = db.query(User).filter(User.email == user.email).first()
        if existing_user:
            raise HTTPException(
                status_code=400, detail="Email already registered")

        # check if username already exists
        existing_username = db.query(User).filter(
            User.username == user.username).first()
        if existing_username:
            raise HTTPException(
                status_code=400, detail="Username already taken")

        # check if email is valid
        try:
            valid = validate_email(user.email)
            email = valid.email
        except EmailNotValidError:
            raise HTTPException(
                status_code=400, detail="Please enter a valid email")

        # hash password
        hashed_password = _hash.bcrypt.hash(user.password)
        user_obj = User(email=email, username=user.username,
                        hashed_password=hashed_password)

        # add user to database
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

# Creating a function to generate JWT token for the user
    async def create_token(user: User):
        # Convert the user object to a schema object (this will serialize the user data to the format defined in the schema)
        user_schema_obj = users_schema.User.from_orm(user)

        # Convert the schema object to a dictionary, which is easier to work with
        user_dict = user_schema_obj.dict()

        # Removing sensitive information (in this case, 'date_created') from the dictionary before encoding it in the token
        del user_dict["date_created"]

        # Create a JWT token by encoding the user data (without sensitive information) and using the secret key for signing
        token = _jwt.encode(user_dict, _JWT_SECRET)

        # Return the token in a dictionary with the type of token (usually "bearer" for authentication)
        return dict(access_token=token, token_type="bearer")

    async def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
        user = await UserServicesClass.get_user_by_email(email=email, db=db)

        if not user:
            return False

        if not user.verify_password(password):
            return False

        return user

    async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
        try:
            payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
            user = db.query(User).get(payload["id"])
        except:
            raise HTTPException(
                status_code=401, detail="Invalid authentication credentials")

        return users_schema.User.from_orm(user)
