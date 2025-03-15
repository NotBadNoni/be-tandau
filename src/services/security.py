import datetime

import jwt

from src.core.config import settings
from src.core.exeptions import CustomException


class JWTHandler:
    secret_key = settings.SECRET_KEY
    algorithm = "HS256"
    access_expire_minutes = settings.JWT_ACCESS_EXPIRE_MINUTES
    refresh_expire_minutes = settings.JWT_REFRESH_EXPIRE_MINUTES

    @staticmethod
    def encode_access_token(payload: dict) -> str:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWTHandler.access_expire_minutes)
        payload.update({"exp": expire, "type": "access"})
        return jwt.encode(payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm)

    @staticmethod
    def encode_refresh_token(payload: dict) -> str:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWTHandler.refresh_expire_minutes)
        payload.update({"exp": expire, "type": "refresh"})
        return jwt.encode(payload, JWTHandler.secret_key, algorithm=JWTHandler.algorithm)

    @staticmethod
    def decode(token: str) -> dict:
        try:
            payload = jwt.decode(
                str(token),
                JWTHandler.secret_key,
                algorithms=[JWTHandler.algorithm],
            )
            return payload
        except jwt.ExpiredSignatureError:
            raise CustomException("Token has expired")
        except jwt.InvalidTokenError as e:
            raise CustomException(f"{str(e)}")
