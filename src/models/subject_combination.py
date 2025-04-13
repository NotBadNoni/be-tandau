import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.models import Base, TimestampMixin
from src.models.speciality import subject_combination_specialties
from src.models.subject import Subject


class SubjectCombination(Base, TimestampMixin):
    __tablename__ = "subject_combinations"

    id: orm.Mapped[int] = orm.mapped_column(sa.Integer, primary_key=True)

    subject1_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("subjects.id"), nullable=False)
    subject2_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("subjects.id"), nullable=False)

    subject1: orm.Mapped["Subject"] = orm.relationship("Subject", foreign_keys=[subject1_id])
    subject2: orm.Mapped["Subject"] = orm.relationship("Subject", foreign_keys=[subject2_id])

    specialties: orm.Mapped[list["Specialty"]] = orm.relationship(
        "Specialty",
        secondary=subject_combination_specialties,
        back_populates="valid_combinations"
    )

    def __repr__(self):
        return f"<SubjectCombination id={self.id} subj1={self.subject1_id} subj2={self.subject2_id}>"
