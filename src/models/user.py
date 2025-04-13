import typing

import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.core.constants import UserRoles
from src.models import TimestampMixin, Base

if typing.TYPE_CHECKING:
    from src.models.profile import Profile


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    email: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True)
    username: orm.Mapped[str] = orm.mapped_column(sa.String, unique=True)
    password: orm.Mapped[str] = orm.mapped_column(sa.String)
    role: orm.Mapped[UserRoles] = orm.mapped_column(sa.Enum(UserRoles), default=UserRoles.CLIENT)

    profile: orm.Mapped["Profile"] = orm.relationship("Profile", back_populates="user", uselist=False)
    chats = orm.relationship("Chat", back_populates="user")

    def __repr__(self):
        return f"<User id={self.id} username={self.username}>"
