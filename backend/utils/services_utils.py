# app/services/utils.py

from fastapi import HTTPException
from sqlalchemy.orm import Session
from exceptions.handlers import handle_exception
from functools import wraps


# function to get a resource or return 404
def get_or_404(model, db: Session, **filters):
    obj = db.query(model).filter_by(**filters).first()
    if not obj:
        handle_exception(404, f"{model.__name__} not found")
    return obj


# function for checking if the user is the owner of the resource
def authorize_user(user, resource_owner_id):
    if user.id != resource_owner_id:
        handle_exception(401, "Unauthorized")


# function to handle exceptions
def handle_exceptions(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"Unhandled Exception: {e}")
            raise handle_exception(500, str(e))
    return wrapper
