import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base, TimestampMixin

university_specialties = sa.Table(
    "university_specialties",
    Base.metadata,
    sa.Column("university_id", sa.Integer, sa.ForeignKey("universities.id"), primary_key=True),
    sa.Column("specialty_id", sa.Integer, sa.ForeignKey("specialties.id"), primary_key=True),
)


class University(Base, TimestampMixin):
    __tablename__ = "universities"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name: Mapped[str] = mapped_column(sa.String(255), nullable=False, index=True)
    image: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    description: Mapped[str] = mapped_column(sa.Text, nullable=False)

    country_name: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    cover_image: Mapped[str] = mapped_column(sa.String(255), nullable=True)

    scholarship_name: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    scholarship_description: Mapped[str] = mapped_column(sa.Text, nullable=True)
    scholarship_benefits: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=True)
    application_steps: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=True)

    specialties: orm.Mapped[list["Specialty"]] = orm.relationship(
        "Specialty",
        secondary="university_specialties",
        backref="universities",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<University id={self.id} name={self.name}>"
