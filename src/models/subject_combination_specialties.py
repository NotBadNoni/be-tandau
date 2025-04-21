import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.models import Base


class SubjectCombinationSpecialties(Base):
    __tablename__ = "subject_combination_specialties"
    subject_combination_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("subject_combinations.id"),
        primary_key=True
    )
    specialty_id: orm.Mapped[int] = orm.mapped_column(
        sa.ForeignKey("specialties.id"),
        primary_key=True
    )

    def __repr__(self):
        return f"<SubjectCombinationSpecialties comb_id={self.subject_combination_id} spec_id={self.specialty_id}>"
