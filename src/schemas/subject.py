from typing import Optional

from pydantic import BaseModel


class SubjectBase(BaseModel):
    name: Optional[str] = None


class SubjectCreate(SubjectBase):
    name: str


class SubjectUpdate(SubjectBase):
    pass


class SubjectResponse(SubjectBase):
    id: int

    class Config:
        from_attributes = True
