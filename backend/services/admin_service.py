from fastapi import HTTPException, Depends
from sqlalchemy.orm import Session
from models.users_models import User
from models.admins_models import Admin
from schemas import admin_schema
import jwt as _jwt
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
import os
from schemas.admin_schema import AdminMaineSchema, AdminCreate
from services.get_db_service import get_db
from email_validator import validate_email, EmailNotValidError
from exceptions.handlers import handle_exception
import bcrypt
from datetime import datetime, timedelta


load_dotenv()
_JWT_SECRET = os.getenv("_JWT_SECRET")
admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/1/admin/token")


class AdminServicesClass:

    @staticmethod
    async def create_admin(
        admin: AdminCreate,
        db: Session = Depends(get_db)
    ) -> AdminMaineSchema:
        try:
            existing_admin = await AdminServicesClass.get_admin_by_email(admin.email, db)
            if existing_admin:
                handle_exception(400, "Email already registered")

            # Validate email format
            try:
                valid = validate_email(admin.email)
                email = valid.email

            except EmailNotValidError:
                handle_exception(400, "Invalid email format")

            # Hash the password
            hashed_password = bcrypt.hashpw(
                admin.password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
            admin_obj = Admin(
                email=email, username=admin.username, hashed_password=hashed_password, is_admin=True
            )

            db.add(admin_obj)
            db.commit()
            db.refresh(admin_obj)
            return admin_obj

        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()
            raise handle_exception(500, str(e))

    @staticmethod
    async def get_all_admins(db: Session = Depends(get_db)) -> list[AdminMaineSchema]:
        try:
            admins = db.query(Admin).all()
            return list(map(AdminMaineSchema.from_orm, admins))

        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    async def authenticate_admin(
        email: str,
        password: str,
        db: Session = Depends(get_db)
    ) -> Admin:
        try:
            # Retrieve the admin based on the email
            admin = db.query(Admin).filter(Admin.email == email).first()
            if not admin:
                handle_exception(401, "Incorrect email or password")

            # Verify the password
            if not bcrypt.checkpw(password.encode("utf-8"), admin.hashed_password.encode("utf-8")):
                handle_exception(401, "Incorrect email or password")

            # Check if the user has admin privileges
            if not admin.is_admin:
                print(admin.is_admin)
                handle_exception(403, "You do not have permission to access this resource")

            return admin

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    async def get_current_admin(
        token: str = Depends(admin_oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> AdminMaineSchema:
        try:
            payload = _jwt.decode(token, _JWT_SECRET, algorithms=["HS256"])
            admin_id = payload.get("id")
            is_admin = payload.get("is_admin")
            print(is_admin)
            print(admin_id)

            if not is_admin:
                handle_exception(
                    403, "You do not have permission to access this resource"
                )

            admin = db.query(Admin).filter(Admin.id == admin_id).first()
            if not admin:
                handle_exception(404, "Admin not found")

            return admin

        except _jwt.ExpiredSignatureError:
            raise handle_exception(401, "Token expired")
        except _jwt.PyJWTError:
            raise handle_exception(401, "Invalid token")

        except HTTPException as he:
            raise he
        except Exception as e:
            raise handle_exception(500, str(e))

    @staticmethod
    async def get_admin_by_id(admin_id: int, db: Session) -> AdminMaineSchema:
        try:
            orm_admin = db.query(Admin).filter(
                Admin.id == admin_id).first()

            if not orm_admin:
                raise handle_exception(404, "Admin not found")

            return AdminMaineSchema.from_orm(orm_admin)

        except HTTPException as he:
            raise he
        except Exception as e:
            raise handle_exception(500, str(e))

    @staticmethod
    async def get_admin_by_email(email: str, db: Session = Depends(get_db)) -> AdminMaineSchema:
        try:
            return db.query(Admin).filter(Admin.email == email).first()

        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    async def update_admin(
        admin_update: admin_schema.AdminUpdate,
        db: Session,
        admin: Admin
    ) -> AdminMaineSchema:
        try:
            # Check if new email is already registered
            if admin_update.email:
                existing_user = await AdminServicesClass.get_admin_by_email(
                    admin_update.email, db
                )
                if existing_user and existing_user.id != admin.id:
                    handle_exception(400, "Email already registered")

            # Apply updates
            if admin_update.username:
                admin.username = admin_update.username
            if admin_update.email:
                admin.email = admin_update.email

            # Save changes
            db.commit()
            db.refresh(admin)
            return admin

        except HTTPException as he:
            raise he
        except Exception as e:
            db.rollback()
            raise HTTPException(500, str(e))

    @staticmethod
    async def delete_admin(db: Session, admin: Admin):
        try:
            if not admin:
                handle_exception(404, "Admin not found")

            # Remove Admin from database
            db.delete(admin)
            db.commit()
            return {"message": "Admin deleted successfully"}

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(500, str(e))

    @staticmethod
    async def get_user_by_id(user_id: int, db: Session):
        try:
            user = db.query(User).filter(User.id == user_id).first()
            if not user:
                handle_exception(404, "User not found")
            return user

        except HTTPException as he:
            raise he
        except Exception as e:
            raise HTTPException(500, str(e))
