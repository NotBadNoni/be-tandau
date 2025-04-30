from typing import Optional, List

from pydantic import BaseModel


class UniversityBase(BaseModel):
    name: str = None
    image: str
    description: Optional[str] = None
    country_name: Optional[str]  = None
    cover_image: Optional[str] = None

    scholarship_name: Optional[str] = None
    scholarship_description: Optional[str] = None
    scholarship_benefits: Optional[List[str]] = []
    application_steps: Optional[List[str]] = []


class UniversityCreate(UniversityBase):
    cover_image: Optional[bytes] = None


class UniversityUpdate(BaseModel):
    name: Optional[str] = None
    image: Optional[str] = None
    description: Optional[str] = None
    country_name: Optional[str] = None
    cover_image: Optional[bytes] = None
    scholarship_name: Optional[str] = None
    scholarship_description: Optional[str] = None
    scholarship_benefits: Optional[List[str]] = None
    application_steps: Optional[List[str]] = None


class UniversityResponse(UniversityBase):
    id: int

    class Config:
        from_attributes = True

    @classmethod
    def from_model(cls, university, lang: str) -> "UniversityResponse":
        return cls(
            id=university.id,
            name=university.get_field("name", lang) or university.name_en,
            image=university.image,
            description=university.get_field("description", lang) or None,
            country_name=university.get_field("country_name", lang) or university.country_name_en,
            scholarship_name=university.get_field("scholarship_name", lang) or university.scholarship_name_en,
            scholarship_description=university.get_field("scholarship_description",
                                                         lang) or university.scholarship_description_en,
            scholarship_benefits=university.get_field("scholarship_benefits",
                                                      lang) or university.scholarship_benefits_en,
            application_steps=university.get_field("application_steps", lang) or university.application_steps_en,
        )