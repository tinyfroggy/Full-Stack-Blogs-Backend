from fastapi import Depends
from sqlalchemy.orm import Session
from .get_db_service import get_db

from models.users_models import User
from models.blogs_models import Blog
from schemas import users_schema, blogs_schema

from exceptions.handlers import handle_exception
import bcrypt
from jwt import decode
from email_validator import validate_email, EmailNotValidError
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

from utils.services_utils import get_or_404, authorize_user, handle_exceptions

from jwt import PyJWTError, decode, ExpiredSignatureError

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET is not defined in the environment variables")

oauth2_scheme = OAuth2PasswordBearer("/api/1/users/token")


class UserServicesClass:
    @staticmethod
    @handle_exceptions
    async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int | None:
        payload = decode(token, JWT_SECRET, algorithms=["HS256"])
        return payload.get("id")

    # Get user by email
    @staticmethod
    @handle_exceptions
    async def get_user_by_email(email: str, db: Session) -> User | None: 
        return db.query(User).filter(User.email == email).first()

    # Get user by username
    @staticmethod
    @handle_exceptions
    async def get_user_by_username(username: str, db: Session) -> User | None: 
        return db.query(User).filter(User.username == username).first()

    # Get user by ID
    @staticmethod
    @handle_exceptions
    async def get_user_by_id(user_id: int, db: Session) -> User | None: 
        return db.query(User).filter(User.id == user_id).first()

    # Create a new user
    @staticmethod
    @handle_exceptions
    async def create_user(
        user: users_schema.UserCreate, db: Session
    ) -> users_schema.User:
        # Check for duplicate email
        existing_user = await UserServicesClass.get_user_by_email(user.email, db)
        if existing_user:
            handle_exception(400, "Email already registered")

        # Check for duplicate username
        existing_username = await UserServicesClass.get_user_by_username(user.username, db)
        if existing_username:
            handle_exception(400, "Username already taken")

        # Validate email format
        try:
            valid = validate_email(user.email)
            email = valid.email
        except EmailNotValidError:
            handle_exception(400, "Invalid email format")

        # Hash the password
        hashed_password = bcrypt.hashpw(
            user.password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        user_obj = User(
            email=email, username=user.username, hashed_password=hashed_password
        )

        # Save the user to the database
        db.add(user_obj)
        db.commit()
        db.refresh(user_obj)
        return user_obj

    # Authenticate user (email and password)
    @staticmethod
    @handle_exceptions
    async def authenticate_user(email: str, password: str, db: Session) -> User | None:
        user = await UserServicesClass.get_user_by_email(email=email, db=db)
        if not user or not user.verify_password(password):
            handle_exception(401, "Invalid email or password")
        return user

    # Get the current user using the token
    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme), 
        db: Session = Depends(get_db)
    ) -> User:
        try:
            payload = decode(token, JWT_SECRET, algorithms=["HS256"])
            user_id = payload.get("id")

            if not user_id:
                raise handle_exception(401, "Invalid token: Missing user ID")

            user = await UserServicesClass.get_user_by_id(user_id, db)
            if not user:
                raise handle_exception(404, "User not found")

            return user

        except ExpiredSignatureError:
            print("Token expired")  
            raise handle_exception(401, "Token expired")

        except PyJWTError as e:
            print(f"JWT Error: {e}")  
            raise handle_exception(401, "Invalid token")

    # Get all users
    @staticmethod
    @handle_exceptions
    async def get_all_users(db: Session) -> list[users_schema.User]:
        users = db.query(User).all()
        return list(map(users_schema.User.from_orm, users))

    # Update user password
    @staticmethod
    @handle_exceptions
    async def update_user_password(
        user: User, new_password: str, db: Session
    ) -> User:
        hashed_password = bcrypt.hashpw(
            new_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        user.hashed_password = hashed_password
        db.commit()
        db.refresh(user)
        return user

    # Update user data (username and email)
    @staticmethod
    @handle_exceptions
    async def update_user(
        user_update: users_schema.UserUpdate, db: Session, user: User
    ) -> User:
        # Check if the new username is already taken
        if user_update.username:
            existing_user = await UserServicesClass.get_user_by_username(
                user_update.username, db
            )
            if existing_user and existing_user.id != user.id:
                handle_exception(400, "Username already taken")

        # Check if the new email is already registered
        if user_update.email:
            existing_user = await UserServicesClass.get_user_by_email(
                user_update.email, db
            )
            if existing_user and existing_user.id != user.id:
                handle_exception(400, "Email already registered")

        # Apply updates
        if user_update.username:
            user.username = user_update.username
        if user_update.email:
            user.email = user_update.email

        db.commit()
        db.refresh(user)
        return user

    # Delete user
    @staticmethod
    @handle_exceptions
    async def delete_user(db: Session, user: User) -> dict | None:
        # Use the helper function get_or_404 to ensure the user exists
        user = get_or_404(User, db, id=user.id)
        db.delete(user)
        db.commit()
        return {}

    # Get all blogs for the current user
    @staticmethod
    @handle_exceptions
    async def get_all_blogs_for_current_user(
        user: User, db: Session
    ) -> list[blogs_schema.Blog]:
        blogs = db.query(Blog).filter(Blog.owner_id == user.id).all()
        if not blogs:
            handle_exception(404, "No blogs found")
        return list(map(blogs_schema.Blog.from_orm, blogs))
