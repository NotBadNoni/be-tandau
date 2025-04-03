from typing import Optional

from pydantic import BaseModel


class BaseUniversity(BaseModel):
    name: str
    image: str
    description: str
    scholarships: str
    admissions: str
    applications: str


class CreateUniversity(BaseUniversity):
    pass


class UpdateUniversity(BaseUniversity):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    scholarships: Optional[str] = None
    admissions: Optional[str] = None
    applications: Optional[str] = None

    class Config:
        exclude_none = True


class UniversityResponse(BaseUniversity):
    id: int

    class Config:
        from_attributes = True
