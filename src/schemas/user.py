from typing import Optional

from pydantic import BaseModel, EmailStr

from src.core.constants import UserRoles


class ProfileBase(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    date_of_birth: Optional[str] = None
    profile_picture: Optional[str] = None


class ProfileCreate(ProfileBase):
    pass


class ProfileUpdate(ProfileBase):
    pass


class ProfileResponse(ProfileBase):
    id: int
    username: str
    email: str

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[str] = None
    role: Optional[UserRoles] = None


class UserUpdate(UserBase):
    password: Optional[str] = None
    new_password: Optional[str] = None
    verify_new_password: Optional[str] = None

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None
    language: Optional[str] = None
    country: Optional[str] = None
    date_of_birth: Optional[str] = None
    profile_picture: Optional[str] = None


class UserResponse(UserBase):
    id: int
    profile: Optional[ProfileBase] = None

    class Config:
        from_attributes = True
