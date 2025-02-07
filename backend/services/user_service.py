from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .get_db_service import get_db

from models.users_models import User
from models.blogs_models import Blog
from schemas import users_schema, blogs_schema

from exceptions.handlers import handle_exception
import bcrypt
from jwt import decode, ExpiredSignatureError, DecodeError
from email_validator import validate_email, EmailNotValidError
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET is not defined in the environment variables")

oauth2_scheme = OAuth2PasswordBearer("/api/1/users/token")


class UserServicesClass:
    @staticmethod
    async def get_current_user_id(token: str = Depends(oauth2_scheme)):
        try:
            payload = decode(token, JWT_SECRET, algorithms=["HS256"])
            return payload.get("id")

        except ExpiredSignatureError:
            handle_exception(401, "Token has expired")
        except DecodeError:
            handle_exception(401, "Invalid token")
        except Exception as e:
            handle_exception(500, str(e))

    # Get user by email
    @staticmethod
    async def get_user_by_email(email: str, db: Session):
        try:
            return db.query(User).filter(User.email == email).first()

        except Exception as e:
            handle_exception(500, str(e))

    # Get user by username
    @staticmethod
    async def get_user_by_username(username: str, db: Session):
        try:
            return db.query(User).filter(User.username == username).first()

        except Exception as e:
            handle_exception(500, str(e))

    # Create a new user
    @staticmethod
    async def create_user(
        user: users_schema.UserCreate, db: Session
    ) -> users_schema.User:
        try:
            # Check if email is already registered
            existing_user = await UserServicesClass.get_user_by_email(user.email, db)
            if existing_user:
                handle_exception(400, "Email already registered")

            # Check if username is already taken
            existing_username = await UserServicesClass.get_user_by_username(
                user.username, db
            )
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

            # Save user to database
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
            return user_obj

        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()
            handle_exception(500, str(e))

    # Authenticate user credentials
    @staticmethod
    async def authenticate_user(
        email: str, password: str, db: Session
    ):
        try:
            user = await UserServicesClass.get_user_by_email(email=email, db=db)
            if not user or not user.verify_password(password):
                handle_exception(401, "Invalid email or password")
            return user

        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()
            handle_exception(500, str(e))

    # Get the current user using token
    @staticmethod
    async def get_current_user(
        token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
    ) -> User:
        try:
            payload = decode(token, JWT_SECRET, algorithms=["HS256"])
            user = db.get(User, payload.get("id"))
            if not user:
                handle_exception(404, "User not found")
            return user

        except HTTPException as he:
            raise he
        except ExpiredSignatureError:
            handle_exception(401, "Token has expired")
        except DecodeError:
            handle_exception(401, "Invalid token")
        except Exception as e:
            handle_exception(500, str(e))

    # Get all users
    @staticmethod
    async def get_all_users(db: Session) -> list[users_schema.User]:
        try:
            users = db.query(User).all()
            return list(map(users_schema.User.from_orm, users))

        except Exception as e:
            handle_exception(500, str(e))

    @staticmethod
    async def update_user_password(
        user: User, new_password: str, db: Session
    ) -> User:
        try:
            hashed_password = bcrypt.hashpw(
                new_password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            user.hashed_password = hashed_password

            db.commit()
            db.refresh(user)
            return user

        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()
            handle_exception(500, str(e))

    # Update user details
    @staticmethod
    async def update_user(
        user_update: users_schema.UserUpdate, db: Session, user: User
    ) -> User:
        try:
            # Check if new username is already taken
            if user_update.username:
                existing_user = await UserServicesClass.get_user_by_username(
                    user_update.username, db
                )
                if existing_user and existing_user.id != user.id:
                    handle_exception(400, "Username already taken")

            # Check if new email is already registered
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

            # Save changes
            db.commit()
            db.refresh(user)
            return user

        except HTTPException as he:
            raise he
        except Exception as e:
            handle_exception(500, str(e))

    # Delete a user
    @staticmethod
    async def delete_user(db: Session, user: User):
        try:

            if not user:
                handle_exception(404, "User not found")

            # Remove user from database
            db.delete(user)
            db.commit()
            return {"message": "User deleted successfully"}

        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()
            handle_exception(500, str(e))

    # Get a all blogs for current user
    @staticmethod
    async def get_all_blogs_for_current_user(
        user: User, db: Session
    ) -> list[blogs_schema.Blog]:
        try:
            blogs = db.query(Blog).filter(Blog.owner_id == user.id).all()
            return list(map(blogs_schema.Blog.from_orm, blogs))

        except HTTPException as he:
            raise he
        except Exception as e:
            handle_exception(500, str(e))
