# schemas/university.py

from typing import Optional, List

from pydantic import BaseModel


class UniversityBase(BaseModel):
    name: str
    image: str
    description: str
    country_name: str
    cover_image: Optional[str] = None

    scholarship_name: Optional[str] = None
    scholarship_description: Optional[str] = None
    scholarship_benefits: Optional[List[str]] = []
    application_steps: Optional[List[str]] = []


class UniversityCreate(UniversityBase):
    pass


class UniversityUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    country_name: Optional[str] = None
    cover_image: Optional[str] = None
    scholarship_name: Optional[str] = None
    scholarship_description: Optional[str] = None
    scholarship_benefits: Optional[List[str]] = None
    application_steps: Optional[List[str]] = None


class UniversityResponse(UniversityBase):
    id: int

    class Config:
        from_attributes = True
