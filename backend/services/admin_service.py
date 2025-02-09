from fastapi import  Depends
from sqlalchemy.orm import Session
from email_validator import validate_email, EmailNotValidError
import bcrypt
from jwt import PyJWTError, decode, ExpiredSignatureError
from dotenv import load_dotenv
import os

from fastapi.security import OAuth2PasswordBearer

from models.users_models import User
from models.admins_models import Admin
from schemas import admin_schema
from schemas.admin_schema import AdminMaineSchema, AdminCreate, AdminUpdate

from services.get_db_service import get_db
from exceptions.handlers import handle_exception
from utils.services_utils import handle_exceptions, get_or_404, authorize_user

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
if not JWT_SECRET:
    raise RuntimeError(
        "JWT_SECRET is not defined in the environment variables")

ALGORITHM = os.getenv("ALGORITHM")
if not ALGORITHM:
    raise RuntimeError(
        "ALGORITHM is not defined in the environment variables")

admin_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/1/admin/token")


class AdminServicesClass:

    @staticmethod
    @handle_exceptions
    async def create_admin(admin: AdminCreate, db: Session) -> AdminMaineSchema:
        existing_admin = await AdminServicesClass.get_admin_by_email(admin.email, db)
        if existing_admin:
            handle_exception(400, "Email already registered")

        try:
            valid = validate_email(admin.email)
            email = valid.email
        except EmailNotValidError:
            handle_exception(400, "Invalid email format")

        hashed_password = bcrypt.hashpw(admin.password.encode(
            "utf-8"), bcrypt.gensalt()).decode("utf-8")

        admin_obj = Admin(
            email=email, username=admin.username, hashed_password=hashed_password, is_admin=True
        )

        db.add(admin_obj)
        db.commit()
        db.refresh(admin_obj)
        return AdminMaineSchema.from_orm(admin_obj)

    @staticmethod
    @handle_exceptions
    async def get_all_admins(db: Session) -> list[AdminMaineSchema]:
        admins = db.query(Admin).all()
        return list(map(AdminMaineSchema.from_orm, admins))

    @staticmethod
    @handle_exceptions
    async def authenticate_admin(email: str, password: str, db: Session) -> Admin:
        admin = db.query(Admin).filter(Admin.email == email).first()
        if not admin or not bcrypt.checkpw(password.encode("utf-8"), admin.hashed_password.encode("utf-8")):
            handle_exception(401, "Incorrect email or password")

        if not admin.is_admin:
            handle_exception(
                403, "You do not have permission to access this resource")

        return admin

    @staticmethod
    async def get_current_admin(
        token: str = Depends(admin_oauth2_scheme),
        db: Session = Depends(get_db)
    ) -> AdminMaineSchema:
        try:
            payload = decode(token, JWT_SECRET, algorithms=[ALGORITHM])
            admin_id = payload.get("id")
            is_admin = payload.get("is_admin")

            if not is_admin:
                handle_exception(
                    403, "You do not have permission to access this resource")

            admin = await AdminServicesClass.get_admin_by_id(admin_id, db)
            return admin

        except ExpiredSignatureError:
            raise handle_exception(401, "Token expired")
        except PyJWTError:
            raise handle_exception(401, "Invalid token")

    @staticmethod
    @handle_exceptions
    async def get_admin_by_id(admin_id: int, db: Session) -> AdminMaineSchema:
        orm_admin = get_or_404(Admin, db, id=admin_id)
        return orm_admin

    @staticmethod
    async def get_admin_by_email(email: str, db: Session) -> Admin | None:
        try:
            return db.query(Admin).filter(Admin.email == email).first()
        except Exception as e:
            print(f"from get_admin_by_email: {str(e)}")
            raise handle_exception(500, str(e))

    @staticmethod
    @handle_exceptions
    async def update_admin(admin_update: AdminUpdate, db: Session, admin: Admin) -> AdminMaineSchema:
        if admin_update.email:
            existing_user = await AdminServicesClass.get_admin_by_email(admin_update.email, db)
            if existing_user and existing_user.id != admin.id:
                handle_exception(400, "Email already registered")

        if admin_update.username:
            admin.username = admin_update.username
        if admin_update.email:
            admin.email = admin_update.email

        db.commit()
        db.refresh(admin)

        updated_admin_schema = AdminMaineSchema.from_orm(admin)
        return updated_admin_schema

    @staticmethod
    @handle_exceptions
    async def delete_admin(db: Session, admin: Admin) -> dict | None:
        get_or_404(Admin, db, id=admin.id)
        db.delete(admin)
        db.commit()
        return {}

    @staticmethod
    @handle_exceptions
    async def get_user_by_id(user_id: int, db: Session) -> User: 
        user = get_or_404(User, db, id=user_id)
        return user
