from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from .get_db_service import get_db
from models.users_models import User
from schemas import users_schema
import bcrypt
import jwt as _jwt
from email_validator import validate_email, EmailNotValidError
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv()
_JWT_SECRET = os.getenv("_JWT_SECRET")

oauth2_scheme = OAuth2PasswordBearer("/api/1/token")


class UserServicesClass:
    # Get user by email
    @staticmethod
    async def get_user_by_email(email: str, db: Session = Depends(get_db)):
        try:
            return db.query(User).filter(User.email == email).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Get user by username
    @staticmethod
    async def get_user_by_username(username: str, db: Session = Depends(get_db)):
        try:
            return db.query(User).filter(User.username == username).first()
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Create a new user
    @staticmethod
    async def create_user(user: users_schema.UserCreate, db: Session = Depends(get_db)):
        try:
            # Check if email is already registered
            existing_user = db.query(User).filter(
                User.email == user.email).first()
            if existing_user:
                raise HTTPException(
                    status_code=400, detail="Email already registered")

            # Check if username is already taken
            existing_username = db.query(User).filter(
                User.username == user.username).first()
            if existing_username:
                raise HTTPException(
                    status_code=400, detail="Username already taken")

            # Validate email format
            try:
                valid = validate_email(user.email)
                email = valid.email
            except EmailNotValidError:
                raise HTTPException(
                    status_code=400, detail="Invalid email format")

            # Hash the password
            hashed_password = bcrypt.hashpw(user.password.encode(
                'utf-8'), bcrypt.gensalt()).decode('utf-8')
            user_obj = User(email=email, username=user.username,
                            hashed_password=hashed_password)

            # Save user to database
            db.add(user_obj)
            db.commit()
            db.refresh(user_obj)
            return user_obj
        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    # Generate JWT token
    @staticmethod
    async def create_token(user: User):
        try:
            user_schema_obj = users_schema.User.from_orm(user)
            user_dict = user_schema_obj.dict()
            if "date_created" in user_dict:
                del user_dict["date_created"]
            token = _jwt.encode(user_dict, _JWT_SECRET, algorithm="HS256")
            return {"access_token": token, "token_type": "bearer"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Authenticate user credentials
    @staticmethod
    async def authenticate_user(email: str, password: str, db: Session = Depends(get_db)):
        try:
            user = await UserServicesClass.get_user_by_email(email=email, db=db)
            if not user or not user.verify_password(password):
                return False
            return user
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

    # Get the current user using token
    @staticmethod
    async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
        try:
            payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
            user = db.get(User, payload.get("id"))
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except _jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Token has expired")
        except _jwt.DecodeError:
            raise HTTPException(status_code=401, detail="Invalid token")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Get user by ID
    @staticmethod
    async def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Get all users
    @staticmethod
    async def get_all_users(db: Session = Depends(get_db)):
        try:
            users = db.query(User).all()
            return list(map(users_schema.User.from_orm, users))
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    # Update user details
    @staticmethod
    async def update_user(user_update: users_schema.UserUpdate, db: Session, user: User) -> User:
        try:
            # Check if new username is already taken
            if user_update.username:
                existing_user = await UserServicesClass.get_user_by_username(user_update.username, db)
                if existing_user and existing_user.id != user.id:
                    raise HTTPException(
                        status_code=400, detail="Username already taken")

            # Check if new email is already registered
            if user_update.email:
                existing_user = await UserServicesClass.get_user_by_email(user_update.email, db)
                if existing_user and existing_user.id != user.id:
                    raise HTTPException(
                        status_code=400, detail="Email already registered")

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
            raise HTTPException(status_code=500, detail=str(e))

    # Delete a user
    @staticmethod
    async def delete_user(db: Session, user: User):
        try:
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            # Remove user from database
            db.delete(user)
            db.commit()
            return {"message": "User deleted successfully"}
        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))
