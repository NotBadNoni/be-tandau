import typing
from datetime import date

import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.models import Base

if typing.TYPE_CHECKING:
    from src.models.user import User


class Profile(Base):
    __tablename__ = "user_profiles"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    first_name: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)
    last_name: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)
    gender: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)
    language: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)
    country: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)
    date_of_birth: orm.Mapped[date] = orm.mapped_column(sa.Date, nullable=True)
    profile_picture: orm.Mapped[str] = orm.mapped_column(sa.String, nullable=True)

    user_id: orm.Mapped[int] = orm.mapped_column(sa.Integer, sa.ForeignKey("users.id"))
    user: orm.Mapped["User"] = orm.relationship("User", back_populates="profile")

    def __repr__(self):
        return f"<Profile id={self.id}>"
