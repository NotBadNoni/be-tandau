import datetime

from sqlalchemy import DateTime, func
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


Base = declarative_base()

from .chat import Chat
from .chat_messages import ChatMessages
from .favorites import Favorites
from .profile import Profile
from .user import User
from .speciality import Specialty
from .subject import Subject
from .subject_combination import SubjectCombination
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
    University
]
