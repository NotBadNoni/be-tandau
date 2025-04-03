from typing import Optional

from pydantic import BaseModel


class BaseUser(BaseModel):
    email: str
    username: str
    full_name: Optional[str] = None


class UserUpdate(BaseUser):
    email: Optional[str] = None
    full_name: Optional[str] = None
    username: Optional[str] = None

    password: Optional[str] = None
    new_password: Optional[str] = None
    verify_new_password: Optional[str] = None


class UserResponse(BaseUser):
    id: int

    class Config:
        from_attributes = True