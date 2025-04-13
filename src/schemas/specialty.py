from typing import Optional

from pydantic import BaseModel


class SpecialtyBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class SpecialtyCreate(SpecialtyBase):
    name: str


class SpecialtyUpdate(SpecialtyBase):
    pass


class SpecialtyResponse(SpecialtyBase):
    id: int

    class Config:
        from_attributes = True
