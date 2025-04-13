import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.models import Base, TimestampMixin

subject_combination_specialties = sa.Table(
    "subject_combination_specialties",
    Base.metadata,
    sa.Column("subject_combination_id", sa.Integer, sa.ForeignKey("subject_combinations.id"), primary_key=True),
    sa.Column("specialty_id", sa.Integer, sa.ForeignKey("specialties.id"), primary_key=True),
)


class Specialty(Base, TimestampMixin):
    __tablename__ = "specialties"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)
    name: orm.Mapped[str] = orm.mapped_column(sa.String(255), unique=True, nullable=False)
    description: orm.Mapped[str] = orm.mapped_column(sa.Text, nullable=True)

    valid_combinations: orm.Mapped[list["SubjectCombination"]] = orm.relationship(
        "SubjectCombination",
        secondary=subject_combination_specialties,
        back_populates="specialties"
    )

    def __repr__(self):
        return f"<Specialty id={self.id} name={self.name}>"
