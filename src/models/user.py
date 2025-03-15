import sqlalchemy as sa
from sqlalchemy.orm import Mapped
from sqlalchemy.testing.schema import mapped_column

from src.models import Base
from src.models import TimestampMixin


class User(TimestampMixin, Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    email: Mapped[str] = mapped_column(sa.String, unique=True)
    username: Mapped[str] = mapped_column(sa.String, unique=True)
    password: Mapped[str] = mapped_column(sa.String)
    full_name: Mapped[str] = mapped_column(sa.String, nullable=True)