import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column

from src.core.constants import UserRoles
from src.models import Base
from src.models import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String)
    full_name: Mapped[str] = mapped_column(sa.String, nullable=True)
    role: Mapped[UserRoles] = mapped_column(sa.Enum(UserRoles), default=UserRoles.CLIENT)