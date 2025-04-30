import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Mapped, mapped_column

from src.models import Base, FieldMixin, TimestampMixin


class University(Base, FieldMixin, TimestampMixin):
    __tablename__ = "universities"

    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    name_en: Mapped[str] = mapped_column(sa.String(255), nullable=False, index=True)
    name_ru: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    name_kk: Mapped[str] = mapped_column(sa.String(255), nullable=True)

    image: Mapped[str] = mapped_column(sa.String(255), nullable=False)
    description_en: Mapped[str] = mapped_column(sa.Text, nullable=False)
    description_ru: Mapped[str] = mapped_column(sa.Text, nullable=True)
    description_kk: Mapped[str] = mapped_column(sa.Text, nullable=True)

    country_name_en: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    country_name_ru: Mapped[str] = mapped_column(sa.String(100), nullable=False)
    country_name_kk: Mapped[str] = mapped_column(sa.String(100), nullable=False)

    cover_image: Mapped[str] = mapped_column(sa.String(255), nullable=True)

    scholarship_name_en: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    scholarship_name_ru: Mapped[str] = mapped_column(sa.String(255), nullable=True)
    scholarship_name_kk: Mapped[str] = mapped_column(sa.String(255), nullable=True)

    scholarship_description_en: Mapped[str] = mapped_column(sa.Text, nullable=True)
    scholarship_description_ru: Mapped[str] = mapped_column(sa.Text, nullable=True)
    scholarship_description_kk: Mapped[str] = mapped_column(sa.Text, nullable=True)

    scholarship_benefits_en: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String),
                                                               nullable=True)
    scholarship_benefits_ru: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=True)
    scholarship_benefits_kk: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=True)

    application_steps_en: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=True)
    application_steps_ru: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=True)
    application_steps_kk: Mapped[list[str]] = mapped_column(sa.ARRAY(sa.String), nullable=True)

    specialties: orm.Mapped[list["Specialty"]] = orm.relationship(
        "Specialty",
        secondary="university_specialties",
        backref="universities",
        lazy="selectin"
    )

    def __repr__(self):
        return f"<University id={self.id} name={self.name_en}>"
