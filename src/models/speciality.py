import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.models import Base, TimestampMixin, FieldMixin


class Specialty(Base, TimestampMixin, FieldMixin):
    __tablename__ = "specialties"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    name_en: orm.Mapped[str] = orm.mapped_column(sa.String(255), unique=True, nullable=False)

    name_ru: orm.Mapped[str] = orm.mapped_column(sa.String(255), nullable=True)
    name_kk: orm.Mapped[str] = orm.mapped_column(sa.String(255), nullable=True)

    description_en: orm.Mapped[str] = orm.mapped_column(sa.Text, nullable=True)

    description_ru: orm.Mapped[str] = orm.mapped_column(sa.Text, nullable=True)
    description_kk: orm.Mapped[str] = orm.mapped_column(sa.Text, nullable=True)

    valid_combinations: orm.Mapped[list["SubjectCombination"]] = orm.relationship(
        "SubjectCombination",
        secondary="subject_combination_specialties",
        back_populates="specialties"
    )

    def __repr__(self):
        return f"<Specialty id={self.id} name={self.name_en}>"
