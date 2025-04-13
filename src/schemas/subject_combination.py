from typing import Optional

from pydantic import BaseModel


class SubjectShort(BaseModel):
    id: int
    name: str


class SubjectCombinationBase(BaseModel):
    subject1_id: Optional[int] = None
    subject2_id: Optional[int] = None


class SubjectCombinationCreate(SubjectCombinationBase):
    subject1_id: int
    subject2_id: int


class SubjectCombinationUpdate(SubjectCombinationBase):
    pass


class SubjectCombinationResponse(BaseModel):
    id: int
    subject1: SubjectShort
    subject2: SubjectShort

    class Config:
        from_attributes = True
