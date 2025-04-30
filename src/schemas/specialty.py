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

    @classmethod
    def from_model(cls, model, lang: str) -> "SpecialtyResponse":
        return cls(
            id=model.id,
            name=model.get_field("name", lang) or model.name_en,
            description=model.get_field("description", lang) or model.description_en
        )
