import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.models import Base, TimestampMixin


class Subject(Base, TimestampMixin):
    __tablename__ = "subjects"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(255), unique=True, nullable=False)

    def __repr__(self):
        return f"<Subject id={self.id} name={self.name}>"
