from datetime import datetime, timedelta
import jwt as _jwt
from exceptions.handlers import handle_exception
from dotenv import load_dotenv
import os

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

class TokenServiceClass:

    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=30)) -> str:
        try:
            to_encode = data.copy()
            expire = datetime.utcnow() + expires_delta
            to_encode.update({"exp": expire})
            encoded_jwt = _jwt.encode(
                to_encode, JWT_SECRET, algorithm="HS256")
            return encoded_jwt

        except Exception as e:
            raise handle_exception(500, f"Error creating token: {str(e)}")