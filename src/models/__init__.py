import datetime

from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, mapped_column


class TimestampMixin:
    @declared_attr
    def created_at(cls):
        return mapped_column(DateTime, default=datetime.datetime.now(), nullable=False)

    @declared_attr
    def updated_at(cls):
        return mapped_column(
            DateTime,
            default=datetime.datetime.now(),
            onupdate=datetime.datetime.now(),
            nullable=False,
        )


class FieldMixin:
    def get_field(self, field: str, lang: str):
        return getattr(self, f"{field}_{lang}", None)


Base = declarative_base()

from .chat import Chat
from .chat_messages import ChatMessages
from .favorites import Favorites
from .profile import Profile
from .user import User
from .speciality import Specialty
from .subject import Subject
from .subject_combination import SubjectCombination
from .university_specialties import UniversitySpecialties
from src.models.university_specialties import UniversitySpecialties
from src.models.subject_combination_specialties import SubjectCombinationSpecialties
from .university import University

sqlalchemy_models = [
    Chat,
    ChatMessages,
    Favorites,
    Profile,
    User,
    Specialty,
    Subject,
    SubjectCombination,
    University,
    UniversitySpecialties,
]
