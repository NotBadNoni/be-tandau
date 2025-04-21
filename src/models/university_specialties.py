import sqlalchemy as sa
import sqlalchemy.orm as orm

from src.models import Base


class UniversitySpecialties(Base):
    __tablename__ = 'university_specialties'

    university_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("universities.id"), primary_key=True)
    specialty_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey("specialties.id"), primary_key=True)

    def __repr__(self):
        return f"<UniversitySpecialties uni_id={self.university_id} spec_id={self.specialty_id}>"
